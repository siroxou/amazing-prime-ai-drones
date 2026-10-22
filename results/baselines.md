# Baselines side by side

The same 50 held-out days (city seeds 1000–1009, days 0–4, 500 parcels each), averaged. Each system has its own results file with every day listed.

<!-- table: written by python -m baselines.run -->

| system | score | delivered today | last parcel | half of all parcels by | by 14:00 | vehicles | driver hours |
|---|---|---|---|---|---|---|---|
| Amazon DSP vans ([dsp-baseline.md](dsp-baseline.md)) | 3.02 h | 100% | 15:46 | 13:05 | 68% | 2.0 vans | 12.5 |
| Amazon Prime Air, 10 drones at the site, plus vans ([prime-air-baseline.md](prime-air-baseline.md)) | 2.71 h | 100% | 16:26 | 12:43 | 73% | 1.1 vans | 7.2 |
| Locker trucks, no drones, 10 min wait ([trucks-only-baseline.md](trucks-only-baseline.md)) | 5.29 h | 82% | 12:17 | 11:22 | 82% | 3.0 trucks | 0.0 |
| Locker trucks, no drones, 30 min wait ([trucks-only-baseline.md](trucks-only-baseline.md)) | 3.88 h | 97% | 16:38 | 13:22 | 57% | 3.0 trucks | 0.0 |
| Trucks with 10 drones each, classical solver, morning only ([classical-solver.md](classical-solver.md)) | 4.13 h | 86% | 12:04 | 11:10 | 86% | 2.0 trucks | 0.0 |
| The same with an afternoon second pass for what's left ([classical-solver.md](classical-solver.md)) | 2.15 h | 96% | 13:39 | 11:09 | 95% | 2.0 trucks | 0.0 |
| The same, drones launching from and landing on the moving truck ([moving-launch.md](moving-launch.md)) | 2.02 h | 96% | 13:32 | 11:02 | 95% | 2.0 trucks | 0.0 |

Score: average hours from 10:00 until a parcel is delivered, a parcel not delivered today counting 24 hours; lower is better (optimiser/routes.py).

All 7 over all 50 days took 2.9 minutes on 18 workers (`python -m baselines.run`).

<!-- end of table -->

"Half of all parcels by" counts parcels that weren't delivered as never delivered. Everything starts from the same distribution centre at 10:00.

## What it says so far

- **With the afternoon second pass, the fleet beats both Amazon systems on the score.** Each truck comes back, reloads and goes out again with what it couldn't deliver in the morning. That takes the fleet from 86% to 96% delivered today and its score from 4.13 h to 2.15 h (2.02 h with moving launches), against 2.71 h for Prime Air with vans and 3.02 h for the DSP vans. It still finishes about two hours before the vans.
- **That rests on one big guess.** A recipient who missed the truck in the morning gets a second notice and is taken to be as quick to come out as anyone else ([docs/days.md](../docs/days.md)). Many real recipients miss the truck because they're out, and would miss it again. Varying the share who come out the second time (`SECOND_SHOW` in sim/day.py), with the drones still flying what they can:

  | share who come out the second time | none | a quarter | half | three quarters | all (the table) |
  |---|---|---|---|---|---|
  | score | 3.73 h | 3.30 h | 2.95 h | 2.55 h | 2.15 h |
  | delivered today | 88% | 90% | 92% | 94% | 96% |

  So the fleet beats the vans if about half come out the second time, and Prime Air with vans if about two thirds do. Nobody publishes that share.
- **It still doesn't deliver everything.** 4% of parcels, about 21 a day, go back to the station at the end of the day. The vans and Prime Air deliver every one.
- **In the morning alone, the fleet is faster but leaves parcels behind.** It gets 86% out by 14:00 against about 65–70% for the vans, finishing around noon instead of about 15:45, but 14% are locker parcels whose recipients didn't come out in time. Drones take 36% of parcels in the morning; the rest go in the locker.
- **Wind is what limits the drones.** With the cost model ([docs/drone-model.md](../docs/drone-model.md)) instead of Phase 2's fixed-speed one, drones take 36% of parcels instead of 46%. On windy days the wind at cruise height outruns the drone's 15 m/s airspeed, or the gusts rule out the drop spot, so those parcels move to the locker.
- **Most of the speed gain over the vans comes from the locker trucks, not the drones.** Locker trucks alone, with a 10-minute wait, finish about three and a half hours before the vans, because nobody walks every parcel to a door; but they leave 18% of parcels behind. Adding the drones makes the fleet a little earlier still and gets 4 more parcels in every 100 delivered.
- **Launching from a moving truck changes only a few minutes,** because the trucks spend most of their day parked at locker pickup points and the drones' short flights fit inside those stops.
- **Without the second pass, Prime Air with vans is best on the score.** Morning only, the fleet scores 4.13 h (3.99 h with moving launches), and 3.03 h with learned locker waits ([learned-waits.md](learned-waits.md)). With the second pass in, the plain 10-minute wait does better than the learned waits, and a re-tuned hand rule does better still.
- **Prime Air saves Amazon driver hours, not time.** Its drones are limited by what they can take, not by how many there are.
- **On 6 of the 50 days the fleet's drones are grounded all morning.** The second pass flies them in the afternoon if the wind has dropped. Prime Air, flying all day, is grounded all day on 4 of the 50.

## How far to trust it

- Every number rests on settings, and many are guesses: how fast recipients come out, and whether those who missed the truck come out the second time, every number in the drone model, the wind limit, the cargo size limits. Amazon's side is calibrated against its public figures. The project's own system isn't calibrated against anything yet, because it doesn't exist outside the sim; Phase 5 checks the drone model against a 3D flight sim.
- The drone's 15 m/s airspeed matters a lot, because the wind so often beats it. A faster drone would lose fewer parcels to wind.
- Porches have no roofs in the city model, so almost every house has a drop spot. Real porches often don't.
- 500 parcels is a small day: the vans run part-full routes, which flatters them, and the fleet runs only two trucks.
- The trucks need no drivers, but remote supervision isn't counted.

## Running it

`python -m baselines.run` runs all seven on all 50 days at their main settings, one day per worker, and rewrites the table above. With the second pass in it took 2.9 minutes on 18 workers (Apple Silicon laptop), so the Phase 2 exit check (all baselines in under 10 minutes) passes. Each system's own command (`python -m baselines.dsp --held-out` and so on, listed in the README) tries more settings and lists every day.

OR-Tools gets a fixed time per solve, so results move a little from run to run. Across four runs of the vans, "half of all parcels by" ranged from 12:54 to 13:16 and "by 14:00" from 65% to 70%. Differences smaller than that between systems don't mean anything.
