"""Classical truck + drone solver: the project's own system, planned with plain heuristics and
OR-Tools, and a fixed-speed drone model. This is the first version of the fleet, and the bar a
learned optimiser will have to beat.

Each autonomous truck carries DRONES drones and a locker. It leaves the distribution centre
and parks at a series of stops. At each stop its drones fly out to the parcels assigned to
that stop and come back to it, and recipients of locker parcels near the stop walk over to
collect them. The truck moves on when the last drone is back and the locker wait is over.

    1. Every parcel a drone can take goes by drone: light enough, small enough, and an address
       with a drop spot that has open sky and room around it (yards and porches), or a top-floor
       balcony it can lower the parcel onto from above.
    2. Locker parcels get pickup points, as in the trucks-only baseline.
    3. Drone parcels are flown from the nearest pickup point within LAUNCH_RADIUS. The rest get
       new launch stops, chosen greedily to cover as many of them as possible.
    4. At each stop the sorties are shared out between the drones, longest first.
    5. OR-Tools routes the trucks through the stops, as for the DSP vans.
    6. The day is driven with real traffic. Drone parcels the weather or airspace stops at the
       time the truck gets there become locker parcels, and the day is planned again once
       (the weather forecast is taken as known, as for Prime Air).

The drone model is deliberately simple, a fixed cruise speed with fixed times to launch, drop
and land; the full cost model with wind, payload and energy comes in Phase 3. Every setting
here is a guess, and they're all in this file.

    python -m baselines.classical                  # one day in the default city
    python -m baselines.classical --held-out       # the 50 held-out days
"""
import argparse
from pathlib import Path

import numpy as np

from baselines import dsp, prime_air, trucks_only
from baselines.dsp import _clock

DRONES = 10  # per truck
SPEED = 15.0  # m/s cruise, fixed
PAYLOAD = 5.0  # kg
SIZES = ("envelope", "small", "medium", "large")
RANGE = 3000.0  # m, furthest a drop can be from the truck
CLEAR = 1.5  # m clear around a yard or porch drop
WINCH_HEIGHT, DRONE_RADIUS = 5.0, 0.7  # m: hovering height over a balcony, and room the drone needs
LAUNCH_LAND = 60.0  # s to take off from the truck and land back on it
DROP = 30.0  # s to come down, lower the parcel and climb back
TURNAROUND = 60.0  # s on the truck to load the next parcel and swap the battery
LAUNCH_RADIUS = 600.0  # m: drone parcels further than this from any pickup point get a launch stop of their own
CAPACITY = 300  # parcels a truck carries, locker and drone parcels together
WINDOW = trucks_only.WINDOW  # minutes the locker waits at a stop, at least
RADII = (300.0, 600.0, 1000.0)  # launch radii tried on the held-out days
PREFERENCE = ("back_yard", "front_yard", "porch", "balcony")


def drone_spots(city):
    """For each address, the spot a drone lowers its parcel onto, or -1: the first of PREFERENCE with
    open sky above. In a yard or on a porch the drone comes down low, so it needs nothing within CLEAR
    from half a metre up. On a balcony it hovers WINCH_HEIGHT above and lowers the parcel on a line, so
    it needs room for itself up there. Covered balconies don't count: nothing can come down onto them."""
    best = np.full(len(city.address_kind), -1)
    for kind in PREFERENCE[::-1]:  # most preferred last, so it wins
        lift, room = (WINCH_HEIGHT, DRONE_RADIUS) if kind == "balcony" else (0.5 + CLEAR, CLEAR)
        for s in np.flatnonzero(city.spot_kind == kind):
            if city.spot_overhead[s] >= 100 and city.obstacles.touching(city.spot_pos[s] + [0, 0, lift], room) is None:
                best[city.spot_address[s]] = s
    return best


def sortie_seconds(distance):
    """Whole cycle for one parcel: out, drop, back, reload."""
    return LAUNCH_LAND + 2 * distance / SPEED + DROP + TURNAROUND


def to_drop_seconds(distance):
    return LAUNCH_LAND / 2 + distance / SPEED + DROP / 2


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


def solve(day, radius=LAUNCH_RADIUS, window=WINDOW, seconds=dsp.SOLVER_SECONDS, moving=False):
    """Plan and run a day. With moving=True the trucks don't wait for their drones: drones launch from
    and land on the truck as it drives (baselines/moving.py)."""
    from baselines import moving as on_the_move

    fly_them = on_the_move.fly if moving else _fly
    city = day.city
    n = len(day.parcel_address)
    spot = drone_spots(city)[day.parcel_address]
    target = city.spot_pos[np.maximum(spot, 0), :2]
    fly = (spot >= 0) & (day.parcel_weight <= PAYLOAD) & np.isin(day.parcel_size, SIZES)
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
    t[flown] = drop_time  # NaN where it couldn't fly after all: back to the station
    locker = np.flatnonzero(~plan["fly"])
    t[locker] = plan["collected"]
    return {
        "radius": radius, "moving": moving, "trucks": plan["trucks"], "stops": len(plan["nodes"]), "parcel_time": t,
        "by_drone": float((~np.isnan(t[flown])).sum() / n),
        "undelivered": int(np.isnan(t).sum()), "last": float(np.nanmax(t)) if (~np.isnan(t)).any() else np.nan,
        "truck_hours": plan["truck_hours"] + extra, "km": plan["km"], "replanned": int(attempt),
    }


def _plan(day, fly, target, radius, window, seconds, parked=True):
    """Stops, drone sorties and truck routes for one split of parcels into drone and locker. Parked, a
    truck waits at each stop until its drones are back; otherwise it only waits for the locker."""
    city = day.city
    base, point, walk = trucks_only.pickup_points(city, day, ~fly)
    nodes, drone_stop = launch_stops(city, target[fly], base, radius)
    stop_xy = city.nodes[nodes]
    length = np.array([prime_air.path_length(city, stop_xy[s], target[i], 13.0) or np.inf
                       for s, i in zip(drone_stop, np.flatnonzero(fly))])
    length[np.linalg.norm(target[fly] - stop_xy[drone_stop], axis=1) > RANGE] = np.inf
    dwell = np.zeros(len(nodes))
    start = np.zeros(int(fly.sum()))
    for s in range(len(nodes)):
        mine = np.flatnonzero((drone_stop == s) & np.isfinite(length))
        start[mine], busy = share_out(sortie_seconds(length[mine]))
        dwell[s] = busy if parked else 0.0
    dwell[np.unique(point[point >= 0])] = np.maximum(dwell[np.unique(point[point >= 0])], window * 60)
    dwell = np.maximum(dwell, 60.0)  # at least a minute to park and set off again
    load = np.r_[0, np.bincount(np.r_[point[point >= 0], drone_stop], minlength=len(nodes))]
    shift = dsp.Shift(day, nodes)
    service = np.r_[0.0, dwell]
    trucks = max(1, int(np.ceil(load.sum() / CAPACITY)))
    while (routes := dsp.plan(shift, service, trucks, seconds=seconds, load=load, capacity=CAPACITY)) is None:
        trucks += 1
    arrive, back, metres = {}, [], 0.0
    for route in routes:
        done, home, m = dsp.drive(shift, route, service)
        arrive.update({j - 1: t - service[j] / 3600 for j, t in done.items()})
        back.append(home)
        metres += m
    at = np.array([arrive.get(s, np.nan) for s in range(len(nodes))])
    # Locker parcels: collected if the recipient turns up while the truck is still there.
    stop_at = np.where(point >= 0, at[np.maximum(point, 0)], np.nan)
    ready = (day.recipient_reply[~fly] + walk / trucks_only.WALK_SPEED / 60) / 60
    came = stop_at - trucks_only.NOTICE / 60 + ready
    leave = stop_at + dwell[np.maximum(point, 0)] / 3600
    collected = np.where(came <= leave, np.maximum(came, stop_at), np.nan)
    return {"fly": fly.copy(), "nodes": nodes, "drone_stop": drone_stop, "length": length, "start": start,
            "at": at, "collected": collected, "trucks": len(routes), "routes": routes, "shift": shift,
            "service": service, "back": back,
            "truck_hours": float(sum(b - dsp.SHIFT_START for b in back)), "km": metres / 1000}


def _fly(day, plan, spot, target):
    """Drop time of each planned drone parcel, and which ones can't fly when the truck gets there."""
    city = day.city
    flown = np.flatnonzero(plan["fly"])
    launch = plan["at"][plan["drone_stop"]] + plan["start"] / 3600
    drop = launch + to_drop_seconds(plan["length"]) / 3600
    failed = ~np.isfinite(drop)
    for k, i in enumerate(flown):
        if failed[k]:
            continue
        point = np.append(city.spot_pos[spot[i]], 0.0)[:3] + [0, 0, prime_air.DROP_HEIGHT]
        if not prime_air.flyable(day, launch[k]) or city.airspace.blocked([point], drop[k])[0]:
            failed[k] = True
    return np.where(failed, np.nan, drop), failed, 0.0


def describe(r):
    t = r["parcel_time"]
    return (f"{r['radius']:.0f} m launch radius: {r['trucks']} trucks, {r['stops']} stops; "
            f"{np.mean(~np.isnan(t)):.0%} delivered ({r['by_drone']:.0%} by drone), last at {_clock(r['last'])}, "
            f"half of all parcels by {_clock(trucks_only.half(t))}, {np.mean(t <= 14):.0%} by 14:00; "
            f"{r['truck_hours']:.1f} truck hours, {r['km']:.0f} km" + (", replanned" if r["replanned"] else ""))


def main():
    from sim.city import City
    from sim.day import HELD_OUT, Day

    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--day", type=int, default=0)
    p.add_argument("--radius", type=float, default=LAUNCH_RADIUS)
    p.add_argument("--held-out", action="store_true")
    a = p.parse_args()
    if not a.held_out:
        print(describe(solve(Day(City(a.seed, day=a.day)), a.radius)))
        return
    rows = []
    for seed, d in HELD_OUT:
        day = Day.load(Path("data/held-out") / f"city{seed}-day{d}.npz", City(seed, day=d))
        for radius in RADII:
            r = solve(day, radius)
            rows.append((seed, d, r))
            print(seed, d, describe(r), flush=True)
    _write_results(rows)


def _write_results(rows):
    def stat(radius, f, fmt):
        return fmt(np.mean([f(r) for *_, r in rows if r["radius"] == radius]))

    measures = [
        ("trucks", lambda r: r["trucks"], lambda v: f"{v:.1f}"),
        ("stops", lambda r: r["stops"], lambda v: f"{v:.0f}"),
        ("parcels delivered today", lambda r: np.mean(~np.isnan(r["parcel_time"])), lambda v: f"{v:.0%}"),
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
        f"fixed-speed drone model ({SPEED:.0f} m/s, up to {PAYLOAD:.0f} kg, {RANGE / 1000:.0f} km from the truck). "
        "Locker settings as in [trucks-only-baseline.md](trucks-only-baseline.md) with a 10-minute wait. "
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
