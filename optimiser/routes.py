"""A planned day, boiled down to what's needed to replay its truck routes with different waits.

The classical solver (baselines/classical.py) plans the day: which parcels go by drone, the
stops, and the order each truck drives them. Replaying keeps all of that and changes only how
long each truck waits at each stop for its locker. A stop's wait never drops below the time
its drones need to get back; the locker wait can make it longer. Drone drops stay at the same
time after the truck gets to the stop, and are checked against the weather at the new time.
Locker recipients turn up as in the trucks-only baseline: told NOTICE minutes before the truck
gets there, they come when they're ready and walk over, and collect if the truck is still there.

The score is the average hours from 10:00 until each parcel is delivered, with a parcel that
isn't delivered today counted as MISSED hours (delivered the next day). One number that weighs
speed against parcels left behind; every report shows the parts as well.
"""
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from baselines import classical, dsp, prime_air, trucks_only

MISSED = 24.0  # hours a parcel not delivered today counts as
START, END = dsp.SHIFT_START + dsp.LOADOUT, dsp.SHIFT_START + dsp.SHIFT


@dataclass
class Stop:
    parcels: np.ndarray  # the day's parcel indices here: locker ones first, then drone ones
    locker_ready: np.ndarray  # hours from being told to turning up, per locker parcel collected here
    locker_walk: np.ndarray  # m each of them walks
    drone_offset: np.ndarray  # hours from the truck arriving to each drone drop (NaN: can't fly at all)
    drone_launch: np.ndarray  # hours from the truck arriving to each drone taking off
    busy: float  # hours until the last drone is back on the truck


@dataclass
class Route:
    stops: list  # Stop per stop, in driving order
    legs: dict  # hour -> matrix of seconds between the route's stops, station first
    gust: np.ndarray  # the day's hourly gusts and rain, for checking the drones at new times
    rain: np.ndarray
    fixed: list = field(default_factory=list)  # hours for parcels whose fate the waits can't change


@dataclass
class Plan:
    routes: list
    parcels: int  # all the day's parcels
    fixed: np.ndarray  # delivery hours (NaN: missed) of parcels on no route, e.g. no pickup point in reach
    fixed_parcels: np.ndarray = None  # their indices
    day_id: tuple = None  # (city seed, day number), to rebuild the day for the second pass


def plan_day(day, seconds=dsp.SOLVER_SECONDS):
    """Plan a day with the classical solver (parked launches) and boil it down for replaying."""
    return from_solve(day, classical.solve(day, seconds=seconds))


def from_solve(day, r):
    """Boil down one classical.solve result for replaying."""
    plan, drop_time = r["plan"], r["drop_time"]
    flown, locker = np.flatnonzero(plan["fly"]), np.flatnonzero(plan["locker"])
    point, walk = plan["point"], plan["walk"]
    ready = (day.recipient_reply[locker] + walk / trucks_only.WALK_SPEED / 60) / 60
    at = plan["at"]
    stops = []
    for j in range(len(plan["nodes"])):
        mine = plan["drone_stop"] == j
        ok = mine & np.isfinite(plan["cycle"])
        _, busy = classical.share_out(plan["cycle"][ok])
        stops.append(Stop(parcels=np.r_[locker[point == j], flown[mine]],
                          locker_ready=ready[point == j], locker_walk=walk[point == j],
                          drone_offset=(drop_time[mine] - at[j]) if np.isfinite(at[j]) else
                          np.full(mine.sum(), np.nan),
                          drone_launch=plan["start"][mine] / 3600, busy=busy / 3600))
    shift = plan["shift"]
    routes = []
    for route in plan["routes"]:
        idx = np.r_[0, route]
        legs = {h: m[np.ix_(idx, idx)] for h, m in shift.hourly.items()}
        routes.append(Route([stops[j - 1] for j in route], legs, day.weather["gust"], day.weather["rain_mm_h"]))
    on_route = {j - 1 for route in plan["routes"] for j in route}
    fixed = [locker[point < 0]]  # nobody would walk to any pickup point
    fixed += [stops[j].parcels for j in sorted(set(range(len(plan["nodes"]))) - on_route)]  # stops no truck got to
    fixed = np.concatenate(fixed).astype(int)
    return Plan(routes, len(day.parcel_address), np.full(len(fixed), np.nan), fixed, (day.seed, day.day))


def leg(route, a, b, clock):
    hours = sorted(route.legs)
    return route.legs[min(max(int(clock), hours[0]), hours[-1])][a, b] / 3600


def stop_times(route, k, arrive, wait):
    """Delivery hours of the parcels at the route's k-th stop if the truck gets there at `arrive` and
    waits `wait` hours for the locker (NaN: missed), and how long it actually stays."""
    s = route.stops[k]
    stay = max(s.busy, wait, 1 / 60)
    came = arrive - trucks_only.NOTICE / 60 + s.locker_ready
    locker = np.where(came <= arrive + stay, np.maximum(came, arrive), np.nan)
    launch = arrive + s.drone_launch
    ok = (np.interp(launch, np.arange(25.0), route.gust) <= prime_air.GUST_LIMIT) & \
         (np.interp(launch, np.arange(25.0), route.rain) <= prime_air.RAIN_LIMIT)
    drones = np.where(ok, arrive + s.drone_offset, np.nan)
    return np.r_[locker, drones], stay


def replay(route, waits, back=False):
    """Drive the route with a wait (hours) at each stop. Stops it can't fit and still be back by the end
    of the shift are skipped, as in dsp.drive. Returns delivery hours of every parcel on it, in stop order
    (and with back=True, also when the truck is back at the station)."""
    clock, at, out = START, 0, []
    for k, wait in enumerate(waits):
        arrive = clock + leg(route, at, k + 1, clock)
        times, stay = stop_times(route, k, arrive, wait)
        if arrive + stay + leg(route, k + 1, 0, arrive + stay) > END:
            out.append(np.full(len(times), np.nan))
            continue
        out.append(times)
        clock, at = arrive + stay, k + 1
    times = np.concatenate(out) if out else np.zeros(0)
    return (times, clock + leg(route, at, 0, clock)) if back else times


def score(times):
    """Average hours from 10:00 to delivery, a missed parcel counting MISSED."""
    t = np.asarray(times, float)
    return float(np.mean(np.where(np.isnan(t), MISSED, t - START))) if len(t) else 0.0


def day_times(plan, waits_per_route):
    """Delivery hours of all the day's parcels, routes replayed with the given waits."""
    return np.concatenate([plan.fixed] + [replay(r, w) for r, w in zip(plan.routes, waits_per_route)])


def with_second_pass(plan, waits_per_route, day):
    """Delivery hours of every parcel (indexed like the day's), the routes replayed with these waits and then
    each truck's afternoon second pass (baselines/classical.second_pass)."""
    t = np.full(plan.parcels, np.nan)
    trucks = []
    for route, waits in zip(plan.routes, waits_per_route):
        times, home = replay(route, waits, back=True)
        parcels = np.concatenate([s.parcels for s in route.stops]).astype(int)
        t[parcels] = times
        trucks.append((home, parcels))
    return classical.second_pass(day, trucks, t)[0]


def summary(times):
    t = np.asarray(times, float)
    return {"score": score(t), "delivered": float(np.mean(~np.isnan(t))),
            "half": trucks_only.half(t), "by14": float(np.mean(t <= 14)),
            "last": float(np.nanmax(t)) if (~np.isnan(t)).any() else np.nan}


def build(pairs, path, workers=None):
    """Plan the (city seed, day) pairs in parallel and save them to `path`."""
    import pickle
    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(workers) as pool:
        plans = list(pool.map(_plan_pair, pairs))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(plans, f)
    return plans


def _plan_pair(pair):
    from sim.city import City
    from sim.day import HELD_OUT, Day

    seed, d = pair
    city = City(seed, day=d)
    held = Path("data/held-out") / f"city{seed}-day{d}.npz"
    day = Day.load(held, city) if (seed, d) in HELD_OUT else Day(city)
    return plan_day(day)


def load(path):
    import pickle

    with open(path, "rb") as f:
        return pickle.load(f)
