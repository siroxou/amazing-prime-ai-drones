"""Classical truck + drone solver: the project's own system, planned with plain heuristics and
OR-Tools, with the drone cost model in sim/drone.py. This is the first version of the fleet, and
the bar a learned optimiser will have to beat.

Each autonomous truck carries DRONES drones and a locker. It leaves the distribution centre
and parks at a series of stops. At each stop its drones fly out to the parcels assigned to
that stop and come back to it, and recipients of locker parcels near the stop walk over to
collect them. The truck moves on when the last drone is back and the locker wait is over.

    1. Every parcel a drone can take goes by drone: light enough, small enough, and an address
       where it can drop, lower or set the parcel down in the day's wind (sim/drone.py drop
       planning), checked at midday.
    2. Locker parcels get pickup points, as in the trucks-only baseline.
    3. Drone parcels are flown from the nearest pickup point within LAUNCH_RADIUS. The rest get
       new launch stops, chosen greedily to cover as many of them as possible.
    4. At each stop the sorties are shared out between the drones, longest first.
    5. OR-Tools routes the trucks through the stops, as for the DSP vans.
    6. The day is driven with real traffic. Drone parcels the weather or airspace stops at the
       time the truck gets there become locker parcels, and the day is planned again once
       (the weather forecast is taken as known, as for Prime Air).
    7. Afternoon second pass: once a truck is back, it reloads for RELOAD and goes out again with
       the parcels it couldn't deliver. Anything a drone can take at that hour goes by drone,
       since the wind may have dropped. Everyone else gets a second notice (they take a fresh
       amount of time to turn up, sim/day.py) and the truck waits SECOND_WAIT at each stop.
       It has to be back by the end of the shift like everyone else.

Each flight's time and battery come from the cost model: its height over the rooftops and
wires, the parcel's weight and size, and the wind at the hour it flies. Every setting is a
guess, here and in sim/drone.py.

    python -m baselines.classical                  # one day in the default city
    python -m baselines.classical --held-out       # the 50 held-out days
"""
import argparse
from pathlib import Path

import numpy as np

from baselines import dsp, prime_air, trucks_only
from baselines.dsp import _clock
from sim import drone

DRONES = 10  # per truck
PAYLOAD = 5.0  # kg
SIZES = ("envelope", "small", "medium", "large")
RANGE = 3000.0  # m, furthest a drop can be from the truck (radio range)
TURNAROUND = 60.0  # s on the truck to load the next parcel and swap the battery
PLAN_HOUR = 13.0  # the weather the plan is made for; each flight is checked again at the hour it flies
RELOAD = 0.25  # h back at the station before the second pass
SECOND_WAIT = 20.0  # minutes the truck waits at each stop on the second pass, guess
SECOND_SECONDS = 1  # OR-Tools seconds for a second-pass route: only a handful of stops
LAUNCH_RADIUS = 600.0  # m: drone parcels further than this from any pickup point get a launch stop of their own
CAPACITY = 300  # parcels a truck carries, locker and drone parcels together
WINDOW = trucks_only.WINDOW  # minutes the locker waits at a stop, at least
RADII = (300.0, 600.0, 1000.0)  # launch radii tried on the held-out days


def drop_spots(day):
    """For each parcel, the spot its quickest drop option uses at PLAN_HOUR, or -1 if no drone can take it."""
    ok = (day.parcel_weight <= PAYLOAD) & np.isin(day.parcel_size, SIZES)
    spot = np.full(len(day.parcel_address), -1)
    for i in np.flatnonzero(ok):
        options = drone.drop_options(day, i, PLAN_HOUR)
        if options:
            spot[i] = options[0][1]
    return spot


def share_out(cycles, drones=DRONES):
    """Longest-first over the drones. Returns (seconds after arriving that each sortie starts,
    seconds until the last drone is back)."""
    start = np.zeros(len(cycles))
    busy = np.zeros(drones)
    for i in np.argsort(-cycles, kind="stable"):
        k = int(busy.argmin())
        start[i], busy[k] = busy[k], busy[k] + cycles[i]
    return start, float((busy - TURNAROUND * (busy > 0)).max(initial=0.0))


def launch_stops(city, targets, base, radius):
    """Stop per drone parcel: the nearest of `base` (road nodes) within radius, else new road nodes
    chosen greedily. Returns (all stop nodes, base first; stop index per parcel)."""
    if len(targets) == 0:
        return np.asarray(base, int), np.zeros(0, int)
    nodes = np.flatnonzero((city.nodes[:, 0] >= 0) & (city.nodes[:, 0] <= city.width)
                           & (city.nodes[:, 1] >= 0) & (city.nodes[:, 1] <= city.height))
    stops = list(base)
    far = np.linalg.norm(targets[:, None] - city.nodes[nodes][None], axis=-1) <= radius
    near_base = np.linalg.norm(targets[:, None] - city.nodes[base][None], axis=-1).min(1, initial=np.inf) <= radius
    left = ~near_base
    while left.any():
        best = int((far & left[:, None]).sum(0).argmax())
        if not far[left, best].any():  # nothing within radius of any road node: fly from the nearest one
            best = int(np.linalg.norm(targets[left][0] - city.nodes[nodes], axis=1).argmin())
            left[np.flatnonzero(left)[0]] = False
        stops.append(nodes[best])
        left &= ~far[:, best]
    stops = np.array(stops, int)
    stop = np.linalg.norm(targets[:, None] - city.nodes[stops][None], axis=-1).argmin(1)
    return stops, stop


def solve(day, radius=LAUNCH_RADIUS, window=WINDOW, seconds=dsp.SOLVER_SECONDS, moving=False, second=True):
    """Plan and run a day. With moving=True the trucks don't wait for their drones: drones launch from
    and land on the truck as it drives (baselines/moving.py). With second=True each truck goes out again
    in the afternoon with what it couldn't deliver."""
    from baselines import moving as on_the_move

    fly_them = on_the_move.fly if moving else _fly
    city = day.city
    n = len(day.parcel_address)
    spot = drop_spots(day)
    target = city.spot_pos[np.maximum(spot, 0), :2]
    fly = spot >= 0
    for attempt in range(2):
        plan = _plan(day, fly, target, radius, window, seconds, parked=not moving)
        drop_time, failed, extra = fly_them(day, plan, spot, target)
        if attempt == 0 and failed.any():
            fly = fly.copy()
            fly[np.flatnonzero(fly)[failed]] = False  # the weather or a no-fly zone stops them: locker instead
            continue
        break
    t = np.full(n, np.nan)
    flown = np.flatnonzero(plan["fly"])
    t[flown] = drop_time  # NaN where it couldn't fly after all
    t[np.flatnonzero(plan["locker"])] = plan["collected"]
    morning = t.copy()
    by_drone = int((~np.isnan(t[flown])).sum())
    later = {"hours": 0.0, "by_drone": 0, "km": 0.0, "plans": []}
    if second:
        t, later = second_pass(day, trucks_of(plan), t, radius)
    return {
        "radius": radius, "moving": moving, "second": second, "trucks": plan["trucks"], "stops": len(plan["nodes"]),
        "parcel_time": t, "by_drone": float((by_drone + later["by_drone"]) / n),
        "second_pass": int((np.isnan(morning) & ~np.isnan(t)).sum()),
        "undelivered": int(np.isnan(t).sum()), "last": float(np.nanmax(t)) if (~np.isnan(t)).any() else np.nan,
        "truck_hours": plan["truck_hours"] + extra + later["hours"], "km": plan["km"] + later["km"],
        "replanned": int(attempt),
        "plan": plan, "drop_time": drop_time,  # what the learned optimiser replays (optimiser/routes.py)
        "spot": spot, "second_plans": later["plans"],  # for the picture of the day (sim/render.py)
    }


def trucks_of(plan):
    """(time back at the station, parcels it carried) for each truck in a plan."""
    locker, flown = np.flatnonzero(plan["locker"]), np.flatnonzero(plan["fly"])
    out = []
    for route, back in zip(plan["routes"], plan["back"]):
        stops = np.array(route) - 1
        out.append((back, np.r_[locker[np.isin(plan["point"], stops)], flown[np.isin(plan["drone_stop"], stops)]]))
    return out


def second_pass(day, trucks, t, radius=LAUNCH_RADIUS, seconds=SECOND_SECONDS):
    """Each truck goes out again with the parcels it carried but couldn't deliver (NaN in t). Returns the
    times with the second pass filled in, and {"hours", "by_drone", "km"} it added, with each truck's
    second-pass plan under "plans" (its drop spots in "spot", its truck in "truck")."""
    t = t.copy()
    added = {"hours": 0.0, "by_drone": 0, "km": 0.0, "plans": []}
    city = day.city
    reply = day.second_reply()
    end = dsp.SHIFT_START + dsp.SHIFT
    for truck, (back, parcels) in enumerate(trucks):
        missed = parcels[np.isnan(t[parcels])]
        begin = back + RELOAD
        if len(missed) == 0 or begin > end - 0.5:
            continue
        hour = begin + 0.5
        only = np.zeros(len(t), bool)
        only[missed] = True
        spot = np.full(len(t), -1)
        for i in missed:
            if day.parcel_weight[i] <= PAYLOAD and day.parcel_size[i] in SIZES:
                options = drone.drop_options(day, i, hour)
                spot[i] = options[0][1] if options else -1
        target = city.spot_pos[np.maximum(spot, 0), :2]
        p = _plan(day, spot >= 0, target, radius, SECOND_WAIT, seconds, start=begin, reply=reply, only=only, hour=hour)
        drop, _, _ = _fly(day, p, spot, target)
        t[np.flatnonzero(p["fly"])] = drop
        t[np.flatnonzero(p["locker"])] = p["collected"]
        added["hours"] += sum(b - back for b in p["back"])
        added["by_drone"] += int((~np.isnan(drop)).sum())
        added["km"] += p["km"]
        added["plans"].append({**p, "spot": spot, "truck": truck})
    return t, added


def _plan(day, fly, target, radius, window, seconds, parked=True, start=None, reply=None, only=None,
          hour=PLAN_HOUR):
    """Stops, drone sorties and truck routes for one split of parcels into drone and locker. Parked, a
    truck waits at each stop until its drones are back; otherwise it only waits for the locker.
    `only` limits it to some parcels, `start` is when the trucks leave (default after loadout),
    `reply` replaces the recipients' reply times, and `hour` is the weather flights are planned for."""
    city = day.city
    only = np.ones(len(fly), bool) if only is None else only
    locker_mask, fly = ~fly & only, fly & only
    begin = dsp.SHIFT_START + dsp.LOADOUT if start is None else start
    base, point, walk = trucks_only.pickup_points(city, day, locker_mask)
    nodes, drone_stop = launch_stops(city, target[fly], base, radius)
    stop_xy = city.nodes[nodes]
    flying = np.flatnonzero(fly)
    trips = [drone.sortie(day, stop_xy[s], i, hour)
             if np.linalg.norm(target[i] - stop_xy[s]) <= RANGE else None for s, i in zip(drone_stop, flying)]
    cycle = np.array([t["seconds"] + TURNAROUND if t else np.inf for t in trips])
    dwell = np.zeros(len(nodes))
    start = np.zeros(len(flying))
    for s in range(len(nodes)):
        mine = np.flatnonzero((drone_stop == s) & np.isfinite(cycle))
        start[mine], busy = share_out(cycle[mine])
        dwell[s] = busy if parked else 0.0
    dwell[np.unique(point[point >= 0])] = np.maximum(dwell[np.unique(point[point >= 0])], window * 60)
    dwell = np.maximum(dwell, 60.0)  # at least a minute to park and set off again
    load = np.r_[0, np.bincount(np.r_[point[point >= 0], drone_stop], minlength=len(nodes))]
    shift = dsp.Shift(day, nodes)
    service = np.r_[0.0, dwell]
    horizon = (dsp.SHIFT_START + dsp.SHIFT - begin) * 3600
    fewest = max(1, int(np.ceil(load.sum() / CAPACITY)))
    routes = []
    for trucks in range(fewest, fewest + 10):  # a late start can leave no time at all: then nothing goes
        if (found := dsp.plan(shift, service, trucks, seconds=seconds, load=load, capacity=CAPACITY,
                              horizon=horizon)) is not None:
            routes = found
            break
    arrive, back, metres = {}, [], 0.0
    for route in routes:
        done, home, m = dsp.drive(shift, route, service, start=begin)
        arrive.update({j - 1: t - service[j] / 3600 for j, t in done.items()})
        back.append(home)
        metres += m
    at = np.array([arrive.get(s, np.nan) for s in range(len(nodes))])
    # Locker parcels: collected if the recipient turns up while the truck is still there.
    stop_at = np.where(point >= 0, at[np.maximum(point, 0)], np.nan)
    ready = ((day.recipient_reply if reply is None else reply)[locker_mask] + walk / trucks_only.WALK_SPEED / 60) / 60
    came = stop_at - trucks_only.NOTICE / 60 + ready
    leave = stop_at + dwell[np.maximum(point, 0)] / 3600
    collected = np.where(came <= leave, np.maximum(came, stop_at), np.nan)
    return {"fly": fly.copy(), "locker": locker_mask, "nodes": nodes, "drone_stop": drone_stop, "cycle": cycle, "start": start,
            "point": point, "walk": walk,
            "at": at, "collected": collected, "trucks": len(routes), "routes": routes, "shift": shift,
            "service": service, "back": back,
            "truck_hours": float(sum(b - dsp.SHIFT_START for b in back)), "km": metres / 1000}


def _fly(day, plan, spot, target):
    """Drop time of each planned drone parcel, and which ones can't fly when the truck gets there:
    each flight is worked out again for the wind and temperature at the hour it actually takes off."""
    city = day.city
    flown = np.flatnonzero(plan["fly"])
    launch = plan["at"][plan["drone_stop"]] + plan["start"] / 3600
    drop = np.full(len(flown), np.nan)
    for k, i in enumerate(flown):
        if not (np.isfinite(plan["cycle"][k]) and np.isfinite(launch[k]) and prime_air.flyable(day, launch[k])):
            continue
        trip = drone.sortie(day, city.nodes[plan["nodes"][plan["drone_stop"][k]]], i, launch[k])
        if trip is None:
            continue
        when = launch[k] + trip["to_drop"] / 3600
        point = city.spot_pos[trip["spot"]] + [0, 0, trip["height"]]
        if not city.airspace.blocked([point], when)[0]:
            drop[k] = when
    return drop, np.isnan(drop), 0.0


def describe(r):
    t = r["parcel_time"]
    return (f"{r['radius']:.0f} m launch radius: {r['trucks']} trucks, {r['stops']} stops; "
            f"{np.mean(~np.isnan(t)):.0%} delivered ({r['by_drone']:.0%} by drone, {r['second_pass']} on the second pass), last at {_clock(r['last'])}, "
            f"half of all parcels by {_clock(trucks_only.half(t))}, {np.mean(t <= 14):.0%} by 14:00; "
            f"{r['truck_hours']:.1f} truck hours, {r['km']:.0f} km" + (", replanned" if r["replanned"] else ""))


def main():
    from sim.city import City
    from sim.day import Day

    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--day", type=int, default=0)
    p.add_argument("--radius", type=float, default=LAUNCH_RADIUS)
    p.add_argument("--held-out", action="store_true")
    a = p.parse_args()
    if not a.held_out:
        print(describe(solve(Day(City(a.seed, day=a.day)), a.radius)))
        return
    from baselines.run import over_held_out

    rows = [(seed, d, r) for seed, d, rs in over_held_out(_every_radius) for r in rs]
    _write_results(rows)


def _every_radius(day):
    return [solve(day, radius) for radius in RADII]


def _write_results(rows):
    def stat(radius, f, fmt):
        return fmt(np.mean([f(r) for *_, r in rows if r["radius"] == radius]))

    measures = [
        ("trucks", lambda r: r["trucks"], lambda v: f"{v:.1f}"),
        ("stops", lambda r: r["stops"], lambda v: f"{v:.0f}"),
        ("parcels delivered today", lambda r: np.mean(~np.isnan(r["parcel_time"])), lambda v: f"{v:.0%}"),
        ("delivered on the afternoon second pass", lambda r: r["second_pass"] / len(r["parcel_time"]), lambda v: f"{v:.0%}"),
        ("by drone", lambda r: r["by_drone"], lambda v: f"{v:.0%}"),
        ("last parcel", lambda r: r["last"], _clock),
        ("half of all parcels by", lambda r: trucks_only.half(r["parcel_time"]), _clock),
        ("delivered by 14:00", lambda r: np.mean(r["parcel_time"] <= 14), lambda v: f"{v:.0%}"),
        ("truck hours", lambda r: r["truck_hours"], lambda v: f"{v:.1f}"),
        ("km driven", lambda r: r["km"], lambda v: f"{v:.0f}"),
        ("days replanned for weather or airspace", lambda r: r["replanned"], lambda v: f"{v:.0%}"),
    ]
    lines = [
        "# Classical truck + drone solver on the held-out days",
        "",
        f"Written by `python -m baselines.classical --held-out`. {len({(s, d) for s, d, _ in rows})} days, 500 "
        f"parcels each, averages over the days. Autonomous trucks with {DRONES} drones and a locker each; a "
        f"drone cost model (sim/drone.py: wind, payload, battery, flight heights, drop planning; up to {PAYLOAD:.0f} kg). "
        "Locker settings as in [trucks-only-baseline.md](trucks-only-baseline.md) with a 10-minute wait. "
        f"Each truck then goes out again in the afternoon with what it couldn't deliver ({SECOND_WAIT:.0f}-minute wait). "
        "Settings are in `baselines/classical.py`.",
        "",
        "| launch radius | " + " | ".join(f"{r:.0f} m" for r in RADII) + " |",
        "|---|" + "---|" * len(RADII),
    ] + [f"| {name} | " + " | ".join(stat(r, f, fmt) for r in RADII) + " |" for name, f, fmt in measures] + [
        "",
        "## Every day",
        "",
        "| city | day | result |",
        "|---|---|---|",
    ] + [f"| {s} | {d} | {describe(r)} |" for s, d, r in rows]
    Path("results").mkdir(exist_ok=True)
    Path("results/classical-solver.md").write_text("\n".join(lines) + "\n")
    print("wrote results/classical-solver.md")


if __name__ == "__main__":
    main()
