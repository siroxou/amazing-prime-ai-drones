# Launching from a moving truck

Written by `python -m baselines.moving --held-out`. 50 days, 500 parcels each, averages over the days. Both columns use the classical solver's plan (600 m launch radius, 10-minute locker wait, drones on the cost model in sim/drone.py). Parked: the truck waits at each stop until its drones are back. Moving: it only waits for the locker, and the drones launch from it and land on it as it drives, with the battery set by the drone cost model. Both include the afternoon second pass.

| | parked launches | moving launches |
|---|---|---|
| trucks | 2.0 | 2.0 |
| stops | 24 | 23 |
| parcels delivered today | 96% | 96% |
| delivered on the afternoon second pass | 9% | 9% |
| by drone | 38% | 39% |
| last parcel | 13:39 | 13:32 |
| half of all parcels by | 11:09 | 11:01 |
| delivered by 14:00 | 95% | 95% |
| truck hours | 8.3 | 8.1 |
| km driven | 16 | 16 |

## What it shows

Launching from a moving truck changes the day by only a few minutes, either way. The trucks spend most of their day parked at locker pickup points: every drone parcel is already within the launch radius of one, so there are no stops just for launching. Each truck waits about 10 minutes at each of its 10 or so points, with short drives between. A drone's flight is a few minutes, so it's usually back while the truck is still there. When the truck doesn't wait for its drones, it leaves sooner, but the drones then have further to fly to catch it and are busy for longer, so the two roughly cancel out.

In this city the locker wait, not the drones, is what holds the trucks up. Moving launches should matter more where trucks drive further between stops: bigger cities, fewer locker parcels, or shorter locker waits.

## Every day

| city | day | launches | result |
|---|---|---|---|
| 1000 | 0 | parked | 600 m launch radius: 2 trucks, 40 stops; 90% delivered (0% by drone, 43 on the second pass), last at 15:09, half of all parcels by 11:25, 82% by 14:00; 11.2 truck hours, 19 km, replanned |
| 1000 | 0 | moving | 600 m launch radius: 2 trucks, 40 stops; 90% delivered (0% by drone, 43 on the second pass), last at 15:09, half of all parcels by 11:25, 82% by 14:00; 11.2 truck hours, 19 km, replanned |
| 1000 | 1 | parked | 600 m launch radius: 2 trucks, 17 stops; 98% delivered (49% by drone, 49 on the second pass), last at 12:53, half of all parcels by 10:53, 98% by 14:00; 7.1 truck hours, 15 km, replanned |
| 1000 | 1 | moving | 600 m launch radius: 2 trucks, 17 stops; 97% delivered (51% by drone, 54 on the second pass), last at 13:03, half of all parcels by 10:59, 97% by 14:00; 7.1 truck hours, 16 km, replanned |
| 1000 | 2 | parked | 600 m launch radius: 2 trucks, 20 stops; 97% delivered (41% by drone, 60 on the second pass), last at 12:55, half of all parcels by 11:06, 97% by 14:00; 7.3 truck hours, 16 km, replanned |
| 1000 | 2 | moving | 600 m launch radius: 2 trucks, 21 stops; 96% delivered (40% by drone, 50 on the second pass), last at 12:54, half of all parcels by 11:03, 96% by 14:00; 7.4 truck hours, 17 km, replanned |
| 1000 | 3 | parked | 600 m launch radius: 2 trucks, 14 stops; 91% delivered (46% by drone, 38 on the second pass), last at 12:18, half of all parcels by 10:35, 91% by 14:00; 5.9 truck hours, 17 km, replanned |
| 1000 | 3 | moving | 600 m launch radius: 2 trucks, 15 stops; 99% delivered (56% by drone, 55 on the second pass), last at 12:20, half of all parcels by 10:36, 99% by 14:00; 6.1 truck hours, 16 km, replanned |
| 1000 | 4 | parked | 600 m launch radius: 2 trucks, 25 stops; 97% delivered (38% by drone, 44 on the second pass), last at 13:37, half of all parcels by 11:26, 97% by 14:00; 8.1 truck hours, 16 km, replanned |
| 1000 | 4 | moving | 600 m launch radius: 2 trucks, 21 stops; 96% delivered (43% by drone, 50 on the second pass), last at 13:29, half of all parcels by 11:09, 96% by 14:00; 7.4 truck hours, 15 km, replanned |
| 1001 | 0 | parked | 600 m launch radius: 2 trucks, 20 stops; 99% delivered (48% by drone, 38 on the second pass), last at 12:48, half of all parcels by 10:42, 99% by 14:00; 7.2 truck hours, 14 km, replanned |
| 1001 | 0 | moving | 600 m launch radius: 2 trucks, 19 stops; 98% delivered (52% by drone, 35 on the second pass), last at 13:03, half of all parcels by 10:53, 98% by 14:00; 7.3 truck hours, 13 km, replanned |
| 1001 | 1 | parked | 600 m launch radius: 2 trucks, 22 stops; 99% delivered (49% by drone, 52 on the second pass), last at 12:47, half of all parcels by 11:02, 99% by 14:00; 6.7 truck hours, 15 km, replanned |
| 1001 | 1 | moving | 600 m launch radius: 2 trucks, 19 stops; 99% delivered (52% by drone, 45 on the second pass), last at 12:18, half of all parcels by 11:06, 99% by 14:00; 6.2 truck hours, 14 km, replanned |
| 1001 | 2 | parked | 600 m launch radius: 2 trucks, 22 stops; 99% delivered (53% by drone, 49 on the second pass), last at 13:01, half of all parcels by 10:36, 99% by 14:00; 7.7 truck hours, 15 km, replanned |
| 1001 | 2 | moving | 600 m launch radius: 2 trucks, 23 stops; 99% delivered (52% by drone, 43 on the second pass), last at 13:15, half of all parcels by 11:01, 99% by 14:00; 7.8 truck hours, 17 km, replanned |
| 1001 | 3 | parked | 600 m launch radius: 2 trucks, 23 stops; 99% delivered (45% by drone, 36 on the second pass), last at 14:53, half of all parcels by 11:24, 98% by 14:00; 9.1 truck hours, 17 km, replanned |
| 1001 | 3 | moving | 600 m launch radius: 2 trucks, 23 stops; 99% delivered (45% by drone, 37 on the second pass), last at 14:06, half of all parcels by 11:12, 98% by 14:00; 9.1 truck hours, 17 km, replanned |
| 1001 | 4 | parked | 600 m launch radius: 2 trucks, 19 stops; 97% delivered (43% by drone, 31 on the second pass), last at 13:10, half of all parcels by 10:56, 97% by 14:00; 7.4 truck hours, 16 km, replanned |
| 1001 | 4 | moving | 600 m launch radius: 2 trucks, 20 stops; 97% delivered (46% by drone, 24 on the second pass), last at 13:11, half of all parcels by 10:44, 97% by 14:00; 7.6 truck hours, 15 km, replanned |
| 1002 | 0 | parked | 600 m launch radius: 2 trucks, 20 stops; 96% delivered (40% by drone, 36 on the second pass), last at 12:27, half of all parcels by 11:16, 96% by 14:00; 6.2 truck hours, 13 km, replanned |
| 1002 | 0 | moving | 600 m launch radius: 2 trucks, 17 stops; 98% delivered (46% by drone, 59 on the second pass), last at 12:12, half of all parcels by 10:39, 98% by 14:00; 5.7 truck hours, 14 km, replanned |
| 1002 | 1 | parked | 600 m launch radius: 2 trucks, 22 stops; 97% delivered (40% by drone, 45 on the second pass), last at 13:13, half of all parcels by 10:44, 97% by 14:00; 7.6 truck hours, 16 km, replanned |
| 1002 | 1 | moving | 600 m launch radius: 2 trucks, 23 stops; 97% delivered (42% by drone, 49 on the second pass), last at 13:05, half of all parcels by 10:43, 97% by 14:00; 7.7 truck hours, 16 km, replanned |
| 1002 | 2 | parked | 600 m launch radius: 2 trucks, 23 stops; 98% delivered (45% by drone, 46 on the second pass), last at 14:32, half of all parcels by 11:03, 97% by 14:00; 9.8 truck hours, 17 km, replanned |
| 1002 | 2 | moving | 600 m launch radius: 2 trucks, 23 stops; 98% delivered (47% by drone, 53 on the second pass), last at 14:26, half of all parcels by 10:52, 98% by 14:00; 9.4 truck hours, 16 km, replanned |
| 1002 | 3 | parked | 600 m launch radius: 2 trucks, 40 stops; 90% delivered (0% by drone, 31 on the second pass), last at 14:56, half of all parcels by 11:03, 86% by 14:00; 11.4 truck hours, 20 km, replanned |
| 1002 | 3 | moving | 600 m launch radius: 2 trucks, 40 stops; 90% delivered (0% by drone, 31 on the second pass), last at 14:56, half of all parcels by 11:03, 86% by 14:00; 11.4 truck hours, 20 km, replanned |
| 1002 | 4 | parked | 600 m launch radius: 2 trucks, 17 stops; 96% delivered (42% by drone, 80 on the second pass), last at 13:07, half of all parcels by 10:52, 96% by 14:00; 7.1 truck hours, 16 km, replanned |
| 1002 | 4 | moving | 600 m launch radius: 2 trucks, 17 stops; 98% delivered (43% by drone, 64 on the second pass), last at 12:51, half of all parcels by 10:42, 98% by 14:00; 6.8 truck hours, 17 km, replanned |
| 1003 | 0 | parked | 600 m launch radius: 2 trucks, 39 stops; 89% delivered (0% by drone, 33 on the second pass), last at 14:43, half of all parcels by 11:41, 85% by 14:00; 10.2 truck hours, 18 km, replanned |
| 1003 | 0 | moving | 600 m launch radius: 2 trucks, 39 stops; 89% delivered (0% by drone, 33 on the second pass), last at 14:43, half of all parcels by 11:41, 85% by 14:00; 10.2 truck hours, 18 km, replanned |
| 1003 | 1 | parked | 600 m launch radius: 2 trucks, 27 stops; 97% delivered (50% by drone, 45 on the second pass), last at 13:59, half of all parcels by 10:54, 97% by 14:00; 9.0 truck hours, 17 km, replanned |
| 1003 | 1 | moving | 600 m launch radius: 2 trucks, 25 stops; 97% delivered (51% by drone, 45 on the second pass), last at 13:31, half of all parcels by 11:04, 97% by 14:00; 8.1 truck hours, 17 km, replanned |
| 1003 | 2 | parked | 600 m launch radius: 2 trucks, 24 stops; 95% delivered (32% by drone, 60 on the second pass), last at 13:55, half of all parcels by 11:16, 95% by 14:00; 8.7 truck hours, 16 km, replanned |
| 1003 | 2 | moving | 600 m launch radius: 2 trucks, 20 stops; 94% delivered (39% by drone, 59 on the second pass), last at 14:06, half of all parcels by 11:10, 94% by 14:00; 8.7 truck hours, 16 km, replanned |
| 1003 | 3 | parked | 600 m launch radius: 2 trucks, 24 stops; 97% delivered (41% by drone, 46 on the second pass), last at 13:18, half of all parcels by 11:09, 97% by 14:00; 7.5 truck hours, 14 km, replanned |
| 1003 | 3 | moving | 600 m launch radius: 2 trucks, 19 stops; 98% delivered (45% by drone, 43 on the second pass), last at 12:56, half of all parcels by 10:50, 98% by 14:00; 6.7 truck hours, 14 km, replanned |
| 1003 | 4 | parked | 600 m launch radius: 2 trucks, 26 stops; 98% delivered (45% by drone, 45 on the second pass), last at 13:48, half of all parcels by 10:45, 98% by 14:00; 9.0 truck hours, 19 km, replanned |
| 1003 | 4 | moving | 600 m launch radius: 2 trucks, 20 stops; 96% delivered (49% by drone, 70 on the second pass), last at 13:37, half of all parcels by 10:54, 96% by 14:00; 7.6 truck hours, 17 km, replanned |
| 1004 | 0 | parked | 600 m launch radius: 2 trucks, 23 stops; 94% delivered (35% by drone, 64 on the second pass), last at 13:46, half of all parcels by 10:56, 94% by 14:00; 8.2 truck hours, 17 km, replanned |
| 1004 | 0 | moving | 600 m launch radius: 2 trucks, 20 stops; 94% delivered (39% by drone, 39 on the second pass), last at 13:15, half of all parcels by 10:32, 94% by 14:00; 8.0 truck hours, 17 km, replanned |
| 1004 | 1 | parked | 600 m launch radius: 2 trucks, 22 stops; 94% delivered (37% by drone, 39 on the second pass), last at 13:17, half of all parcels by 11:16, 94% by 14:00; 7.3 truck hours, 16 km, replanned |
| 1004 | 1 | moving | 600 m launch radius: 2 trucks, 22 stops; 94% delivered (39% by drone, 45 on the second pass), last at 12:00, half of all parcels by 10:42, 94% by 14:00; 7.3 truck hours, 16 km, replanned |
| 1004 | 2 | parked | 600 m launch radius: 2 trucks, 27 stops; 98% delivered (44% by drone, 49 on the second pass), last at 14:24, half of all parcels by 11:03, 93% by 14:00; 9.4 truck hours, 17 km, replanned |
| 1004 | 2 | moving | 600 m launch radius: 2 trucks, 25 stops; 98% delivered (44% by drone, 54 on the second pass), last at 14:14, half of all parcels by 11:23, 97% by 14:00; 9.1 truck hours, 15 km, replanned |
| 1004 | 3 | parked | 600 m launch radius: 2 trucks, 42 stops; 91% delivered (0% by drone, 50 on the second pass), last at 15:48, half of all parcels by 12:36, 83% by 14:00; 12.3 truck hours, 17 km, replanned |
| 1004 | 3 | moving | 600 m launch radius: 2 trucks, 42 stops; 91% delivered (0% by drone, 50 on the second pass), last at 15:48, half of all parcels by 12:36, 83% by 14:00; 12.3 truck hours, 17 km, replanned |
| 1004 | 4 | parked | 600 m launch radius: 2 trucks, 27 stops; 97% delivered (38% by drone, 43 on the second pass), last at 14:24, half of all parcels by 11:27, 97% by 14:00; 9.1 truck hours, 16 km, replanned |
| 1004 | 4 | moving | 600 m launch radius: 2 trucks, 24 stops; 97% delivered (42% by drone, 48 on the second pass), last at 13:27, half of all parcels by 11:21, 97% by 14:00; 8.3 truck hours, 17 km, replanned |
| 1005 | 0 | parked | 600 m launch radius: 2 trucks, 23 stops; 94% delivered (40% by drone, 41 on the second pass), last at 13:20, half of all parcels by 10:42, 94% by 14:00; 7.5 truck hours, 18 km, replanned |
| 1005 | 0 | moving | 600 m launch radius: 2 trucks, 21 stops; 95% delivered (41% by drone, 62 on the second pass), last at 13:44, half of all parcels by 11:05, 95% by 14:00; 7.6 truck hours, 17 km, replanned |
| 1005 | 1 | parked | 600 m launch radius: 2 trucks, 27 stops; 97% delivered (45% by drone, 33 on the second pass), last at 13:12, half of all parcels by 11:19, 97% by 14:00; 7.8 truck hours, 16 km, replanned |
| 1005 | 1 | moving | 600 m launch radius: 2 trucks, 25 stops; 94% delivered (45% by drone, 31 on the second pass), last at 13:01, half of all parcels by 11:13, 94% by 14:00; 7.5 truck hours, 17 km, replanned |
| 1005 | 2 | parked | 600 m launch radius: 2 trucks, 21 stops; 95% delivered (37% by drone, 59 on the second pass), last at 14:17, half of all parcels by 11:18, 93% by 14:00; 8.8 truck hours, 18 km, replanned |
| 1005 | 2 | moving | 600 m launch radius: 2 trucks, 20 stops; 97% delivered (42% by drone, 52 on the second pass), last at 13:48, half of all parcels by 10:33, 97% by 14:00; 8.3 truck hours, 18 km, replanned |
| 1005 | 3 | parked | 600 m launch radius: 2 trucks, 23 stops; 96% delivered (41% by drone, 63 on the second pass), last at 13:41, half of all parcels by 11:24, 96% by 14:00; 8.4 truck hours, 18 km, replanned |
| 1005 | 3 | moving | 600 m launch radius: 2 trucks, 22 stops; 96% delivered (41% by drone, 46 on the second pass), last at 13:37, half of all parcels by 11:11, 96% by 14:00; 8.3 truck hours, 18 km, replanned |
| 1005 | 4 | parked | 600 m launch radius: 2 trucks, 18 stops; 97% delivered (43% by drone, 62 on the second pass), last at 13:12, half of all parcels by 10:55, 97% by 14:00; 7.0 truck hours, 16 km, replanned |
| 1005 | 4 | moving | 600 m launch radius: 2 trucks, 18 stops; 95% delivered (39% by drone, 76 on the second pass), last at 13:23, half of all parcels by 10:55, 95% by 14:00; 7.3 truck hours, 16 km, replanned |
| 1006 | 0 | parked | 600 m launch radius: 2 trucks, 18 stops; 99% delivered (49% by drone, 49 on the second pass), last at 13:01, half of all parcels by 11:03, 99% by 14:00; 7.2 truck hours, 14 km, replanned |
| 1006 | 0 | moving | 600 m launch radius: 2 trucks, 18 stops; 99% delivered (48% by drone, 42 on the second pass), last at 13:03, half of all parcels by 10:36, 99% by 14:00; 6.9 truck hours, 15 km, replanned |
| 1006 | 1 | parked | 600 m launch radius: 2 trucks, 20 stops; 99% delivered (52% by drone, 44 on the second pass), last at 13:27, half of all parcels by 10:47, 99% by 14:00; 8.0 truck hours, 17 km, replanned |
| 1006 | 1 | moving | 600 m launch radius: 2 trucks, 21 stops; 99% delivered (51% by drone, 46 on the second pass), last at 13:33, half of all parcels by 10:56, 99% by 14:00; 8.1 truck hours, 16 km, replanned |
| 1006 | 2 | parked | 600 m launch radius: 2 trucks, 29 stops; 82% delivered (13% by drone, 35 on the second pass), last at 13:59, half of all parcels by 11:55, 82% by 14:00; 9.2 truck hours, 18 km, replanned |
| 1006 | 2 | moving | 600 m launch radius: 2 trucks, 30 stops; 84% delivered (15% by drone, 35 on the second pass), last at 14:23, half of all parcels by 11:14, 82% by 14:00; 9.3 truck hours, 16 km, replanned |
| 1006 | 3 | parked | 600 m launch radius: 2 trucks, 20 stops; 98% delivered (48% by drone, 33 on the second pass), last at 12:57, half of all parcels by 11:03, 98% by 14:00; 7.1 truck hours, 14 km, replanned |
| 1006 | 3 | moving | 600 m launch radius: 2 trucks, 21 stops; 98% delivered (48% by drone, 30 on the second pass), last at 13:15, half of all parcels by 10:52, 98% by 14:00; 7.6 truck hours, 14 km, replanned |
| 1006 | 4 | parked | 600 m launch radius: 2 trucks, 22 stops; 97% delivered (44% by drone, 49 on the second pass), last at 13:06, half of all parcels by 11:03, 97% by 14:00; 7.6 truck hours, 14 km, replanned |
| 1006 | 4 | moving | 600 m launch radius: 2 trucks, 19 stops; 98% delivered (48% by drone, 44 on the second pass), last at 13:04, half of all parcels by 10:48, 98% by 14:00; 6.8 truck hours, 14 km, replanned |
| 1007 | 0 | parked | 600 m launch radius: 2 trucks, 28 stops; 94% delivered (47% by drone, 63 on the second pass), last at 14:29, half of all parcels by 11:04, 92% by 14:00; 9.7 truck hours, 17 km, replanned |
| 1007 | 0 | moving | 600 m launch radius: 2 trucks, 27 stops; 94% delivered (49% by drone, 54 on the second pass), last at 14:38, half of all parcels by 10:55, 87% by 14:00; 9.5 truck hours, 18 km, replanned |
| 1007 | 1 | parked | 600 m launch radius: 2 trucks, 17 stops; 94% delivered (44% by drone, 48 on the second pass), last at 13:12, half of all parcels by 10:52, 94% by 14:00; 7.5 truck hours, 16 km, replanned |
| 1007 | 1 | moving | 600 m launch radius: 2 trucks, 17 stops; 95% delivered (46% by drone, 47 on the second pass), last at 13:03, half of all parcels by 10:43, 95% by 14:00; 7.4 truck hours, 16 km, replanned |
| 1007 | 2 | parked | 600 m launch radius: 2 trucks, 20 stops; 95% delivered (40% by drone, 43 on the second pass), last at 13:11, half of all parcels by 11:16, 95% by 14:00; 7.6 truck hours, 17 km, replanned |
| 1007 | 2 | moving | 600 m launch radius: 2 trucks, 19 stops; 97% delivered (41% by drone, 44 on the second pass), last at 12:43, half of all parcels by 10:41, 97% by 14:00; 7.1 truck hours, 16 km, replanned |
| 1007 | 3 | parked | 600 m launch radius: 2 trucks, 19 stops; 97% delivered (50% by drone, 52 on the second pass), last at 13:04, half of all parcels by 11:05, 97% by 14:00; 7.4 truck hours, 16 km, replanned |
| 1007 | 3 | moving | 600 m launch radius: 2 trucks, 20 stops; 97% delivered (50% by drone, 48 on the second pass), last at 13:36, half of all parcels by 10:39, 97% by 14:00; 7.9 truck hours, 16 km, replanned |
| 1007 | 4 | parked | 600 m launch radius: 2 trucks, 21 stops; 97% delivered (44% by drone, 49 on the second pass), last at 13:00, half of all parcels by 11:15, 97% by 14:00; 8.5 truck hours, 18 km, replanned |
| 1007 | 4 | moving | 600 m launch radius: 2 trucks, 21 stops; 97% delivered (44% by drone, 54 on the second pass), last at 13:41, half of all parcels by 10:53, 97% by 14:00; 8.5 truck hours, 17 km, replanned |
| 1008 | 0 | parked | 600 m launch radius: 2 trucks, 21 stops; 97% delivered (46% by drone, 54 on the second pass), last at 13:55, half of all parcels by 11:14, 97% by 14:00; 8.4 truck hours, 17 km, replanned |
| 1008 | 0 | moving | 600 m launch radius: 2 trucks, 20 stops; 97% delivered (47% by drone, 52 on the second pass), last at 13:27, half of all parcels by 11:01, 97% by 14:00; 8.2 truck hours, 17 km, replanned |
| 1008 | 1 | parked | 600 m launch radius: 2 trucks, 19 stops; 98% delivered (55% by drone, 50 on the second pass), last at 13:15, half of all parcels by 10:57, 98% by 14:00; 6.9 truck hours, 14 km, replanned |
| 1008 | 1 | moving | 600 m launch radius: 2 trucks, 20 stops; 96% delivered (56% by drone, 37 on the second pass), last at 13:05, half of all parcels by 10:51, 96% by 14:00; 7.4 truck hours, 16 km, replanned |
| 1008 | 2 | parked | 600 m launch radius: 2 trucks, 37 stops; 98% delivered (15% by drone, 83 on the second pass), last at 14:16, half of all parcels by 11:55, 95% by 14:00; 10.2 truck hours, 19 km, replanned |
| 1008 | 2 | moving | 600 m launch radius: 2 trucks, 33 stops; 96% delivered (20% by drone, 59 on the second pass), last at 14:16, half of all parcels by 11:50, 93% by 14:00; 9.5 truck hours, 17 km, replanned |
| 1008 | 3 | parked | 600 m launch radius: 2 trucks, 23 stops; 98% delivered (47% by drone, 44 on the second pass), last at 13:23, half of all parcels by 11:14, 98% by 14:00; 7.8 truck hours, 17 km, replanned |
| 1008 | 3 | moving | 600 m launch radius: 2 trucks, 21 stops; 98% delivered (49% by drone, 49 on the second pass), last at 13:13, half of all parcels by 11:14, 98% by 14:00; 7.5 truck hours, 17 km, replanned |
| 1008 | 4 | parked | 600 m launch radius: 2 trucks, 24 stops; 96% delivered (48% by drone, 24 on the second pass), last at 13:28, half of all parcels by 11:36, 96% by 14:00; 7.6 truck hours, 16 km, replanned |
| 1008 | 4 | moving | 600 m launch radius: 2 trucks, 21 stops; 95% delivered (51% by drone, 33 on the second pass), last at 13:16, half of all parcels by 11:04, 95% by 14:00; 7.8 truck hours, 16 km, replanned |
| 1009 | 0 | parked | 600 m launch radius: 2 trucks, 32 stops; 91% delivered (0% by drone, 26 on the second pass), last at 14:27, half of all parcels by 11:46, 90% by 14:00; 10.0 truck hours, 17 km, replanned |
| 1009 | 0 | moving | 600 m launch radius: 2 trucks, 32 stops; 91% delivered (0% by drone, 26 on the second pass), last at 14:27, half of all parcels by 11:46, 90% by 14:00; 10.0 truck hours, 17 km, replanned |
| 1009 | 1 | parked | 600 m launch radius: 2 trucks, 17 stops; 99% delivered (44% by drone, 36 on the second pass), last at 13:09, half of all parcels by 10:45, 99% by 14:00; 7.4 truck hours, 15 km, replanned |
| 1009 | 1 | moving | 600 m launch radius: 2 trucks, 20 stops; 99% delivered (42% by drone, 48 on the second pass), last at 13:07, half of all parcels by 10:34, 99% by 14:00; 7.6 truck hours, 17 km, replanned |
| 1009 | 2 | parked | 600 m launch radius: 2 trucks, 18 stops; 97% delivered (52% by drone, 58 on the second pass), last at 13:03, half of all parcels by 10:42, 97% by 14:00; 6.9 truck hours, 15 km, replanned |
| 1009 | 2 | moving | 600 m launch radius: 2 trucks, 17 stops; 98% delivered (53% by drone, 46 on the second pass), last at 12:46, half of all parcels by 10:32, 98% by 14:00; 6.7 truck hours, 14 km, replanned |
| 1009 | 3 | parked | 600 m launch radius: 2 trucks, 21 stops; 97% delivered (35% by drone, 59 on the second pass), last at 13:35, half of all parcels by 10:34, 97% by 14:00; 8.8 truck hours, 16 km, replanned |
| 1009 | 3 | moving | 600 m launch radius: 2 trucks, 13 stops; 97% delivered (40% by drone, 50 on the second pass), last at 13:09, half of all parcels by 10:37, 97% by 14:00; 7.1 truck hours, 17 km, replanned |
| 1009 | 4 | parked | 600 m launch radius: 2 trucks, 35 stops; 92% delivered (0% by drone, 37 on the second pass), last at 14:32, half of all parcels by 11:34, 86% by 14:00; 10.2 truck hours, 19 km, replanned |
| 1009 | 4 | moving | 600 m launch radius: 2 trucks, 35 stops; 92% delivered (0% by drone, 37 on the second pass), last at 14:32, half of all parcels by 11:34, 86% by 14:00; 10.2 truck hours, 19 km, replanned |
