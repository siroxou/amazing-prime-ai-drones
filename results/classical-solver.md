# Classical truck + drone solver on the held-out days

Written by `python -m baselines.classical --held-out`. 50 days, 500 parcels each, averages over the days. Autonomous trucks with 10 drones and a locker each; a fixed-speed drone model (15 m/s, up to 5 kg, 3 km from the truck). Locker settings as in [trucks-only-baseline.md](trucks-only-baseline.md) with a 10-minute wait. Settings are in `baselines/classical.py`.

| launch radius | 300 m | 600 m | 1000 m |
|---|---|---|---|
| trucks | 2.0 | 2.0 | 2.0 |
| stops | 23 | 20 | 20 |
| parcels delivered today | 90% | 90% | 90% |
| by drone | 46% | 46% | 46% |
| last parcel | 11:52 | 11:45 | 11:45 |
| half of all parcels by | 11:00 | 10:58 | 10:57 |
| delivered by 14:00 | 90% | 90% | 90% |
| truck hours | 4.9 | 4.6 | 4.6 |
| km driven | 10 | 9 | 9 |
| days replanned for weather or airspace | 100% | 100% | 100% |

## Every day

| city | day | result |
|---|---|---|
| 1000 | 0 | 300 m launch radius: 2 trucks, 40 stops; 82% delivered (0% by drone), last at 13:26, half of all parcels by 11:25, 82% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1000 | 0 | 600 m launch radius: 2 trucks, 40 stops; 82% delivered (0% by drone), last at 13:26, half of all parcels by 11:25, 82% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1000 | 0 | 1000 m launch radius: 2 trucks, 40 stops; 82% delivered (0% by drone), last at 13:26, half of all parcels by 11:25, 82% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1000 | 1 | 300 m launch radius: 2 trucks, 21 stops; 92% delivered (57% by drone), last at 11:32, half of all parcels by 11:05, 92% by 14:00; 4.2 truck hours, 10 km, replanned |
| 1000 | 1 | 600 m launch radius: 2 trucks, 15 stops; 92% delivered (57% by drone), last at 11:24, half of all parcels by 10:55, 92% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1000 | 1 | 1000 m launch radius: 2 trucks, 15 stops; 92% delivered (57% by drone), last at 11:24, half of all parcels by 10:55, 92% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1000 | 2 | 300 m launch radius: 2 trucks, 21 stops; 90% delivered (53% by drone), last at 11:41, half of all parcels by 10:54, 90% by 14:00; 4.4 truck hours, 10 km, replanned |
| 1000 | 2 | 600 m launch radius: 2 trucks, 17 stops; 90% delivered (53% by drone), last at 11:26, half of all parcels by 10:46, 90% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1000 | 2 | 1000 m launch radius: 2 trucks, 17 stops; 90% delivered (53% by drone), last at 11:26, half of all parcels by 10:46, 90% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1000 | 3 | 300 m launch radius: 2 trucks, 19 stops; 91% delivered (56% by drone), last at 11:28, half of all parcels by 11:09, 91% by 14:00; 4.0 truck hours, 10 km, replanned |
| 1000 | 3 | 600 m launch radius: 2 trucks, 14 stops; 91% delivered (56% by drone), last at 11:15, half of all parcels by 10:46, 91% by 14:00; 3.6 truck hours, 9 km, replanned |
| 1000 | 3 | 1000 m launch radius: 2 trucks, 14 stops; 91% delivered (56% by drone), last at 11:15, half of all parcels by 10:46, 91% by 14:00; 3.6 truck hours, 9 km, replanned |
| 1000 | 4 | 300 m launch radius: 2 trucks, 20 stops; 93% delivered (55% by drone), last at 11:34, half of all parcels by 10:35, 93% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1000 | 4 | 600 m launch radius: 2 trucks, 17 stops; 93% delivered (55% by drone), last at 11:29, half of all parcels by 10:48, 93% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1000 | 4 | 1000 m launch radius: 2 trucks, 17 stops; 93% delivered (55% by drone), last at 11:29, half of all parcels by 10:48, 93% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1001 | 0 | 300 m launch radius: 2 trucks, 21 stops; 94% delivered (56% by drone), last at 11:42, half of all parcels by 11:00, 94% by 14:00; 4.5 truck hours, 9 km, replanned |
| 1001 | 0 | 600 m launch radius: 2 trucks, 18 stops; 94% delivered (56% by drone), last at 11:35, half of all parcels by 10:51, 94% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1001 | 0 | 1000 m launch radius: 2 trucks, 18 stops; 94% delivered (56% by drone), last at 11:35, half of all parcels by 10:51, 94% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1001 | 1 | 300 m launch radius: 2 trucks, 18 stops; 91% delivered (54% by drone), last at 11:29, half of all parcels by 10:59, 91% by 14:00; 4.0 truck hours, 9 km, replanned |
| 1001 | 1 | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (54% by drone), last at 11:26, half of all parcels by 10:58, 91% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1001 | 1 | 1000 m launch radius: 2 trucks, 16 stops; 91% delivered (54% by drone), last at 11:26, half of all parcels by 10:58, 91% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1001 | 2 | 300 m launch radius: 2 trucks, 21 stops; 93% delivered (57% by drone), last at 11:45, half of all parcels by 10:54, 93% by 14:00; 4.5 truck hours, 10 km, replanned |
| 1001 | 2 | 600 m launch radius: 2 trucks, 18 stops; 93% delivered (57% by drone), last at 11:37, half of all parcels by 10:46, 93% by 14:00; 4.3 truck hours, 8 km, replanned |
| 1001 | 2 | 1000 m launch radius: 2 trucks, 18 stops; 93% delivered (57% by drone), last at 11:37, half of all parcels by 11:07, 93% by 14:00; 4.3 truck hours, 8 km, replanned |
| 1001 | 3 | 300 m launch radius: 2 trucks, 22 stops; 92% delivered (52% by drone), last at 11:48, half of all parcels by 11:12, 92% by 14:00; 4.8 truck hours, 9 km, replanned |
| 1001 | 3 | 600 m launch radius: 2 trucks, 21 stops; 92% delivered (52% by drone), last at 11:47, half of all parcels by 11:09, 92% by 14:00; 4.7 truck hours, 8 km, replanned |
| 1001 | 3 | 1000 m launch radius: 2 trucks, 21 stops; 92% delivered (52% by drone), last at 11:47, half of all parcels by 11:09, 92% by 14:00; 4.7 truck hours, 8 km, replanned |
| 1001 | 4 | 300 m launch radius: 2 trucks, 21 stops; 94% delivered (53% by drone), last at 11:38, half of all parcels by 10:53, 94% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1001 | 4 | 600 m launch radius: 2 trucks, 18 stops; 94% delivered (53% by drone), last at 11:35, half of all parcels by 10:55, 94% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1001 | 4 | 1000 m launch radius: 2 trucks, 18 stops; 94% delivered (53% by drone), last at 11:35, half of all parcels by 10:55, 94% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1002 | 0 | 300 m launch radius: 2 trucks, 21 stops; 93% delivered (57% by drone), last at 11:36, half of all parcels by 10:58, 93% by 14:00; 4.3 truck hours, 10 km, replanned |
| 1002 | 0 | 600 m launch radius: 2 trucks, 16 stops; 93% delivered (57% by drone), last at 11:26, half of all parcels by 10:56, 93% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1002 | 0 | 1000 m launch radius: 2 trucks, 16 stops; 93% delivered (57% by drone), last at 11:26, half of all parcels by 10:56, 93% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1002 | 1 | 300 m launch radius: 2 trucks, 19 stops; 90% delivered (56% by drone), last at 11:32, half of all parcels by 10:43, 90% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1002 | 1 | 600 m launch radius: 2 trucks, 16 stops; 90% delivered (56% by drone), last at 11:26, half of all parcels by 10:45, 90% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1002 | 1 | 1000 m launch radius: 2 trucks, 16 stops; 90% delivered (56% by drone), last at 11:26, half of all parcels by 10:45, 90% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1002 | 2 | 300 m launch radius: 2 trucks, 24 stops; 91% delivered (52% by drone), last at 11:59, half of all parcels by 10:00, 91% by 14:00; 5.0 truck hours, 10 km, replanned |
| 1002 | 2 | 600 m launch radius: 2 trucks, 21 stops; 91% delivered (52% by drone), last at 11:46, half of all parcels by 11:03, 91% by 14:00; 4.8 truck hours, 9 km, replanned |
| 1002 | 2 | 1000 m launch radius: 2 trucks, 21 stops; 91% delivered (52% by drone), last at 11:46, half of all parcels by 11:03, 91% by 14:00; 4.8 truck hours, 9 km, replanned |
| 1002 | 3 | 300 m launch radius: 2 trucks, 40 stops; 84% delivered (0% by drone), last at 13:22, half of all parcels by 11:44, 84% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1002 | 3 | 600 m launch radius: 2 trucks, 40 stops; 84% delivered (0% by drone), last at 13:22, half of all parcels by 11:44, 84% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1002 | 3 | 1000 m launch radius: 2 trucks, 40 stops; 84% delivered (0% by drone), last at 13:22, half of all parcels by 11:44, 84% by 14:00; 8.0 truck hours, 12 km, replanned |
| 1002 | 4 | 300 m launch radius: 2 trucks, 19 stops; 88% delivered (51% by drone), last at 11:31, half of all parcels by 10:37, 88% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1002 | 4 | 600 m launch radius: 2 trucks, 16 stops; 88% delivered (51% by drone), last at 11:25, half of all parcels by 10:34, 88% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1002 | 4 | 1000 m launch radius: 2 trucks, 16 stops; 88% delivered (51% by drone), last at 11:25, half of all parcels by 10:34, 88% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1003 | 0 | 300 m launch radius: 2 trucks, 39 stops; 83% delivered (0% by drone), last at 13:27, half of all parcels by 11:41, 83% by 14:00; 7.8 truck hours, 11 km, replanned |
| 1003 | 0 | 600 m launch radius: 2 trucks, 39 stops; 83% delivered (0% by drone), last at 13:27, half of all parcels by 11:31, 83% by 14:00; 7.8 truck hours, 12 km, replanned |
| 1003 | 0 | 1000 m launch radius: 2 trucks, 39 stops; 83% delivered (0% by drone), last at 13:27, half of all parcels by 11:09, 83% by 14:00; 7.8 truck hours, 12 km, replanned |
| 1003 | 1 | 300 m launch radius: 2 trucks, 23 stops; 92% delivered (58% by drone), last at 11:49, half of all parcels by 10:42, 92% by 14:00; 4.7 truck hours, 9 km, replanned |
| 1003 | 1 | 600 m launch radius: 2 trucks, 20 stops; 92% delivered (58% by drone), last at 11:41, half of all parcels by 11:10, 92% by 14:00; 4.5 truck hours, 9 km, replanned |
| 1003 | 1 | 1000 m launch radius: 2 trucks, 20 stops; 92% delivered (58% by drone), last at 11:41, half of all parcels by 11:10, 92% by 14:00; 4.5 truck hours, 9 km, replanned |
| 1003 | 2 | 300 m launch radius: 2 trucks, 21 stops; 91% delivered (53% by drone), last at 11:37, half of all parcels by 10:43, 91% by 14:00; 4.5 truck hours, 9 km, replanned |
| 1003 | 2 | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (53% by drone), last at 11:29, half of all parcels by 10:55, 91% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1003 | 2 | 1000 m launch radius: 2 trucks, 17 stops; 91% delivered (53% by drone), last at 11:29, half of all parcels by 10:55, 91% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1003 | 3 | 300 m launch radius: 2 trucks, 21 stops; 93% delivered (54% by drone), last at 11:41, half of all parcels by 10:54, 93% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1003 | 3 | 600 m launch radius: 2 trucks, 16 stops; 93% delivered (54% by drone), last at 11:25, half of all parcels by 10:46, 93% by 14:00; 3.9 truck hours, 7 km, replanned |
| 1003 | 3 | 1000 m launch radius: 2 trucks, 16 stops; 93% delivered (54% by drone), last at 11:25, half of all parcels by 10:46, 93% by 14:00; 3.9 truck hours, 7 km, replanned |
| 1003 | 4 | 300 m launch radius: 2 trucks, 19 stops; 91% delivered (57% by drone), last at 11:36, half of all parcels by 10:46, 91% by 14:00; 4.2 truck hours, 9 km, replanned |
| 1003 | 4 | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (57% by drone), last at 11:29, half of all parcels by 10:56, 91% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1003 | 4 | 1000 m launch radius: 2 trucks, 16 stops; 91% delivered (57% by drone), last at 11:26, half of all parcels by 10:52, 91% by 14:00; 3.9 truck hours, 7 km, replanned |
| 1004 | 0 | 300 m launch radius: 2 trucks, 16 stops; 91% delivered (54% by drone), last at 11:18, half of all parcels by 10:41, 91% by 14:00; 3.7 truck hours, 8 km, replanned |
| 1004 | 0 | 600 m launch radius: 2 trucks, 12 stops; 91% delivered (54% by drone), last at 11:07, half of all parcels by 10:34, 91% by 14:00; 3.3 truck hours, 8 km, replanned |
| 1004 | 0 | 1000 m launch radius: 2 trucks, 12 stops; 91% delivered (54% by drone), last at 11:07, half of all parcels by 10:34, 91% by 14:00; 3.3 truck hours, 8 km, replanned |
| 1004 | 1 | 300 m launch radius: 2 trucks, 19 stops; 92% delivered (55% by drone), last at 11:28, half of all parcels by 10:40, 92% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1004 | 1 | 600 m launch radius: 2 trucks, 15 stops; 92% delivered (55% by drone), last at 11:22, half of all parcels by 10:43, 92% by 14:00; 3.7 truck hours, 7 km, replanned |
| 1004 | 1 | 1000 m launch radius: 2 trucks, 15 stops; 92% delivered (55% by drone), last at 11:22, half of all parcels by 10:43, 92% by 14:00; 3.7 truck hours, 7 km, replanned |
| 1004 | 2 | 300 m launch radius: 2 trucks, 24 stops; 91% delivered (52% by drone), last at 12:01, half of all parcels by 10:53, 91% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1004 | 2 | 600 m launch radius: 2 trucks, 22 stops; 91% delivered (52% by drone), last at 11:56, half of all parcels by 11:15, 91% by 14:00; 4.9 truck hours, 9 km, replanned |
| 1004 | 2 | 1000 m launch radius: 2 trucks, 22 stops; 91% delivered (52% by drone), last at 11:56, half of all parcels by 11:15, 91% by 14:00; 4.9 truck hours, 9 km, replanned |
| 1004 | 3 | 300 m launch radius: 2 trucks, 42 stops; 81% delivered (0% by drone), last at 13:32, half of all parcels by 12:36, 81% by 14:00; 8.3 truck hours, 11 km, replanned |
| 1004 | 3 | 600 m launch radius: 2 trucks, 42 stops; 81% delivered (0% by drone), last at 13:32, half of all parcels by 12:36, 81% by 14:00; 8.3 truck hours, 11 km, replanned |
| 1004 | 3 | 1000 m launch radius: 2 trucks, 42 stops; 81% delivered (0% by drone), last at 13:32, half of all parcels by 12:36, 81% by 14:00; 8.3 truck hours, 11 km, replanned |
| 1004 | 4 | 300 m launch radius: 2 trucks, 23 stops; 93% delivered (52% by drone), last at 11:48, half of all parcels by 10:51, 93% by 14:00; 4.7 truck hours, 10 km, replanned |
| 1004 | 4 | 600 m launch radius: 2 trucks, 19 stops; 93% delivered (52% by drone), last at 11:40, half of all parcels by 10:52, 93% by 14:00; 4.4 truck hours, 10 km, replanned |
| 1004 | 4 | 1000 m launch radius: 2 trucks, 19 stops; 93% delivered (52% by drone), last at 11:40, half of all parcels by 10:52, 93% by 14:00; 4.4 truck hours, 10 km, replanned |
| 1005 | 0 | 300 m launch radius: 2 trucks, 22 stops; 92% delivered (56% by drone), last at 11:38, half of all parcels by 10:00, 92% by 14:00; 4.5 truck hours, 11 km, replanned |
| 1005 | 0 | 600 m launch radius: 2 trucks, 17 stops; 92% delivered (56% by drone), last at 11:28, half of all parcels by 10:44, 92% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1005 | 0 | 1000 m launch radius: 2 trucks, 17 stops; 92% delivered (56% by drone), last at 11:28, half of all parcels by 10:44, 92% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1005 | 1 | 300 m launch radius: 2 trucks, 19 stops; 94% delivered (59% by drone), last at 11:35, half of all parcels by 10:54, 94% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1005 | 1 | 600 m launch radius: 2 trucks, 15 stops; 94% delivered (59% by drone), last at 11:25, half of all parcels by 10:39, 94% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1005 | 1 | 1000 m launch radius: 2 trucks, 15 stops; 94% delivered (59% by drone), last at 11:25, half of all parcels by 10:39, 94% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1005 | 2 | 300 m launch radius: 2 trucks, 19 stops; 91% delivered (53% by drone), last at 11:36, half of all parcels by 10:48, 91% by 14:00; 4.3 truck hours, 10 km, replanned |
| 1005 | 2 | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (53% by drone), last at 11:22, half of all parcels by 10:48, 91% by 14:00; 4.0 truck hours, 9 km, replanned |
| 1005 | 2 | 1000 m launch radius: 2 trucks, 16 stops; 91% delivered (53% by drone), last at 11:22, half of all parcels by 10:48, 91% by 14:00; 4.0 truck hours, 9 km, replanned |
| 1005 | 3 | 300 m launch radius: 2 trucks, 19 stops; 92% delivered (53% by drone), last at 11:32, half of all parcels by 10:52, 92% by 14:00; 4.1 truck hours, 10 km, replanned |
| 1005 | 3 | 600 m launch radius: 2 trucks, 16 stops; 92% delivered (53% by drone), last at 11:26, half of all parcels by 10:46, 92% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1005 | 3 | 1000 m launch radius: 2 trucks, 16 stops; 92% delivered (53% by drone), last at 11:26, half of all parcels by 10:46, 92% by 14:00; 3.9 truck hours, 9 km, replanned |
| 1005 | 4 | 300 m launch radius: 2 trucks, 19 stops; 90% delivered (53% by drone), last at 11:28, half of all parcels by 10:47, 90% by 14:00; 4.0 truck hours, 9 km, replanned |
| 1005 | 4 | 600 m launch radius: 2 trucks, 15 stops; 91% delivered (53% by drone), last at 11:19, half of all parcels by 10:44, 91% by 14:00; 3.8 truck hours, 8 km, replanned |
| 1005 | 4 | 1000 m launch radius: 2 trucks, 15 stops; 91% delivered (53% by drone), last at 11:19, half of all parcels by 10:44, 91% by 14:00; 3.8 truck hours, 8 km, replanned |
| 1006 | 0 | 300 m launch radius: 2 trucks, 20 stops; 92% delivered (56% by drone), last at 11:36, half of all parcels by 10:46, 92% by 14:00; 4.2 truck hours, 8 km, replanned |
| 1006 | 0 | 600 m launch radius: 2 trucks, 17 stops; 92% delivered (56% by drone), last at 11:33, half of all parcels by 10:31, 92% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1006 | 0 | 1000 m launch radius: 2 trucks, 17 stops; 92% delivered (56% by drone), last at 11:33, half of all parcels by 10:31, 92% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1006 | 1 | 300 m launch radius: 2 trucks, 19 stops; 91% delivered (57% by drone), last at 11:34, half of all parcels by 10:46, 91% by 14:00; 4.2 truck hours, 9 km, replanned |
| 1006 | 1 | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (57% by drone), last at 11:25, half of all parcels by 10:48, 91% by 14:00; 4.0 truck hours, 9 km, replanned |
| 1006 | 1 | 1000 m launch radius: 2 trucks, 16 stops; 91% delivered (57% by drone), last at 11:25, half of all parcels by 10:43, 91% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1006 | 2 | 300 m launch radius: 2 trucks, 30 stops; 66% delivered (13% by drone), last at 12:34, half of all parcels by 11:06, 66% by 14:00; 6.3 truck hours, 10 km, replanned |
| 1006 | 2 | 600 m launch radius: 2 trucks, 23 stops; 70% delivered (20% by drone), last at 11:59, half of all parcels by 11:03, 70% by 14:00; 5.1 truck hours, 9 km, replanned |
| 1006 | 2 | 1000 m launch radius: 2 trucks, 23 stops; 70% delivered (20% by drone), last at 11:59, half of all parcels by 11:03, 70% by 14:00; 5.1 truck hours, 9 km, replanned |
| 1006 | 3 | 300 m launch radius: 2 trucks, 23 stops; 93% delivered (55% by drone), last at 11:44, half of all parcels by 10:54, 93% by 14:00; 4.7 truck hours, 10 km, replanned |
| 1006 | 3 | 600 m launch radius: 2 trucks, 19 stops; 93% delivered (55% by drone), last at 11:41, half of all parcels by 11:02, 93% by 14:00; 4.5 truck hours, 8 km, replanned |
| 1006 | 3 | 1000 m launch radius: 2 trucks, 19 stops; 93% delivered (55% by drone), last at 11:41, half of all parcels by 11:02, 93% by 14:00; 4.5 truck hours, 8 km, replanned |
| 1006 | 4 | 300 m launch radius: 2 trucks, 21 stops; 91% delivered (53% by drone), last at 11:34, half of all parcels by 10:50, 91% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1006 | 4 | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (53% by drone), last at 11:25, half of all parcels by 10:38, 91% by 14:00; 3.9 truck hours, 7 km, replanned |
| 1006 | 4 | 1000 m launch radius: 2 trucks, 16 stops; 91% delivered (53% by drone), last at 11:25, half of all parcels by 10:38, 91% by 14:00; 3.9 truck hours, 7 km, replanned |
| 1007 | 0 | 300 m launch radius: 2 trucks, 26 stops; 89% delivered (53% by drone), last at 12:03, half of all parcels by 11:16, 89% by 14:00; 5.3 truck hours, 11 km, replanned |
| 1007 | 0 | 600 m launch radius: 2 trucks, 23 stops; 92% delivered (56% by drone), last at 12:00, half of all parcels by 11:08, 92% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1007 | 0 | 1000 m launch radius: 2 trucks, 23 stops; 92% delivered (56% by drone), last at 12:00, half of all parcels by 11:08, 92% by 14:00; 5.1 truck hours, 10 km, replanned |
| 1007 | 1 | 300 m launch radius: 2 trucks, 21 stops; 91% delivered (56% by drone), last at 11:38, half of all parcels by 10:54, 91% by 14:00; 4.3 truck hours, 10 km, replanned |
| 1007 | 1 | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (56% by drone), last at 11:31, half of all parcels by 10:44, 91% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1007 | 1 | 1000 m launch radius: 2 trucks, 17 stops; 91% delivered (56% by drone), last at 11:31, half of all parcels by 10:44, 91% by 14:00; 4.1 truck hours, 8 km, replanned |
| 1007 | 2 | 300 m launch radius: 2 trucks, 21 stops; 91% delivered (47% by drone), last at 11:41, half of all parcels by 10:59, 91% by 14:00; 4.4 truck hours, 10 km, replanned |
| 1007 | 2 | 600 m launch radius: 2 trucks, 18 stops; 91% delivered (47% by drone), last at 11:33, half of all parcels by 10:42, 91% by 14:00; 4.2 truck hours, 9 km, replanned |
| 1007 | 2 | 1000 m launch radius: 2 trucks, 18 stops; 91% delivered (47% by drone), last at 11:33, half of all parcels by 10:42, 91% by 14:00; 4.2 truck hours, 9 km, replanned |
| 1007 | 3 | 300 m launch radius: 2 trucks, 20 stops; 91% delivered (56% by drone), last at 11:31, half of all parcels by 10:43, 91% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1007 | 3 | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (56% by drone), last at 11:23, half of all parcels by 10:32, 91% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1007 | 3 | 1000 m launch radius: 2 trucks, 16 stops; 91% delivered (56% by drone), last at 11:23, half of all parcels by 10:32, 91% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1007 | 4 | 300 m launch radius: 2 trucks, 22 stops; 91% delivered (56% by drone), last at 11:46, half of all parcels by 10:56, 91% by 14:00; 4.6 truck hours, 10 km, replanned |
| 1007 | 4 | 600 m launch radius: 2 trucks, 18 stops; 91% delivered (56% by drone), last at 11:38, half of all parcels by 10:48, 91% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1007 | 4 | 1000 m launch radius: 2 trucks, 18 stops; 91% delivered (56% by drone), last at 11:38, half of all parcels by 10:48, 91% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1008 | 0 | 300 m launch radius: 2 trucks, 20 stops; 89% delivered (53% by drone), last at 11:32, half of all parcels by 10:52, 89% by 14:00; 4.4 truck hours, 10 km, replanned |
| 1008 | 0 | 600 m launch radius: 2 trucks, 17 stops; 89% delivered (53% by drone), last at 11:28, half of all parcels by 10:50, 89% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1008 | 0 | 1000 m launch radius: 2 trucks, 17 stops; 89% delivered (53% by drone), last at 11:28, half of all parcels by 10:50, 89% by 14:00; 4.1 truck hours, 9 km, replanned |
| 1008 | 1 | 300 m launch radius: 2 trucks, 21 stops; 93% delivered (60% by drone), last at 11:38, half of all parcels by 11:03, 93% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1008 | 1 | 600 m launch radius: 2 trucks, 17 stops; 93% delivered (60% by drone), last at 11:28, half of all parcels by 10:42, 93% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1008 | 1 | 1000 m launch radius: 2 trucks, 17 stops; 93% delivered (60% by drone), last at 11:28, half of all parcels by 10:42, 93% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1008 | 2 | 300 m launch radius: 2 trucks, 35 stops; 74% delivered (9% by drone), last at 13:04, half of all parcels by 11:45, 74% by 14:00; 7.2 truck hours, 12 km, replanned |
| 1008 | 2 | 600 m launch radius: 2 trucks, 33 stops; 72% delivered (7% by drone), last at 12:49, half of all parcels by 12:10, 72% by 14:00; 6.8 truck hours, 11 km, replanned |
| 1008 | 2 | 1000 m launch radius: 2 trucks, 33 stops; 72% delivered (7% by drone), last at 12:49, half of all parcels by 12:10, 72% by 14:00; 6.8 truck hours, 11 km, replanned |
| 1008 | 3 | 300 m launch radius: 2 trucks, 20 stops; 90% delivered (55% by drone), last at 11:31, half of all parcels by 10:44, 90% by 14:00; 4.3 truck hours, 10 km, replanned |
| 1008 | 3 | 600 m launch radius: 2 trucks, 17 stops; 90% delivered (55% by drone), last at 11:29, half of all parcels by 10:43, 90% by 14:00; 4.1 truck hours, 10 km, replanned |
| 1008 | 3 | 1000 m launch radius: 2 trucks, 17 stops; 90% delivered (55% by drone), last at 11:29, half of all parcels by 10:43, 90% by 14:00; 4.1 truck hours, 10 km, replanned |
| 1008 | 4 | 300 m launch radius: 2 trucks, 22 stops; 95% delivered (59% by drone), last at 11:48, half of all parcels by 10:53, 95% by 14:00; 4.7 truck hours, 10 km, replanned |
| 1008 | 4 | 600 m launch radius: 2 trucks, 19 stops; 95% delivered (59% by drone), last at 11:44, half of all parcels by 10:53, 95% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1008 | 4 | 1000 m launch radius: 2 trucks, 19 stops; 95% delivered (59% by drone), last at 11:44, half of all parcels by 10:53, 95% by 14:00; 4.4 truck hours, 9 km, replanned |
| 1009 | 0 | 300 m launch radius: 2 trucks, 32 stops; 86% delivered (0% by drone), last at 12:45, half of all parcels by 11:46, 86% by 14:00; 6.6 truck hours, 10 km, replanned |
| 1009 | 0 | 600 m launch radius: 2 trucks, 32 stops; 86% delivered (0% by drone), last at 12:45, half of all parcels by 11:46, 86% by 14:00; 6.6 truck hours, 10 km, replanned |
| 1009 | 0 | 1000 m launch radius: 2 trucks, 32 stops; 86% delivered (0% by drone), last at 12:45, half of all parcels by 11:46, 86% by 14:00; 6.6 truck hours, 10 km, replanned |
| 1009 | 1 | 300 m launch radius: 2 trucks, 21 stops; 91% delivered (50% by drone), last at 11:35, half of all parcels by 11:01, 91% by 14:00; 4.4 truck hours, 10 km, replanned |
| 1009 | 1 | 600 m launch radius: 2 trucks, 17 stops; 91% delivered (50% by drone), last at 11:28, half of all parcels by 10:52, 91% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1009 | 1 | 1000 m launch radius: 2 trucks, 17 stops; 91% delivered (50% by drone), last at 11:28, half of all parcels by 10:52, 91% by 14:00; 4.0 truck hours, 8 km, replanned |
| 1009 | 2 | 300 m launch radius: 2 trucks, 20 stops; 91% delivered (54% by drone), last at 11:37, half of all parcels by 10:41, 91% by 14:00; 4.3 truck hours, 9 km, replanned |
| 1009 | 2 | 600 m launch radius: 2 trucks, 16 stops; 91% delivered (54% by drone), last at 11:27, half of all parcels by 10:36, 91% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1009 | 2 | 1000 m launch radius: 2 trucks, 16 stops; 91% delivered (54% by drone), last at 11:27, half of all parcels by 10:36, 91% by 14:00; 3.9 truck hours, 8 km, replanned |
| 1009 | 3 | 300 m launch radius: 2 trucks, 17 stops; 88% delivered (51% by drone), last at 11:15, half of all parcels by 10:41, 88% by 14:00; 3.6 truck hours, 10 km, replanned |
| 1009 | 3 | 600 m launch radius: 2 trucks, 12 stops; 88% delivered (51% by drone), last at 11:08, half of all parcels by 10:32, 88% by 14:00; 3.3 truck hours, 7 km, replanned |
| 1009 | 3 | 1000 m launch radius: 2 trucks, 12 stops; 88% delivered (51% by drone), last at 11:08, half of all parcels by 10:32, 88% by 14:00; 3.3 truck hours, 7 km, replanned |
| 1009 | 4 | 300 m launch radius: 2 trucks, 35 stops; 85% delivered (0% by drone), last at 13:03, half of all parcels by 11:34, 85% by 14:00; 7.2 truck hours, 12 km, replanned |
| 1009 | 4 | 600 m launch radius: 2 trucks, 35 stops; 85% delivered (0% by drone), last at 13:03, half of all parcels by 11:34, 85% by 14:00; 7.2 truck hours, 12 km, replanned |
| 1009 | 4 | 1000 m launch radius: 2 trucks, 35 stops; 85% delivered (0% by drone), last at 13:03, half of all parcels by 11:34, 85% by 14:00; 7.2 truck hours, 12 km, replanned |
