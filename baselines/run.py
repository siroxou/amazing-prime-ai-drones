"""Every baseline on the 50 held-out days at its main setting, days in parallel. Writes the
table at the top of results/baselines.md and says how long it took.

    python -m baselines.run                # one worker per core
    python -m baselines.run --workers 4

Each baseline's own `--held-out` run tries more settings and lists every day; this is the
quick side-by-side. OR-Tools gets the same seconds per solve here as in those runs. On slower
cores it searches less within that time, so the numbers can differ by a few minutes.
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")  # one process per core; no thread pools fighting over them

import argparse  # noqa: E402
import re  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402
from pathlib import Path  # noqa: E402
from time import perf_counter  # noqa: E402

import numpy as np  # noqa: E402

from baselines import classical, dsp, prime_air, trucks_only  # noqa: E402
from baselines.dsp import _clock  # noqa: E402
from sim.city import City  # noqa: E402
from sim.day import HELD_OUT, Day  # noqa: E402
from optimiser.routes import score  # noqa: E402

SYSTEMS = (
    ("Amazon DSP vans", "dsp-baseline.md", lambda day: dsp.baseline(day), "vans"),
    ("Amazon Prime Air, 10 drones at the site, plus vans", "prime-air-baseline.md",
     lambda day: prime_air.baseline(day, 10), "vans"),
    ("Locker trucks, no drones, 10 min wait", "trucks-only-baseline.md",
     lambda day: trucks_only.baseline(day, 10.0), "trucks"),
    ("Locker trucks, no drones, 30 min wait", "trucks-only-baseline.md",
     lambda day: trucks_only.baseline(day, 30.0), "trucks"),
    ("Trucks with 10 drones each, classical solver, 600 m launch radius", "classical-solver.md",
     lambda day: classical.solve(day), "trucks"),
    ("The same, drones launching from and landing on the moving truck", "moving-launch.md",
     lambda day: classical.solve(day, moving=True), "trucks"),
)
START, END = "<!-- table: written by python -m baselines.run -->", "<!-- end of table -->"


def one_day(seed_day):
    """All the systems on one held-out day. Returns the few numbers the table needs."""
    seed, d = seed_day
    day = Day.load(Path("data/held-out") / f"city{seed}-day{d}.npz", City(seed, day=d))
    out = []
    for _, _, run, vehicle in SYSTEMS:
        r = run(day)
        t = r["parcel_time"]
        out.append({"score": score(t), "delivered": np.mean(~np.isnan(t)), "last": np.nanmax(t), "half": trucks_only.half(t),
                    "by14": np.mean(t <= 14), "vehicles": r["vans"] if vehicle == "vans" else r["trucks"],
                    "driver_hours": r.get("driver_hours", 0.0)})
    return out


def _load_and_run(job):
    fn, seed, d = job
    return fn(Day.load(Path("data/held-out") / f"city{seed}-day{d}.npz", City(seed, day=d)))


def over_held_out(fn, workers=None):
    """fn(day) on every held-out day, days in parallel. fn must be a module-level function.
    Returns [(city seed, day number, fn's result)] in HELD_OUT order."""
    with ProcessPoolExecutor(workers or os.cpu_count()) as pool:
        results = pool.map(_load_and_run, [(fn, s, d) for s, d in HELD_OUT])
        return [(s, d, r) for (s, d), r in zip(HELD_OUT, results)]


def table(days, workers, minutes):
    lines = [
        START,
        "",
        "| system | score | delivered today | last parcel | half of all parcels by | by 14:00 | vehicles | driver hours |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for k, (name, link, _, vehicle) in enumerate(SYSTEMS):
        rs = [day[k] for day in days]
        mean = {key: np.mean([r[key] for r in rs]) for key in rs[0]}
        lines.append(f"| {name} ([{link}]({link})) | {mean['score']:.2f} h | {mean['delivered']:.0%} | {_clock(mean['last'])} | "
                     f"{_clock(mean['half'])} | {mean['by14']:.0%} | {mean['vehicles']:.1f} {vehicle} | "
                     f"{mean['driver_hours']:.1f} |")
    lines += ["", "Score: average hours from 10:00 until a parcel is delivered, a parcel not delivered today "
              "counting 24 hours; lower is better (optimiser/routes.py).", "",
              f"All six over all {len(days)} days took {minutes:.1f} minutes on {workers} workers "
              "(`python -m baselines.run`).", "", END]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--workers", type=int, default=os.cpu_count())
    a = p.parse_args()
    start = perf_counter()
    with ProcessPoolExecutor(a.workers) as pool:
        days = []
        for i, result in enumerate(pool.map(one_day, HELD_OUT), 1):
            days.append(result)
            print(f"{i}/{len(HELD_OUT)} days done, {(perf_counter() - start) / 60:.1f} min", flush=True)
    minutes = (perf_counter() - start) / 60
    path = Path("results/baselines.md")
    text = path.read_text()
    new = table(days, a.workers, minutes)
    if START in text:
        text = re.sub(re.escape(START) + ".*?" + re.escape(END), lambda _: new, text, flags=re.S)
    else:
        text = text.replace("\n\n", "\n\n" + new + "\n\n", 1)
    path.write_text(text)
    print(new)
    print(f"took {minutes:.1f} minutes")


if __name__ == "__main__":
    main()
