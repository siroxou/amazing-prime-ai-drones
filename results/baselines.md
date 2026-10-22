# Baselines side by side

The same 50 held-out days (city seeds 1000–1009, days 0–4, 500 parcels each), averaged. Each system has its own results file with every day listed.

<!-- table: written by python -m baselines.run -->

| system | score | delivered today | last parcel | half of all parcels by | by 14:00 | vehicles | driver hours |
|---|---|---|---|---|---|---|---|
| Amazon DSP vans ([dsp-baseline.md](dsp-baseline.md)) | 3.01 h | 100% | 15:46 | 13:05 | 67% | 2.0 vans | 12.5 |
| Amazon Prime Air, 10 drones at the site, plus vans ([prime-air-baseline.md](prime-air-baseline.md)) | 2.71 h | 100% | 16:26 | 12:43 | 73% | 1.1 vans | 7.2 |
| Locker trucks, no drones, 10 min wait ([trucks-only-baseline.md](trucks-only-baseline.md)) | 5.28 h | 82% | 12:17 | 11:21 | 82% | 3.0 trucks | 0.0 |
| Locker trucks, no drones, 30 min wait ([trucks-only-baseline.md](trucks-only-baseline.md)) | 3.88 h | 97% | 16:38 | 13:19 | 57% | 3.0 trucks | 0.0 |
| Trucks with 10 drones each, classical solver, 600 m launch radius ([classical-solver.md](classical-solver.md)) | 4.13 h | 86% | 12:04 | 11:09 | 86% | 2.0 trucks | 0.0 |
| The same, drones launching from and landing on the moving truck ([moving-launch.md](moving-launch.md)) | 3.99 h | 87% | 11:58 | 11:01 | 87% | 2.0 trucks | 0.0 |

Score: average hours from 10:00 until a parcel is delivered, a parcel not delivered today counting 24 hours; lower is better (optimiser/routes.py).

All six over all 50 days took 2.2 minutes on 18 workers (`python -m baselines.run`).

<!-- end of table -->

"Half of all parcels by" counts parcels that weren't delivered as never delivered. Everything starts from the same distribution centre at 10:00.

## What it says so far

- **The truck + drone fleet is faster for the parcels it delivers.** It gets 86% of parcels out by 14:00 against about 65–70% for the vans, and finishes around noon instead of about 15:45. Drones take 36% of parcels; the rest go in the locker.
- **It doesn't deliver everything.** 14% of parcels go back to the station, all of them locker parcels whose recipients didn't come out in time. The vans deliver every parcel. So the fleet doesn't beat the vans outright; it trades parcels left behind for speed, and the locker wait is the knob.
- **Wind is what limits the drones.** With the cost model ([docs/drone-model.md](../docs/drone-model.md)) instead of Phase 2's fixed-speed one, drones take 36% of parcels instead of 46%. On windy days the wind at cruise height outruns the drone's 15 m/s airspeed, or the gusts rule out the drop spot, so those parcels move to the locker.
- **Most of the speed gain over the vans comes from the locker trucks, not the drones.** Locker trucks alone, with a 10-minute wait, finish about three and a half hours before the vans, because nobody walks every parcel to a door; but they leave 18% of parcels behind. Adding the drones makes the fleet a little earlier still and gets 4 more parcels in every 100 delivered.
- **Launching from a moving truck changes only a few minutes,** because the trucks spend most of their day parked at locker pickup points and the drones' short flights fit inside those stops.
- **On one score, Prime Air with vans is best.** Counting a parcel left for tomorrow as 24 hours, Prime Air with vans scores 2.71 h, the DSP vans 3.01 h, and the fleet 4.13 h (3.99 h with moving launches). With learned locker waits ([learned-waits.md](learned-waits.md)) the fleet gets to 3.03 h, level with the vans but still behind Prime Air: it's faster, but it leaves parcels behind.
- **Prime Air saves Amazon driver hours, not time.** Its drones are limited by what they can take, not by how many there are.
- **On 6 of the 50 days the fleet's drones are grounded all morning,** and with it done by noon, the morning is all that matters. Prime Air, flying all day, is grounded all day on 4 of the 50.

## How far to trust it

- Every number rests on settings, and many are guesses: how fast recipients come out, every number in the drone model, the wind limit, the cargo size limits. Amazon's side is calibrated against its public figures. The project's own system isn't calibrated against anything yet, because it doesn't exist outside the sim; Phase 5 checks the drone model against a 3D flight sim.
- The drone's 15 m/s airspeed matters a lot, because the wind so often beats it. A faster drone would lose fewer parcels to wind.
- Porches have no roofs in the city model, so almost every house has a drop spot. Real porches often don't.
- 500 parcels is a small day: the vans run part-full routes, which flatters them, and the fleet runs only two trucks.
- The trucks need no drivers, but remote supervision isn't counted.

## Running it

`python -m baselines.run` runs all six on all 50 days at their main settings, one day per worker, and rewrites the table above. It took 6.3 minutes on 6 workers and 2.1 minutes on 18 (Apple Silicon laptop), so the Phase 2 exit check (all baselines in under 10 minutes) passes. Each system's own command (`python -m baselines.dsp --held-out` and so on, listed in the README) tries more settings and lists every day.

OR-Tools gets a fixed time per solve, so results move a little from run to run. Across four runs of the vans, "half of all parcels by" ranged from 12:54 to 13:16 and "by 14:00" from 65% to 70%. Differences smaller than that between systems don't mean anything.
