"""Check the DSP van model against Amazon's public figures before comparing anything with it.

Amazon's own figures put a DSP route at 150-190 stops and 200-300 packages in a 10-hour shift
(docs/amazon-baseline.md). Here one van works an area of houses in a big city (24 x 24
blocks, about 2.9 x 2.5 km) where SHARE of the houses get parcels that day, and delivers as
many as fit in its shift. For each district, the service time per stop that gives 190 stops
(the fast end) and 150 stops (the slow end) is found by bisection.

The check passes if a window of service times inside the plausible range puts every
district inside 150-190 stops, and a van on a fresh set of houses at the middle of that
window lands inside the range too. The baseline then uses the fast end of the window, the
most generous choice for Amazon; routes there sit at about 190 stops, the top of the range.

Plausible range: 30 s to about 3.8 minutes per stop. Less than 30 s doesn't leave time to
park, walk to a door, put a parcel down and walk back. The top comes from Amazon's own
numbers: 10 hours less the loadout, over 150 stops, leaves 228 s per stop for everything,
driving between stops included, so the time at the stop alone can't be more.

    python -m baselines.calibrate        # about 10 minutes; writes results/dsp-calibration.md
"""
from pathlib import Path

import numpy as np

from baselines.dsp import EXTRA_PACKAGE, LOADOUT, SHIFT, SHIFT_START, Shift, _clock, drive, plan, service_times, stops
from sim.city import City
from sim.day import EXTRA_PER_STOP, Day

SHARE, SHARES = 0.15, (0.10, 0.25)  # share of houses with parcels today; the main value, then the sensitivity check
DISTRICTS = ("dense", "suburb")
TARGET = (150, 190)
PLAUSIBLE = (30.0, (SHIFT - LOADOUT) * 3600 / TARGET[0])
CITY_SEED, BLOCKS = 500, 24
SOLVER_SECONDS = 5


class Area:
    """One van's day in one district: which houses get parcels, and the drive times between them."""

    def __init__(self, city, district, share, seed):
        rng = np.random.default_rng([city.seed, seed, int(share * 1000)])
        houses = np.flatnonzero(city.address_district == district)
        chosen = np.sort(rng.choice(houses, int(len(houses) * share), replace=False))
        _, nodes, self.packages, _ = stops(city, chosen, 1 + rng.poisson(EXTRA_PER_STOP, len(chosen)))
        self.shift = Shift(Day(city, parcels=10), nodes)

    def route(self, service):
        """Stops and packages one van delivers in its shift at this service time."""
        svc = service_times(self.packages, service)
        best = plan(self.shift, svc, 1, optional=True, seconds=SOLVER_SECONDS)[0]
        done, _, _ = drive(self.shift, best, svc)
        served = np.array(sorted(done)) - 1
        return len(served), int(self.packages[served].sum())


def service_for(area, target, lo=10.0, hi=400.0, steps=7):
    """Service time (s) at which the van delivers about `target` stops; fewer stops as it grows."""
    for _ in range(steps):
        mid = np.sqrt(lo * hi)
        if area.route(mid)[0] > target:
            lo = mid
        else:
            hi = mid
    return np.sqrt(lo * hi)


def main():
    city = City(CITY_SEED, blocks=BLOCKS)
    rows = []
    for share in (SHARE, *SHARES):
        for district in DISTRICTS:
            area = Area(city, district, share, seed=1)
            fast, slow = (service_for(area, t) for t in TARGET[::-1])
            rows.append((share, district, len(area.packages), fast, slow))
            print(share, district, len(area.packages), round(fast), round(slow), flush=True)

    main_rows = [r for r in rows if r[0] == SHARE]
    chosen = max(r[3] for r in main_rows)  # fastest time that keeps every district at or under 190 stops
    upper = min(r[4] for r in main_rows)
    middle = (chosen + upper) / 2
    check = []
    for district in DISTRICTS:
        area = Area(city, district, SHARE, seed=2)  # fresh houses, so the check isn't on the ones it was tuned on
        check.append((district, *area.route(middle), *area.route(chosen)))
    ok = PLAUSIBLE[0] <= chosen < upper <= PLAUSIBLE[1] and all(TARGET[0] <= c[1] <= TARGET[1] for c in check)
    _write(rows, chosen, upper, middle, check, ok, city)
    print("check", "passed" if ok else "FAILED", f"service {chosen:.0f} s")


def _write(rows, chosen, upper, middle, check, ok, city):
    lines = [
        "# DSP calibration",
        "",
        f"Written by `python -m baselines.calibrate`. **Check {'passed' if ok else 'failed'}.**",
        "",
        "Does the DSP van model reproduce Amazon's public figures (150–190 stops, 200–300 packages per 10-hour "
        "route)? One van works an area of houses in a 24 x 24-block city (seed "
        f"{CITY_SEED}, {city.width / 1000:.1f} x {city.height / 1000:.1f} km), where a share of the houses get parcels "
        f"that day ({EXTRA_PER_STOP + 1:.2f} parcels each on average). The shift runs {_clock(SHIFT_START)} to "
        f"{_clock(SHIFT_START + SHIFT)} with {LOADOUT * 60:.0f} min of loadout, routes come from OR-Tools "
        f"({SOLVER_SECONDS} s per solve), and each stop takes the service time below plus {EXTRA_PACKAGE:.0f} s per "
        "extra package. The service time is found by bisection, so each value is within a few percent.",
        "",
        "| share of houses with parcels | district | houses with parcels | service time for 190 stops | for 150 stops |",
        "|---|---|---|---|---|",
    ] + [f"| {share:.0%} | {d} | {n} | {fast:.0f} s | {slow:.0f} s |" for share, d, n, fast, slow in rows] + [
        "",
        f"With 15% of houses getting parcels, a service time between **{chosen:.0f} s and {upper:.0f} s** puts every "
        f"district in range. The plausible range is {PLAUSIBLE[0]:.0f}–{PLAUSIBLE[1]:.0f} s (reasoning in "
        "`baselines/calibrate.py`). The baseline uses the fast end, "
        f"**{chosen:.0f} s**, the most generous choice for Amazon.",
        "",
        f"Checked on a fresh set of houses, at the middle of the window ({middle:.0f} s), and at the fast end the "
        "baseline uses. At the fast end routes should come out at about 190 stops, give or take the solver's noise:",
        "",
        f"| district | stops at {middle:.0f} s | packages | in range | stops at {chosen:.0f} s | packages |",
        "|---|---|---|---|---|---|",
    ] + [f"| {d} | {s} | {p} | {'yes' if TARGET[0] <= s <= TARGET[1] else 'no'} | {s2} | {p2} |"
         for d, s, p, s2, p2 in check] + [
        "",
        "## What this does and doesn't show",
        "",
        "- It shows the model can reproduce the public figures with a believable service time. It doesn't prove "
        "the model is right: the service time was fitted to make it match.",
        "- The rows at 10% and 25% show how much the answer depends on how many houses get parcels, which isn't "
        "public. Denser deliveries mean less driving between stops, so the same stop count needs a longer service "
        "time.",
        "- Apartment blocks aren't calibrated: a whole block is one stop with many packages, and Amazon only says "
        "those routes carry more packages. The baseline uses the same service time plus the per-package time there.",
        "- The model has no breaks; the service time absorbs them, because the public stop counts include them.",
    ]
    Path("results").mkdir(exist_ok=True)
    Path("results/dsp-calibration.md").write_text("\n".join(lines) + "\n")
    print("wrote results/dsp-calibration.md")


if __name__ == "__main__":
    main()
