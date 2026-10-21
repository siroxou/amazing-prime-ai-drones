# Baselines side by side

The same 50 held-out days (city seeds 1000–1009, days 0–4, 500 parcels each), averaged. Each system has its own results file with every day listed.

<!-- table: written by python -m baselines.run -->

| system | delivered today | last parcel | half of all parcels by | by 14:00 | vehicles | driver hours |
|---|---|---|---|---|---|---|
| Amazon DSP vans ([dsp-baseline.md](dsp-baseline.md)) | 100% | 15:46 | 12:54 | 70% | 2.0 vans | 12.5 |
| Amazon Prime Air, 10 drones at the site, plus vans ([prime-air-baseline.md](prime-air-baseline.md)) | 100% | 16:26 | 12:44 | 72% | 1.1 vans | 7.2 |
| Locker trucks, no drones, 10 min wait ([trucks-only-baseline.md](trucks-only-baseline.md)) | 82% | 12:17 | 11:24 | 82% | 3.0 trucks | 0.0 |
| Locker trucks, no drones, 30 min wait ([trucks-only-baseline.md](trucks-only-baseline.md)) | 97% | 16:37 | 13:21 | 57% | 3.0 trucks | 0.0 |
| Trucks with 10 drones each, classical solver, 600 m launch radius ([classical-solver.md](classical-solver.md)) | 90% | 11:45 | 10:58 | 90% | 2.0 trucks | 0.0 |
| The same, drones launching from and landing on the moving truck ([moving-launch.md](moving-launch.md)) | 90% | 11:43 | 10:52 | 90% | 2.0 trucks | 0.0 |

All six over all 50 days took 6.3 minutes on 6 workers (`python -m baselines.run`).

<!-- end of table -->

"Half of all parcels by" counts parcels that weren't delivered as never delivered. Everything starts from the same distribution centre at 10:00.

## What it says so far

- **The truck + drone fleet finishes about four hours earlier than the vans,** and gets 90% of parcels out by 14:00 against about 70%. Drones take 46% of parcels, and the rest go in the locker.
- **It doesn't deliver everything.** 10% of parcels, all locker ones, go back to the station because their recipients didn't come out in time. The vans deliver every parcel. A fair score has to count that, and the locker wait is the knob that trades one against the other.
- **Most of the speed gain over the vans comes from the locker trucks, not the drones.** Locker trucks alone, with a 10-minute wait, finish about three and a half hours before the vans, because nobody walks every parcel to a door; but they leave 18% of parcels behind. Adding the drones gains another half hour and gets 8 more parcels in every 100 delivered. So far, the drones' main job is covering parcels the locker would miss.
- **Launching from a moving truck adds almost nothing here,** a few minutes, because the trucks spend most of their day parked at locker pickup points and the drones' short flights fit inside those stops.
- **Prime Air saves Amazon driver hours, not time.** Its drones are limited by what they can take, not by how many there are.
- **On 6 of the 50 days the fleet's drones are grounded all morning,** and with it done by noon, the morning is all that matters. Prime Air, flying all day, is grounded all day on 4 of the 50.

## How far to trust it

- Every number rests on settings, and many are guesses: how fast recipients come out, the drone's speed and reload time, the wind limit, the cargo size limits. Amazon's side is calibrated against its public figures; the project's own system isn't calibrated against anything yet, because it doesn't exist outside the sim.
- The fleet's drone model is fixed-speed: no wind, no payload or battery effects. Phase 3 replaces it with the full cost model, and Phase 5 checks it against the 3D flight sim. The gain may shrink.
- Porches have no roofs in the city model, so almost every house has a drop spot. Real porches often don't.
- 500 parcels is a small day: the vans run part-full routes, which flatters them, and the fleet runs only two trucks.
- The trucks need no drivers, but remote supervision isn't counted.

## Running it

`python -m baselines.run` runs all six on all 50 days at their main settings, one day per worker, and rewrites the table above. It took 6.3 minutes on 6 workers and 2.1 minutes on 18 (Apple Silicon laptop), so the Phase 2 exit check (all baselines in under 10 minutes) passes. Each system's own command (`python -m baselines.dsp --held-out` and so on, listed in the README) tries more settings and lists every day.

OR-Tools gets a fixed time per solve, so results move a little from run to run. Across three runs of the vans, "half of all parcels by" ranged from 12:54 to 13:05 and "by 14:00" from 67% to 70%. Differences smaller than that between systems don't mean anything.
