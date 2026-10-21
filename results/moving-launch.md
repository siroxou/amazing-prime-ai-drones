# Launching from a moving truck

Written by `python -m baselines.moving --held-out`. 50 days, 500 parcels each, averages over the days. Both columns use the classical solver's plan (600 m launch radius, 10-minute locker wait, fixed-speed drones). Parked: the truck waits at each stop until its drones are back. Moving: it only waits for the locker, and the drones launch from it and land on it as it drives, with 25 minutes in the air per battery.

| | parked launches | moving launches |
|---|---|---|
| trucks | 2.0 | 2.0 |
| stops | 20 | 20 |
| parcels delivered today | 90% | 90% |
| by drone | 46% | 47% |
| last parcel | 11:45 | 11:43 |
| half of all parcels by | 10:58 | 10:52 |
| delivered by 14:00 | 90% | 90% |
| truck hours | 4.6 | 4.6 |
| km driven | 9 | 9 |

## What it shows

Launching from a moving truck barely changes anything here: the last parcel goes out 2 minutes earlier and half the parcels 6 minutes earlier. On three sample days, only 12–15% of drones took off while the truck was driving, and 5–10% landed on it while it was moving. The rest flew while it was parked.

The reason is that the trucks spend most of their day parked. Every drone parcel is already within 600 m of a locker pickup point, so there are no stops just for launching (a 3 km launch radius gives the same 20 stops on five sample days). Each truck spends about 10 minutes at each of its 10 or so pickup points, with short drives in between. Flights are short (about 2.4 minutes, launch to landing), so a drone is usually back while the truck is still at the stop.

So in this city the locker wait is what holds the trucks up, not the drones. Moving launches should matter more where trucks drive further between stops: bigger cities, fewer locker parcels, or shorter locker waits. This also uses the simple fixed-speed drone model.

## Every day

| city | day | launches | result |
|---|---|---|---|
| 1000 | 0 | parked | 600 m launch radius: 2 trucks, 40 stops; 82% delivered (0% by drone), last at 13:26, half of all parcels by 11:25, 82% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1000 | 0 | moving | 600 m launch radius: 2 trucks, 40 stops; 82% delivered (0% by drone), last at 13:26, half of all parcels by 11:25, 82% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1000 | 1 | parked | 600 m launch radius: 2 trucks, 15 stops; 92% delivered (57% by drone), last at 11:24, half of all parcels by 10:55, 92% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1000 | 1 | moving | 600 m launch radius: 2 trucks, 15 stops; 92% delivered (57% by drone), last at 11:15, half of all parcels by 10:43, 92% by 14:00; 3.7 truck hours, 7 km, replanned |
| 1000 | 2 | parked | 600 m launch radius: 2 trucks, 17 stops; 90% delivered (53% by drone), last at 11:26, half of all parcels by 10:46, 90% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1000 | 2 | moving | 600 m launch radius: 2 trucks, 17 stops; 90% delivered (53% by drone), last at 11:25, half of all parcels by 10:44, 90% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1000 | 3 | parked | 600 m launch radius: 2 trucks, 14 stops; 91% delivered (56% by drone), last at 11:15, half of all parcels by 10:46, 91% by 14:00; 3.6 truck hours, 9 km, replanned |
| 1000 | 3 | moving | 600 m launch radius: 2 trucks, 14 stops; 91% delivered (56% by drone), last at 11:13, half of all parcels by 10:20, 91% by 14:00; 3.6 truck hours, 8 km, replanned |
| 1000 | 4 | parked | 600 m launch radius: 2 trucks, 17 stops; 93% delivered (55% by drone), last at 11:29, half of all parcels by 10:48, 93% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1000 | 4 | moving | 600 m launch radius: 2 trucks, 17 stops; 93% delivered (55% by drone), last at 11:29, half of all parcels by 10:44, 93% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1001 | 0 | parked | 600 m launch radius: 2 trucks, 18 stops; 94% delivered (56% by drone), last at 11:35, half of all parcels by 10:51, 94% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1001 | 0 | moving | 600 m launch radius: 2 trucks, 18 stops; 94% delivered (56% by drone), last at 11:34, half of all parcels by 10:53, 94% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1001 | 1 | parked | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (54% by drone), last at 11:26, half of all parcels by 10:58, 91% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1001 | 1 | moving | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (54% by drone), last at 11:20, half of all parcels by 10:34, 91% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1001 | 2 | parked | 600 m launch radius: 2 trucks, 18 stops; 93% delivered (57% by drone), last at 11:37, half of all parcels by 11:04, 93% by 14:00; 4.3 truck hours, 8 km, replanned |
| 1001 | 2 | moving | 600 m launch radius: 2 trucks, 18 stops; 93% delivered (57% by drone), last at 11:32, half of all parcels by 10:28, 93% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1001 | 3 | parked | 600 m launch radius: 2 trucks, 21 stops; 92% delivered (52% by drone), last at 11:47, half of all parcels by 11:09, 92% by 14:00; 4.7 truck hours, 8 km, replanned |
| 1001 | 3 | moving | 600 m launch radius: 2 trucks, 21 stops; 92% delivered (52% by drone), last at 11:47, half of all parcels by 11:09, 92% by 14:00; 4.7 truck hours, 8 km, replanned |
| 1001 | 4 | parked | 600 m launch radius: 2 trucks, 18 stops; 94% delivered (53% by drone), last at 11:35, half of all parcels by 10:55, 94% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1001 | 4 | moving | 600 m launch radius: 2 trucks, 18 stops; 94% delivered (53% by drone), last at 11:33, half of all parcels by 10:53, 94% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1002 | 0 | parked | 600 m launch radius: 2 trucks, 16 stops; 93% delivered (57% by drone), last at 11:26, half of all parcels by 10:56, 93% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1002 | 0 | moving | 600 m launch radius: 2 trucks, 16 stops; 93% delivered (57% by drone), last at 11:24, half of all parcels by 10:36, 93% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1002 | 1 | parked | 600 m launch radius: 2 trucks, 16 stops; 90% delivered (56% by drone), last at 11:26, half of all parcels by 10:45, 90% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1002 | 1 | moving | 600 m launch radius: 2 trucks, 16 stops; 90% delivered (56% by drone), last at 11:26, half of all parcels by 10:45, 90% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1002 | 2 | parked | 600 m launch radius: 2 trucks, 21 stops; 91% delivered (52% by drone), last at 11:46, half of all parcels by 11:03, 91% by 14:00; 4.8 truck hours, 9 km, replanned |
| 1002 | 2 | moving | 600 m launch radius: 2 trucks, 21 stops; 91% delivered (52% by drone), last at 11:51, half of all parcels by 10:55, 91% by 14:00; 4.7 truck hours, 9 km, replanned |
| 1002 | 3 | parked | 600 m launch radius: 2 trucks, 40 stops; 84% delivered (0% by drone), last at 13:28, half of all parcels by 11:57, 84% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1002 | 3 | moving | 600 m launch radius: 2 trucks, 40 stops; 84% delivered (0% by drone), last at 13:28, half of all parcels by 11:57, 84% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1002 | 4 | parked | 600 m launch radius: 2 trucks, 16 stops; 88% delivered (51% by drone), last at 11:25, half of all parcels by 10:34, 88% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1002 | 4 | moving | 600 m launch radius: 2 trucks, 16 stops; 88% delivered (51% by drone), last at 11:25, half of all parcels by 10:34, 88% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1003 | 0 | parked | 600 m launch radius: 2 trucks, 39 stops; 83% delivered (0% by drone), last at 13:27, half of all parcels by 11:03, 83% by 14:00; 7.8 truck hours, 12 km, replanned |
| 1003 | 0 | moving | 600 m launch radius: 2 trucks, 39 stops; 83% delivered (0% by drone), last at 13:27, half of all parcels by 11:03, 83% by 14:00; 7.8 truck hours, 12 km, replanned |
| 1003 | 1 | parked | 600 m launch radius: 2 trucks, 20 stops; 92% delivered (58% by drone), last at 11:41, half of all parcels by 11:10, 92% by 14:00; 4.5 truck hours, 9 km, replanned |
| 1003 | 1 | moving | 600 m launch radius: 2 trucks, 20 stops; 92% delivered (58% by drone), last at 11:42, half of all parcels by 10:46, 92% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1003 | 2 | parked | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (53% by drone), last at 11:29, half of all parcels by 10:55, 91% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1003 | 2 | moving | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (53% by drone), last at 11:33, half of all parcels by 10:45, 91% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1003 | 3 | parked | 600 m launch radius: 2 trucks, 16 stops; 93% delivered (54% by drone), last at 11:25, half of all parcels by 10:46, 93% by 14:00; 3.9 truck hours, 7 km, replanned |
| 1003 | 3 | moving | 600 m launch radius: 2 trucks, 16 stops; 93% delivered (54% by drone), last at 11:15, half of all parcels by 10:43, 93% by 14:00; 3.9 truck hours, 7 km, replanned |
| 1003 | 4 | parked | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (57% by drone), last at 11:29, half of all parcels by 10:56, 91% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1003 | 4 | moving | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (57% by drone), last at 11:34, half of all parcels by 10:48, 91% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1004 | 0 | parked | 600 m launch radius: 2 trucks, 12 stops; 91% delivered (54% by drone), last at 11:07, half of all parcels by 10:34, 91% by 14:00; 3.3 truck hours, 8 km, replanned |
| 1004 | 0 | moving | 600 m launch radius: 2 trucks, 12 stops; 91% delivered (54% by drone), last at 11:02, half of all parcels by 10:31, 91% by 14:00; 3.2 truck hours, 8 km, replanned |
| 1004 | 1 | parked | 600 m launch radius: 2 trucks, 15 stops; 92% delivered (55% by drone), last at 11:22, half of all parcels by 10:43, 92% by 14:00; 3.7 truck hours, 7 km, replanned |
| 1004 | 1 | moving | 600 m launch radius: 2 trucks, 15 stops; 92% delivered (55% by drone), last at 11:17, half of all parcels by 10:40, 92% by 14:00; 3.7 truck hours, 6 km, replanned |
| 1004 | 2 | parked | 600 m launch radius: 2 trucks, 22 stops; 91% delivered (52% by drone), last at 11:56, half of all parcels by 11:15, 91% by 14:00; 4.9 truck hours, 9 km, replanned |
| 1004 | 2 | moving | 600 m launch radius: 2 trucks, 22 stops; 91% delivered (52% by drone), last at 11:56, half of all parcels by 10:49, 91% by 14:00; 4.9 truck hours, 9 km, replanned |
| 1004 | 3 | parked | 600 m launch radius: 2 trucks, 42 stops; 81% delivered (0% by drone), last at 13:32, half of all parcels by 12:36, 81% by 14:00; 8.3 truck hours, 11 km, replanned |
| 1004 | 3 | moving | 600 m launch radius: 2 trucks, 42 stops; 81% delivered (0% by drone), last at 13:32, half of all parcels by 12:36, 81% by 14:00; 8.3 truck hours, 11 km, replanned |
| 1004 | 4 | parked | 600 m launch radius: 2 trucks, 19 stops; 93% delivered (52% by drone), last at 11:40, half of all parcels by 10:52, 93% by 14:00; 4.4 truck hours, 10 km, replanned |
| 1004 | 4 | moving | 600 m launch radius: 2 trucks, 19 stops; 93% delivered (52% by drone), last at 11:36, half of all parcels by 10:52, 93% by 14:00; 4.4 truck hours, 10 km, replanned |
| 1005 | 0 | parked | 600 m launch radius: 2 trucks, 17 stops; 92% delivered (56% by drone), last at 11:30, half of all parcels by 10:56, 92% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1005 | 0 | moving | 600 m launch radius: 2 trucks, 17 stops; 92% delivered (56% by drone), last at 11:30, half of all parcels by 10:49, 92% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1005 | 1 | parked | 600 m launch radius: 2 trucks, 15 stops; 94% delivered (59% by drone), last at 11:25, half of all parcels by 10:39, 94% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1005 | 1 | moving | 600 m launch radius: 2 trucks, 15 stops; 94% delivered (59% by drone), last at 11:22, half of all parcels by 10:44, 94% by 14:00; 3.7 truck hours, 8 km, replanned |
| 1005 | 2 | parked | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (53% by drone), last at 11:22, half of all parcels by 10:48, 91% by 14:00; 4.0 truck hours, 9 km, replanned |
| 1005 | 2 | moving | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (53% by drone), last at 11:24, half of all parcels by 10:44, 91% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1005 | 3 | parked | 600 m launch radius: 2 trucks, 16 stops; 92% delivered (53% by drone), last at 11:26, half of all parcels by 10:46, 92% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1005 | 3 | moving | 600 m launch radius: 2 trucks, 16 stops; 92% delivered (53% by drone), last at 11:25, half of all parcels by 10:45, 92% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1005 | 4 | parked | 600 m launch radius: 2 trucks, 15 stops; 91% delivered (53% by drone), last at 11:19, half of all parcels by 10:44, 91% by 14:00; 3.8 truck hours, 8 km, replanned |
| 1005 | 4 | moving | 600 m launch radius: 2 trucks, 15 stops; 90% delivered (53% by drone), last at 11:22, half of all parcels by 10:42, 90% by 14:00; 3.7 truck hours, 8 km, replanned |
| 1006 | 0 | parked | 600 m launch radius: 2 trucks, 17 stops; 92% delivered (56% by drone), last at 11:33, half of all parcels by 10:31, 92% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1006 | 0 | moving | 600 m launch radius: 2 trucks, 17 stops; 92% delivered (56% by drone), last at 11:28, half of all parcels by 10:36, 92% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1006 | 1 | parked | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (57% by drone), last at 11:25, half of all parcels by 10:48, 91% by 14:00; 4.0 truck hours, 9 km, replanned |
| 1006 | 1 | moving | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (57% by drone), last at 11:23, half of all parcels by 10:42, 91% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1006 | 2 | parked | 600 m launch radius: 2 trucks, 23 stops; 70% delivered (20% by drone), last at 11:59, half of all parcels by 11:03, 70% by 14:00; 5.1 truck hours, 9 km, replanned |
| 1006 | 2 | moving | 600 m launch radius: 2 trucks, 23 stops; 75% delivered (28% by drone), last at 12:03, half of all parcels by 10:57, 75% by 14:00; 5.1 truck hours, 9 km, replanned |
| 1006 | 3 | parked | 600 m launch radius: 2 trucks, 19 stops; 93% delivered (55% by drone), last at 11:41, half of all parcels by 11:02, 93% by 14:00; 4.5 truck hours, 8 km, replanned |
| 1006 | 3 | moving | 600 m launch radius: 2 trucks, 19 stops; 93% delivered (55% by drone), last at 11:34, half of all parcels by 10:32, 93% by 14:00; 4.4 truck hours, 8 km, replanned |
| 1006 | 4 | parked | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (53% by drone), last at 11:25, half of all parcels by 10:38, 91% by 14:00; 3.9 truck hours, 7 km, replanned |
| 1006 | 4 | moving | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (53% by drone), last at 11:24, half of all parcels by 10:35, 91% by 14:00; 3.9 truck hours, 7 km, replanned |
| 1007 | 0 | parked | 600 m launch radius: 2 trucks, 23 stops; 92% delivered (56% by drone), last at 12:00, half of all parcels by 11:08, 92% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1007 | 0 | moving | 600 m launch radius: 2 trucks, 23 stops; 92% delivered (56% by drone), last at 12:00, half of all parcels by 11:06, 92% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1007 | 1 | parked | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (56% by drone), last at 11:31, half of all parcels by 10:44, 91% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1007 | 1 | moving | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (56% by drone), last at 11:32, half of all parcels by 10:41, 91% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1007 | 2 | parked | 600 m launch radius: 2 trucks, 18 stops; 91% delivered (47% by drone), last at 11:33, half of all parcels by 10:42, 91% by 14:00; 4.2 truck hours, 9 km, replanned |
| 1007 | 2 | moving | 600 m launch radius: 2 trucks, 18 stops; 91% delivered (47% by drone), last at 11:32, half of all parcels by 10:40, 91% by 14:00; 4.2 truck hours, 9 km, replanned |
| 1007 | 3 | parked | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (56% by drone), last at 11:23, half of all parcels by 10:32, 91% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1007 | 3 | moving | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (56% by drone), last at 11:23, half of all parcels by 10:29, 91% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1007 | 4 | parked | 600 m launch radius: 2 trucks, 18 stops; 91% delivered (56% by drone), last at 11:38, half of all parcels by 10:48, 91% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1007 | 4 | moving | 600 m launch radius: 2 trucks, 18 stops; 91% delivered (56% by drone), last at 11:32, half of all parcels by 10:56, 91% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1008 | 0 | parked | 600 m launch radius: 2 trucks, 17 stops; 89% delivered (53% by drone), last at 11:28, half of all parcels by 10:50, 89% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1008 | 0 | moving | 600 m launch radius: 2 trucks, 17 stops; 89% delivered (53% by drone), last at 11:25, half of all parcels by 10:45, 89% by 14:00; 4.0 truck hours, 9 km, replanned |
| 1008 | 1 | parked | 600 m launch radius: 2 trucks, 17 stops; 93% delivered (60% by drone), last at 11:28, half of all parcels by 10:42, 93% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1008 | 1 | moving | 600 m launch radius: 2 trucks, 17 stops; 93% delivered (60% by drone), last at 11:26, half of all parcels by 10:47, 93% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1008 | 2 | parked | 600 m launch radius: 2 trucks, 33 stops; 72% delivered (7% by drone), last at 12:49, half of all parcels by 12:10, 72% by 14:00; 6.8 truck hours, 11 km, replanned |
| 1008 | 2 | moving | 600 m launch radius: 2 trucks, 30 stops; 72% delivered (11% by drone), last at 12:31, half of all parcels by 11:44, 72% by 14:00; 6.3 truck hours, 10 km, replanned |
| 1008 | 3 | parked | 600 m launch radius: 2 trucks, 17 stops; 90% delivered (55% by drone), last at 11:29, half of all parcels by 10:43, 90% by 14:00; 4.1 truck hours, 10 km, replanned |
| 1008 | 3 | moving | 600 m launch radius: 2 trucks, 17 stops; 90% delivered (55% by drone), last at 11:25, half of all parcels by 10:35, 90% by 14:00; 4.1 truck hours, 10 km, replanned |
| 1008 | 4 | parked | 600 m launch radius: 2 trucks, 19 stops; 95% delivered (59% by drone), last at 11:44, half of all parcels by 10:53, 95% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1008 | 4 | moving | 600 m launch radius: 2 trucks, 19 stops; 95% delivered (59% by drone), last at 11:44, half of all parcels by 10:42, 95% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1009 | 0 | parked | 600 m launch radius: 2 trucks, 32 stops; 86% delivered (0% by drone), last at 12:45, half of all parcels by 11:46, 86% by 14:00; 6.6 truck hours, 10 km, replanned |
| 1009 | 0 | moving | 600 m launch radius: 2 trucks, 32 stops; 86% delivered (0% by drone), last at 12:45, half of all parcels by 11:46, 86% by 14:00; 6.6 truck hours, 10 km, replanned |
| 1009 | 1 | parked | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (50% by drone), last at 11:28, half of all parcels by 10:52, 91% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1009 | 1 | moving | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (50% by drone), last at 11:28, half of all parcels by 10:49, 91% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1009 | 2 | parked | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (54% by drone), last at 11:27, half of all parcels by 10:36, 91% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1009 | 2 | moving | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (54% by drone), last at 11:18, half of all parcels by 10:45, 91% by 14:00; 3.9 truck hours, 7 km, replanned |
| 1009 | 3 | parked | 600 m launch radius: 2 trucks, 12 stops; 88% delivered (51% by drone), last at 11:08, half of all parcels by 10:32, 88% by 14:00; 3.3 truck hours, 7 km, replanned |
| 1009 | 3 | moving | 600 m launch radius: 2 trucks, 12 stops; 88% delivered (51% by drone), last at 10:57, half of all parcels by 10:29, 88% by 14:00; 3.2 truck hours, 8 km, replanned |
| 1009 | 4 | parked | 600 m launch radius: 2 trucks, 35 stops; 85% delivered (0% by drone), last at 13:03, half of all parcels by 11:34, 85% by 14:00; 7.2 truck hours, 12 km, replanned |
| 1009 | 4 | moving | 600 m launch radius: 2 trucks, 35 stops; 85% delivered (0% by drone), last at 13:03, half of all parcels by 11:34, 85% by 14:00; 7.2 truck hours, 12 km, replanned |
