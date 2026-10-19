"""Amazon DSP van baseline: one van and one driver per route, out of the distribution centre.

Each van loads at the station for LOADOUT, leaves, delivers its stops in the order OR-Tools
plans, and has to be back by the end of its SHIFT. Routes are planned on drive times
averaged over the shift, then driven with the traffic at the actual time of each leg, so
rush hour costs what it costs. A stop is a building: every flat in an apartment block is
one stop, the way a driver counts it.

Settings and their sources are in docs/amazon-baseline.md. SERVICE comes out of the
calibration (baselines/calibrate.py, results/dsp-calibration.md).

    python -m baselines.dsp                      # one day in the default city
    python -m baselines.dsp --held-out           # all 50 held-out days, writes results/dsp-baseline.md
"""
import argparse
from pathlib import Path

import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from sim.roads import drive_times, nearest_nodes

SHIFT_START, LOADOUT, SHIFT = 9.5, 0.5, 10.0  # hours: when the shift starts, loading at the station, whole shift
SERVICE = 166.0  # seconds per stop to park, walk to the door, drop and walk back: the fast end from results/dsp-calibration.md
EXTRA_PACKAGE = 10.0  # seconds for each extra package at the same stop
MAX_STOPS = 190  # the top of the public range; used only to guess how many vans to start from
SOLVER_SECONDS = 5
SKIPPED = 10 ** 7  # cost of leaving a stop out, when stops may be left out
BALANCE = 10  # weight on the longest route against total driving time


def stops(city, addresses, packages):
    """Group deliveries by building: (address of each stop, road node of each stop, packages per stop,
    and for every address the stop it belongs to)."""
    building = city.address_building[addresses]
    _, first, which = np.unique(building, return_index=True, return_inverse=True)
    rep = addresses[first]
    return rep, nearest_nodes(city, city.address_street[rep]), np.bincount(which, weights=packages), which


def service_times(packages, service=SERVICE):
    """Seconds spent at each stop, with the station (index 0) at 0."""
    return np.r_[0.0, service + EXTRA_PACKAGE * (np.asarray(packages) - 1)]


class Shift:
    """Drive times for one shift between the station (index 0) and the stops (1..n), hour by hour."""

    def __init__(self, day, stop_nodes):
        city = day.city
        self.nodes = np.r_[city.station_node, stop_nodes]
        self.hours = list(range(int(SHIFT_START), int(np.ceil(SHIFT_START + SHIFT)) + 1))
        self.hourly = {h: drive_times(city, day.travel_time(h + 0.5), self.nodes) for h in self.hours}
        self.mean = np.mean([self.hourly[h] for h in self.hours], 0)
        self.metres = drive_times(city, city.edge_length, self.nodes)  # shortest distance, close to what's driven

    def leg(self, i, j, clock):
        """Seconds from stop i to stop j leaving at `clock` (hours)."""
        return self.hourly[min(max(int(clock), self.hours[0]), self.hours[-1])][i, j]


def plan(shift, service, vans, optional=False, seconds=SOLVER_SECONDS):
    """Routes for up to `vans` vans that all fit in the shift, or None if OR-Tools finds none.
    With optional=True, stops may be left out (it then fits in as many as it can).
    Each route is a list of stop indices (1..n) in driving order."""
    n = len(shift.nodes)
    cost = np.rint(shift.mean + service[None, :]).astype(int)  # drive from i to j, then deliver at j
    np.fill_diagonal(cost, 0)
    table = cost.tolist()
    manager = pywrapcp.RoutingIndexManager(n, vans, 0)
    routing = pywrapcp.RoutingModel(manager)
    transit = routing.RegisterTransitCallback(lambda a, b: table[manager.IndexToNode(a)][manager.IndexToNode(b)])
    routing.SetArcCostEvaluatorOfAllVehicles(transit)
    routing.AddDimension(transit, 0, int((SHIFT - LOADOUT) * 3600), True, "time")
    # Also keep the longest route short, so the work is shared out between the vans and the last
    # parcel goes out as early as it can. Real routes are balanced too.
    routing.GetDimensionOrDie("time").SetGlobalSpanCostCoefficient(BALANCE)
    if optional:
        for node in range(1, n):
            routing.AddDisjunction([manager.NodeToIndex(node)], SKIPPED)
    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    params.time_limit.FromSeconds(seconds)
    solution = routing.SolveWithParameters(params)
    if solution is None:
        return None
    routes = []
    for v in range(vans):
        i, route = routing.Start(v), []
        while not routing.IsEnd(i):
            if manager.IndexToNode(i):
                route.append(manager.IndexToNode(i))
            i = solution.Value(routing.NextVar(i))
        if route:
            routes.append(route)
    return routes


def drive(shift, route, service):
    """Drive a route with the traffic at the time of each leg. Returns ({stop: time delivered}, time back,
    metres driven). A stop that would make the van late back is skipped and its parcels go back to the
    station, as a real driver would bring them back."""
    end = SHIFT_START + SHIFT
    clock, at, done, metres = SHIFT_START + LOADOUT, 0, {}, 0.0
    for j in route:
        leave = clock + (shift.leg(at, j, clock) + service[j]) / 3600
        if leave + shift.leg(j, 0, leave) / 3600 > end:
            continue
        done[j] = leave
        metres += shift.metres[at, j]
        clock, at = leave, j
    return done, clock + shift.leg(at, 0, clock) / 3600, metres + shift.metres[at, 0]


def baseline(day, service=SERVICE, seconds=SOLVER_SECONDS):
    """Deliver a whole day with as few DSP vans as OR-Tools can fit it into."""
    city = day.city
    addresses, packages = np.unique(day.parcel_address, return_counts=True)
    _, nodes, per_stop, which = stops(city, addresses, packages)
    svc = service_times(per_stop, service)
    shift = Shift(day, nodes)
    vans = max(1, int(np.ceil(len(nodes) / MAX_STOPS)))
    while (routes := plan(shift, svc, vans, seconds=seconds)) is None:
        vans += 1
    delivered, back, metres = {}, [], 0.0
    for route in routes:
        done, home, m = drive(shift, route, svc)
        delivered.update(done)
        back.append(home)
        metres += m
    stop_time = np.array([delivered.get(j + 1, np.nan) for j in range(len(nodes))])
    parcel_time = stop_time[which[np.searchsorted(addresses, day.parcel_address)]]
    return {
        "vans": len(routes),
        "stops": [len(r) for r in routes],
        "packages": [int(per_stop[np.array(r) - 1].sum()) for r in routes],
        "parcel_time": parcel_time,  # clock time each parcel was delivered, NaN if it came back undelivered
        "undelivered": int(np.isnan(parcel_time).sum()),
        "last": float(np.nanmax(parcel_time)),
        "driver_hours": float(sum(b - SHIFT_START for b in back)),
        "km": metres / 1000,
    }


def describe(r):
    t = r["parcel_time"]
    return (f"{r['vans']} vans, stops {r['stops']}, packages {r['packages']}; last parcel at {_clock(r['last'])}, "
            f"half delivered by {_clock(np.nanmedian(t))}, {np.mean(t <= 14):.0%} by 14:00; "
            f"{r['undelivered']} undelivered; {r['driver_hours']:.1f} driver hours, {r['km']:.0f} km")


def _clock(h):
    return f"{int(h):02d}:{int(round(h % 1 * 60)) % 60:02d}"


def main():
    from sim.city import City
    from sim.day import HELD_OUT, Day

    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--day", type=int, default=0)
    p.add_argument("--held-out", action="store_true")
    a = p.parse_args()
    if not a.held_out:
        print(describe(baseline(Day(City(a.seed, day=a.day)))))
        return
    rows = []
    for seed, d in HELD_OUT:
        city = City(seed, day=d)
        r = baseline(Day.load(Path("data/held-out") / f"city{seed}-day{d}.npz", city))
        rows.append((seed, d, r))
        print(seed, d, describe(r), flush=True)
    _write_results(rows)


def _write_results(rows):
    last = np.array([r["last"] for *_, r in rows])
    median = np.array([np.nanmedian(r["parcel_time"]) for *_, r in rows])
    by14 = np.array([np.mean(r["parcel_time"] <= 14) for *_, r in rows])
    lines = [
        "# DSP van baseline on the held-out days",
        "",
        f"Written by `python -m baselines.dsp --held-out`. {len(rows)} days, 500 parcels each, service time "
        f"{SERVICE:.0f} s per stop plus {EXTRA_PACKAGE:.0f} s per extra package (from [dsp-calibration.md]"
        f"(dsp-calibration.md)), shift {_clock(SHIFT_START)} to {_clock(SHIFT_START + SHIFT)}, "
        f"{LOADOUT * 60:.0f} min loadout, routes by OR-Tools with {SOLVER_SECONDS} s per day.",
        "",
        "| | mean | best day | worst day |",
        "|---|---|---|---|",
        f"| vans | {np.mean([r['vans'] for *_, r in rows]):.1f} | {min(r['vans'] for *_, r in rows)} | "
        f"{max(r['vans'] for *_, r in rows)} |",
        f"| last parcel delivered | {_clock(last.mean())} | {_clock(last.min())} | {_clock(last.max())} |",
        f"| half the parcels delivered by | {_clock(median.mean())} | {_clock(median.min())} | {_clock(median.max())} |",
        f"| delivered by 14:00 | {by14.mean():.0%} | {by14.max():.0%} | {by14.min():.0%} |",
        f"| driver hours | {np.mean([r['driver_hours'] for *_, r in rows]):.1f} | "
        f"{min(r['driver_hours'] for *_, r in rows):.1f} | {max(r['driver_hours'] for *_, r in rows):.1f} |",
        f"| km driven | {np.mean([r['km'] for *_, r in rows]):.0f} | {min(r['km'] for *_, r in rows):.0f} | "
        f"{max(r['km'] for *_, r in rows):.0f} |",
        f"| parcels brought back undelivered | {np.mean([r['undelivered'] for *_, r in rows]):.1f} | "
        f"{min(r['undelivered'] for *_, r in rows)} | {max(r['undelivered'] for *_, r in rows)} |",
        "",
        "## Every day",
        "",
        "| city | day | result |",
        "|---|---|---|",
    ] + [f"| {seed} | {d} | {describe(r)} |" for seed, d, r in rows]
    Path("results").mkdir(exist_ok=True)
    Path("results/dsp-baseline.md").write_text("\n".join(lines) + "\n")
    print("wrote results/dsp-baseline.md")


if __name__ == "__main__":
    main()
