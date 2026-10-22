"""Drones that launch from a moving truck and land on it further along its route.

The plan is the classical solver's (baselines/classical.py): the same split into drone and
locker parcels, the same pickup points and launch waypoints, the same OR-Tools routes. The
difference is that a truck no longer waits for its drones. It stops only as long as its
locker needs (a minute at a launch waypoint) and drives on.

Each drone takes off from wherever the truck is, flies to its parcel, puts it down, and flies
to meet the truck where it will be by then, landing on it on the move. For each parcel, in
the order the truck passes closest to it, the drone that's free soonest is sent, at the
launch time (from up to LEAD before the truck's closest pass) that gets it back on the truck
soonest. A drone isn't sent if it would be out of RANGE of the truck at the drop, couldn't
catch the truck before its battery runs down, or would land after the end of the shift.

The drone's speeds over the ground, its time climbing, putting the parcel down and coming in
to land, and its battery draw come from the cost model (sim/drone.py) for a round trip from
where the truck passes closest, at that hour. ponytail: the wind is taken along that line,
not the actual one, and the rendezvous leg flies straight at the truck.

Truck positions come from its real route along the roads, spread evenly in time along each
leg. ponytail: real trucks slow for junctions; the drone aims at the average position.

    python -m baselines.moving                 # one day in the default city
    python -m baselines.moving --held-out      # 50 held-out days, moving and parked launches side by side
"""
import argparse
from pathlib import Path

import numpy as np

from baselines import classical, dsp, prime_air
from baselines.classical import DRONES, RANGE, TURNAROUND
from sim import drone
from sim.roads import Paths

ENDURANCE = 40.0  # minutes: the longest any flight is looked at; the battery usually ends it sooner
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
            i = flown[mine[m]]
            trip = drone.sortie(day, where[closest[m]], i, grid[closest[m]])
            if trip is None:
                continue
            seconds_up = drone.usable_wh(day.weather_at(grid[closest[m]])["temp_c"]) / trip["watts"] * 3600
            out = far[m, go]
            done = grid[go] + (trip["fixed_out"] + out / trip["speed_out"]) / 3600  # parcel down, heading back
            later = np.minimum(go[:, None] + np.arange(1, steps)[None], len(grid) - 1)
            flying = (grid[later] - done[:, None]) * 3600 - trip["fixed_back"]
            catch = (flying >= 0) & (far[m, later] <= trip["speed_back"] * flying)
            reached = catch.any(1)
            land = grid[later[np.arange(len(go)), catch.argmax(1)]]
            good = reached & (out <= RANGE) & ok_weather[go] & (land <= end) & \
                (land - grid[go] <= min(ENDURANCE * 60, seconds_up) / 3600)
            if not good.any():
                continue
            c = int(np.argmin(np.where(good, land, np.inf)))
            when = done[c]
            point = city.spot_pos[trip["spot"]] + [0, 0, trip["height"]]
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
    from sim.day import Day

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
    from baselines.run import over_held_out

    rows = [(seed, d, r) for seed, d, rs in over_held_out(_both) for r in rs]
    _write_results(rows)


def _both(day):
    return [classical.solve(day, moving=moving) for moving in (False, True)]


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
        "10-minute locker wait, drones on the cost model in sim/drone.py). Parked: the truck waits at each stop until its drones are "
        "back. Moving: it only waits for the locker, and the drones launch from it and land on it as it drives, "
        f"with the battery set by the drone cost model.",
        "",
        "| | parked launches | moving launches |",
        "|---|---|---|",
    ] + [f"| {name} | {stat(False, f, fmt)} | {stat(True, f, fmt)} |" for name, f, fmt in measures] + [
        "",
        "## What it shows",
        "",
        "Launching from a moving truck changes the day by only a few minutes, either way. The trucks spend most "
        "of their day parked at locker pickup points: every drone parcel is already within the launch radius of "
        "one, so there are no stops just for launching. Each truck waits about 10 minutes at each of its 10 or "
        "so points, with short drives between. A drone's flight is a few minutes, so it's usually back while the "
        "truck is still there. When the truck doesn't wait for its drones, it leaves sooner, but the drones then "
        "have further to fly to catch it and are busy for longer, so the two roughly cancel out.",
        "",
        "In this city the locker wait, not the drones, is what holds the trucks up. Moving launches should "
        "matter more where trucks drive further between stops: bigger cities, fewer locker parcels, or shorter "
        "locker waits.",
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
