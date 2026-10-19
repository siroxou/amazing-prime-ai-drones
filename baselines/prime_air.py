"""Amazon Prime Air baseline: delivery drones flying from a fixed site, with DSP vans taking
every parcel the drones can't.

The drone site is at the distribution centre, as Prime Air sites sit at Amazon delivery
facilities. Each drone carries one parcel: it climbs to cruise height, flies out (around any
no-fly zone it can't fly over), comes down to DROP_HEIGHT over the customer's yard, lets go,
climbs and flies back, and then takes TURNAROUND to load the next parcel and change battery.
The drones are scheduled in the morning, with the day's weather known in advance (which
flatters them). Parcels they can't take go on the vans, which leave at 10:00 as usual.

Settings and sources are in docs/amazon-baseline.md.

    python -m baselines.prime_air                 # one day in the default city
    python -m baselines.prime_air --held-out      # 50 held-out days at 5, 10 and 20 drones
"""
import argparse
from pathlib import Path

import numpy as np

from baselines import dsp
from baselines.dsp import _clock

PAYLOAD = 2.27  # kg (5 lb)
SIZES = ("envelope", "small", "medium")  # guess at what fits the cargo box; no box size is published
RANGE = 12_070.0  # m (7.5 miles) from the site
CRUISE_SPEED = 30.0  # m/s (58 knots)
CRUISE_HEIGHT, MAX_HEIGHT, UNDER_HEIGHT, DROP_HEIGHT = 61.0, 122.0, 25.0, 4.0  # m above the ground
CLIMB, DESCEND = 3.0, 2.0  # m/s, guess
DROP = 15.0  # s hovering to let the parcel go, guess
TURNAROUND = 300.0  # s at the site to load the next parcel and change battery, guess
CLEAR_RADIUS = 3.0  # m kept clear around the drop (10 ft)
RAIN_LIMIT = 2.5  # mm/h: light rain is fine; 2.5 mm/h is where "light rain" ends
GUST_LIMIT = 12.0  # m/s, guess: no wind limit is published
OPEN, CLOSE = dsp.SHIFT_START + dsp.LOADOUT, dsp.SHIFT_START + dsp.SHIFT  # flying hours, the same as the vans
DRONES = 10
STEP = 0.25  # h to wait before trying again when the weather or a no-fly zone is in the way


def drop_spots(city):
    """For each address, the drop spot a Prime Air drone would use, or -1. Houses only: the drone
    lowers a parcel into a yard. A spot needs open sky and nothing within CLEAR_RADIUS from 1.5 m up
    (so a garden fence is fine but a shed roof or a tree isn't). Back yard first, then front."""
    best = np.full(len(city.address_kind), -1)
    for kind in ("front_yard", "back_yard"):  # back yard written last, so it wins
        for s in np.flatnonzero(city.spot_kind == kind):
            a = city.spot_address[s]
            if city.spot_overhead[s] >= 100 and city.obstacles.touching(
                    city.spot_pos[s] + [0, 0, 1.5 + CLEAR_RADIUS], CLEAR_RADIUS) is None:
                best[a] = s
    best[city.address_kind != "house"] = -1
    return best


def _walls(city, hour):
    """No-fly zones a drone can't fly over or under at this hour, as circles (centre, radius).
    ponytail: a rectangle is treated as the circle around it; only the runway is one of these."""
    sky = city.airspace
    on = sky.active & (sky.hours[:, 0] <= hour) & (hour < sky.hours[:, 1])
    wall = on & (sky.floor < UNDER_HEIGHT) & (sky.ceiling > MAX_HEIGHT)
    radius = np.where(sky.circle, sky.half[:, 0], np.hypot(*sky.half.T))
    return sky.centre[wall], radius[wall]


def path_length(city, a, b, hour):
    """Flight distance from a to b going round no-fly walls, or None if b is inside one.
    ponytail: goes round each circle on its own; overlapping walls would need a real planner."""
    centres, radii = _walls(city, hour)
    ab = b - a
    length = float(np.linalg.norm(ab))
    for c, r in zip(centres, radii):
        if np.linalg.norm(b - c) < r:
            return None
        t = np.clip((c - a) @ ab / max(ab @ ab, 1e-9), 0, 1)
        d = float(np.linalg.norm(a + t * ab - c))
        if d < r:
            length += 2 * r * np.arccos(d / r) - 2 * np.sqrt(r * r - d * d)  # the arc instead of the chord
    return length


def ground_speeds(day, site, heading, hour):
    """Ground speed out and back along `heading` in the day's wind at cruise height, or None if the
    wind across the track is faster than the drone."""
    w = day.wind_at([[*site, day.city.terrain.height(*site) + CRUISE_HEIGHT]], hour)[0, :2]
    along, across = w @ heading, abs(w[0] * heading[1] - w[1] * heading[0])
    if across >= CRUISE_SPEED:
        return None
    still = np.sqrt(CRUISE_SPEED ** 2 - across ** 2)
    out, back = still + along, still - along
    return (out, back) if min(out, back) > 1 else None


def sortie(day, site, target, hour):
    """(seconds from take-off to the drop, seconds until the drone can take off again), or None."""
    length = path_length(day.city, site, target, hour)
    if length is None:
        return None
    straight = np.linalg.norm(target - site)
    speeds = ground_speeds(day, site, (target - site) / max(straight, 1e-9), hour)
    if speeds is None:
        return None
    out, back = speeds
    to_drop = CRUISE_HEIGHT / CLIMB + length / out + (CRUISE_HEIGHT - DROP_HEIGHT) / DESCEND + DROP
    home = (CRUISE_HEIGHT - DROP_HEIGHT) / CLIMB + length / back + CRUISE_HEIGHT / DESCEND
    return to_drop, to_drop + home + TURNAROUND


def flyable(day, hour):
    w = day.weather_at(hour)
    return w["gust"] <= GUST_LIMIT and w["rain_mm_h"] <= RAIN_LIMIT


def schedule(day, drones=DRONES):
    """Plan the drones' day. Returns (drop time per parcel, NaN if not by drone; reason per parcel
    it couldn't take; number of sorties; flight hours). Shortest sorties go first, which gets the
    most parcels out early; each goes to the drone free soonest."""
    city = day.city
    site = city.station_centre
    n = len(day.parcel_address)
    spot = drop_spots(city)[day.parcel_address]
    target = city.spot_pos[np.maximum(spot, 0), :2]
    reason = np.full(n, "", dtype=object)
    reason[spot < 0] = "no drop spot"
    reason[np.linalg.norm(target - site, axis=1) > RANGE] = "out of range"
    reason[~np.isin(day.parcel_size, SIZES)] = "too big"
    reason[day.parcel_weight > PAYLOAD] = "too heavy"
    times = np.full(n, np.nan)
    candidates = np.flatnonzero(reason == "")
    order = candidates[np.argsort(np.linalg.norm(target[candidates] - site, axis=1), kind="stable")]
    free = np.full(drones, OPEN)
    sorties, flying = 0, 0.0
    for i in order:
        k = int(free.argmin())
        start, why = free[k], "no time"
        drop = np.append(city.spot_pos[spot[i]], 0.0)[:3] + [0, 0, DROP_HEIGHT]
        while start < CLOSE:
            if not flyable(day, start):
                why, start = "weather", start + STEP
                continue
            trip = sortie(day, site, target[i], start)
            if trip is None:
                why, start = "no-fly zone", start + STEP
                continue
            at = start + trip[0] / 3600
            if city.airspace.blocked([drop], at)[0]:
                why, start = "no-fly zone", start + STEP
                continue
            if start + (trip[1] - TURNAROUND) / 3600 > CLOSE:
                why = "no time"
                break
            times[i], free[k] = at, start + trip[1] / 3600
            sorties, flying = sorties + 1, flying + (trip[1] - TURNAROUND) / 3600
            break
        if np.isnan(times[i]):
            reason[i] = why
    return times, reason, sorties, flying


def baseline(day, drones=DRONES, seconds=dsp.SOLVER_SECONDS):
    """Drones from the site first, then DSP vans for everything else."""
    times, reason, sorties, flying = schedule(day, drones)
    vans = dsp.baseline(day, seconds=seconds, by_van=np.isnan(times))
    parcel_time = np.where(np.isnan(times), vans["parcel_time"], times)
    return {
        "drones": drones, "by_drone": float(np.mean(~np.isnan(times))), "sorties": sorties, "flight_hours": flying,
        "reasons": {r: int((reason == r).sum()) for r in sorted(set(reason) - {""})},
        "vans": vans["vans"], "driver_hours": vans["driver_hours"], "km": vans["km"],
        "parcel_time": parcel_time, "undelivered": int(np.isnan(parcel_time).sum()),
        "last": float(np.nanmax(parcel_time)),
    }


def describe(r):
    t = r["parcel_time"]
    return (f"{r['drones']} drones: {r['by_drone']:.0%} by drone ({r['sorties']} sorties), {r['vans']} vans; "
            f"last parcel at {_clock(r['last'])}, half delivered by {_clock(np.nanmedian(t))}, "
            f"{np.mean(t <= 14):.0%} by 14:00; {r['driver_hours']:.1f} driver hours; not by drone: {r['reasons']}")


def main():
    from sim.city import City
    from sim.day import HELD_OUT, Day

    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--day", type=int, default=0)
    p.add_argument("--drones", type=int, default=DRONES)
    p.add_argument("--held-out", action="store_true")
    a = p.parse_args()
    if not a.held_out:
        print(describe(baseline(Day(City(a.seed, day=a.day)), a.drones)))
        return
    rows = []
    for seed, d in HELD_OUT:
        day = Day.load(Path("data/held-out") / f"city{seed}-day{d}.npz", City(seed, day=d))
        for drones in (5, 10, 20):
            r = baseline(day, drones)
            rows.append((seed, d, r))
            print(seed, d, describe(r), flush=True)
    _write_results(rows)


def _write_results(rows):
    lines = [
        "# Prime Air baseline on the held-out days",
        "",
        f"Written by `python -m baselines.prime_air --held-out`. {len({(s, d) for s, d, _ in rows})} days, 500 parcels "
        "each. Drones fly from a site at the distribution centre between "
        f"{_clock(OPEN)} and {_clock(CLOSE)}, one parcel at a time; DSP vans take the rest, as in "
        "[dsp-baseline.md](dsp-baseline.md). Settings are in [docs/amazon-baseline.md](../docs/amazon-baseline.md).",
        "",
        "| drones at the site | by drone | vans | last parcel | half delivered by | by 14:00 | driver hours |",
        "|---|---|---|---|---|---|---|",
    ]
    for drones in (5, 10, 20):
        rs = [r for *_, r in rows if r["drones"] == drones]
        lines.append(
            f"| {drones} | {np.mean([r['by_drone'] for r in rs]):.0%} | {np.mean([r['vans'] for r in rs]):.1f} | "
            f"{_clock(np.mean([r['last'] for r in rs]))} | "
            f"{_clock(np.mean([np.nanmedian(r['parcel_time']) for r in rs]))} | "
            f"{np.mean([np.mean(r['parcel_time'] <= 14) for r in rs]):.0%} | "
            f"{np.mean([r['driver_hours'] for r in rs]):.1f} |")
    rs = [r for *_, r in rows if r["drones"] == 10]
    total = sum(len(r["parcel_time"]) for r in rs)
    reasons = {}
    for r in rs:
        for k, v in r["reasons"].items():
            reasons[k] = reasons.get(k, 0) + v
    lines += [
        "",
        "## Why parcels didn't go by drone (10 drones)",
        "",
        "| reason | share of all parcels |",
        "|---|---|",
    ] + [f"| {k} | {v / total:.1%} |" for k, v in sorted(reasons.items(), key=lambda kv: -kv[1])] + [
        "",
        "## Every day",
        "",
        "| city | day | result |",
        "|---|---|---|",
    ] + [f"| {s} | {d} | {describe(r)} |" for s, d, r in rows]
    Path("results").mkdir(exist_ok=True)
    Path("results/prime-air-baseline.md").write_text("\n".join(lines) + "\n")
    print("wrote results/prime-air-baseline.md")


if __name__ == "__main__":
    main()
