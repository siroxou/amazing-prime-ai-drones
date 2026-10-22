# Classical truck + drone solver on the held-out days

Written by `python -m baselines.classical --held-out`. 50 days, 500 parcels each, averages over the days. Autonomous trucks with 10 drones and a locker each; a drone cost model (sim/drone.py: wind, payload, battery, flight heights, drop planning; up to 5 kg). Locker settings as in [trucks-only-baseline.md](trucks-only-baseline.md) with a 10-minute wait. Each truck then goes out again in the afternoon with what it couldn't deliver (20-minute wait). Settings are in `baselines/classical.py`.

| launch radius | 300 m | 600 m | 1000 m |
|---|---|---|---|
| trucks | 2.0 | 2.0 | 2.0 |
| stops | 25 | 24 | 24 |
| parcels delivered today | 96% | 96% | 96% |
| delivered on the afternoon second pass | 9% | 9% | 9% |
| by drone | 40% | 38% | 38% |
| last parcel | 13:32 | 13:39 | 13:37 |
| half of all parcels by | 11:02 | 11:10 | 11:09 |
| delivered by 14:00 | 96% | 95% | 95% |
| truck hours | 8.2 | 8.3 | 8.3 |
| km driven | 18 | 16 | 16 |
| days replanned for weather or airspace | 100% | 100% | 100% |

## Every day

| city | day | result |
|---|---|---|
| 1000 | 0 | 300 m launch radius: 2 trucks, 40 stops; 90% delivered (0% by drone, 43 on the second pass), last at 15:17, half of all parcels by 11:25, 84% by 14:00; 11.4 truck hours, 22 km, replanned |
| 1000 | 0 | 600 m launch radius: 2 trucks, 40 stops; 90% delivered (0% by drone, 43 on the second pass), last at 15:09, half of all parcels by 11:25, 82% by 14:00; 11.2 truck hours, 19 km, replanned |
| 1000 | 0 | 1000 m launch radius: 2 trucks, 40 stops; 90% delivered (0% by drone, 43 on the second pass), last at 14:49, half of all parcels by 11:25, 84% by 14:00; 11.0 truck hours, 18 km, replanned |
| 1000 | 1 | 300 m launch radius: 2 trucks, 21 stops; 98% delivered (51% by drone, 44 on the second pass), last at 12:57, half of all parcels by 10:39, 98% by 14:00; 7.0 truck hours, 17 km, replanned |
| 1000 | 1 | 600 m launch radius: 2 trucks, 17 stops; 98% delivered (49% by drone, 49 on the second pass), last at 12:53, half of all parcels by 10:53, 98% by 14:00; 7.1 truck hours, 15 km, replanned |
| 1000 | 1 | 1000 m launch radius: 2 trucks, 17 stops; 98% delivered (49% by drone, 49 on the second pass), last at 12:53, half of all parcels by 10:53, 98% by 14:00; 7.0 truck hours, 14 km, replanned |
| 1000 | 2 | 300 m launch radius: 2 trucks, 21 stops; 98% delivered (46% by drone, 62 on the second pass), last at 12:47, half of all parcels by 10:57, 98% by 14:00; 6.8 truck hours, 17 km, replanned |
| 1000 | 2 | 600 m launch radius: 2 trucks, 20 stops; 97% delivered (41% by drone, 60 on the second pass), last at 12:55, half of all parcels by 11:06, 97% by 14:00; 7.3 truck hours, 16 km, replanned |
| 1000 | 2 | 1000 m launch radius: 2 trucks, 20 stops; 97% delivered (41% by drone, 60 on the second pass), last at 12:52, half of all parcels by 11:06, 97% by 14:00; 7.2 truck hours, 15 km, replanned |
| 1000 | 3 | 300 m launch radius: 2 trucks, 17 stops; 93% delivered (49% by drone, 55 on the second pass), last at 12:25, half of all parcels by 10:57, 93% by 14:00; 6.2 truck hours, 18 km, replanned |
| 1000 | 3 | 600 m launch radius: 2 trucks, 14 stops; 91% delivered (46% by drone, 38 on the second pass), last at 12:18, half of all parcels by 10:35, 91% by 14:00; 5.9 truck hours, 17 km, replanned |
| 1000 | 3 | 1000 m launch radius: 2 trucks, 14 stops; 91% delivered (46% by drone, 38 on the second pass), last at 12:18, half of all parcels by 10:35, 91% by 14:00; 5.9 truck hours, 17 km, replanned |
| 1000 | 4 | 300 m launch radius: 2 trucks, 26 stops; 99% delivered (41% by drone, 54 on the second pass), last at 13:12, half of all parcels by 11:10, 99% by 14:00; 7.7 truck hours, 17 km, replanned |
| 1000 | 4 | 600 m launch radius: 2 trucks, 25 stops; 97% delivered (38% by drone, 44 on the second pass), last at 13:37, half of all parcels by 11:26, 97% by 14:00; 8.1 truck hours, 16 km, replanned |
| 1000 | 4 | 1000 m launch radius: 2 trucks, 25 stops; 98% delivered (39% by drone, 49 on the second pass), last at 13:37, half of all parcels by 11:26, 98% by 14:00; 8.1 truck hours, 16 km, replanned |
| 1001 | 0 | 300 m launch radius: 2 trucks, 24 stops; 99% delivered (49% by drone, 33 on the second pass), last at 13:21, half of all parcels by 10:53, 99% by 14:00; 8.0 truck hours, 17 km, replanned |
| 1001 | 0 | 600 m launch radius: 2 trucks, 20 stops; 99% delivered (48% by drone, 38 on the second pass), last at 12:48, half of all parcels by 10:42, 99% by 14:00; 7.2 truck hours, 14 km, replanned |
| 1001 | 0 | 1000 m launch radius: 2 trucks, 20 stops; 99% delivered (48% by drone, 38 on the second pass), last at 12:48, half of all parcels by 10:42, 99% by 14:00; 7.2 truck hours, 14 km, replanned |
| 1001 | 1 | 300 m launch radius: 2 trucks, 25 stops; 99% delivered (49% by drone, 51 on the second pass), last at 13:08, half of all parcels by 10:54, 99% by 14:00; 7.4 truck hours, 19 km, replanned |
| 1001 | 1 | 600 m launch radius: 2 trucks, 22 stops; 99% delivered (49% by drone, 52 on the second pass), last at 12:47, half of all parcels by 11:02, 99% by 14:00; 6.7 truck hours, 15 km, replanned |
| 1001 | 1 | 1000 m launch radius: 2 trucks, 22 stops; 99% delivered (49% by drone, 52 on the second pass), last at 12:47, half of all parcels by 11:02, 99% by 14:00; 6.7 truck hours, 15 km, replanned |
| 1001 | 2 | 300 m launch radius: 2 trucks, 24 stops; 99% delivered (54% by drone, 44 on the second pass), last at 13:03, half of all parcels by 11:07, 99% by 14:00; 7.6 truck hours, 16 km, replanned |
| 1001 | 2 | 600 m launch radius: 2 trucks, 22 stops; 99% delivered (53% by drone, 49 on the second pass), last at 13:01, half of all parcels by 10:36, 99% by 14:00; 7.7 truck hours, 15 km, replanned |
| 1001 | 2 | 1000 m launch radius: 2 trucks, 22 stops; 99% delivered (53% by drone, 49 on the second pass), last at 13:01, half of all parcels by 10:36, 99% by 14:00; 7.6 truck hours, 15 km, replanned |
| 1001 | 3 | 300 m launch radius: 2 trucks, 22 stops; 100% delivered (46% by drone, 40 on the second pass), last at 13:58, half of all parcels by 10:56, 100% by 14:00; 8.3 truck hours, 16 km, replanned |
| 1001 | 3 | 600 m launch radius: 2 trucks, 23 stops; 99% delivered (45% by drone, 36 on the second pass), last at 14:53, half of all parcels by 11:24, 98% by 14:00; 9.1 truck hours, 17 km, replanned |
| 1001 | 3 | 1000 m launch radius: 2 trucks, 23 stops; 99% delivered (46% by drone, 38 on the second pass), last at 14:26, half of all parcels by 10:55, 96% by 14:00; 9.4 truck hours, 16 km, replanned |
| 1001 | 4 | 300 m launch radius: 2 trucks, 20 stops; 97% delivered (45% by drone, 24 on the second pass), last at 12:59, half of all parcels by 11:14, 97% by 14:00; 7.2 truck hours, 15 km, replanned |
| 1001 | 4 | 600 m launch radius: 2 trucks, 19 stops; 97% delivered (43% by drone, 31 on the second pass), last at 13:10, half of all parcels by 10:56, 97% by 14:00; 7.4 truck hours, 16 km, replanned |
| 1001 | 4 | 1000 m launch radius: 2 trucks, 19 stops; 97% delivered (43% by drone, 31 on the second pass), last at 13:10, half of all parcels by 10:56, 97% by 14:00; 7.4 truck hours, 15 km, replanned |
| 1002 | 0 | 300 m launch radius: 2 trucks, 21 stops; 98% delivered (47% by drone, 46 on the second pass), last at 12:33, half of all parcels by 11:05, 98% by 14:00; 6.3 truck hours, 18 km, replanned |
| 1002 | 0 | 600 m launch radius: 2 trucks, 20 stops; 96% delivered (40% by drone, 36 on the second pass), last at 12:27, half of all parcels by 11:16, 96% by 14:00; 6.2 truck hours, 13 km, replanned |
| 1002 | 0 | 1000 m launch radius: 2 trucks, 20 stops; 96% delivered (40% by drone, 36 on the second pass), last at 12:27, half of all parcels by 11:16, 96% by 14:00; 6.2 truck hours, 13 km, replanned |
| 1002 | 1 | 300 m launch radius: 2 trucks, 22 stops; 99% delivered (45% by drone, 62 on the second pass), last at 13:05, half of all parcels by 10:47, 99% by 14:00; 7.4 truck hours, 16 km, replanned |
| 1002 | 1 | 600 m launch radius: 2 trucks, 22 stops; 97% delivered (40% by drone, 45 on the second pass), last at 13:13, half of all parcels by 10:44, 97% by 14:00; 7.6 truck hours, 16 km, replanned |
| 1002 | 1 | 1000 m launch radius: 2 trucks, 22 stops; 97% delivered (40% by drone, 44 on the second pass), last at 13:04, half of all parcels by 10:44, 97% by 14:00; 7.6 truck hours, 14 km, replanned |
| 1002 | 2 | 300 m launch radius: 2 trucks, 24 stops; 99% delivered (46% by drone, 46 on the second pass), last at 14:31, half of all parcels by 11:07, 97% by 14:00; 9.4 truck hours, 20 km, replanned |
| 1002 | 2 | 600 m launch radius: 2 trucks, 23 stops; 98% delivered (45% by drone, 46 on the second pass), last at 14:32, half of all parcels by 11:03, 97% by 14:00; 9.8 truck hours, 17 km, replanned |
| 1002 | 2 | 1000 m launch radius: 2 trucks, 22 stops; 97% delivered (44% by drone, 44 on the second pass), last at 14:18, half of all parcels by 11:06, 96% by 14:00; 9.7 truck hours, 18 km, replanned |
| 1002 | 3 | 300 m launch radius: 2 trucks, 40 stops; 90% delivered (0% by drone, 31 on the second pass), last at 14:51, half of all parcels by 11:44, 84% by 14:00; 11.2 truck hours, 20 km, replanned |
| 1002 | 3 | 600 m launch radius: 2 trucks, 40 stops; 90% delivered (0% by drone, 31 on the second pass), last at 14:51, half of all parcels by 12:09, 84% by 14:00; 11.1 truck hours, 19 km, replanned |
| 1002 | 3 | 1000 m launch radius: 2 trucks, 40 stops; 90% delivered (0% by drone, 31 on the second pass), last at 14:51, half of all parcels by 12:09, 84% by 14:00; 11.0 truck hours, 18 km, replanned |
| 1002 | 4 | 300 m launch radius: 2 trucks, 21 stops; 98% delivered (44% by drone, 55 on the second pass), last at 13:32, half of all parcels by 10:51, 98% by 14:00; 7.2 truck hours, 16 km, replanned |
| 1002 | 4 | 600 m launch radius: 2 trucks, 17 stops; 96% delivered (42% by drone, 80 on the second pass), last at 13:07, half of all parcels by 10:52, 96% by 14:00; 7.1 truck hours, 16 km, replanned |
| 1002 | 4 | 1000 m launch radius: 2 trucks, 17 stops; 96% delivered (42% by drone, 80 on the second pass), last at 13:07, half of all parcels by 10:52, 96% by 14:00; 7.1 truck hours, 16 km, replanned |
| 1003 | 0 | 300 m launch radius: 2 trucks, 39 stops; 89% delivered (0% by drone, 33 on the second pass), last at 14:32, half of all parcels by 11:09, 85% by 14:00; 10.4 truck hours, 19 km, replanned |
| 1003 | 0 | 600 m launch radius: 2 trucks, 39 stops; 89% delivered (0% by drone, 33 on the second pass), last at 14:43, half of all parcels by 11:09, 85% by 14:00; 10.2 truck hours, 18 km, replanned |
| 1003 | 0 | 1000 m launch radius: 2 trucks, 39 stops; 89% delivered (0% by drone, 33 on the second pass), last at 14:43, half of all parcels by 11:09, 84% by 14:00; 10.1 truck hours, 16 km, replanned |
| 1003 | 1 | 300 m launch radius: 2 trucks, 25 stops; 99% delivered (52% by drone, 48 on the second pass), last at 13:36, half of all parcels by 11:14, 99% by 14:00; 8.8 truck hours, 18 km, replanned |
| 1003 | 1 | 600 m launch radius: 2 trucks, 27 stops; 97% delivered (50% by drone, 45 on the second pass), last at 13:59, half of all parcels by 10:54, 97% by 14:00; 9.0 truck hours, 17 km, replanned |
| 1003 | 1 | 1000 m launch radius: 2 trucks, 27 stops; 97% delivered (50% by drone, 45 on the second pass), last at 13:59, half of all parcels by 10:54, 97% by 14:00; 9.0 truck hours, 17 km, replanned |
| 1003 | 2 | 300 m launch radius: 2 trucks, 24 stops; 96% delivered (38% by drone, 60 on the second pass), last at 13:24, half of all parcels by 10:53, 96% by 14:00; 7.7 truck hours, 18 km, replanned |
| 1003 | 2 | 600 m launch radius: 2 trucks, 24 stops; 95% delivered (32% by drone, 60 on the second pass), last at 13:55, half of all parcels by 11:16, 95% by 14:00; 8.7 truck hours, 16 km, replanned |
| 1003 | 2 | 1000 m launch radius: 2 trucks, 26 stops; 95% delivered (30% by drone, 63 on the second pass), last at 13:54, half of all parcels by 11:26, 95% by 14:00; 8.9 truck hours, 16 km, replanned |
| 1003 | 3 | 300 m launch radius: 2 trucks, 24 stops; 97% delivered (43% by drone, 36 on the second pass), last at 13:07, half of all parcels by 10:00, 97% by 14:00; 7.2 truck hours, 16 km, replanned |
| 1003 | 3 | 600 m launch radius: 2 trucks, 24 stops; 97% delivered (41% by drone, 46 on the second pass), last at 13:18, half of all parcels by 11:09, 97% by 14:00; 7.5 truck hours, 14 km, replanned |
| 1003 | 3 | 1000 m launch radius: 2 trucks, 24 stops; 97% delivered (41% by drone, 46 on the second pass), last at 13:18, half of all parcels by 11:09, 97% by 14:00; 7.5 truck hours, 14 km, replanned |
| 1003 | 4 | 300 m launch radius: 2 trucks, 26 stops; 97% delivered (45% by drone, 52 on the second pass), last at 13:34, half of all parcels by 10:53, 97% by 14:00; 8.9 truck hours, 19 km, replanned |
| 1003 | 4 | 600 m launch radius: 2 trucks, 26 stops; 98% delivered (45% by drone, 45 on the second pass), last at 13:48, half of all parcels by 10:45, 98% by 14:00; 9.0 truck hours, 19 km, replanned |
| 1003 | 4 | 1000 m launch radius: 2 trucks, 26 stops; 98% delivered (45% by drone, 45 on the second pass), last at 13:48, half of all parcels by 10:45, 98% by 14:00; 9.0 truck hours, 19 km, replanned |
| 1004 | 0 | 300 m launch radius: 2 trucks, 21 stops; 93% delivered (38% by drone, 51 on the second pass), last at 13:12, half of all parcels by 10:43, 93% by 14:00; 7.6 truck hours, 18 km, replanned |
| 1004 | 0 | 600 m launch radius: 2 trucks, 23 stops; 94% delivered (35% by drone, 64 on the second pass), last at 13:46, half of all parcels by 10:56, 94% by 14:00; 8.2 truck hours, 17 km, replanned |
| 1004 | 0 | 1000 m launch radius: 2 trucks, 23 stops; 94% delivered (35% by drone, 63 on the second pass), last at 13:46, half of all parcels by 10:56, 94% by 14:00; 8.1 truck hours, 16 km, replanned |
| 1004 | 1 | 300 m launch radius: 2 trucks, 21 stops; 95% delivered (40% by drone, 36 on the second pass), last at 12:47, half of all parcels by 10:58, 95% by 14:00; 6.6 truck hours, 15 km, replanned |
| 1004 | 1 | 600 m launch radius: 2 trucks, 22 stops; 94% delivered (37% by drone, 39 on the second pass), last at 13:17, half of all parcels by 11:16, 94% by 14:00; 7.3 truck hours, 16 km, replanned |
| 1004 | 1 | 1000 m launch radius: 2 trucks, 22 stops; 95% delivered (38% by drone, 45 on the second pass), last at 13:30, half of all parcels by 11:16, 95% by 14:00; 7.2 truck hours, 14 km, replanned |
| 1004 | 2 | 300 m launch radius: 2 trucks, 27 stops; 98% delivered (45% by drone, 42 on the second pass), last at 13:45, half of all parcels by 11:17, 98% by 14:00; 8.8 truck hours, 16 km, replanned |
| 1004 | 2 | 600 m launch radius: 2 trucks, 27 stops; 98% delivered (44% by drone, 49 on the second pass), last at 14:24, half of all parcels by 11:03, 93% by 14:00; 9.4 truck hours, 17 km, replanned |
| 1004 | 2 | 1000 m launch radius: 2 trucks, 27 stops; 98% delivered (44% by drone, 49 on the second pass), last at 14:24, half of all parcels by 11:03, 93% by 14:00; 9.4 truck hours, 17 km, replanned |
| 1004 | 3 | 300 m launch radius: 2 trucks, 42 stops; 91% delivered (0% by drone, 50 on the second pass), last at 15:44, half of all parcels by 12:36, 82% by 14:00; 12.5 truck hours, 19 km, replanned |
| 1004 | 3 | 600 m launch radius: 2 trucks, 42 stops; 91% delivered (0% by drone, 50 on the second pass), last at 15:48, half of all parcels by 12:36, 83% by 14:00; 12.3 truck hours, 17 km, replanned |
| 1004 | 3 | 1000 m launch radius: 2 trucks, 42 stops; 91% delivered (0% by drone, 50 on the second pass), last at 15:48, half of all parcels by 12:36, 83% by 14:00; 12.3 truck hours, 17 km, replanned |
| 1004 | 4 | 300 m launch radius: 2 trucks, 25 stops; 97% delivered (43% by drone, 37 on the second pass), last at 13:43, half of all parcels by 11:05, 97% by 14:00; 8.4 truck hours, 17 km, replanned |
| 1004 | 4 | 600 m launch radius: 2 trucks, 27 stops; 97% delivered (38% by drone, 43 on the second pass), last at 14:24, half of all parcels by 11:27, 97% by 14:00; 9.1 truck hours, 16 km, replanned |
| 1004 | 4 | 1000 m launch radius: 2 trucks, 27 stops; 97% delivered (38% by drone, 43 on the second pass), last at 14:24, half of all parcels by 11:27, 97% by 14:00; 9.1 truck hours, 16 km, replanned |
| 1005 | 0 | 300 m launch radius: 2 trucks, 22 stops; 94% delivered (44% by drone, 45 on the second pass), last at 13:14, half of all parcels by 11:07, 94% by 14:00; 7.6 truck hours, 18 km, replanned |
| 1005 | 0 | 600 m launch radius: 2 trucks, 23 stops; 94% delivered (40% by drone, 41 on the second pass), last at 13:20, half of all parcels by 10:42, 94% by 14:00; 7.5 truck hours, 18 km, replanned |
| 1005 | 0 | 1000 m launch radius: 2 trucks, 23 stops; 95% delivered (41% by drone, 44 on the second pass), last at 13:20, half of all parcels by 10:42, 95% by 14:00; 7.5 truck hours, 17 km, replanned |
| 1005 | 1 | 300 m launch radius: 2 trucks, 24 stops; 99% delivered (52% by drone, 40 on the second pass), last at 12:57, half of all parcels by 10:58, 99% by 14:00; 7.1 truck hours, 18 km, replanned |
| 1005 | 1 | 600 m launch radius: 2 trucks, 27 stops; 97% delivered (45% by drone, 33 on the second pass), last at 13:12, half of all parcels by 11:19, 97% by 14:00; 7.8 truck hours, 16 km, replanned |
| 1005 | 1 | 1000 m launch radius: 2 trucks, 27 stops; 97% delivered (45% by drone, 32 on the second pass), last at 13:18, half of all parcels by 11:11, 97% by 14:00; 7.7 truck hours, 15 km, replanned |
| 1005 | 2 | 300 m launch radius: 2 trucks, 22 stops; 95% delivered (39% by drone, 59 on the second pass), last at 13:50, half of all parcels by 10:58, 95% by 14:00; 8.3 truck hours, 19 km, replanned |
| 1005 | 2 | 600 m launch radius: 2 trucks, 21 stops; 95% delivered (37% by drone, 59 on the second pass), last at 14:17, half of all parcels by 11:18, 93% by 14:00; 8.8 truck hours, 18 km, replanned |
| 1005 | 2 | 1000 m launch radius: 2 trucks, 21 stops; 95% delivered (37% by drone, 59 on the second pass), last at 14:17, half of all parcels by 11:18, 93% by 14:00; 8.8 truck hours, 18 km, replanned |
| 1005 | 3 | 300 m launch radius: 2 trucks, 25 stops; 98% delivered (43% by drone, 61 on the second pass), last at 14:00, half of all parcels by 11:04, 98% by 14:00; 8.6 truck hours, 19 km, replanned |
| 1005 | 3 | 600 m launch radius: 2 trucks, 23 stops; 96% delivered (41% by drone, 63 on the second pass), last at 13:41, half of all parcels by 11:24, 96% by 14:00; 8.4 truck hours, 18 km, replanned |
| 1005 | 3 | 1000 m launch radius: 2 trucks, 23 stops; 96% delivered (41% by drone, 63 on the second pass), last at 13:41, half of all parcels by 11:24, 96% by 14:00; 8.4 truck hours, 18 km, replanned |
| 1005 | 4 | 300 m launch radius: 2 trucks, 21 stops; 95% delivered (46% by drone, 76 on the second pass), last at 13:10, half of all parcels by 10:38, 95% by 14:00; 7.5 truck hours, 16 km, replanned |
| 1005 | 4 | 600 m launch radius: 2 trucks, 18 stops; 97% delivered (43% by drone, 62 on the second pass), last at 13:12, half of all parcels by 10:55, 97% by 14:00; 7.0 truck hours, 16 km, replanned |
| 1005 | 4 | 1000 m launch radius: 2 trucks, 18 stops; 97% delivered (43% by drone, 61 on the second pass), last at 13:12, half of all parcels by 10:55, 97% by 14:00; 6.9 truck hours, 15 km, replanned |
| 1006 | 0 | 300 m launch radius: 2 trucks, 22 stops; 99% delivered (49% by drone, 43 on the second pass), last at 13:06, half of all parcels by 10:51, 99% by 14:00; 7.4 truck hours, 15 km, replanned |
| 1006 | 0 | 600 m launch radius: 2 trucks, 18 stops; 99% delivered (49% by drone, 49 on the second pass), last at 13:01, half of all parcels by 11:03, 99% by 14:00; 7.2 truck hours, 14 km, replanned |
| 1006 | 0 | 1000 m launch radius: 2 trucks, 18 stops; 99% delivered (49% by drone, 49 on the second pass), last at 13:01, half of all parcels by 11:03, 99% by 14:00; 7.2 truck hours, 14 km, replanned |
| 1006 | 1 | 300 m launch radius: 2 trucks, 17 stops; 99% delivered (57% by drone, 43 on the second pass), last at 12:47, half of all parcels by 10:43, 99% by 14:00; 7.1 truck hours, 15 km, replanned |
| 1006 | 1 | 600 m launch radius: 2 trucks, 20 stops; 99% delivered (52% by drone, 44 on the second pass), last at 13:27, half of all parcels by 10:47, 99% by 14:00; 8.0 truck hours, 17 km, replanned |
| 1006 | 1 | 1000 m launch radius: 2 trucks, 20 stops; 99% delivered (52% by drone, 44 on the second pass), last at 13:27, half of all parcels by 10:47, 99% by 14:00; 8.0 truck hours, 17 km, replanned |
| 1006 | 2 | 300 m launch radius: 2 trucks, 33 stops; 85% delivered (13% by drone, 35 on the second pass), last at 14:22, half of all parcels by 11:07, 85% by 14:00; 9.9 truck hours, 21 km, replanned |
| 1006 | 2 | 600 m launch radius: 2 trucks, 29 stops; 82% delivered (13% by drone, 35 on the second pass), last at 13:59, half of all parcels by 11:55, 82% by 14:00; 9.2 truck hours, 18 km, replanned |
| 1006 | 2 | 1000 m launch radius: 2 trucks, 29 stops; 82% delivered (13% by drone, 35 on the second pass), last at 13:59, half of all parcels by 11:55, 82% by 14:00; 9.2 truck hours, 18 km, replanned |
| 1006 | 3 | 300 m launch radius: 2 trucks, 23 stops; 98% delivered (48% by drone, 29 on the second pass), last at 13:14, half of all parcels by 11:08, 98% by 14:00; 8.0 truck hours, 15 km, replanned |
| 1006 | 3 | 600 m launch radius: 2 trucks, 20 stops; 98% delivered (48% by drone, 33 on the second pass), last at 12:57, half of all parcels by 11:03, 98% by 14:00; 7.1 truck hours, 14 km, replanned |
| 1006 | 3 | 1000 m launch radius: 2 trucks, 20 stops; 98% delivered (48% by drone, 32 on the second pass), last at 12:57, half of all parcels by 11:03, 98% by 14:00; 7.1 truck hours, 14 km, replanned |
| 1006 | 4 | 300 m launch radius: 2 trucks, 23 stops; 98% delivered (49% by drone, 40 on the second pass), last at 12:52, half of all parcels by 10:47, 98% by 14:00; 7.4 truck hours, 18 km, replanned |
| 1006 | 4 | 600 m launch radius: 2 trucks, 22 stops; 97% delivered (44% by drone, 49 on the second pass), last at 13:06, half of all parcels by 11:03, 97% by 14:00; 7.6 truck hours, 14 km, replanned |
| 1006 | 4 | 1000 m launch radius: 2 trucks, 22 stops; 99% delivered (45% by drone, 55 on the second pass), last at 13:12, half of all parcels by 11:03, 99% by 14:00; 7.5 truck hours, 14 km, replanned |
| 1007 | 0 | 300 m launch radius: 2 trucks, 28 stops; 91% delivered (45% by drone, 37 on the second pass), last at 14:15, half of all parcels by 10:44, 91% by 14:00; 9.5 truck hours, 18 km, replanned |
| 1007 | 0 | 600 m launch radius: 2 trucks, 28 stops; 94% delivered (47% by drone, 63 on the second pass), last at 14:29, half of all parcels by 11:04, 92% by 14:00; 9.7 truck hours, 17 km, replanned |
| 1007 | 0 | 1000 m launch radius: 2 trucks, 28 stops; 94% delivered (46% by drone, 61 on the second pass), last at 14:25, half of all parcels by 11:04, 91% by 14:00; 9.7 truck hours, 17 km, replanned |
| 1007 | 1 | 300 m launch radius: 2 trucks, 22 stops; 97% delivered (44% by drone, 61 on the second pass), last at 13:43, half of all parcels by 10:54, 97% by 14:00; 8.4 truck hours, 18 km, replanned |
| 1007 | 1 | 600 m launch radius: 2 trucks, 17 stops; 94% delivered (44% by drone, 48 on the second pass), last at 13:12, half of all parcels by 10:52, 94% by 14:00; 7.5 truck hours, 16 km, replanned |
| 1007 | 1 | 1000 m launch radius: 2 trucks, 17 stops; 94% delivered (44% by drone, 48 on the second pass), last at 13:12, half of all parcels by 10:52, 94% by 14:00; 7.5 truck hours, 16 km, replanned |
| 1007 | 2 | 300 m launch radius: 2 trucks, 22 stops; 97% delivered (41% by drone, 48 on the second pass), last at 13:25, half of all parcels by 10:56, 97% by 14:00; 7.6 truck hours, 17 km, replanned |
| 1007 | 2 | 600 m launch radius: 2 trucks, 20 stops; 95% delivered (40% by drone, 43 on the second pass), last at 13:11, half of all parcels by 11:16, 95% by 14:00; 7.6 truck hours, 17 km, replanned |
| 1007 | 2 | 1000 m launch radius: 2 trucks, 20 stops; 96% delivered (41% by drone, 47 on the second pass), last at 13:08, half of all parcels by 11:16, 96% by 14:00; 7.6 truck hours, 17 km, replanned |
| 1007 | 3 | 300 m launch radius: 2 trucks, 21 stops; 96% delivered (51% by drone, 51 on the second pass), last at 12:58, half of all parcels by 10:42, 96% by 14:00; 7.6 truck hours, 19 km, replanned |
| 1007 | 3 | 600 m launch radius: 2 trucks, 19 stops; 97% delivered (50% by drone, 52 on the second pass), last at 13:04, half of all parcels by 11:05, 97% by 14:00; 7.4 truck hours, 16 km, replanned |
| 1007 | 3 | 1000 m launch radius: 2 trucks, 19 stops; 96% delivered (48% by drone, 43 on the second pass), last at 13:04, half of all parcels by 11:05, 96% by 14:00; 7.4 truck hours, 16 km, replanned |
| 1007 | 4 | 300 m launch radius: 2 trucks, 22 stops; 99% delivered (47% by drone, 60 on the second pass), last at 13:18, half of all parcels by 10:32, 99% by 14:00; 8.1 truck hours, 18 km, replanned |
| 1007 | 4 | 600 m launch radius: 2 trucks, 21 stops; 97% delivered (44% by drone, 49 on the second pass), last at 13:00, half of all parcels by 11:15, 97% by 14:00; 8.5 truck hours, 18 km, replanned |
| 1007 | 4 | 1000 m launch radius: 2 trucks, 21 stops; 97% delivered (43% by drone, 48 on the second pass), last at 13:00, half of all parcels by 11:15, 97% by 14:00; 8.4 truck hours, 18 km, replanned |
| 1008 | 0 | 300 m launch radius: 2 trucks, 24 stops; 98% delivered (48% by drone, 54 on the second pass), last at 13:44, half of all parcels by 11:17, 98% by 14:00; 8.8 truck hours, 20 km, replanned |
| 1008 | 0 | 600 m launch radius: 2 trucks, 21 stops; 97% delivered (46% by drone, 54 on the second pass), last at 13:55, half of all parcels by 11:14, 97% by 14:00; 8.4 truck hours, 17 km, replanned |
| 1008 | 0 | 1000 m launch radius: 2 trucks, 21 stops; 97% delivered (46% by drone, 54 on the second pass), last at 13:55, half of all parcels by 11:14, 97% by 14:00; 8.4 truck hours, 17 km, replanned |
| 1008 | 1 | 300 m launch radius: 2 trucks, 23 stops; 98% delivered (57% by drone, 32 on the second pass), last at 12:59, half of all parcels by 10:47, 98% by 14:00; 7.0 truck hours, 17 km, replanned |
| 1008 | 1 | 600 m launch radius: 2 trucks, 19 stops; 98% delivered (55% by drone, 50 on the second pass), last at 13:15, half of all parcels by 10:57, 98% by 14:00; 6.9 truck hours, 14 km, replanned |
| 1008 | 1 | 1000 m launch radius: 2 trucks, 19 stops; 98% delivered (55% by drone, 50 on the second pass), last at 13:15, half of all parcels by 10:57, 98% by 14:00; 6.9 truck hours, 14 km, replanned |
| 1008 | 2 | 300 m launch radius: 2 trucks, 28 stops; 95% delivered (27% by drone, 101 on the second pass), last at 14:14, half of all parcels by 11:47, 94% by 14:00; 9.1 truck hours, 19 km, replanned |
| 1008 | 2 | 600 m launch radius: 2 trucks, 37 stops; 98% delivered (15% by drone, 83 on the second pass), last at 14:16, half of all parcels by 11:55, 95% by 14:00; 10.2 truck hours, 19 km, replanned |
| 1008 | 2 | 1000 m launch radius: 2 trucks, 37 stops; 98% delivered (15% by drone, 83 on the second pass), last at 14:16, half of all parcels by 11:55, 95% by 14:00; 10.2 truck hours, 19 km, replanned |
| 1008 | 3 | 300 m launch radius: 2 trucks, 26 stops; 97% delivered (48% by drone, 49 on the second pass), last at 13:12, half of all parcels by 10:44, 97% by 14:00; 8.0 truck hours, 17 km, replanned |
| 1008 | 3 | 600 m launch radius: 2 trucks, 23 stops; 98% delivered (47% by drone, 44 on the second pass), last at 13:23, half of all parcels by 11:14, 98% by 14:00; 7.8 truck hours, 17 km, replanned |
| 1008 | 3 | 1000 m launch radius: 2 trucks, 23 stops; 98% delivered (47% by drone, 44 on the second pass), last at 13:23, half of all parcels by 11:14, 98% by 14:00; 7.7 truck hours, 16 km, replanned |
| 1008 | 4 | 300 m launch radius: 2 trucks, 27 stops; 97% delivered (52% by drone, 34 on the second pass), last at 13:06, half of all parcels by 10:43, 97% by 14:00; 7.6 truck hours, 18 km, replanned |
| 1008 | 4 | 600 m launch radius: 2 trucks, 24 stops; 96% delivered (48% by drone, 24 on the second pass), last at 13:28, half of all parcels by 11:36, 96% by 14:00; 7.6 truck hours, 16 km, replanned |
| 1008 | 4 | 1000 m launch radius: 2 trucks, 24 stops; 96% delivered (48% by drone, 24 on the second pass), last at 13:28, half of all parcels by 11:36, 96% by 14:00; 7.6 truck hours, 15 km, replanned |
| 1009 | 0 | 300 m launch radius: 2 trucks, 32 stops; 91% delivered (0% by drone, 26 on the second pass), last at 14:10, half of all parcels by 11:46, 91% by 14:00; 10.1 truck hours, 18 km, replanned |
| 1009 | 0 | 600 m launch radius: 2 trucks, 32 stops; 91% delivered (0% by drone, 26 on the second pass), last at 14:27, half of all parcels by 11:46, 90% by 14:00; 10.0 truck hours, 17 km, replanned |
| 1009 | 0 | 1000 m launch radius: 2 trucks, 32 stops; 91% delivered (0% by drone, 26 on the second pass), last at 14:27, half of all parcels by 11:46, 90% by 14:00; 9.9 truck hours, 16 km, replanned |
| 1009 | 1 | 300 m launch radius: 2 trucks, 22 stops; 98% delivered (43% by drone, 36 on the second pass), last at 13:15, half of all parcels by 10:49, 98% by 14:00; 7.4 truck hours, 16 km, replanned |
| 1009 | 1 | 600 m launch radius: 2 trucks, 17 stops; 99% delivered (44% by drone, 36 on the second pass), last at 13:09, half of all parcels by 10:45, 99% by 14:00; 7.4 truck hours, 15 km, replanned |
| 1009 | 1 | 1000 m launch radius: 2 trucks, 17 stops; 99% delivered (44% by drone, 36 on the second pass), last at 13:09, half of all parcels by 10:45, 99% by 14:00; 7.4 truck hours, 15 km, replanned |
| 1009 | 2 | 300 m launch radius: 2 trucks, 24 stops; 98% delivered (53% by drone, 48 on the second pass), last at 13:48, half of all parcels by 11:04, 98% by 14:00; 7.7 truck hours, 16 km, replanned |
| 1009 | 2 | 600 m launch radius: 2 trucks, 18 stops; 97% delivered (52% by drone, 58 on the second pass), last at 13:03, half of all parcels by 10:42, 97% by 14:00; 6.9 truck hours, 15 km, replanned |
| 1009 | 2 | 1000 m launch radius: 2 trucks, 18 stops; 97% delivered (52% by drone, 57 on the second pass), last at 12:55, half of all parcels by 10:46, 97% by 14:00; 6.9 truck hours, 14 km, replanned |
| 1009 | 3 | 300 m launch radius: 2 trucks, 20 stops; 97% delivered (39% by drone, 53 on the second pass), last at 13:43, half of all parcels by 10:47, 97% by 14:00; 8.4 truck hours, 16 km, replanned |
| 1009 | 3 | 600 m launch radius: 2 trucks, 21 stops; 97% delivered (35% by drone, 59 on the second pass), last at 13:35, half of all parcels by 10:34, 97% by 14:00; 8.8 truck hours, 16 km, replanned |
| 1009 | 3 | 1000 m launch radius: 2 trucks, 21 stops; 97% delivered (35% by drone, 59 on the second pass), last at 13:35, half of all parcels by 10:34, 97% by 14:00; 8.8 truck hours, 16 km, replanned |
| 1009 | 4 | 300 m launch radius: 2 trucks, 35 stops; 92% delivered (0% by drone, 37 on the second pass), last at 14:33, half of all parcels by 11:34, 88% by 14:00; 10.3 truck hours, 20 km, replanned |
| 1009 | 4 | 600 m launch radius: 2 trucks, 35 stops; 92% delivered (0% by drone, 37 on the second pass), last at 14:32, half of all parcels by 11:34, 86% by 14:00; 10.2 truck hours, 19 km, replanned |
| 1009 | 4 | 1000 m launch radius: 2 trucks, 35 stops; 92% delivered (0% by drone, 37 on the second pass), last at 14:32, half of all parcels by 11:34, 88% by 14:00; 10.2 truck hours, 19 km, replanned |
