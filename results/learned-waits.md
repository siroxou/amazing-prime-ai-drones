# Learned locker waits

Written by `python -m optimiser.waits evaluate`. The classical solver's plan for each of the 50 held-out days, replayed with different waits at each stop for the locker. The score is the average hours from 10:00 until a parcel is delivered, a parcel not delivered today counting 24 hours: lower is better. The policies were trained with PPO on 100 days from training cities and never saw these days.

| waits | score | delivered today | half of all parcels by | by 14:00 | last parcel |
|---|---|---|---|---|---|
| fixed 10 min (classical solver as published) | 4.13 h | 86% | 11:09 | 86% | 12:05 |
| best fixed wait, tuned on training days (20 min) | 3.64 h | 92% | 12:05 | 87% | 14:01 |
| hand rule, tuned on training days (0.5 min per locker parcel + up to 20 min along the route) | 3.02 h | 92% | 11:15 | 91% | 13:32 |
| learned waits, seed 0 | 3.01 h | 93% | 11:17 | 90% | 13:56 |
| learned waits, seed 1 | 3.05 h | 93% | 11:20 | 90% | 13:56 |
| learned waits, seed 2 | 3.02 h | 93% | 11:17 | 91% | 13:45 |

Learned waits over 3 seeds: score 3.03 h (seeds range 3.01 to 3.05).

## What it shows

- **The learned waits beat the classical solver**, on every seed: 3.03 h against 4.13 h for its 10-minute wait and 3.64 h for the best fixed wait. They deliver as many parcels as the long fixed wait while getting them out much sooner.
- **What the policy learned is simple.** It waits longer where more locker recipients are coming and later in the route, where a long wait delays fewer stops after it, and doesn't wait at all where only drones are working.
- **So simple that a hand rule does as well.** Two settings tuned on the same training days score 3.02 h. Learning found the rule, but learning isn't needed to use it; the classical solver can just adopt the rule. The case for learning has to come from decisions without an obvious rule: which parcels go by drone, the routes, and replanning when the day goes off plan.
- **Against Amazon** (same score, [baselines.md](baselines.md)): better waits bring the fleet level with the DSP vans, still behind Prime Air with vans. The fleet is faster for what it delivers, but every parcel left for tomorrow counts 24 hours. A smaller penalty would favour the fleet; a parcel a day late is a real cost, though, so 24 hours stays.

Fixed waits on the training days, for choosing the tuned one:

| wait | 0 min | 5 min | 10 min | 15 min | 20 min | 25 min | 30 min | 40 min |
|---|---|---|---|---|---|---|---|---|
| score | 7.69 h | 5.74 h | 4.15 h | 3.68 h | 3.61 h | 3.84 h | 4.22 h | 5.54 h |
