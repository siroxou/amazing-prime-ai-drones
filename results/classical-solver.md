# Classical truck + drone solver on the held-out days

Written by `python -m baselines.classical --held-out`. 50 days, 500 parcels each, averages over the days. Autonomous trucks with 10 drones and a locker each; a drone cost model (sim/drone.py: wind, payload, battery, flight heights, drop planning; up to 5 kg). Locker settings as in [trucks-only-baseline.md](trucks-only-baseline.md) with a 10-minute wait. Settings are in `baselines/classical.py`.

| launch radius | 300 m | 600 m | 1000 m |
|---|---|---|---|
| trucks | 2.0 | 2.0 | 2.0 |
| stops | 25 | 24 | 24 |
| parcels delivered today | 87% | 86% | 86% |
| by drone | 38% | 36% | 36% |
| last parcel | 12:01 | 12:04 | 12:05 |
| half of all parcels by | 11:02 | 11:10 | 11:08 |
| delivered by 14:00 | 87% | 86% | 86% |
| truck hours | 5.1 | 5.3 | 5.3 |
| km driven | 10 | 10 | 10 |
| days replanned for weather or airspace | 100% | 100% | 100% |

## Every day

| city | day | result |
|---|---|---|
| 1000 | 0 | 300 m launch radius: 2 trucks, 40 stops; 82% delivered (0% by drone), last at 13:26, half of all parcels by 11:25, 82% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1000 | 0 | 600 m launch radius: 2 trucks, 40 stops; 82% delivered (0% by drone), last at 13:26, half of all parcels by 11:25, 82% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1000 | 0 | 1000 m launch radius: 2 trucks, 40 stops; 82% delivered (0% by drone), last at 13:26, half of all parcels by 11:25, 82% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1000 | 1 | 300 m launch radius: 2 trucks, 21 stops; 89% delivered (50% by drone), last at 11:37, half of all parcels by 10:39, 89% by 14:00; 4.3 truck hours, 11 km, replanned |
| 1000 | 1 | 600 m launch radius: 2 trucks, 17 stops; 88% delivered (47% by drone), last at 11:31, half of all parcels by 10:53, 88% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1000 | 1 | 1000 m launch radius: 2 trucks, 17 stops; 88% delivered (47% by drone), last at 11:31, half of all parcels by 10:53, 88% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1000 | 2 | 300 m launch radius: 2 trucks, 21 stops; 85% delivered (42% by drone), last at 11:41, half of all parcels by 10:57, 85% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1000 | 2 | 600 m launch radius: 2 trucks, 20 stops; 85% delivered (39% by drone), last at 11:44, half of all parcels by 11:06, 85% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1000 | 2 | 1000 m launch radius: 2 trucks, 20 stops; 85% delivered (39% by drone), last at 11:44, half of all parcels by 11:06, 85% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1000 | 3 | 300 m launch radius: 2 trucks, 17 stops; 82% delivered (44% by drone), last at 11:19, half of all parcels by 10:57, 82% by 14:00; 3.7 truck hours, 9 km, replanned |
| 1000 | 3 | 600 m launch radius: 2 trucks, 14 stops; 83% delivered (45% by drone), last at 11:15, half of all parcels by 10:35, 83% by 14:00; 3.6 truck hours, 9 km, replanned |
| 1000 | 3 | 1000 m launch radius: 2 trucks, 14 stops; 83% delivered (45% by drone), last at 11:15, half of all parcels by 10:35, 83% by 14:00; 3.6 truck hours, 9 km, replanned |
| 1000 | 4 | 300 m launch radius: 2 trucks, 26 stops; 88% delivered (37% by drone), last at 12:05, half of all parcels by 11:10, 88% by 14:00; 5.3 truck hours, 10 km, replanned |
| 1000 | 4 | 600 m launch radius: 2 trucks, 25 stops; 88% delivered (36% by drone), last at 12:06, half of all parcels by 11:26, 88% by 14:00; 5.4 truck hours, 10 km, replanned |
| 1000 | 4 | 1000 m launch radius: 2 trucks, 25 stops; 88% delivered (36% by drone), last at 12:06, half of all parcels by 11:26, 88% by 14:00; 5.4 truck hours, 10 km, replanned |
| 1001 | 0 | 300 m launch radius: 2 trucks, 24 stops; 92% delivered (49% by drone), last at 11:55, half of all parcels by 10:53, 92% by 14:00; 4.9 truck hours, 10 km, replanned |
| 1001 | 0 | 600 m launch radius: 2 trucks, 20 stops; 92% delivered (47% by drone), last at 11:38, half of all parcels by 10:42, 92% by 14:00; 4.6 truck hours, 8 km, replanned |
| 1001 | 0 | 1000 m launch radius: 2 trucks, 20 stops; 92% delivered (47% by drone), last at 11:38, half of all parcels by 10:42, 92% by 14:00; 4.6 truck hours, 8 km, replanned |
| 1001 | 1 | 300 m launch radius: 2 trucks, 25 stops; 89% delivered (47% by drone), last at 11:55, half of all parcels by 10:54, 89% by 14:00; 4.9 truck hours, 11 km, replanned |
| 1001 | 1 | 600 m launch radius: 2 trucks, 22 stops; 88% delivered (46% by drone), last at 11:52, half of all parcels by 11:02, 88% by 14:00; 4.8 truck hours, 10 km, replanned |
| 1001 | 1 | 1000 m launch radius: 2 trucks, 22 stops; 88% delivered (46% by drone), last at 11:52, half of all parcels by 11:02, 88% by 14:00; 4.8 truck hours, 10 km, replanned |
| 1001 | 2 | 300 m launch radius: 2 trucks, 24 stops; 90% delivered (52% by drone), last at 11:55, half of all parcels by 11:07, 90% by 14:00; 4.9 truck hours, 9 km, replanned |
| 1001 | 2 | 600 m launch radius: 2 trucks, 22 stops; 89% delivered (50% by drone), last at 11:57, half of all parcels by 10:36, 89% by 14:00; 5.0 truck hours, 10 km, replanned |
| 1001 | 2 | 1000 m launch radius: 2 trucks, 22 stops; 89% delivered (50% by drone), last at 11:57, half of all parcels by 10:36, 89% by 14:00; 5.0 truck hours, 10 km, replanned |
| 1001 | 3 | 300 m launch radius: 2 trucks, 22 stops; 92% delivered (46% by drone), last at 11:53, half of all parcels by 10:56, 92% by 14:00; 4.9 truck hours, 9 km, replanned |
| 1001 | 3 | 600 m launch radius: 2 trucks, 23 stops; 92% delivered (45% by drone), last at 11:59, half of all parcels by 11:24, 92% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1001 | 3 | 1000 m launch radius: 2 trucks, 23 stops; 91% delivered (45% by drone), last at 12:04, half of all parcels by 10:55, 91% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1001 | 4 | 300 m launch radius: 2 trucks, 20 stops; 92% delivered (45% by drone), last at 11:33, half of all parcels by 11:14, 92% by 14:00; 4.2 truck hours, 9 km, replanned |
| 1001 | 4 | 600 m launch radius: 2 trucks, 19 stops; 91% delivered (41% by drone), last at 11:42, half of all parcels by 10:56, 91% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1001 | 4 | 1000 m launch radius: 2 trucks, 19 stops; 91% delivered (41% by drone), last at 11:42, half of all parcels by 10:56, 91% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1002 | 0 | 300 m launch radius: 2 trucks, 21 stops; 89% delivered (45% by drone), last at 11:34, half of all parcels by 11:05, 89% by 14:00; 4.2 truck hours, 10 km, replanned |
| 1002 | 0 | 600 m launch radius: 2 trucks, 20 stops; 88% delivered (39% by drone), last at 11:45, half of all parcels by 11:16, 88% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1002 | 0 | 1000 m launch radius: 2 trucks, 20 stops; 88% delivered (39% by drone), last at 11:45, half of all parcels by 11:16, 88% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1002 | 1 | 300 m launch radius: 2 trucks, 22 stops; 87% delivered (42% by drone), last at 11:47, half of all parcels by 10:47, 87% by 14:00; 4.6 truck hours, 10 km, replanned |
| 1002 | 1 | 600 m launch radius: 2 trucks, 22 stops; 88% delivered (39% by drone), last at 11:53, half of all parcels by 10:44, 88% by 14:00; 4.9 truck hours, 10 km, replanned |
| 1002 | 1 | 1000 m launch radius: 2 trucks, 22 stops; 88% delivered (39% by drone), last at 11:53, half of all parcels by 10:44, 88% by 14:00; 4.9 truck hours, 10 km, replanned |
| 1002 | 2 | 300 m launch radius: 2 trucks, 24 stops; 89% delivered (43% by drone), last at 11:54, half of all parcels by 11:07, 89% by 14:00; 5.0 truck hours, 10 km, replanned |
| 1002 | 2 | 600 m launch radius: 2 trucks, 23 stops; 89% delivered (43% by drone), last at 12:01, half of all parcels by 11:03, 89% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1002 | 2 | 1000 m launch radius: 2 trucks, 22 stops; 88% delivered (42% by drone), last at 11:55, half of all parcels by 11:06, 88% by 14:00; 4.9 truck hours, 10 km, replanned |
| 1002 | 3 | 300 m launch radius: 2 trucks, 40 stops; 84% delivered (0% by drone), last at 13:28, half of all parcels by 11:57, 84% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1002 | 3 | 600 m launch radius: 2 trucks, 40 stops; 84% delivered (0% by drone), last at 13:27, half of all parcels by 12:09, 84% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1002 | 3 | 1000 m launch radius: 2 trucks, 40 stops; 84% delivered (0% by drone), last at 13:24, half of all parcels by 11:03, 84% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1002 | 4 | 300 m launch radius: 2 trucks, 21 stops; 87% delivered (43% by drone), last at 11:29, half of all parcels by 10:51, 87% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1002 | 4 | 600 m launch radius: 2 trucks, 17 stops; 80% delivered (36% by drone), last at 11:26, half of all parcels by 10:52, 80% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1002 | 4 | 1000 m launch radius: 2 trucks, 17 stops; 80% delivered (36% by drone), last at 11:26, half of all parcels by 10:52, 80% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1003 | 0 | 300 m launch radius: 2 trucks, 39 stops; 83% delivered (0% by drone), last at 13:27, half of all parcels by 11:09, 83% by 14:00; 7.8 truck hours, 12 km, replanned |
| 1003 | 0 | 600 m launch radius: 2 trucks, 39 stops; 83% delivered (0% by drone), last at 13:27, half of all parcels by 11:09, 83% by 14:00; 7.8 truck hours, 12 km, replanned |
| 1003 | 0 | 1000 m launch radius: 2 trucks, 39 stops; 83% delivered (0% by drone), last at 13:27, half of all parcels by 11:41, 83% by 14:00; 7.8 truck hours, 11 km, replanned |
| 1003 | 1 | 300 m launch radius: 2 trucks, 25 stops; 89% delivered (50% by drone), last at 12:10, half of all parcels by 11:14, 89% by 14:00; 5.3 truck hours, 11 km, replanned |
| 1003 | 1 | 600 m launch radius: 2 trucks, 27 stops; 88% delivered (49% by drone), last at 12:17, half of all parcels by 10:54, 88% by 14:00; 5.7 truck hours, 10 km, replanned |
| 1003 | 1 | 1000 m launch radius: 2 trucks, 27 stops; 88% delivered (49% by drone), last at 12:17, half of all parcels by 10:54, 88% by 14:00; 5.7 truck hours, 10 km, replanned |
| 1003 | 2 | 300 m launch radius: 2 trucks, 24 stops; 84% delivered (36% by drone), last at 11:49, half of all parcels by 10:53, 84% by 14:00; 4.6 truck hours, 10 km, replanned |
| 1003 | 2 | 600 m launch radius: 2 trucks, 24 stops; 83% delivered (29% by drone), last at 12:06, half of all parcels by 11:16, 83% by 14:00; 5.3 truck hours, 10 km, replanned |
| 1003 | 2 | 1000 m launch radius: 2 trucks, 26 stops; 82% delivered (27% by drone), last at 12:16, half of all parcels by 11:26, 82% by 14:00; 5.6 truck hours, 10 km, replanned |
| 1003 | 3 | 300 m launch radius: 2 trucks, 24 stops; 89% delivered (43% by drone), last at 11:53, half of all parcels by 11:00, 89% by 14:00; 4.8 truck hours, 10 km, replanned |
| 1003 | 3 | 600 m launch radius: 2 trucks, 24 stops; 88% delivered (39% by drone), last at 12:01, half of all parcels by 11:09, 88% by 14:00; 5.2 truck hours, 9 km, replanned |
| 1003 | 3 | 1000 m launch radius: 2 trucks, 24 stops; 88% delivered (39% by drone), last at 12:01, half of all parcels by 11:09, 88% by 14:00; 5.2 truck hours, 9 km, replanned |
| 1003 | 4 | 300 m launch radius: 2 trucks, 26 stops; 87% delivered (43% by drone), last at 12:12, half of all parcels by 10:53, 87% by 14:00; 5.5 truck hours, 10 km, replanned |
| 1003 | 4 | 600 m launch radius: 2 trucks, 26 stops; 89% delivered (44% by drone), last at 12:15, half of all parcels by 10:45, 89% by 14:00; 5.6 truck hours, 11 km, replanned |
| 1003 | 4 | 1000 m launch radius: 2 trucks, 26 stops; 89% delivered (44% by drone), last at 12:16, half of all parcels by 10:47, 89% by 14:00; 5.6 truck hours, 11 km, replanned |
| 1004 | 0 | 300 m launch radius: 2 trucks, 21 stops; 83% delivered (35% by drone), last at 11:43, half of all parcels by 10:43, 83% by 14:00; 4.5 truck hours, 10 km, replanned |
| 1004 | 0 | 600 m launch radius: 2 trucks, 23 stops; 81% delivered (29% by drone), last at 11:57, half of all parcels by 10:56, 81% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1004 | 0 | 1000 m launch radius: 2 trucks, 23 stops; 81% delivered (29% by drone), last at 11:57, half of all parcels by 10:56, 81% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1004 | 1 | 300 m launch radius: 2 trucks, 21 stops; 88% delivered (40% by drone), last at 11:36, half of all parcels by 10:58, 88% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1004 | 1 | 600 m launch radius: 2 trucks, 22 stops; 86% delivered (36% by drone), last at 11:56, half of all parcels by 11:16, 86% by 14:00; 4.9 truck hours, 10 km, replanned |
| 1004 | 1 | 1000 m launch radius: 2 trucks, 22 stops; 86% delivered (36% by drone), last at 11:56, half of all parcels by 11:16, 86% by 14:00; 4.9 truck hours, 10 km, replanned |
| 1004 | 2 | 300 m launch radius: 2 trucks, 27 stops; 89% delivered (45% by drone), last at 12:14, half of all parcels by 11:17, 89% by 14:00; 5.5 truck hours, 11 km, replanned |
| 1004 | 2 | 600 m launch radius: 2 trucks, 27 stops; 88% delivered (42% by drone), last at 12:18, half of all parcels by 11:03, 88% by 14:00; 5.8 truck hours, 11 km, replanned |
| 1004 | 2 | 1000 m launch radius: 2 trucks, 27 stops; 88% delivered (42% by drone), last at 12:18, half of all parcels by 11:03, 88% by 14:00; 5.8 truck hours, 11 km, replanned |
| 1004 | 3 | 300 m launch radius: 2 trucks, 42 stops; 81% delivered (0% by drone), last at 13:32, half of all parcels by 12:36, 81% by 14:00; 8.3 truck hours, 11 km, replanned |
| 1004 | 3 | 600 m launch radius: 2 trucks, 42 stops; 81% delivered (0% by drone), last at 13:32, half of all parcels by 12:36, 81% by 14:00; 8.3 truck hours, 11 km, replanned |
| 1004 | 3 | 1000 m launch radius: 2 trucks, 42 stops; 81% delivered (0% by drone), last at 13:32, half of all parcels by 12:36, 81% by 14:00; 8.3 truck hours, 11 km, replanned |
| 1004 | 4 | 300 m launch radius: 2 trucks, 25 stops; 90% delivered (42% by drone), last at 12:01, half of all parcels by 11:05, 90% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1004 | 4 | 600 m launch radius: 2 trucks, 27 stops; 89% delivered (36% by drone), last at 12:16, half of all parcels by 11:27, 89% by 14:00; 5.8 truck hours, 10 km, replanned |
| 1004 | 4 | 1000 m launch radius: 2 trucks, 27 stops; 89% delivered (36% by drone), last at 12:20, half of all parcels by 11:06, 89% by 14:00; 5.8 truck hours, 11 km, replanned |
| 1005 | 0 | 300 m launch radius: 2 trucks, 22 stops; 85% delivered (42% by drone), last at 11:43, half of all parcels by 11:07, 85% by 14:00; 4.5 truck hours, 10 km, replanned |
| 1005 | 0 | 600 m launch radius: 2 trucks, 23 stops; 86% delivered (39% by drone), last at 11:57, half of all parcels by 10:42, 86% by 14:00; 5.2 truck hours, 12 km, replanned |
| 1005 | 0 | 1000 m launch radius: 2 trucks, 23 stops; 86% delivered (39% by drone), last at 12:05, half of all parcels by 11:30, 86% by 14:00; 5.1 truck hours, 11 km, replanned |
| 1005 | 1 | 300 m launch radius: 2 trucks, 24 stops; 91% delivered (50% by drone), last at 11:54, half of all parcels by 10:58, 91% by 14:00; 5.1 truck hours, 11 km, replanned |
| 1005 | 1 | 600 m launch radius: 2 trucks, 27 stops; 90% delivered (44% by drone), last at 12:24, half of all parcels by 11:13, 90% by 14:00; 5.8 truck hours, 10 km, replanned |
| 1005 | 1 | 1000 m launch radius: 2 trucks, 27 stops; 90% delivered (44% by drone), last at 12:25, half of all parcels by 11:02, 90% by 14:00; 5.8 truck hours, 10 km, replanned |
| 1005 | 2 | 300 m launch radius: 2 trucks, 22 stops; 83% delivered (36% by drone), last at 11:46, half of all parcels by 10:58, 83% by 14:00; 4.6 truck hours, 11 km, replanned |
| 1005 | 2 | 600 m launch radius: 2 trucks, 21 stops; 83% delivered (34% by drone), last at 11:53, half of all parcels by 11:18, 83% by 14:00; 4.8 truck hours, 11 km, replanned |
| 1005 | 2 | 1000 m launch radius: 2 trucks, 21 stops; 83% delivered (34% by drone), last at 11:53, half of all parcels by 11:18, 83% by 14:00; 4.8 truck hours, 11 km, replanned |
| 1005 | 3 | 300 m launch radius: 2 trucks, 25 stops; 86% delivered (38% by drone), last at 12:04, half of all parcels by 11:04, 86% by 14:00; 5.2 truck hours, 11 km, replanned |
| 1005 | 3 | 600 m launch radius: 2 trucks, 23 stops; 84% delivered (36% by drone), last at 12:02, half of all parcels by 11:24, 84% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1005 | 3 | 1000 m launch radius: 2 trucks, 23 stops; 84% delivered (36% by drone), last at 12:05, half of all parcels by 10:53, 84% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1005 | 4 | 300 m launch radius: 2 trucks, 21 stops; 80% delivered (40% by drone), last at 11:41, half of all parcels by 10:38, 80% by 14:00; 4.4 truck hours, 10 km, replanned |
| 1005 | 4 | 600 m launch radius: 2 trucks, 18 stops; 85% delivered (39% by drone), last at 11:34, half of all parcels by 10:55, 85% by 14:00; 4.2 truck hours, 9 km, replanned |
| 1005 | 4 | 1000 m launch radius: 2 trucks, 18 stops; 85% delivered (39% by drone), last at 11:34, half of all parcels by 10:55, 85% by 14:00; 4.2 truck hours, 9 km, replanned |
| 1006 | 0 | 300 m launch radius: 2 trucks, 22 stops; 91% delivered (48% by drone), last at 11:42, half of all parcels by 10:51, 91% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1006 | 0 | 600 m launch radius: 2 trucks, 18 stops; 90% delivered (47% by drone), last at 11:37, half of all parcels by 11:03, 90% by 14:00; 4.3 truck hours, 8 km, replanned |
| 1006 | 0 | 1000 m launch radius: 2 trucks, 18 stops; 90% delivered (47% by drone), last at 11:37, half of all parcels by 11:03, 90% by 14:00; 4.3 truck hours, 8 km, replanned |
| 1006 | 1 | 300 m launch radius: 2 trucks, 17 stops; 90% delivered (57% by drone), last at 11:22, half of all parcels by 10:43, 90% by 14:00; 3.8 truck hours, 9 km, replanned |
| 1006 | 1 | 600 m launch radius: 2 trucks, 20 stops; 90% delivered (52% by drone), last at 11:43, half of all parcels by 10:47, 90% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1006 | 1 | 1000 m launch radius: 2 trucks, 20 stops; 90% delivered (52% by drone), last at 11:43, half of all parcels by 10:47, 90% by 14:00; 4.6 truck hours, 9 km, replanned |
| 1006 | 2 | 300 m launch radius: 2 trucks, 27 stops; 77% delivered (17% by drone), last at 12:21, half of all parcels by 11:05, 77% by 14:00; 5.8 truck hours, 11 km, replanned |
| 1006 | 2 | 600 m launch radius: 2 trucks, 29 stops; 75% delivered (13% by drone), last at 12:31, half of all parcels by 11:55, 75% by 14:00; 6.2 truck hours, 11 km, replanned |
| 1006 | 2 | 1000 m launch radius: 2 trucks, 29 stops; 71% delivered (10% by drone), last at 12:27, half of all parcels by 11:45, 71% by 14:00; 6.2 truck hours, 11 km, replanned |
| 1006 | 3 | 300 m launch radius: 2 trucks, 23 stops; 92% delivered (48% by drone), last at 11:48, half of all parcels by 11:08, 92% by 14:00; 4.6 truck hours, 8 km, replanned |
| 1006 | 3 | 600 m launch radius: 2 trucks, 20 stops; 92% delivered (47% by drone), last at 11:43, half of all parcels by 11:03, 92% by 14:00; 4.4 truck hours, 8 km, replanned |
| 1006 | 3 | 1000 m launch radius: 2 trucks, 20 stops; 92% delivered (47% by drone), last at 11:43, half of all parcels by 11:03, 92% by 14:00; 4.4 truck hours, 8 km, replanned |
| 1006 | 4 | 300 m launch radius: 2 trucks, 23 stops; 90% delivered (48% by drone), last at 11:49, half of all parcels by 10:47, 90% by 14:00; 4.7 truck hours, 11 km, replanned |
| 1006 | 4 | 600 m launch radius: 2 trucks, 22 stops; 88% delivered (41% by drone), last at 11:56, half of all parcels by 11:03, 88% by 14:00; 4.9 truck hours, 9 km, replanned |
| 1006 | 4 | 1000 m launch radius: 2 trucks, 22 stops; 88% delivered (41% by drone), last at 11:56, half of all parcels by 11:03, 88% by 14:00; 4.9 truck hours, 9 km, replanned |
| 1007 | 0 | 300 m launch radius: 2 trucks, 28 stops; 84% delivered (44% by drone), last at 12:18, half of all parcels by 10:44, 84% by 14:00; 5.7 truck hours, 10 km, replanned |
| 1007 | 0 | 600 m launch radius: 2 trucks, 28 stops; 81% delivered (41% by drone), last at 12:27, half of all parcels by 11:04, 81% by 14:00; 6.0 truck hours, 11 km, replanned |
| 1007 | 0 | 1000 m launch radius: 2 trucks, 28 stops; 84% delivered (44% by drone), last at 12:22, half of all parcels by 10:54, 84% by 14:00; 6.0 truck hours, 11 km, replanned |
| 1007 | 1 | 300 m launch radius: 2 trucks, 22 stops; 86% delivered (42% by drone), last at 11:45, half of all parcels by 11:06, 86% by 14:00; 4.6 truck hours, 11 km, replanned |
| 1007 | 1 | 600 m launch radius: 2 trucks, 17 stops; 85% delivered (43% by drone), last at 11:30, half of all parcels by 10:52, 85% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1007 | 1 | 1000 m launch radius: 2 trucks, 17 stops; 85% delivered (43% by drone), last at 11:30, half of all parcels by 10:52, 85% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1007 | 2 | 300 m launch radius: 2 trucks, 22 stops; 88% delivered (38% by drone), last at 11:47, half of all parcels by 10:56, 88% by 14:00; 4.6 truck hours, 10 km, replanned |
| 1007 | 2 | 600 m launch radius: 2 trucks, 20 stops; 87% delivered (38% by drone), last at 11:46, half of all parcels by 11:16, 87% by 14:00; 4.6 truck hours, 10 km, replanned |
| 1007 | 2 | 1000 m launch radius: 2 trucks, 20 stops; 87% delivered (38% by drone), last at 11:46, half of all parcels by 11:16, 87% by 14:00; 4.6 truck hours, 10 km, replanned |
| 1007 | 3 | 300 m launch radius: 2 trucks, 21 stops; 86% delivered (48% by drone), last at 11:32, half of all parcels by 10:42, 86% by 14:00; 4.2 truck hours, 10 km, replanned |
| 1007 | 3 | 600 m launch radius: 2 trucks, 19 stops; 87% delivered (47% by drone), last at 11:38, half of all parcels by 11:05, 87% by 14:00; 4.4 truck hours, 10 km, replanned |
| 1007 | 3 | 1000 m launch radius: 2 trucks, 19 stops; 87% delivered (47% by drone), last at 11:38, half of all parcels by 11:05, 87% by 14:00; 4.4 truck hours, 10 km, replanned |
| 1007 | 4 | 300 m launch radius: 2 trucks, 22 stops; 87% delivered (44% by drone), last at 11:49, half of all parcels by 10:32, 87% by 14:00; 4.7 truck hours, 10 km, replanned |
| 1007 | 4 | 600 m launch radius: 2 trucks, 21 stops; 87% delivered (43% by drone), last at 11:51, half of all parcels by 11:15, 87% by 14:00; 4.8 truck hours, 11 km, replanned |
| 1007 | 4 | 1000 m launch radius: 2 trucks, 21 stops; 87% delivered (43% by drone), last at 11:51, half of all parcels by 11:15, 87% by 14:00; 4.8 truck hours, 11 km, replanned |
| 1008 | 0 | 300 m launch radius: 2 trucks, 24 stops; 88% delivered (48% by drone), last at 11:53, half of all parcels by 10:55, 88% by 14:00; 5.1 truck hours, 11 km, replanned |
| 1008 | 0 | 600 m launch radius: 2 trucks, 21 stops; 86% delivered (46% by drone), last at 11:49, half of all parcels by 11:14, 86% by 14:00; 4.7 truck hours, 10 km, replanned |
| 1008 | 0 | 1000 m launch radius: 2 trucks, 21 stops; 86% delivered (46% by drone), last at 11:49, half of all parcels by 11:14, 86% by 14:00; 4.7 truck hours, 10 km, replanned |
| 1008 | 1 | 300 m launch radius: 2 trucks, 23 stops; 92% delivered (55% by drone), last at 11:36, half of all parcels by 10:47, 92% by 14:00; 4.3 truck hours, 10 km, replanned |
| 1008 | 1 | 600 m launch radius: 2 trucks, 19 stops; 88% delivered (50% by drone), last at 11:36, half of all parcels by 10:57, 88% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1008 | 1 | 1000 m launch radius: 2 trucks, 19 stops; 88% delivered (50% by drone), last at 11:36, half of all parcels by 10:57, 88% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1008 | 2 | 300 m launch radius: 2 trucks, 30 stops; 73% delivered (8% by drone), last at 12:32, half of all parcels by 11:44, 73% by 14:00; 6.2 truck hours, 10 km, replanned |
| 1008 | 2 | 600 m launch radius: 2 trucks, 37 stops; 82% delivered (7% by drone), last at 13:14, half of all parcels by 11:55, 82% by 14:00; 7.5 truck hours, 13 km, replanned |
| 1008 | 2 | 1000 m launch radius: 2 trucks, 37 stops; 82% delivered (7% by drone), last at 13:14, half of all parcels by 11:55, 82% by 14:00; 7.5 truck hours, 13 km, replanned |
| 1008 | 3 | 300 m launch radius: 2 trucks, 26 stops; 88% delivered (46% by drone), last at 12:03, half of all parcels by 10:44, 88% by 14:00; 5.3 truck hours, 10 km, replanned |
| 1008 | 3 | 600 m launch radius: 2 trucks, 23 stops; 89% delivered (47% by drone), last at 11:58, half of all parcels by 11:14, 89% by 14:00; 5.1 truck hours, 11 km, replanned |
| 1008 | 3 | 1000 m launch radius: 2 trucks, 23 stops; 89% delivered (47% by drone), last at 11:58, half of all parcels by 11:14, 89% by 14:00; 5.1 truck hours, 11 km, replanned |
| 1008 | 4 | 300 m launch radius: 2 trucks, 27 stops; 90% delivered (49% by drone), last at 12:04, half of all parcels by 10:43, 90% by 14:00; 5.2 truck hours, 10 km, replanned |
| 1008 | 4 | 600 m launch radius: 2 trucks, 24 stops; 91% delivered (47% by drone), last at 12:06, half of all parcels by 11:36, 91% by 14:00; 5.3 truck hours, 10 km, replanned |
| 1008 | 4 | 1000 m launch radius: 2 trucks, 24 stops; 91% delivered (47% by drone), last at 12:06, half of all parcels by 11:36, 91% by 14:00; 5.3 truck hours, 10 km, replanned |
| 1009 | 0 | 300 m launch radius: 2 trucks, 32 stops; 86% delivered (0% by drone), last at 12:45, half of all parcels by 11:46, 86% by 14:00; 6.6 truck hours, 10 km, replanned |
| 1009 | 0 | 600 m launch radius: 2 trucks, 32 stops; 86% delivered (0% by drone), last at 12:45, half of all parcels by 11:46, 86% by 14:00; 6.6 truck hours, 10 km, replanned |
| 1009 | 0 | 1000 m launch radius: 2 trucks, 32 stops; 86% delivered (0% by drone), last at 12:45, half of all parcels by 11:46, 86% by 14:00; 6.6 truck hours, 10 km, replanned |
| 1009 | 1 | 300 m launch radius: 2 trucks, 22 stops; 91% delivered (43% by drone), last at 11:40, half of all parcels by 10:49, 91% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1009 | 1 | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (44% by drone), last at 11:28, half of all parcels by 10:45, 91% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1009 | 1 | 1000 m launch radius: 2 trucks, 17 stops; 91% delivered (44% by drone), last at 11:28, half of all parcels by 10:45, 91% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1009 | 2 | 300 m launch radius: 2 trucks, 24 stops; 89% delivered (51% by drone), last at 11:42, half of all parcels by 11:04, 89% by 14:00; 4.7 truck hours, 10 km, replanned |
| 1009 | 2 | 600 m launch radius: 2 trucks, 18 stops; 86% delivered (48% by drone), last at 11:30, half of all parcels by 10:42, 86% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1009 | 2 | 1000 m launch radius: 2 trucks, 18 stops; 86% delivered (48% by drone), last at 11:30, half of all parcels by 10:46, 86% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1009 | 3 | 300 m launch radius: 2 trucks, 20 stops; 86% delivered (38% by drone), last at 11:37, half of all parcels by 10:47, 86% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1009 | 3 | 600 m launch radius: 2 trucks, 21 stops; 85% delivered (32% by drone), last at 11:50, half of all parcels by 10:34, 85% by 14:00; 4.8 truck hours, 9 km, replanned |
| 1009 | 3 | 1000 m launch radius: 2 trucks, 21 stops; 85% delivered (32% by drone), last at 11:50, half of all parcels by 10:34, 85% by 14:00; 4.8 truck hours, 9 km, replanned |
| 1009 | 4 | 300 m launch radius: 2 trucks, 35 stops; 85% delivered (0% by drone), last at 13:03, half of all parcels by 11:34, 85% by 14:00; 7.2 truck hours, 12 km, replanned |
| 1009 | 4 | 600 m launch radius: 2 trucks, 35 stops; 85% delivered (0% by drone), last at 13:03, half of all parcels by 11:34, 85% by 14:00; 7.2 truck hours, 12 km, replanned |
| 1009 | 4 | 1000 m launch radius: 2 trucks, 35 stops; 85% delivered (0% by drone), last at 13:03, half of all parcels by 11:34, 85% by 14:00; 7.2 truck hours, 12 km, replanned |
