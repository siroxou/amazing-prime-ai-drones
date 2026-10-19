# DSP calibration

Written by `python -m baselines.calibrate`. **Check passed.**

Does the DSP van model reproduce Amazon's public figures (150–190 stops, 200–300 packages per 10-hour route)? One van works an area of houses in a 24 x 24-block city (seed 500, 2.9 x 2.4 km), where a share of the houses get parcels that day (1.45 parcels each on average). The shift runs 09:30 to 19:30 with 30 min of loadout, routes come from OR-Tools (5 s per solve), and each stop takes the service time below plus 10 s per extra package. The service time is found by bisection, so each value is within a few percent.

| share of houses with parcels | district | houses with parcels | service time for 190 stops | for 150 stops |
|---|---|---|---|---|
| 15% | dense | 303 | 166 s | 215 s |
| 15% | suburb | 399 | 157 s | 209 s |
| 10% | dense | 202 | 161 s | 215 s |
| 10% | suburb | 266 | 157 s | 203 s |
| 25% | dense | 506 | 171 s | 215 s |
| 25% | suburb | 665 | 166 s | 215 s |

With 15% of houses getting parcels, a service time between **166 s and 209 s** puts every district in range. The plausible range is 30–228 s (reasoning in `baselines/calibrate.py`). The baseline uses the fast end, **166 s**, the most generous choice for Amazon.

Checked on a fresh set of houses, at the middle of the window (188 s), and at the fast end the baseline uses. At the fast end routes should come out at about 190 stops, give or take the solver's noise:

| district | stops at 188 s | packages | in range | stops at 166 s | packages |
|---|---|---|---|---|---|
| dense | 172 | 219 | yes | 191 | 265 |
| suburb | 165 | 216 | yes | 184 | 241 |

## What this does and doesn't show

- It shows the model can reproduce the public figures with a believable service time. It doesn't prove the model is right: the service time was fitted to make it match.
- The rows at 10% and 25% show how much the answer depends on how many houses get parcels, which isn't public. Denser deliveries mean less driving between stops, so the same stop count needs a longer service time.
- Apartment blocks aren't calibrated: a whole block is one stop with many packages, and Amazon only says those routes carry more packages. The baseline uses the same service time plus the per-package time there.
- The model has no breaks; the service time absorbs them, because the public stop counts include them.
