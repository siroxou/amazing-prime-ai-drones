# Trucks-only baseline on the held-out days

Written by `python -m baselines.trucks_only --held-out`. 50 days, 500 parcels each, averages over the days. Autonomous trucks with 200-compartment lockers and no drones, leaving at 10:00 and back by 19:30. Recipients get 10 minutes' warning and walk at 1.3 m/s on pavements 1.3x the straight line. Collected parcels count as delivered; the rest go back to the station and count as not delivered today.

| truck waits at each point | 10 min | 20 min | 30 min |
|---|---|---|---|
| trucks | 3.0 | 3.0 | 3.0 |
| pickup points | 39 | 39 | 39 |
| parcels collected | 82% | 93% | 97% |
| last parcel collected | 12:17 | 14:28 | 16:38 |
| half of all parcels collected by | 11:23 | 12:23 | 13:18 |
| collected by 14:00 | 82% | 86% | 57% |
| average walk | 90 m | 90 m | 90 m |
| truck hours | 8.5 | 15.0 | 21.6 |
| km driven | 14 | 14 | 14 |

## Every day

| city | day | result |
|---|---|---|
| 1000 | 0 | 10 min wait: 3 trucks, 40 pickup points; 82% collected, last at 12:21, half of all parcels by 11:14, 82% by 14:00; 92 back to the station (0 too far to walk); average walk 95 m; 8.6 truck hours, 14 km |
| 1000 | 0 | 20 min wait: 3 trucks, 40 pickup points; 94% collected, last at 14:31, half of all parcels by 12:32, 87% by 14:00; 31 back to the station (0 too far to walk); average walk 95 m; 15.2 truck hours, 14 km |
| 1000 | 0 | 30 min wait: 3 trucks, 40 pickup points; 97% collected, last at 16:41, half of all parcels by 14:11, 43% by 14:00; 15 back to the station (0 too far to walk); average walk 95 m; 21.9 truck hours, 14 km |
| 1000 | 1 | 10 min wait: 3 trucks, 36 pickup points; 81% collected, last at 12:01, half of all parcels by 10:47, 81% by 14:00; 97 back to the station (0 too far to walk); average walk 96 m; 7.9 truck hours, 14 km |
| 1000 | 1 | 20 min wait: 3 trucks, 36 pickup points; 90% collected, last at 13:54, half of all parcels by 11:30, 90% by 14:00; 49 back to the station (0 too far to walk); average walk 96 m; 13.9 truck hours, 15 km |
| 1000 | 1 | 30 min wait: 3 trucks, 36 pickup points; 96% collected, last at 16:01, half of all parcels by 12:44, 64% by 14:00; 22 back to the station (0 too far to walk); average walk 96 m; 19.9 truck hours, 15 km |
| 1000 | 2 | 10 min wait: 3 trucks, 41 pickup points; 80% collected, last at 12:22, half of all parcels by 10:58, 80% by 14:00; 99 back to the station (1 too far to walk); average walk 81 m; 8.8 truck hours, 15 km |
| 1000 | 2 | 20 min wait: 3 trucks, 41 pickup points; 94% collected, last at 14:33, half of all parcels by 12:38, 78% by 14:00; 29 back to the station (1 too far to walk); average walk 81 m; 15.6 truck hours, 15 km |
| 1000 | 2 | 30 min wait: 3 trucks, 41 pickup points; 97% collected, last at 16:49, half of all parcels by 13:06, 67% by 14:00; 16 back to the station (1 too far to walk); average walk 81 m; 22.5 truck hours, 17 km |
| 1000 | 3 | 10 min wait: 3 trucks, 36 pickup points; 83% collected, last at 12:04, half of all parcels by 11:36, 83% by 14:00; 84 back to the station (4 too far to walk); average walk 96 m; 7.9 truck hours, 14 km |
| 1000 | 3 | 20 min wait: 3 trucks, 36 pickup points; 95% collected, last at 14:04, half of all parcels by 12:45, 94% by 14:00; 25 back to the station (4 too far to walk); average walk 96 m; 13.9 truck hours, 14 km |
| 1000 | 3 | 30 min wait: 3 trucks, 36 pickup points; 98% collected, last at 16:03, half of all parcels by 12:33, 70% by 14:00; 11 back to the station (4 too far to walk); average walk 96 m; 19.9 truck hours, 14 km |
| 1000 | 4 | 10 min wait: 3 trucks, 39 pickup points; 84% collected, last at 12:16, half of all parcels by 11:04, 84% by 14:00; 79 back to the station (0 too far to walk); average walk 90 m; 8.4 truck hours, 13 km |
| 1000 | 4 | 20 min wait: 3 trucks, 39 pickup points; 96% collected, last at 14:26, half of all parcels by 11:44, 90% by 14:00; 22 back to the station (0 too far to walk); average walk 90 m; 14.9 truck hours, 14 km |
| 1000 | 4 | 30 min wait: 3 trucks, 39 pickup points; 98% collected, last at 16:27, half of all parcels by 12:09, 70% by 14:00; 11 back to the station (0 too far to walk); average walk 90 m; 21.4 truck hours, 14 km |
| 1001 | 0 | 10 min wait: 3 trucks, 37 pickup points; 82% collected, last at 12:13, half of all parcels by 11:02, 82% by 14:00; 91 back to the station (0 too far to walk); average walk 85 m; 8.0 truck hours, 13 km |
| 1001 | 0 | 20 min wait: 3 trucks, 37 pickup points; 95% collected, last at 14:23, half of all parcels by 11:42, 93% by 14:00; 26 back to the station (0 too far to walk); average walk 85 m; 14.2 truck hours, 13 km |
| 1001 | 0 | 30 min wait: 3 trucks, 37 pickup points; 97% collected, last at 16:19, half of all parcels by 13:50, 51% by 14:00; 16 back to the station (0 too far to walk); average walk 85 m; 20.4 truck hours, 13 km |
| 1001 | 1 | 10 min wait: 3 trucks, 40 pickup points; 81% collected, last at 12:17, half of all parcels by 11:37, 81% by 14:00; 94 back to the station (0 too far to walk); average walk 87 m; 8.5 truck hours, 13 km |
| 1001 | 1 | 20 min wait: 3 trucks, 40 pickup points; 96% collected, last at 14:44, half of all parcels by 12:04, 84% by 14:00; 20 back to the station (0 too far to walk); average walk 87 m; 15.2 truck hours, 13 km |
| 1001 | 1 | 30 min wait: 3 trucks, 40 pickup points; 99% collected, last at 16:54, half of all parcels by 13:35, 53% by 14:00; 7 back to the station (0 too far to walk); average walk 87 m; 21.9 truck hours, 13 km |
| 1001 | 2 | 10 min wait: 3 trucks, 40 pickup points; 84% collected, last at 12:22, half of all parcels by 11:16, 84% by 14:00; 82 back to the station (2 too far to walk); average walk 97 m; 8.6 truck hours, 14 km |
| 1001 | 2 | 20 min wait: 3 trucks, 40 pickup points; 94% collected, last at 14:39, half of all parcels by 13:01, 83% by 14:00; 32 back to the station (2 too far to walk); average walk 97 m; 15.2 truck hours, 14 km |
| 1001 | 2 | 30 min wait: 3 trucks, 40 pickup points; 98% collected, last at 16:55, half of all parcels by 14:06, 46% by 14:00; 9 back to the station (2 too far to walk); average walk 97 m; 21.9 truck hours, 14 km |
| 1001 | 3 | 10 min wait: 3 trucks, 41 pickup points; 83% collected, last at 12:20, half of all parcels by 11:13, 83% by 14:00; 85 back to the station (0 too far to walk); average walk 82 m; 8.7 truck hours, 14 km |
| 1001 | 3 | 20 min wait: 3 trucks, 41 pickup points; 94% collected, last at 14:44, half of all parcels by 11:46, 88% by 14:00; 31 back to the station (0 too far to walk); average walk 82 m; 15.6 truck hours, 14 km |
| 1001 | 3 | 30 min wait: 3 trucks, 41 pickup points; 98% collected, last at 16:47, half of all parcels by 13:03, 65% by 14:00; 10 back to the station (0 too far to walk); average walk 82 m; 22.5 truck hours, 15 km |
| 1001 | 4 | 10 min wait: 3 trucks, 37 pickup points; 85% collected, last at 12:15, half of all parcels by 11:13, 85% by 14:00; 77 back to the station (5 too far to walk); average walk 90 m; 8.0 truck hours, 13 km |
| 1001 | 4 | 20 min wait: 3 trucks, 37 pickup points; 93% collected, last at 14:15, half of all parcels by 11:54, 90% by 14:00; 37 back to the station (5 too far to walk); average walk 90 m; 14.2 truck hours, 13 km |
| 1001 | 4 | 30 min wait: 3 trucks, 37 pickup points; 98% collected, last at 16:15, half of all parcels by 14:06, 45% by 14:00; 12 back to the station (5 too far to walk); average walk 90 m; 20.4 truck hours, 14 km |
| 1002 | 0 | 10 min wait: 3 trucks, 38 pickup points; 83% collected, last at 12:14, half of all parcels by 11:21, 83% by 14:00; 85 back to the station (2 too far to walk); average walk 95 m; 8.2 truck hours, 15 km |
| 1002 | 0 | 20 min wait: 3 trucks, 38 pickup points; 94% collected, last at 14:17, half of all parcels by 12:24, 90% by 14:00; 30 back to the station (2 too far to walk); average walk 95 m; 14.6 truck hours, 15 km |
| 1002 | 0 | 30 min wait: 3 trucks, 38 pickup points; 97% collected, last at 16:25, half of all parcels by 14:04, 48% by 14:00; 17 back to the station (2 too far to walk); average walk 95 m; 20.9 truck hours, 14 km |
| 1002 | 1 | 10 min wait: 3 trucks, 42 pickup points; 81% collected, last at 12:27, half of all parcels by 11:44, 81% by 14:00; 96 back to the station (2 too far to walk); average walk 89 m; 8.9 truck hours, 14 km |
| 1002 | 1 | 20 min wait: 3 trucks, 42 pickup points; 94% collected, last at 14:41, half of all parcels by 13:05, 73% by 14:00; 29 back to the station (2 too far to walk); average walk 89 m; 15.9 truck hours, 14 km |
| 1002 | 1 | 30 min wait: 3 trucks, 42 pickup points; 98% collected, last at 16:57, half of all parcels by 12:03, 69% by 14:00; 9 back to the station (2 too far to walk); average walk 89 m; 22.9 truck hours, 15 km |
| 1002 | 2 | 10 min wait: 3 trucks, 42 pickup points; 81% collected, last at 12:26, half of all parcels by 11:36, 81% by 14:00; 94 back to the station (2 too far to walk); average walk 87 m; 8.9 truck hours, 15 km |
| 1002 | 2 | 20 min wait: 3 trucks, 42 pickup points; 92% collected, last at 14:45, half of all parcels by 13:06, 82% by 14:00; 38 back to the station (2 too far to walk); average walk 87 m; 15.9 truck hours, 15 km |
| 1002 | 2 | 30 min wait: 3 trucks, 42 pickup points; 97% collected, last at 17:06, half of all parcels by 13:04, 58% by 14:00; 15 back to the station (2 too far to walk); average walk 87 m; 23.0 truck hours, 15 km |
| 1002 | 3 | 10 min wait: 3 trucks, 40 pickup points; 84% collected, last at 12:16, half of all parcels by 11:25, 84% by 14:00; 82 back to the station (3 too far to walk); average walk 91 m; 8.6 truck hours, 14 km |
| 1002 | 3 | 20 min wait: 3 trucks, 40 pickup points; 95% collected, last at 14:30, half of all parcels by 13:04, 87% by 14:00; 27 back to the station (3 too far to walk); average walk 91 m; 15.2 truck hours, 14 km |
| 1002 | 3 | 30 min wait: 3 trucks, 40 pickup points; 97% collected, last at 16:45, half of all parcels by 14:34, 33% by 14:00; 14 back to the station (3 too far to walk); average walk 91 m; 21.9 truck hours, 14 km |
| 1002 | 4 | 10 min wait: 3 trucks, 37 pickup points; 78% collected, last at 12:06, half of all parcels by 11:36, 78% by 14:00; 110 back to the station (2 too far to walk); average walk 88 m; 8.0 truck hours, 13 km |
| 1002 | 4 | 20 min wait: 3 trucks, 37 pickup points; 92% collected, last at 14:05, half of all parcels by 12:27, 91% by 14:00; 41 back to the station (2 too far to walk); average walk 88 m; 14.2 truck hours, 13 km |
| 1002 | 4 | 30 min wait: 3 trucks, 37 pickup points; 97% collected, last at 16:20, half of all parcels by 14:03, 49% by 14:00; 17 back to the station (2 too far to walk); average walk 88 m; 20.4 truck hours, 14 km |
| 1003 | 0 | 10 min wait: 3 trucks, 39 pickup points; 83% collected, last at 12:17, half of all parcels by 11:15, 83% by 14:00; 87 back to the station (1 too far to walk); average walk 90 m; 8.4 truck hours, 15 km |
| 1003 | 0 | 20 min wait: 3 trucks, 39 pickup points; 94% collected, last at 14:23, half of all parcels by 12:07, 80% by 14:00; 28 back to the station (1 too far to walk); average walk 90 m; 14.9 truck hours, 14 km |
| 1003 | 0 | 30 min wait: 3 trucks, 39 pickup points; 97% collected, last at 16:34, half of all parcels by 13:42, 51% by 14:00; 13 back to the station (1 too far to walk); average walk 90 m; 21.4 truck hours, 14 km |
| 1003 | 1 | 10 min wait: 3 trucks, 45 pickup points; 80% collected, last at 12:35, half of all parcels by 11:56, 80% by 14:00; 98 back to the station (1 too far to walk); average walk 86 m; 9.4 truck hours, 14 km |
| 1003 | 1 | 20 min wait: 3 trucks, 45 pickup points; 95% collected, last at 15:03, half of all parcels by 12:04, 80% by 14:00; 27 back to the station (1 too far to walk); average walk 86 m; 16.9 truck hours, 14 km |
| 1003 | 1 | 30 min wait: 3 trucks, 45 pickup points; 97% collected, last at 17:22, half of all parcels by 12:11, 65% by 14:00; 13 back to the station (1 too far to walk); average walk 86 m; 24.5 truck hours, 15 km |
| 1003 | 2 | 10 min wait: 3 trucks, 41 pickup points; 80% collected, last at 12:23, half of all parcels by 11:01, 80% by 14:00; 102 back to the station (3 too far to walk); average walk 80 m; 8.7 truck hours, 14 km |
| 1003 | 2 | 20 min wait: 3 trucks, 41 pickup points; 91% collected, last at 14:45, half of all parcels by 13:08, 79% by 14:00; 43 back to the station (3 too far to walk); average walk 80 m; 15.6 truck hours, 15 km |
| 1003 | 2 | 30 min wait: 3 trucks, 41 pickup points; 97% collected, last at 16:56, half of all parcels by 12:09, 63% by 14:00; 15 back to the station (3 too far to walk); average walk 80 m; 22.5 truck hours, 15 km |
| 1003 | 3 | 10 min wait: 3 trucks, 43 pickup points; 86% collected, last at 12:28, half of all parcels by 11:37, 86% by 14:00; 70 back to the station (2 too far to walk); average walk 87 m; 9.1 truck hours, 15 km |
| 1003 | 3 | 20 min wait: 3 trucks, 43 pickup points; 95% collected, last at 14:57, half of all parcels by 12:24, 81% by 14:00; 26 back to the station (2 too far to walk); average walk 87 m; 16.2 truck hours, 14 km |
| 1003 | 3 | 30 min wait: 3 trucks, 43 pickup points; 97% collected, last at 17:34, half of all parcels by 14:38, 31% by 14:00; 15 back to the station (2 too far to walk); average walk 87 m; 23.5 truck hours, 15 km |
| 1003 | 4 | 10 min wait: 3 trucks, 45 pickup points; 81% collected, last at 12:35, half of all parcels by 11:46, 81% by 14:00; 97 back to the station (2 too far to walk); average walk 87 m; 9.4 truck hours, 15 km |
| 1003 | 4 | 20 min wait: 3 trucks, 45 pickup points; 92% collected, last at 15:02, half of all parcels by 11:00, 78% by 14:00; 38 back to the station (2 too far to walk); average walk 87 m; 16.9 truck hours, 15 km |
| 1003 | 4 | 30 min wait: 3 trucks, 45 pickup points; 96% collected, last at 17:23, half of all parcels by 14:04, 49% by 14:00; 19 back to the station (2 too far to walk); average walk 87 m; 24.5 truck hours, 15 km |
| 1004 | 0 | 10 min wait: 3 trucks, 37 pickup points; 78% collected, last at 12:05, half of all parcels by 11:35, 78% by 14:00; 109 back to the station (5 too far to walk); average walk 100 m; 8.0 truck hours, 13 km |
| 1004 | 0 | 20 min wait: 3 trucks, 37 pickup points; 91% collected, last at 14:12, half of all parcels by 12:03, 90% by 14:00; 43 back to the station (5 too far to walk); average walk 100 m; 14.2 truck hours, 14 km |
| 1004 | 0 | 30 min wait: 3 trucks, 37 pickup points; 97% collected, last at 16:05, half of all parcels by 13:05, 61% by 14:00; 15 back to the station (5 too far to walk); average walk 100 m; 20.4 truck hours, 14 km |
| 1004 | 1 | 10 min wait: 3 trucks, 35 pickup points; 81% collected, last at 12:05, half of all parcels by 11:24, 81% by 14:00; 93 back to the station (4 too far to walk); average walk 88 m; 7.7 truck hours, 14 km |
| 1004 | 1 | 20 min wait: 3 trucks, 35 pickup points; 92% collected, last at 13:53, half of all parcels by 11:22, 92% by 14:00; 39 back to the station (4 too far to walk); average walk 88 m; 13.5 truck hours, 13 km |
| 1004 | 1 | 30 min wait: 3 trucks, 35 pickup points; 96% collected, last at 16:03, half of all parcels by 12:49, 64% by 14:00; 20 back to the station (4 too far to walk); average walk 88 m; 19.4 truck hours, 13 km |
| 1004 | 2 | 10 min wait: 3 trucks, 39 pickup points; 80% collected, last at 12:16, half of all parcels by 11:15, 80% by 14:00; 101 back to the station (1 too far to walk); average walk 84 m; 8.4 truck hours, 14 km |
| 1004 | 2 | 20 min wait: 3 trucks, 39 pickup points; 94% collected, last at 14:27, half of all parcels by 12:10, 86% by 14:00; 30 back to the station (1 too far to walk); average walk 84 m; 14.9 truck hours, 15 km |
| 1004 | 2 | 30 min wait: 3 trucks, 39 pickup points; 98% collected, last at 16:28, half of all parcels by 12:19, 77% by 14:00; 11 back to the station (1 too far to walk); average walk 84 m; 21.5 truck hours, 14 km |
| 1004 | 3 | 10 min wait: 3 trucks, 42 pickup points; 81% collected, last at 12:20, half of all parcels by 11:25, 81% by 14:00; 97 back to the station (1 too far to walk); average walk 80 m; 8.9 truck hours, 13 km |
| 1004 | 3 | 20 min wait: 3 trucks, 42 pickup points; 92% collected, last at 14:39, half of all parcels by 11:44, 84% by 14:00; 39 back to the station (1 too far to walk); average walk 80 m; 15.8 truck hours, 13 km |
| 1004 | 3 | 30 min wait: 3 trucks, 42 pickup points; 98% collected, last at 16:00, half of all parcels by 12:33, 66% by 14:00; 12 back to the station (1 too far to walk); average walk 80 m; 22.9 truck hours, 12 km |
| 1004 | 4 | 10 min wait: 3 trucks, 42 pickup points; 83% collected, last at 12:24, half of all parcels by 11:56, 83% by 14:00; 84 back to the station (1 too far to walk); average walk 85 m; 8.9 truck hours, 14 km |
| 1004 | 4 | 20 min wait: 3 trucks, 42 pickup points; 93% collected, last at 14:42, half of all parcels by 12:44, 84% by 14:00; 33 back to the station (1 too far to walk); average walk 85 m; 15.9 truck hours, 14 km |
| 1004 | 4 | 30 min wait: 3 trucks, 42 pickup points; 96% collected, last at 16:59, half of all parcels by 12:33, 65% by 14:00; 19 back to the station (1 too far to walk); average walk 85 m; 22.9 truck hours, 14 km |
| 1005 | 0 | 10 min wait: 3 trucks, 45 pickup points; 76% collected, last at 12:36, half of all parcels by 11:59, 76% by 14:00; 118 back to the station (0 too far to walk); average walk 90 m; 9.4 truck hours, 15 km |
| 1005 | 0 | 20 min wait: 3 trucks, 45 pickup points; 91% collected, last at 15:07, half of all parcels by 12:45, 82% by 14:00; 46 back to the station (0 too far to walk); average walk 90 m; 17.0 truck hours, 15 km |
| 1005 | 0 | 30 min wait: 3 trucks, 45 pickup points; 95% collected, last at 17:31, half of all parcels by 14:38, 38% by 14:00; 23 back to the station (0 too far to walk); average walk 90 m; 24.5 truck hours, 15 km |
| 1005 | 1 | 10 min wait: 3 trucks, 41 pickup points; 81% collected, last at 12:20, half of all parcels by 11:03, 81% by 14:00; 97 back to the station (5 too far to walk); average walk 90 m; 8.8 truck hours, 15 km |
| 1005 | 1 | 20 min wait: 3 trucks, 41 pickup points; 94% collected, last at 14:31, half of all parcels by 11:50, 87% by 14:00; 29 back to the station (5 too far to walk); average walk 90 m; 15.6 truck hours, 15 km |
| 1005 | 1 | 30 min wait: 3 trucks, 41 pickup points; 97% collected, last at 16:53, half of all parcels by 12:39, 67% by 14:00; 14 back to the station (5 too far to walk); average walk 90 m; 22.5 truck hours, 16 km |
| 1005 | 2 | 10 min wait: 3 trucks, 36 pickup points; 82% collected, last at 12:07, half of all parcels by 11:04, 82% by 14:00; 92 back to the station (7 too far to walk); average walk 91 m; 7.9 truck hours, 14 km |
| 1005 | 2 | 20 min wait: 3 trucks, 36 pickup points; 92% collected, last at 14:05, half of all parcels by 13:05, 92% by 14:00; 39 back to the station (7 too far to walk); average walk 91 m; 13.9 truck hours, 13 km |
| 1005 | 2 | 30 min wait: 3 trucks, 36 pickup points; 95% collected, last at 16:05, half of all parcels by 14:35, 43% by 14:00; 26 back to the station (7 too far to walk); average walk 91 m; 19.9 truck hours, 13 km |
| 1005 | 3 | 10 min wait: 3 trucks, 40 pickup points; 82% collected, last at 12:23, half of all parcels by 10:57, 82% by 14:00; 91 back to the station (3 too far to walk); average walk 87 m; 8.6 truck hours, 15 km |
| 1005 | 3 | 20 min wait: 3 trucks, 40 pickup points; 93% collected, last at 14:33, half of all parcels by 12:53, 90% by 14:00; 35 back to the station (3 too far to walk); average walk 87 m; 15.2 truck hours, 15 km |
| 1005 | 3 | 30 min wait: 3 trucks, 40 pickup points; 97% collected, last at 16:51, half of all parcels by 12:02, 72% by 14:00; 14 back to the station (3 too far to walk); average walk 87 m; 21.9 truck hours, 15 km |
| 1005 | 4 | 10 min wait: 3 trucks, 36 pickup points; 81% collected, last at 12:06, half of all parcels by 11:16, 81% by 14:00; 95 back to the station (1 too far to walk); average walk 89 m; 7.9 truck hours, 14 km |
| 1005 | 4 | 20 min wait: 3 trucks, 36 pickup points; 93% collected, last at 14:03, half of all parcels by 11:42, 92% by 14:00; 36 back to the station (1 too far to walk); average walk 89 m; 13.9 truck hours, 14 km |
| 1005 | 4 | 30 min wait: 3 trucks, 36 pickup points; 95% collected, last at 16:02, half of all parcels by 12:06, 78% by 14:00; 25 back to the station (1 too far to walk); average walk 89 m; 19.9 truck hours, 14 km |
| 1006 | 0 | 10 min wait: 3 trucks, 37 pickup points; 80% collected, last at 12:10, half of all parcels by 11:16, 80% by 14:00; 98 back to the station (0 too far to walk); average walk 97 m; 8.1 truck hours, 14 km |
| 1006 | 0 | 20 min wait: 3 trucks, 37 pickup points; 94% collected, last at 14:16, half of all parcels by 13:04, 92% by 14:00; 31 back to the station (0 too far to walk); average walk 97 m; 14.2 truck hours, 14 km |
| 1006 | 0 | 30 min wait: 3 trucks, 37 pickup points; 97% collected, last at 16:16, half of all parcels by 14:03, 50% by 14:00; 15 back to the station (0 too far to walk); average walk 97 m; 20.4 truck hours, 14 km |
| 1006 | 1 | 10 min wait: 3 trucks, 40 pickup points; 81% collected, last at 12:23, half of all parcels by 11:17, 81% by 14:00; 97 back to the station (4 too far to walk); average walk 91 m; 8.6 truck hours, 14 km |
| 1006 | 1 | 20 min wait: 3 trucks, 40 pickup points; 93% collected, last at 14:26, half of all parcels by 12:22, 83% by 14:00; 37 back to the station (4 too far to walk); average walk 91 m; 15.3 truck hours, 15 km |
| 1006 | 1 | 30 min wait: 3 trucks, 40 pickup points; 96% collected, last at 16:39, half of all parcels by 12:33, 70% by 14:00; 21 back to the station (4 too far to walk); average walk 91 m; 22.0 truck hours, 15 km |
| 1006 | 2 | 10 min wait: 3 trucks, 39 pickup points; 84% collected, last at 12:16, half of all parcels by 11:38, 84% by 14:00; 81 back to the station (4 too far to walk); average walk 91 m; 8.5 truck hours, 14 km |
| 1006 | 2 | 20 min wait: 3 trucks, 39 pickup points; 96% collected, last at 14:25, half of all parcels by 12:44, 84% by 14:00; 22 back to the station (4 too far to walk); average walk 91 m; 14.9 truck hours, 14 km |
| 1006 | 2 | 30 min wait: 3 trucks, 39 pickup points; 98% collected, last at 16:32, half of all parcels by 13:11, 57% by 14:00; 12 back to the station (4 too far to walk); average walk 91 m; 21.5 truck hours, 15 km |
| 1006 | 3 | 10 min wait: 3 trucks, 40 pickup points; 81% collected, last at 12:19, half of all parcels by 11:36, 81% by 14:00; 94 back to the station (1 too far to walk); average walk 84 m; 8.6 truck hours, 14 km |
| 1006 | 3 | 20 min wait: 3 trucks, 40 pickup points; 95% collected, last at 14:29, half of all parcels by 13:07, 83% by 14:00; 26 back to the station (1 too far to walk); average walk 84 m; 15.3 truck hours, 15 km |
| 1006 | 3 | 30 min wait: 3 trucks, 40 pickup points; 98% collected, last at 16:57, half of all parcels by 13:02, 62% by 14:00; 12 back to the station (1 too far to walk); average walk 84 m; 22.0 truck hours, 15 km |
| 1006 | 4 | 10 min wait: 3 trucks, 42 pickup points; 84% collected, last at 12:26, half of all parcels by 11:38, 84% by 14:00; 82 back to the station (0 too far to walk); average walk 87 m; 8.9 truck hours, 14 km |
| 1006 | 4 | 20 min wait: 3 trucks, 42 pickup points; 95% collected, last at 14:35, half of all parcels by 13:15, 82% by 14:00; 26 back to the station (0 too far to walk); average walk 87 m; 15.9 truck hours, 14 km |
| 1006 | 4 | 30 min wait: 3 trucks, 42 pickup points; 98% collected, last at 16:51, half of all parcels by 13:33, 55% by 14:00; 12 back to the station (0 too far to walk); average walk 87 m; 22.9 truck hours, 14 km |
| 1007 | 0 | 10 min wait: 3 trucks, 44 pickup points; 82% collected, last at 12:32, half of all parcels by 11:13, 82% by 14:00; 92 back to the station (3 too far to walk); average walk 83 m; 9.3 truck hours, 15 km |
| 1007 | 0 | 20 min wait: 3 trucks, 44 pickup points; 93% collected, last at 15:07, half of all parcels by 12:56, 78% by 14:00; 34 back to the station (3 too far to walk); average walk 83 m; 16.7 truck hours, 16 km |
| 1007 | 0 | 30 min wait: 3 trucks, 44 pickup points; 97% collected, last at 17:35, half of all parcels by 13:37, 54% by 14:00; 13 back to the station (3 too far to walk); average walk 83 m; 24.0 truck hours, 15 km |
| 1007 | 1 | 10 min wait: 3 trucks, 36 pickup points; 80% collected, last at 12:06, half of all parcels by 11:25, 80% by 14:00; 99 back to the station (4 too far to walk); average walk 96 m; 7.9 truck hours, 13 km |
| 1007 | 1 | 20 min wait: 3 trucks, 36 pickup points; 92% collected, last at 13:00, half of all parcels by 11:26, 92% by 14:00; 42 back to the station (4 too far to walk); average walk 96 m; 13.9 truck hours, 14 km |
| 1007 | 1 | 30 min wait: 3 trucks, 36 pickup points; 97% collected, last at 15:58, half of all parcels by 13:04, 60% by 14:00; 17 back to the station (4 too far to walk); average walk 96 m; 19.9 truck hours, 14 km |
| 1007 | 2 | 10 min wait: 3 trucks, 43 pickup points; 83% collected, last at 12:31, half of all parcels by 11:45, 83% by 14:00; 83 back to the station (2 too far to walk); average walk 83 m; 9.1 truck hours, 15 km |
| 1007 | 2 | 20 min wait: 3 trucks, 43 pickup points; 94% collected, last at 14:57, half of all parcels by 13:04, 83% by 14:00; 28 back to the station (2 too far to walk); average walk 83 m; 16.3 truck hours, 15 km |
| 1007 | 2 | 30 min wait: 3 trucks, 43 pickup points; 96% collected, last at 17:17, half of all parcels by 15:07, 27% by 14:00; 18 back to the station (2 too far to walk); average walk 83 m; 23.5 truck hours, 15 km |
| 1007 | 3 | 10 min wait: 3 trucks, 34 pickup points; 82% collected, last at 12:04, half of all parcels by 11:16, 82% by 14:00; 91 back to the station (2 too far to walk); average walk 102 m; 7.5 truck hours, 13 km |
| 1007 | 3 | 20 min wait: 3 trucks, 34 pickup points; 92% collected, last at 14:04, half of all parcels by 11:41, 92% by 14:00; 39 back to the station (2 too far to walk); average walk 102 m; 13.2 truck hours, 14 km |
| 1007 | 3 | 30 min wait: 3 trucks, 34 pickup points; 96% collected, last at 15:54, half of all parcels by 12:39, 68% by 14:00; 18 back to the station (2 too far to walk); average walk 102 m; 18.9 truck hours, 13 km |
| 1007 | 4 | 10 min wait: 3 trucks, 42 pickup points; 83% collected, last at 12:26, half of all parcels by 11:56, 83% by 14:00; 83 back to the station (2 too far to walk); average walk 93 m; 8.9 truck hours, 15 km |
| 1007 | 4 | 20 min wait: 3 trucks, 42 pickup points; 92% collected, last at 14:42, half of all parcels by 12:10, 79% by 14:00; 38 back to the station (2 too far to walk); average walk 93 m; 15.9 truck hours, 14 km |
| 1007 | 4 | 30 min wait: 3 trucks, 42 pickup points; 96% collected, last at 17:02, half of all parcels by 13:47, 50% by 14:00; 22 back to the station (2 too far to walk); average walk 93 m; 23.0 truck hours, 15 km |
| 1008 | 0 | 10 min wait: 3 trucks, 37 pickup points; 80% collected, last at 12:07, half of all parcels by 11:13, 80% by 14:00; 99 back to the station (0 too far to walk); average walk 89 m; 8.1 truck hours, 15 km |
| 1008 | 0 | 20 min wait: 3 trucks, 37 pickup points; 93% collected, last at 14:16, half of all parcels by 11:44, 92% by 14:00; 37 back to the station (0 too far to walk); average walk 89 m; 14.2 truck hours, 15 km |
| 1008 | 0 | 30 min wait: 3 trucks, 37 pickup points; 97% collected, last at 16:05, half of all parcels by 12:09, 79% by 14:00; 14 back to the station (0 too far to walk); average walk 89 m; 20.4 truck hours, 14 km |
| 1008 | 1 | 10 min wait: 3 trucks, 41 pickup points; 84% collected, last at 12:19, half of all parcels by 11:04, 84% by 14:00; 81 back to the station (7 too far to walk); average walk 95 m; 8.7 truck hours, 15 km |
| 1008 | 1 | 20 min wait: 3 trucks, 41 pickup points; 94% collected, last at 14:42, half of all parcels by 12:34, 87% by 14:00; 29 back to the station (7 too far to walk); average walk 95 m; 15.6 truck hours, 15 km |
| 1008 | 1 | 30 min wait: 3 trucks, 41 pickup points; 97% collected, last at 16:52, half of all parcels by 13:55, 51% by 14:00; 13 back to the station (7 too far to walk); average walk 95 m; 22.5 truck hours, 15 km |
| 1008 | 2 | 10 min wait: 3 trucks, 38 pickup points; 82% collected, last at 12:16, half of all parcels by 11:16, 82% by 14:00; 91 back to the station (1 too far to walk); average walk 84 m; 8.2 truck hours, 15 km |
| 1008 | 2 | 20 min wait: 3 trucks, 38 pickup points; 94% collected, last at 14:19, half of all parcels by 11:45, 91% by 14:00; 28 back to the station (1 too far to walk); average walk 84 m; 14.6 truck hours, 15 km |
| 1008 | 2 | 30 min wait: 3 trucks, 38 pickup points; 98% collected, last at 16:16, half of all parcels by 14:04, 46% by 14:00; 10 back to the station (1 too far to walk); average walk 84 m; 20.9 truck hours, 15 km |
| 1008 | 3 | 10 min wait: 3 trucks, 40 pickup points; 82% collected, last at 12:19, half of all parcels by 11:46, 82% by 14:00; 89 back to the station (5 too far to walk); average walk 93 m; 8.6 truck hours, 14 km |
| 1008 | 3 | 20 min wait: 3 trucks, 40 pickup points; 95% collected, last at 14:35, half of all parcels by 12:24, 81% by 14:00; 25 back to the station (5 too far to walk); average walk 93 m; 15.2 truck hours, 15 km |
| 1008 | 3 | 30 min wait: 3 trucks, 40 pickup points; 98% collected, last at 16:56, half of all parcels by 11:33, 70% by 14:00; 9 back to the station (5 too far to walk); average walk 93 m; 21.9 truck hours, 15 km |
| 1008 | 4 | 10 min wait: 3 trucks, 46 pickup points; 83% collected, last at 12:42, half of all parcels by 11:47, 83% by 14:00; 85 back to the station (0 too far to walk); average walk 87 m; 9.6 truck hours, 15 km |
| 1008 | 4 | 20 min wait: 3 trucks, 46 pickup points; 92% collected, last at 15:20, half of all parcels by 13:39, 69% by 14:00; 40 back to the station (0 too far to walk); average walk 87 m; 17.3 truck hours, 15 km |
| 1008 | 4 | 30 min wait: 3 trucks, 46 pickup points; 96% collected, last at 18:02, half of all parcels by 15:11, 31% by 14:00; 21 back to the station (0 too far to walk); average walk 87 m; 25.0 truck hours, 15 km |
| 1009 | 0 | 10 min wait: 3 trucks, 32 pickup points; 86% collected, last at 11:52, half of all parcels by 11:03, 86% by 14:00; 71 back to the station (0 too far to walk); average walk 96 m; 7.2 truck hours, 13 km |
| 1009 | 0 | 20 min wait: 3 trucks, 32 pickup points; 95% collected, last at 13:37, half of all parcels by 12:11, 95% by 14:00; 23 back to the station (0 too far to walk); average walk 96 m; 12.5 truck hours, 12 km |
| 1009 | 0 | 30 min wait: 3 trucks, 32 pickup points; 97% collected, last at 15:17, half of all parcels by 12:07, 81% by 14:00; 13 back to the station (0 too far to walk); average walk 96 m; 17.8 truck hours, 12 km |
| 1009 | 1 | 10 min wait: 3 trucks, 38 pickup points; 82% collected, last at 12:14, half of all parcels by 11:04, 82% by 14:00; 89 back to the station (5 too far to walk); average walk 88 m; 8.2 truck hours, 15 km |
| 1009 | 1 | 20 min wait: 3 trucks, 38 pickup points; 94% collected, last at 14:14, half of all parcels by 12:24, 91% by 14:00; 30 back to the station (5 too far to walk); average walk 88 m; 14.6 truck hours, 13 km |
| 1009 | 1 | 30 min wait: 3 trucks, 38 pickup points; 97% collected, last at 16:36, half of all parcels by 13:08, 68% by 14:00; 14 back to the station (5 too far to walk); average walk 88 m; 20.9 truck hours, 14 km |
| 1009 | 2 | 10 min wait: 3 trucks, 37 pickup points; 79% collected, last at 12:06, half of all parcels by 11:18, 79% by 14:00; 103 back to the station (5 too far to walk); average walk 89 m; 8.0 truck hours, 12 km |
| 1009 | 2 | 20 min wait: 3 trucks, 37 pickup points; 93% collected, last at 14:04, half of all parcels by 12:02, 93% by 14:00; 33 back to the station (5 too far to walk); average walk 89 m; 14.2 truck hours, 12 km |
| 1009 | 2 | 30 min wait: 3 trucks, 37 pickup points; 96% collected, last at 16:05, half of all parcels by 13:35, 57% by 14:00; 21 back to the station (5 too far to walk); average walk 89 m; 20.4 truck hours, 12 km |
| 1009 | 3 | 10 min wait: 3 trucks, 35 pickup points; 80% collected, last at 12:04, half of all parcels by 11:18, 80% by 14:00; 101 back to the station (4 too far to walk); average walk 94 m; 7.7 truck hours, 14 km |
| 1009 | 3 | 20 min wait: 3 trucks, 35 pickup points; 94% collected, last at 14:03, half of all parcels by 12:30, 93% by 14:00; 32 back to the station (4 too far to walk); average walk 94 m; 13.5 truck hours, 13 km |
| 1009 | 3 | 30 min wait: 3 trucks, 35 pickup points; 97% collected, last at 15:56, half of all parcels by 14:08, 43% by 14:00; 13 back to the station (4 too far to walk); average walk 94 m; 19.4 truck hours, 14 km |
| 1009 | 4 | 10 min wait: 3 trucks, 35 pickup points; 85% collected, last at 12:04, half of all parcels by 11:04, 85% by 14:00; 75 back to the station (0 too far to walk); average walk 93 m; 7.7 truck hours, 14 km |
| 1009 | 4 | 20 min wait: 3 trucks, 35 pickup points; 93% collected, last at 14:03, half of all parcels by 12:48, 93% by 14:00; 34 back to the station (0 too far to walk); average walk 93 m; 13.5 truck hours, 13 km |
| 1009 | 4 | 30 min wait: 3 trucks, 35 pickup points; 97% collected, last at 15:45, half of all parcels by 13:34, 64% by 14:00; 14 back to the station (0 too far to walk); average walk 93 m; 19.4 truck hours, 13 km |
