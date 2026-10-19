"""One delivery day in a city: the parcels waiting at the distribution centre that morning,
the people they're for, the weather hour by hour, and how busy each street is.

A day is fixed by the city's seed and its day number, so Day(City(seed, day=d)) always
gives the same parcels, weather and traffic. Every distribution here is a setting, with
its source or reasoning in docs/days.md.

    python -m sim.day                             # build city 0, day 0 with 500 parcels, print it, time it
    python -m sim.day --held-out data/held-out    # write the fixed benchmark days
"""
import argparse
import hashlib
from pathlib import Path
from time import perf_counter

import numpy as np

from .city import City

# Parcels
SIZES = ("envelope", "small", "medium", "large", "oversize")
SIZE_SHARE = (0.30, 0.35, 0.22, 0.10, 0.03)
SIZE_DIMS = ((0.30, 0.22, 0.02), (0.25, 0.20, 0.10), (0.40, 0.30, 0.20), (0.60, 0.40, 0.40), (1.00, 0.60, 0.50))  # m
SIZE_WEIGHT = (0.2, 0.8, 1.5, 5.0, 12.0)  # median kg for each size
WEIGHT_SPREAD = 0.5  # log-normal sigma around those medians
MAX_WEIGHT = 30.0  # kg; heavier things go by freight, not parcel delivery
FRAGILITY = ("robust", "careful", "fragile")
FRAGILITY_SHARE = (0.70, 0.20, 0.10)
EXTRA_PER_STOP = 0.45  # parcels per address is 1 + Poisson(0.45), about 1.45 on average

# Recipients, for parcels collected from the truck's locker
WALK_MEDIAN, WALK_SPREAD, WALK_MAX = 250.0, 0.6, 800.0  # how far they'll walk to the truck, m
REPLY_MEDIAN, REPLY_SPREAD = 10.0, 0.7  # minutes from being told the truck is there to turning up

# Weather
RAIN_CHANCE = 0.3
WIND_SHEAR = 0.25  # wind grows with height as (height / 10 m) ** WIND_SHEAR

# Traffic
MORNING, EVENING = (8.0, 1.0, 0.6), (17.5, 1.2, 0.8)  # rush hours: peak hour, spread, extra delay
BUSY = {"arterial": 1.0, "local": 0.4}  # how much rush hour slows each kind of street

# Fixed benchmark days: city seeds 1000+ are never used for training.
HELD_OUT = tuple((1000 + c, d) for c in range(10) for d in range(5))


class Day:
    def __init__(self, city, parcels=500):
        self.city, self.seed, self.day = city, city.seed, city.day
        rng = np.random.default_rng([city.seed, city.day, 1])
        self._parcels(rng, parcels)
        self._recipients(rng)
        self.weather = _weather(rng)
        streets = np.random.default_rng([city.seed, 2])  # how busy each street is belongs to the city, not the day
        self.busy = np.where(city.edge_arterial, BUSY["arterial"], BUSY["local"]) * streets.lognormal(0, 0.3, len(city.edges))
        self.traffic_level = rng.uniform(0.8, 1.2)  # some days are busier than others

    def _parcels(self, rng, n):
        """Addresses get 1 + Poisson(EXTRA_PER_STOP) parcels each until there are n."""
        city = self.city
        stops = rng.choice(len(city.address_kind), size=min(int(n / 1.3) + 10, len(city.address_kind)), replace=False)
        count = 1 + rng.poisson(EXTRA_PER_STOP, len(stops))
        address = np.repeat(stops, count)[:n]
        if len(address) < n:
            raise ValueError(f"{n} parcels don't fit in a city with {len(city.address_kind)} addresses")
        size = rng.choice(len(SIZES), n, p=SIZE_SHARE)
        self.parcel_address = address
        self.parcel_size = np.array(SIZES)[size]
        self.parcel_dims = np.array(SIZE_DIMS)[size] * rng.uniform(0.8, 1.2, (n, 3))  # m
        self.parcel_weight = np.minimum(np.array(SIZE_WEIGHT)[size] * rng.lognormal(0, WEIGHT_SPREAD, n), MAX_WEIGHT)  # kg
        self.parcel_fragility = np.array(FRAGILITY)[rng.choice(len(FRAGILITY), n, p=FRAGILITY_SHARE)]

    def _recipients(self, rng):
        """One person per address: everyone at an address walks as far and answers as fast."""
        stops, first = np.unique(self.parcel_address, return_inverse=True)
        walk = np.minimum(WALK_MEDIAN * rng.lognormal(0, WALK_SPREAD, len(stops)), WALK_MAX)
        self.recipient_walk = walk[first]  # m
        self.recipient_reply = (REPLY_MEDIAN * rng.lognormal(0, REPLY_SPREAD, len(stops)))[first]  # minutes

    def weather_at(self, hour):
        """Weather at a time of day (0-24), interpolated between the hourly values."""
        w = self.weather
        out = {k: float(np.interp(hour, w["hour"], w[k])) for k in ("temp_c", "wind", "gust", "rain_mm_h")}
        out["wind_dir"] = float(np.interp(hour, w["hour"], np.unwrap(w["wind_dir"])) % (2 * np.pi))
        return out

    def wind_at(self, points, hour):
        """Mean wind vector (m/s) at each point: the day's 10 m wind, stronger higher above the ground.
        ponytail: no sheltering behind buildings or funnelling between them yet; that comes with the micro sim."""
        p = np.asarray(points, float).reshape(-1, 3)
        w = self.weather_at(hour)
        height = np.maximum(p[:, 2] - self.city.terrain.height(p[:, 0], p[:, 1]), 1.0)
        speed = w["wind"] * (height / 10.0) ** WIND_SHEAR
        return np.stack([speed * np.cos(w["wind_dir"]), speed * np.sin(w["wind_dir"]), np.zeros(len(p))], 1)

    def travel_time(self, hour):
        """Seconds to drive each road edge (city.edges) at this hour, with traffic and rain."""
        rush = sum(extra * np.exp(-0.5 * ((hour - peak) / spread) ** 2) for peak, spread, extra in (MORNING, EVENING))
        wet = 1.0 + 0.15 * (self.weather_at(hour)["rain_mm_h"] > 0.5)
        free = self.city.edge_length / self.city.edge_speed
        return free * (1.0 + self.busy * self.traffic_level * (0.1 + rush)) * wet

    def summary(self):
        w = self.weather
        stops = len(np.unique(self.parcel_address))
        sizes = ", ".join(f"{(self.parcel_size == s).mean():.0%} {s}" for s in SIZES)
        fragile = ", ".join(f"{(self.parcel_fragility == f).mean():.0%} {f}" for f in FRAGILITY)
        arterial = self.city.edge_arterial
        slow8 = (self.travel_time(8.0)[arterial] / self.travel_time(3.0)[arterial]).mean()
        return "\n".join([
            f"city seed {self.seed}, day {self.day}: {len(self.parcel_address)} parcels to {stops} addresses "
            f"({len(self.parcel_address) / stops:.2f} per stop)",
            f"sizes: {sizes}",
            f"weight: median {np.median(self.parcel_weight):.1f} kg, {(self.parcel_weight <= 2.27).mean():.0%} "
            f"at 5 lb (2.27 kg) or less, heaviest {self.parcel_weight.max():.1f} kg",
            f"fragility: {fragile}",
            f"recipients walk up to a median {np.median(self.recipient_walk):.0f} m and turn up after a median "
            f"{np.median(self.recipient_reply):.0f} min",
            f"weather: {w['temp_c'].min():.0f} to {w['temp_c'].max():.0f} C, wind {w['wind'].mean():.1f} m/s average "
            f"with gusts to {w['gust'].max():.1f} m/s, {w['rain_mm_h'].sum():.1f} mm of rain",
            f"traffic: arterials take {slow8:.2f}x as long at 8:00 as at 3:00",
        ])

    # Day files

    def save(self, path):
        """Write everything about the day to a .npz, tied to the city it was made for."""
        np.savez_compressed(path, city_seed=self.seed, day=self.day, fingerprint=fingerprint(self.city),
                            traffic_level=self.traffic_level, busy=self.busy,
                            **{k: getattr(self, k) for k in _PARCEL_FIELDS},
                            **{f"weather_{k}": v for k, v in self.weather.items()})

    @classmethod
    def load(cls, path, city):
        """Read a day file back exactly as saved. `city` must be the one it was made for."""
        data = np.load(path)
        if (int(data["city_seed"]), int(data["day"])) != (city.seed, city.day) or str(data["fingerprint"]) != fingerprint(city):
            raise ValueError(f"{path} was made for city seed {int(data['city_seed'])} day {int(data['day'])} "
                             "and doesn't match this city; rebuild the day files")
        day = cls.__new__(cls)
        day.city, day.seed, day.day = city, city.seed, city.day
        day.traffic_level, day.busy = float(data["traffic_level"]), data["busy"]
        for k in _PARCEL_FIELDS:
            setattr(day, k, data[k])
        day.weather = {k[8:]: data[k] for k in data.files if k.startswith("weather_")}
        return day


_PARCEL_FIELDS = ("parcel_address", "parcel_size", "parcel_dims", "parcel_weight", "parcel_fragility",
                  "recipient_walk", "recipient_reply")


def fingerprint(city):
    """Short hash of the city's addresses, so a day file can't be used with a different city."""
    return hashlib.sha1(np.round(city.address_door, 3).tobytes()).hexdigest()[:16]


def _wobble(rng, n, sd, keep=0.8):
    """Smooth random variation: each hour keeps `keep` of the last hour's offset."""
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = keep * x[i - 1] + rng.normal(0, sd)
    return x


def _weather(rng):
    """Hourly weather for one day, hours 0 to 24. Wind direction is the way it blows towards,
    as an angle from +x."""
    hour = np.arange(25.0)
    season = rng.uniform(0, 1)  # 0 = midwinter, 0.5 = midsummer
    mean = 12 - 10 * np.cos(2 * np.pi * season) + rng.normal(0, 3)
    temp = mean + rng.uniform(3, 7) * np.cos(2 * np.pi * (hour - 15) / 24) + _wobble(rng, 25, 0.5)
    base = 5.0 * rng.weibull(2.0)  # m/s at 10 m
    wind = np.maximum(base * (1 + 0.25 * np.cos(2 * np.pi * (hour - 14) / 24) + _wobble(rng, 25, 0.12)), 0.0)
    gust = wind * (1 + rng.uniform(0.3, 0.6) + np.abs(_wobble(rng, 25, 0.08)))
    direction = (rng.uniform(0, 2 * np.pi) + np.cumsum(rng.normal(0, 0.15, 25))) % (2 * np.pi)
    rain = np.zeros(25)
    if rng.random() < RAIN_CHANCE:
        for _ in range(int(rng.integers(1, 3))):
            start, length, rate = rng.uniform(0, 22), rng.uniform(1, 5), rng.exponential(2.0)
            rain += np.where((hour >= start) & (hour < start + length), rate, 0.0)
    return {"hour": hour, "temp_c": temp, "wind": wind, "gust": gust, "wind_dir": direction, "rain_mm_h": rain}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--day", type=int, default=0)
    p.add_argument("--parcels", type=int, default=500)
    p.add_argument("--held-out", metavar="DIR", help="write the held-out benchmark days to DIR")
    a = p.parse_args()
    if a.held_out:
        out = Path(a.held_out)
        out.mkdir(parents=True, exist_ok=True)
        for seed, d in HELD_OUT:
            Day(City(seed, day=d), a.parcels).save(out / f"city{seed}-day{d}.npz")
        print(f"wrote {len(HELD_OUT)} days to {out}")
        return
    start = perf_counter()
    city = City(a.seed, day=a.day)
    built = perf_counter() - start
    day = Day(city, a.parcels)
    total = perf_counter() - start
    print(day.summary())
    print(f"city built in {built * 1000:.0f} ms, city + day in {total * 1000:.0f} ms")


if __name__ == "__main__":
    main()
