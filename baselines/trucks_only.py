"""Trucks-only baseline: this project's autonomous trucks with their lockers, but no drones.

Every parcel rides in a locker on a truck. The trucks drive themselves out of the
distribution centre and stop at pickup points on the street. Everyone with a parcel is
told NOTICE minutes before their truck gets to the nearest pickup point they'll walk to;
they turn up when they're ready (the day's recipient reply time plus the walk) and open
their compartment. The truck waits WINDOW minutes at each point; anyone who doesn't make
it in time has their parcel taken back to the station. It's the drone fleet minus the
drones, so it shows how much of any gain comes from the drones.

Pickup points are chosen greedily: each next one is the road node that most of the
uncovered parcels' recipients would walk to, until everyone is covered. Routes come from
OR-Tools, as for the DSP vans, with the locker size as a limit.

All the settings here are guesses; recipients' walk and reply times are in docs/days.md.

    python -m baselines.trucks_only                # one day in the default city
    python -m baselines.trucks_only --held-out     # the 50 held-out days, waiting 10, 20 and 30 minutes
"""
import argparse
from pathlib import Path

import numpy as np

from baselines import dsp
from baselines.dsp import _clock

NOTICE = 10.0  # minutes' warning before the truck reaches a pickup point
WINDOW = 10.0  # minutes the truck waits at each point; the held-out run also tries 20 and 30
WINDOWS = (10.0, 20.0, 30.0)
WALK_SPEED = 1.3  # m/s
WALK_DETOUR = 1.3  # walking distance along pavements, over the straight line; guess
LOCKER = 200  # compartments per truck, one parcel each; guess


def pickup_points(city, day, which=None):
    """Choose pickup points for the parcels `which` picks out (a mask; default all). Returns (road node
    per point, point index per chosen parcel or -1 if its recipient won't walk to any road node,
    walking distance per chosen parcel)."""
    which = np.ones(len(day.parcel_address), bool) if which is None else np.asarray(which, bool)
    door = city.address_door[day.parcel_address[which], :2]
    limit = day.recipient_walk[which]
    nodes = np.flatnonzero((city.nodes[:, 0] >= 0) & (city.nodes[:, 0] <= city.width)
                           & (city.nodes[:, 1] >= 0) & (city.nodes[:, 1] <= city.height))
    walk = WALK_DETOUR * np.linalg.norm(door[:, None] - city.nodes[nodes][None], axis=-1)  # parcels x nodes
    reach = walk <= limit[:, None]
    chosen, left = [], reach.any(1)
    while left.any():
        best = int((reach & left[:, None]).sum(0).argmax())
        chosen.append(best)
        left &= ~reach[:, best]
    chosen = np.array(chosen, int)
    if len(chosen) == 0:
        return np.zeros(0, int), np.full(len(door), -1), np.full(len(door), np.nan)
    options = np.where(reach[:, chosen], walk[:, chosen], np.inf)
    point = np.where(np.isfinite(options).any(1), options.argmin(1), -1)
    distance = np.where(point >= 0, options[np.arange(len(door)), np.maximum(point, 0)], np.nan)
    return nodes[chosen], point, distance


def baseline(day, window=WINDOW, seconds=dsp.SOLVER_SECONDS):
    city = day.city
    nodes, point, distance = pickup_points(city, day)
    load = np.r_[0, np.bincount(point[point >= 0], minlength=len(nodes))]
    service = np.r_[0.0, np.full(len(nodes), window * 60)]
    shift = dsp.Shift(day, nodes)
    trucks = max(1, int(np.ceil(load.sum() / LOCKER)))
    while (routes := dsp.plan(shift, service, trucks, seconds=seconds, load=load, capacity=LOCKER)) is None:
        trucks += 1
    arrive, back, metres = {}, [], 0.0
    for route in routes:
        done, home, m = dsp.drive(shift, route, service)
        arrive.update({j: t - window / 60 for j, t in done.items()})
        back.append(home)
        metres += m
    at = np.array([arrive.get(p + 1, np.nan) if p >= 0 else np.nan for p in point])
    ready = (day.recipient_reply + distance / WALK_SPEED / 60) / 60  # hours after being told
    collected = at - NOTICE / 60 + ready
    collected = np.where(collected <= at + window / 60, np.maximum(collected, at), np.nan)
    return {
        "window": window, "trucks": len(routes), "points": len(nodes), "parcel_time": collected,
        "uncollected": int(np.isnan(collected).sum()), "no_point": int((point < 0).sum()),
        "walk": float(np.nanmean(distance)), "last": float(np.nanmax(collected)),
        "truck_hours": float(sum(b - dsp.SHIFT_START for b in back)), "km": metres / 1000,
    }


def half(t):
    """By when at least half of all the day's parcels were delivered, counting uncollected ones as never."""
    return float(np.percentile(np.where(np.isnan(t), np.inf, t), 50, method="higher"))


def describe(r):
    t = r["parcel_time"]
    return (f"{r['window']:.0f} min wait: {r['trucks']} trucks, {r['points']} pickup points; "
            f"{np.mean(~np.isnan(t)):.0%} collected, last at {_clock(r['last'])}, half of all parcels by "
            f"{_clock(half(t))}, "
            f"{np.mean(t <= 14):.0%} by 14:00; {r['uncollected']} back to the station "
            f"({r['no_point']} too far to walk); average walk {r['walk']:.0f} m; "
            f"{r['truck_hours']:.1f} truck hours, {r['km']:.0f} km")


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
        day = Day.load(Path("data/held-out") / f"city{seed}-day{d}.npz", City(seed, day=d))
        for window in WINDOWS:
            r = baseline(day, window)
            rows.append((seed, d, r))
            print(seed, d, describe(r), flush=True)
    _write_results(rows)


def _write_results(rows):
    def stat(window, f, fmt):
        return fmt(np.mean([f(r) for *_, r in rows if r["window"] == window]))

    measures = [
        ("trucks", lambda r: r["trucks"], lambda v: f"{v:.1f}"),
        ("pickup points", lambda r: r["points"], lambda v: f"{v:.0f}"),
        ("parcels collected", lambda r: np.mean(~np.isnan(r["parcel_time"])), lambda v: f"{v:.0%}"),
        ("last parcel collected", lambda r: r["last"], _clock),
        ("half of all parcels collected by", lambda r: half(r["parcel_time"]), _clock),
        ("collected by 14:00", lambda r: np.mean(r["parcel_time"] <= 14), lambda v: f"{v:.0%}"),
        ("average walk", lambda r: r["walk"], lambda v: f"{v:.0f} m"),
        ("truck hours", lambda r: r["truck_hours"], lambda v: f"{v:.1f}"),
        ("km driven", lambda r: r["km"], lambda v: f"{v:.0f}"),
    ]
    lines = [
        "# Trucks-only baseline on the held-out days",
        "",
        f"Written by `python -m baselines.trucks_only --held-out`. {len({(s, d) for s, d, _ in rows})} days, 500 "
        f"parcels each, averages over the days. Autonomous trucks with {LOCKER}-compartment lockers and no drones, "
        f"leaving at {_clock(dsp.SHIFT_START + dsp.LOADOUT)} and back by {_clock(dsp.SHIFT_START + dsp.SHIFT)}. "
        f"Recipients get {NOTICE:.0f} minutes' warning and walk at {WALK_SPEED} m/s on pavements {WALK_DETOUR}x the "
        "straight line. Collected parcels count as delivered; the rest go back to the station and count as not "
        "delivered today.",
        "",
        "| truck waits at each point | " + " | ".join(f"{w:.0f} min" for w in WINDOWS) + " |",
        "|---|" + "---|" * len(WINDOWS),
    ] + [f"| {name} | " + " | ".join(stat(w, f, fmt) for w in WINDOWS) + " |" for name, f, fmt in measures] + [
        "",
        "## Every day",
        "",
        "| city | day | result |",
        "|---|---|---|",
    ] + [f"| {s} | {d} | {describe(r)} |" for s, d, r in rows]
    Path("results").mkdir(exist_ok=True)
    Path("results/trucks-only-baseline.md").write_text("\n".join(lines) + "\n")
    print("wrote results/trucks-only-baseline.md")


if __name__ == "__main__":
    main()
