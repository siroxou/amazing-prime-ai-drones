"""Drones that launch from a moving truck and land on it further along its route.

The plan is the classical solver's (baselines/classical.py): the same split into drone and
locker parcels, the same pickup points and launch waypoints, the same OR-Tools routes. The
difference is that a truck no longer waits for its drones. It stops only as long as its
locker needs (a minute at a launch waypoint) and drives on.

Each drone takes off from wherever the truck is, flies to its parcel, lowers it, and flies
to meet the truck where it will be by then, landing on it on the move. For each parcel, in
the order the truck passes closest to it, the drone that's free soonest is sent, at the
launch time (from up to LEAD before the truck's closest pass) that gets it back on the truck
soonest. A drone isn't sent if it would be out of RANGE of the truck at the drop, couldn't
catch the truck within ENDURANCE, or would land after the end of the shift.

Truck positions come from its real route along the roads, spread evenly in time along each
leg. ponytail: real trucks slow for junctions; the drone aims at the average position.

    python -m baselines.moving                 # one day in the default city
    python -m baselines.moving --held-out      # 50 held-out days, moving and parked launches side by side
"""
import argparse
from pathlib import Path

import numpy as np

from baselines import classical, dsp, prime_air
from baselines.classical import DROP, DRONES, LAUNCH_LAND, RANGE, SPEED, TURNAROUND
from sim.roads import Paths

ENDURANCE = 25.0  # minutes in the air on one battery, guess
LEAD = 15.0  # minutes before the truck's closest pass a drone may set off
TICK = 10.0  # seconds between the truck positions the drones plan against


def trajectory(city, shift, paths, route, service):
    """Times (h) and places the truck passes, from leaving the station until it's back, following
    the same rules as dsp.drive (stops it can't fit are skipped)."""
    end = dsp.SHIFT_START + dsp.SHIFT
    clock, at = dsp.SHIFT_START + dsp.LOADOUT, 0
    times, places = [clock], [city.nodes[shift.nodes[0]]]

    def go(a, b, depart, arrive):
        p = city.nodes[paths.between(shift.nodes[a], shift.nodes[b])]
        along = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
        frac = along / along[-1] if along[-1] > 0 else np.zeros(len(p))
        times.extend(depart + frac[1:] * (arrive - depart))
        places.extend(p[1:])

    for j in route:
        arrive = clock + shift.leg(at, j, clock) / 3600
        leave = arrive + service[j] / 3600
        if leave + shift.leg(j, 0, leave) / 3600 > end:
            continue
        go(at, j, clock, arrive)
        times.append(leave)
        places.append(city.nodes[shift.nodes[j]])
        clock, at = leave, j
    go(at, 0, clock, clock + shift.leg(at, 0, clock) / 3600)
    return np.array(times), np.array(places)


def _flyable_grid(day, hours):
    w = day.weather
    return (np.interp(hours, w["hour"], w["gust"]) <= prime_air.GUST_LIMIT) & \
           (np.interp(hours, w["hour"], w["rain_mm_h"]) <= prime_air.RAIN_LIMIT)


def fly(day, plan, spot, target):
    """Drop time of each planned drone parcel (NaN where it can't go), which ones can't go, and the
    extra truck hours spent waiting at the station for the last drones home. Every flight is also
    recorded in plan["flights"] as (parcel, route, launch, drop, landing) times in hours, and each
    route's trajectory in plan["trajectories"]."""
    city = day.city
    flown = np.flatnonzero(plan["fly"])
    drop = np.full(len(flown), np.nan)
    shift, service = plan["shift"], plan["service"]
    paths = Paths(city, np.mean([day.travel_time(h + 0.5) for h in shift.hours], 0), shift.nodes)
    end = dsp.SHIFT_START + dsp.SHIFT
    extra = 0.0
    plan["flights"], plan["trajectories"] = [], []
    steps = int(ENDURANCE * 60 / TICK)
    stop_of = np.full(len(shift.nodes) - 1, -1)
    for r, route in enumerate(plan["routes"]):
        stop_of[np.array(route) - 1] = r
    for r, route in enumerate(plan["routes"]):
        mine = np.flatnonzero(stop_of[plan["drone_stop"]] == r)
        times, places = trajectory(city, shift, paths, route, service)
        plan["trajectories"].append((times, places))
        grid = np.arange(times[0], end + ENDURANCE / 60, TICK / 3600)
        where = np.stack([np.interp(grid, times, places[:, 0]), np.interp(grid, times, places[:, 1])], 1)
        ok_weather = _flyable_grid(day, grid)
        far = np.linalg.norm(where[None] - target[flown[mine]][:, None], axis=-1)  # parcels x ticks
        closest = far.argmin(1)
        free = np.full(DRONES, grid[0])
        last = 0.0
        for m in np.argsort(closest, kind="stable"):
            k = int(free.argmin())
            first = max(int(np.searchsorted(grid, free[k])), closest[m] - int(LEAD * 60 / TICK))
            go = np.arange(first, min(first + 3 * int(LEAD * 60 / TICK), len(grid) - 1), 3)
            if len(go) == 0:
                continue
            out = far[m, go]
            at_drop = grid[go] + (LAUNCH_LAND / 2 + out / SPEED) / 3600 + DROP / 3600
            later = np.minimum(go[:, None] + np.arange(1, steps)[None], len(grid) - 1)
            catch = (grid[later] >= at_drop[:, None]) & \
                    (far[m, later] <= SPEED * (grid[later] - at_drop[:, None]) * 3600)
            reached = catch.any(1)
            land = grid[later[np.arange(len(go)), catch.argmax(1)]] + LAUNCH_LAND / 2 / 3600
            good = reached & (out <= RANGE) & ok_weather[go] & (land <= end) & (land - grid[go] <= ENDURANCE / 60)
            if not good.any():
                continue
            c = int(np.argmin(np.where(good, land, np.inf)))
            when = grid[go[c]] + (LAUNCH_LAND / 2 + out[c] / SPEED + DROP / 2) / 3600
            i = flown[mine[m]]
            point = np.append(city.spot_pos[spot[i]], 0.0)[:3] + [0, 0, prime_air.DROP_HEIGHT]
            if prime_air.path_length(city, where[go[c]], target[i], when) is None or \
                    city.airspace.blocked([point], when)[0]:
                continue
            drop[mine[m]] = when
            plan["flights"].append((i, r, grid[go[c]], when, land[c]))
            free[k] = land[c] + TURNAROUND / 3600
            last = max(last, land[c])
        extra += max(0.0, last - plan["back"][r])
    return drop, np.isnan(drop), extra


def main():
    from sim.city import City
    from sim.day import HELD_OUT, Day

    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--day", type=int, default=0)
    p.add_argument("--held-out", action="store_true")
    a = p.parse_args()
    if not a.held_out:
        day = Day(City(a.seed, day=a.day))
        for moving in (False, True):
            print(("moving: " if moving else "parked: ") + classical.describe(classical.solve(day, moving=moving)))
        return
    rows = []
    for seed, d in HELD_OUT:
        day = Day.load(Path("data/held-out") / f"city{seed}-day{d}.npz", City(seed, day=d))
        for moving in (False, True):
            r = classical.solve(day, moving=moving)
            rows.append((seed, d, r))
            print(seed, d, "moving" if moving else "parked", classical.describe(r), flush=True)
    _write_results(rows)


def _write_results(rows):
    from baselines.trucks_only import half

    def stat(moving, f, fmt):
        return fmt(np.mean([f(r) for *_, r in rows if r["moving"] == moving]))

    measures = [
        ("trucks", lambda r: r["trucks"], lambda v: f"{v:.1f}"),
        ("stops", lambda r: r["stops"], lambda v: f"{v:.0f}"),
        ("parcels delivered today", lambda r: np.mean(~np.isnan(r["parcel_time"])), lambda v: f"{v:.0%}"),
        ("by drone", lambda r: r["by_drone"], lambda v: f"{v:.0%}"),
        ("last parcel", lambda r: r["last"], dsp._clock),
        ("half of all parcels by", lambda r: half(r["parcel_time"]), dsp._clock),
        ("delivered by 14:00", lambda r: np.mean(r["parcel_time"] <= 14), lambda v: f"{v:.0%}"),
        ("truck hours", lambda r: r["truck_hours"], lambda v: f"{v:.1f}"),
        ("km driven", lambda r: r["km"], lambda v: f"{v:.0f}"),
    ]
    lines = [
        "# Launching from a moving truck",
        "",
        f"Written by `python -m baselines.moving --held-out`. {len({(s, d) for s, d, _ in rows})} days, 500 "
        "parcels each, averages over the days. Both columns use the classical solver's plan (600 m launch radius, "
        "10-minute locker wait, fixed-speed drones). Parked: the truck waits at each stop until its drones are "
        "back. Moving: it only waits for the locker, and the drones launch from it and land on it as it drives, "
        f"with {ENDURANCE:.0f} minutes in the air per battery.",
        "",
        "| | parked launches | moving launches |",
        "|---|---|---|",
    ] + [f"| {name} | {stat(False, f, fmt)} | {stat(True, f, fmt)} |" for name, f, fmt in measures] + [
        "",
        "## Every day",
        "",
        "| city | day | launches | result |",
        "|---|---|---|---|",
    ] + [f"| {s} | {d} | {'moving' if r['moving'] else 'parked'} | {classical.describe(r)} |" for s, d, r in rows]
    Path("results").mkdir(exist_ok=True)
    Path("results/moving-launch.md").write_text("\n".join(lines) + "\n")
    print("wrote results/moving-launch.md")


if __name__ == "__main__":
    main()
