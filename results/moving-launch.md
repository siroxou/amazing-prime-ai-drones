# Launching from a moving truck

Written by `python -m baselines.moving --held-out`. 50 days, 500 parcels each, averages over the days. Both columns use the classical solver's plan (600 m launch radius, 10-minute locker wait, drones on the cost model in sim/drone.py). Parked: the truck waits at each stop until its drones are back. Moving: it only waits for the locker, and the drones launch from it and land on it as it drives, with the battery set by the drone cost model.

| | parked launches | moving launches |
|---|---|---|
| trucks | 2.0 | 2.0 |
| stops | 24 | 23 |
| parcels delivered today | 86% | 87% |
| by drone | 36% | 38% |
| last parcel | 12:04 | 11:58 |
| half of all parcels by | 11:10 | 11:01 |
| delivered by 14:00 | 86% | 87% |
| truck hours | 5.3 | 5.1 |
| km driven | 10 | 10 |

## What it shows

Launching from a moving truck changes the day by only a few minutes, either way. The trucks spend most of their day parked at locker pickup points: every drone parcel is already within the launch radius of one, so there are no stops just for launching. Each truck waits about 10 minutes at each of its 10 or so points, with short drives between. A drone's flight is a few minutes, so it's usually back while the truck is still there. When the truck doesn't wait for its drones, it leaves sooner, but the drones then have further to fly to catch it and are busy for longer, so the two roughly cancel out.

In this city the locker wait, not the drones, is what holds the trucks up. Moving launches should matter more where trucks drive further between stops: bigger cities, fewer locker parcels, or shorter locker waits.

## Every day

| city | day | launches | result |
|---|---|---|---|
| 1000 | 0 | parked | 600 m launch radius: 2 trucks, 40 stops; 82% delivered (0% by drone), last at 13:26, half of all parcels by 11:25, 82% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1000 | 0 | moving | 600 m launch radius: 2 trucks, 40 stops; 82% delivered (0% by drone), last at 13:26, half of all parcels by 11:25, 82% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1000 | 1 | parked | 600 m launch radius: 2 trucks, 17 stops; 88% delivered (47% by drone), last at 11:31, half of all parcels by 10:53, 88% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1000 | 1 | moving | 600 m launch radius: 2 trucks, 17 stops; 87% delivered (48% by drone), last at 11:28, half of all parcels by 10:59, 87% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1000 | 2 | parked | 600 m launch radius: 2 trucks, 20 stops; 85% delivered (39% by drone), last at 11:44, half of all parcels by 11:06, 85% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1000 | 2 | moving | 600 m launch radius: 2 trucks, 21 stops; 86% delivered (39% by drone), last at 11:51, half of all parcels by 11:03, 86% by 14:00; 4.8 truck hours, 11 km, replanned |
| 1000 | 3 | parked | 600 m launch radius: 2 trucks, 14 stops; 83% delivered (45% by drone), last at 11:15, half of all parcels by 10:35, 83% by 14:00; 3.6 truck hours, 9 km, replanned |
| 1000 | 3 | moving | 600 m launch radius: 2 trucks, 15 stops; 88% delivered (52% by drone), last at 11:15, half of all parcels by 10:36, 88% by 14:00; 3.7 truck hours, 8 km, replanned |
| 1000 | 4 | parked | 600 m launch radius: 2 trucks, 25 stops; 88% delivered (36% by drone), last at 12:06, half of all parcels by 11:26, 88% by 14:00; 5.4 truck hours, 10 km, replanned |
| 1000 | 4 | moving | 600 m launch radius: 2 trucks, 21 stops; 86% delivered (39% by drone), last at 11:46, half of all parcels by 11:09, 86% by 14:00; 4.7 truck hours, 9 km, replanned |
| 1001 | 0 | parked | 600 m launch radius: 2 trucks, 20 stops; 92% delivered (47% by drone), last at 11:38, half of all parcels by 10:42, 92% by 14:00; 4.6 truck hours, 8 km, replanned |
| 1001 | 0 | moving | 600 m launch radius: 2 trucks, 19 stops; 91% delivered (51% by drone), last at 11:36, half of all parcels by 10:53, 91% by 14:00; 4.4 truck hours, 7 km, replanned |
| 1001 | 1 | parked | 600 m launch radius: 2 trucks, 22 stops; 88% delivered (46% by drone), last at 11:52, half of all parcels by 11:02, 88% by 14:00; 4.8 truck hours, 10 km, replanned |
| 1001 | 1 | moving | 600 m launch radius: 2 trucks, 19 stops; 90% delivered (51% by drone), last at 11:35, half of all parcels by 11:06, 90% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1001 | 2 | parked | 600 m launch radius: 2 trucks, 22 stops; 89% delivered (50% by drone), last at 11:58, half of all parcels by 11:06, 89% by 14:00; 5.0 truck hours, 10 km, replanned |
| 1001 | 2 | moving | 600 m launch radius: 2 trucks, 23 stops; 90% delivered (51% by drone), last at 12:01, half of all parcels by 11:01, 90% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1001 | 3 | parked | 600 m launch radius: 2 trucks, 23 stops; 92% delivered (45% by drone), last at 12:02, half of all parcels by 11:24, 92% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1001 | 3 | moving | 600 m launch radius: 2 trucks, 23 stops; 92% delivered (45% by drone), last at 11:55, half of all parcels by 11:12, 92% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1001 | 4 | parked | 600 m launch radius: 2 trucks, 19 stops; 91% delivered (41% by drone), last at 11:42, half of all parcels by 10:56, 91% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1001 | 4 | moving | 600 m launch radius: 2 trucks, 20 stops; 92% delivered (46% by drone), last at 11:43, half of all parcels by 10:44, 92% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1002 | 0 | parked | 600 m launch radius: 2 trucks, 20 stops; 88% delivered (39% by drone), last at 11:45, half of all parcels by 11:16, 88% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1002 | 0 | moving | 600 m launch radius: 2 trucks, 17 stops; 86% delivered (41% by drone), last at 11:27, half of all parcels by 10:39, 86% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1002 | 1 | parked | 600 m launch radius: 2 trucks, 22 stops; 88% delivered (39% by drone), last at 11:53, half of all parcels by 10:44, 88% by 14:00; 4.9 truck hours, 10 km, replanned |
| 1002 | 1 | moving | 600 m launch radius: 2 trucks, 23 stops; 87% delivered (41% by drone), last at 11:57, half of all parcels by 10:43, 87% by 14:00; 4.9 truck hours, 9 km, replanned |
| 1002 | 2 | parked | 600 m launch radius: 2 trucks, 23 stops; 89% delivered (43% by drone), last at 12:01, half of all parcels by 11:03, 89% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1002 | 2 | moving | 600 m launch radius: 2 trucks, 23 stops; 88% delivered (44% by drone), last at 11:59, half of all parcels by 10:52, 88% by 14:00; 5.1 truck hours, 9 km, replanned |
| 1002 | 3 | parked | 600 m launch radius: 2 trucks, 40 stops; 84% delivered (0% by drone), last at 13:28, half of all parcels by 11:57, 84% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1002 | 3 | moving | 600 m launch radius: 2 trucks, 40 stops; 84% delivered (0% by drone), last at 13:22, half of all parcels by 11:44, 84% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1002 | 4 | parked | 600 m launch radius: 2 trucks, 17 stops; 80% delivered (36% by drone), last at 11:26, half of all parcels by 10:52, 80% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1002 | 4 | moving | 600 m launch radius: 2 trucks, 17 stops; 85% delivered (41% by drone), last at 11:27, half of all parcels by 10:42, 85% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1003 | 0 | parked | 600 m launch radius: 2 trucks, 39 stops; 83% delivered (0% by drone), last at 13:27, half of all parcels by 11:03, 83% by 14:00; 7.8 truck hours, 12 km, replanned |
| 1003 | 0 | moving | 600 m launch radius: 2 trucks, 39 stops; 83% delivered (0% by drone), last at 13:27, half of all parcels by 11:09, 83% by 14:00; 7.8 truck hours, 12 km, replanned |
| 1003 | 1 | parked | 600 m launch radius: 2 trucks, 27 stops; 88% delivered (49% by drone), last at 12:17, half of all parcels by 10:54, 88% by 14:00; 5.7 truck hours, 10 km, replanned |
| 1003 | 1 | moving | 600 m launch radius: 2 trucks, 25 stops; 88% delivered (50% by drone), last at 12:12, half of all parcels by 11:04, 88% by 14:00; 5.5 truck hours, 10 km, replanned |
| 1003 | 2 | parked | 600 m launch radius: 2 trucks, 24 stops; 83% delivered (29% by drone), last at 12:06, half of all parcels by 11:16, 83% by 14:00; 5.3 truck hours, 10 km, replanned |
| 1003 | 2 | moving | 600 m launch radius: 2 trucks, 20 stops; 82% delivered (37% by drone), last at 11:39, half of all parcels by 11:10, 82% by 14:00; 4.6 truck hours, 10 km, replanned |
| 1003 | 3 | parked | 600 m launch radius: 2 trucks, 24 stops; 88% delivered (39% by drone), last at 12:01, half of all parcels by 11:09, 88% by 14:00; 5.2 truck hours, 9 km, replanned |
| 1003 | 3 | moving | 600 m launch radius: 2 trucks, 19 stops; 89% delivered (43% by drone), last at 11:43, half of all parcels by 10:50, 89% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1003 | 4 | parked | 600 m launch radius: 2 trucks, 26 stops; 89% delivered (44% by drone), last at 12:15, half of all parcels by 10:45, 89% by 14:00; 5.6 truck hours, 11 km, replanned |
| 1003 | 4 | moving | 600 m launch radius: 2 trucks, 20 stops; 82% delivered (43% by drone), last at 11:42, half of all parcels by 10:54, 82% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1004 | 0 | parked | 600 m launch radius: 2 trucks, 23 stops; 81% delivered (29% by drone), last at 11:57, half of all parcels by 10:56, 81% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1004 | 0 | moving | 600 m launch radius: 2 trucks, 20 stops; 86% delivered (39% by drone), last at 11:37, half of all parcels by 10:32, 86% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1004 | 1 | parked | 600 m launch radius: 2 trucks, 22 stops; 86% delivered (36% by drone), last at 11:56, half of all parcels by 11:16, 86% by 14:00; 4.9 truck hours, 10 km, replanned |
| 1004 | 1 | moving | 600 m launch radius: 2 trucks, 22 stops; 85% delivered (37% by drone), last at 11:52, half of all parcels by 10:42, 85% by 14:00; 4.9 truck hours, 10 km, replanned |
| 1004 | 2 | parked | 600 m launch radius: 2 trucks, 27 stops; 88% delivered (42% by drone), last at 12:18, half of all parcels by 11:03, 88% by 14:00; 5.8 truck hours, 11 km, replanned |
| 1004 | 2 | moving | 600 m launch radius: 2 trucks, 25 stops; 87% delivered (42% by drone), last at 12:06, half of all parcels by 11:23, 87% by 14:00; 5.4 truck hours, 9 km, replanned |
| 1004 | 3 | parked | 600 m launch radius: 2 trucks, 42 stops; 81% delivered (0% by drone), last at 13:32, half of all parcels by 12:36, 81% by 14:00; 8.3 truck hours, 11 km, replanned |
| 1004 | 3 | moving | 600 m launch radius: 2 trucks, 42 stops; 81% delivered (0% by drone), last at 13:32, half of all parcels by 12:36, 81% by 14:00; 8.3 truck hours, 11 km, replanned |
| 1004 | 4 | parked | 600 m launch radius: 2 trucks, 27 stops; 89% delivered (36% by drone), last at 12:16, half of all parcels by 11:27, 89% by 14:00; 5.8 truck hours, 10 km, replanned |
| 1004 | 4 | moving | 600 m launch radius: 2 trucks, 24 stops; 88% delivered (39% by drone), last at 12:01, half of all parcels by 11:21, 88% by 14:00; 5.3 truck hours, 10 km, replanned |
| 1005 | 0 | parked | 600 m launch radius: 2 trucks, 23 stops; 86% delivered (39% by drone), last at 11:57, half of all parcels by 10:42, 86% by 14:00; 5.2 truck hours, 12 km, replanned |
| 1005 | 0 | moving | 600 m launch radius: 2 trucks, 21 stops; 83% delivered (36% by drone), last at 11:47, half of all parcels by 11:05, 83% by 14:00; 4.8 truck hours, 11 km, replanned |
| 1005 | 1 | parked | 600 m launch radius: 2 trucks, 27 stops; 90% delivered (44% by drone), last at 12:24, half of all parcels by 11:19, 90% by 14:00; 5.8 truck hours, 10 km, replanned |
| 1005 | 1 | moving | 600 m launch radius: 2 trucks, 25 stops; 88% delivered (44% by drone), last at 12:11, half of all parcels by 11:13, 88% by 14:00; 5.5 truck hours, 11 km, replanned |
| 1005 | 2 | parked | 600 m launch radius: 2 trucks, 21 stops; 83% delivered (34% by drone), last at 11:53, half of all parcels by 11:18, 83% by 14:00; 4.8 truck hours, 11 km, replanned |
| 1005 | 2 | moving | 600 m launch radius: 2 trucks, 20 stops; 87% delivered (40% by drone), last at 11:44, half of all parcels by 10:33, 87% by 14:00; 4.6 truck hours, 10 km, replanned |
| 1005 | 3 | parked | 600 m launch radius: 2 trucks, 23 stops; 84% delivered (36% by drone), last at 12:02, half of all parcels by 11:24, 84% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1005 | 3 | moving | 600 m launch radius: 2 trucks, 22 stops; 87% delivered (40% by drone), last at 11:53, half of all parcels by 11:11, 87% by 14:00; 4.9 truck hours, 10 km, replanned |
| 1005 | 4 | parked | 600 m launch radius: 2 trucks, 18 stops; 85% delivered (39% by drone), last at 11:34, half of all parcels by 10:55, 85% by 14:00; 4.2 truck hours, 9 km, replanned |
| 1005 | 4 | moving | 600 m launch radius: 2 trucks, 18 stops; 80% delivered (32% by drone), last at 11:30, half of all parcels by 10:55, 80% by 14:00; 4.2 truck hours, 9 km, replanned |
| 1006 | 0 | parked | 600 m launch radius: 2 trucks, 18 stops; 90% delivered (47% by drone), last at 11:37, half of all parcels by 11:03, 90% by 14:00; 4.3 truck hours, 8 km, replanned |
| 1006 | 0 | moving | 600 m launch radius: 2 trucks, 18 stops; 91% delivered (48% by drone), last at 11:35, half of all parcels by 10:36, 91% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1006 | 1 | parked | 600 m launch radius: 2 trucks, 20 stops; 90% delivered (52% by drone), last at 11:43, half of all parcels by 10:47, 90% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1006 | 1 | moving | 600 m launch radius: 2 trucks, 21 stops; 89% delivered (50% by drone), last at 11:51, half of all parcels by 10:56, 89% by 14:00; 4.8 truck hours, 10 km, replanned |
| 1006 | 2 | parked | 600 m launch radius: 2 trucks, 29 stops; 75% delivered (13% by drone), last at 12:31, half of all parcels by 11:55, 75% by 14:00; 6.2 truck hours, 11 km, replanned |
| 1006 | 2 | moving | 600 m launch radius: 2 trucks, 30 stops; 77% delivered (15% by drone), last at 12:38, half of all parcels by 11:14, 77% by 14:00; 6.3 truck hours, 10 km, replanned |
| 1006 | 3 | parked | 600 m launch radius: 2 trucks, 20 stops; 92% delivered (47% by drone), last at 11:43, half of all parcels by 11:03, 92% by 14:00; 4.4 truck hours, 8 km, replanned |
| 1006 | 3 | moving | 600 m launch radius: 2 trucks, 21 stops; 92% delivered (47% by drone), last at 11:45, half of all parcels by 10:52, 92% by 14:00; 4.6 truck hours, 8 km, replanned |
| 1006 | 4 | parked | 600 m launch radius: 2 trucks, 22 stops; 88% delivered (41% by drone), last at 11:56, half of all parcels by 11:03, 88% by 14:00; 4.9 truck hours, 9 km, replanned |
| 1006 | 4 | moving | 600 m launch radius: 2 trucks, 19 stops; 89% delivered (46% by drone), last at 11:35, half of all parcels by 10:48, 89% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1007 | 0 | parked | 600 m launch radius: 2 trucks, 28 stops; 81% delivered (41% by drone), last at 12:27, half of all parcels by 11:04, 81% by 14:00; 6.0 truck hours, 11 km, replanned |
| 1007 | 0 | moving | 600 m launch radius: 2 trucks, 27 stops; 83% delivered (45% by drone), last at 12:25, half of all parcels by 10:55, 83% by 14:00; 5.8 truck hours, 11 km, replanned |
| 1007 | 1 | parked | 600 m launch radius: 2 trucks, 17 stops; 85% delivered (43% by drone), last at 11:30, half of all parcels by 10:52, 85% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1007 | 1 | moving | 600 m launch radius: 2 trucks, 17 stops; 86% delivered (46% by drone), last at 11:32, half of all parcels by 10:43, 86% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1007 | 2 | parked | 600 m launch radius: 2 trucks, 20 stops; 87% delivered (38% by drone), last at 11:46, half of all parcels by 11:16, 87% by 14:00; 4.6 truck hours, 10 km, replanned |
| 1007 | 2 | moving | 600 m launch radius: 2 trucks, 19 stops; 88% delivered (39% by drone), last at 11:41, half of all parcels by 10:41, 88% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1007 | 3 | parked | 600 m launch radius: 2 trucks, 19 stops; 87% delivered (47% by drone), last at 11:38, half of all parcels by 11:05, 87% by 14:00; 4.4 truck hours, 10 km, replanned |
| 1007 | 3 | moving | 600 m launch radius: 2 trucks, 20 stops; 87% delivered (48% by drone), last at 11:45, half of all parcels by 10:39, 87% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1007 | 4 | parked | 600 m launch radius: 2 trucks, 21 stops; 87% delivered (43% by drone), last at 11:51, half of all parcels by 11:15, 87% by 14:00; 4.8 truck hours, 11 km, replanned |
| 1007 | 4 | moving | 600 m launch radius: 2 trucks, 21 stops; 86% delivered (42% by drone), last at 11:46, half of all parcels by 10:53, 86% by 14:00; 4.8 truck hours, 10 km, replanned |
| 1008 | 0 | parked | 600 m launch radius: 2 trucks, 21 stops; 86% delivered (46% by drone), last at 11:49, half of all parcels by 11:14, 86% by 14:00; 4.7 truck hours, 10 km, replanned |
| 1008 | 0 | moving | 600 m launch radius: 2 trucks, 20 stops; 87% delivered (47% by drone), last at 11:39, half of all parcels by 11:01, 87% by 14:00; 4.6 truck hours, 10 km, replanned |
| 1008 | 1 | parked | 600 m launch radius: 2 trucks, 19 stops; 88% delivered (50% by drone), last at 11:36, half of all parcels by 10:57, 88% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1008 | 1 | moving | 600 m launch radius: 2 trucks, 20 stops; 89% delivered (53% by drone), last at 11:39, half of all parcels by 10:51, 89% by 14:00; 4.4 truck hours, 10 km, replanned |
| 1008 | 2 | parked | 600 m launch radius: 2 trucks, 37 stops; 82% delivered (7% by drone), last at 13:14, half of all parcels by 11:55, 82% by 14:00; 7.5 truck hours, 13 km, replanned |
| 1008 | 2 | moving | 600 m launch radius: 2 trucks, 33 stops; 84% delivered (17% by drone), last at 12:50, half of all parcels by 11:50, 84% by 14:00; 6.8 truck hours, 12 km, replanned |
| 1008 | 3 | parked | 600 m launch radius: 2 trucks, 23 stops; 89% delivered (47% by drone), last at 11:58, half of all parcels by 11:14, 89% by 14:00; 5.1 truck hours, 11 km, replanned |
| 1008 | 3 | moving | 600 m launch radius: 2 trucks, 21 stops; 88% delivered (48% by drone), last at 11:47, half of all parcels by 11:14, 88% by 14:00; 4.8 truck hours, 11 km, replanned |
| 1008 | 4 | parked | 600 m launch radius: 2 trucks, 24 stops; 91% delivered (47% by drone), last at 12:06, half of all parcels by 11:36, 91% by 14:00; 5.3 truck hours, 10 km, replanned |
| 1008 | 4 | moving | 600 m launch radius: 2 trucks, 21 stops; 89% delivered (48% by drone), last at 11:46, half of all parcels by 11:04, 89% by 14:00; 4.8 truck hours, 9 km, replanned |
| 1009 | 0 | parked | 600 m launch radius: 2 trucks, 32 stops; 86% delivered (0% by drone), last at 12:45, half of all parcels by 11:46, 86% by 14:00; 6.6 truck hours, 10 km, replanned |
| 1009 | 0 | moving | 600 m launch radius: 2 trucks, 32 stops; 86% delivered (0% by drone), last at 12:45, half of all parcels by 11:46, 86% by 14:00; 6.6 truck hours, 10 km, replanned |
| 1009 | 1 | parked | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (44% by drone), last at 11:28, half of all parcels by 10:45, 91% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1009 | 1 | moving | 600 m launch radius: 2 trucks, 20 stops; 89% delivered (39% by drone), last at 11:41, half of all parcels by 10:34, 89% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1009 | 2 | parked | 600 m launch radius: 2 trucks, 18 stops; 86% delivered (48% by drone), last at 11:30, half of all parcels by 10:42, 86% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1009 | 2 | moving | 600 m launch radius: 2 trucks, 17 stops; 89% delivered (52% by drone), last at 11:28, half of all parcels by 10:32, 89% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1009 | 3 | parked | 600 m launch radius: 2 trucks, 21 stops; 85% delivered (32% by drone), last at 11:50, half of all parcels by 10:34, 85% by 14:00; 4.8 truck hours, 9 km, replanned |
| 1009 | 3 | moving | 600 m launch radius: 2 trucks, 13 stops; 87% delivered (40% by drone), last at 11:09, half of all parcels by 10:37, 87% by 14:00; 3.4 truck hours, 9 km, replanned |
| 1009 | 4 | parked | 600 m launch radius: 2 trucks, 35 stops; 85% delivered (0% by drone), last at 13:03, half of all parcels by 11:34, 85% by 14:00; 7.2 truck hours, 12 km, replanned |
| 1009 | 4 | moving | 600 m launch radius: 2 trucks, 35 stops; 85% delivered (0% by drone), last at 13:03, half of all parcels by 11:34, 85% by 14:00; 7.2 truck hours, 12 km, replanned |
