# Prime Air baseline on the held-out days

Written by `python -m baselines.prime_air --held-out`. 50 days, 500 parcels each. Drones fly from a site at the distribution centre between 10:00 and 19:30, one parcel at a time; DSP vans take the rest, as in [dsp-baseline.md](dsp-baseline.md). Settings are in [docs/amazon-baseline.md](../docs/amazon-baseline.md).

| drones at the site | by drone | vans | last parcel | half delivered by | by 14:00 | driver hours |
|---|---|---|---|---|---|---|
| 5 | 29% | 1.1 | 16:54 | 13:04 | 67% | 7.4 |
| 10 | 30% | 1.1 | 16:26 | 12:41 | 73% | 7.2 |
| 20 | 30% | 1.1 | 16:24 | 12:30 | 74% | 7.2 |

## Why parcels didn't go by drone (10 drones)

| reason | share of all parcels |
|---|---|
| no drop spot | 47.7% |
| too heavy | 17.1% |
| weather | 2.9% |
| no-fly zone | 1.6% |
| too big | 0.6% |
| no time | 0.2% |

## Every day

| city | day | result |
|---|---|---|
| 1000 | 0 | 5 drones: 0% by drone (0 sorties), 2 vans; last parcel at 16:04, half delivered by 12:32, 75% by 14:00; 13.1 driver hours; not by drone: {'no drop spot': 207, 'too big': 4, 'too heavy': 78, 'weather': 211} |
| 1000 | 0 | 10 drones: 0% by drone (0 sorties), 2 vans; last parcel at 16:04, half delivered by 12:32, 75% by 14:00; 13.1 driver hours; not by drone: {'no drop spot': 207, 'too big': 4, 'too heavy': 78, 'weather': 211} |
| 1000 | 0 | 20 drones: 0% by drone (0 sorties), 2 vans; last parcel at 16:04, half delivered by 12:32, 75% by 14:00; 13.1 driver hours; not by drone: {'no drop spot': 207, 'too big': 4, 'too heavy': 78, 'weather': 211} |
| 1000 | 1 | 5 drones: 36% by drone (181 sorties), 1 vans; last parcel at 16:19, half delivered by 11:50, 73% by 14:00; 6.6 driver hours; not by drone: {'no drop spot': 226, 'no-fly zone': 8, 'too big': 3, 'too heavy': 82} |
| 1000 | 1 | 10 drones: 36% by drone (181 sorties), 1 vans; last parcel at 16:12, half delivered by 11:30, 83% by 14:00; 6.6 driver hours; not by drone: {'no drop spot': 226, 'no-fly zone': 8, 'too big': 3, 'too heavy': 82} |
| 1000 | 1 | 20 drones: 36% by drone (181 sorties), 1 vans; last parcel at 16:03, half delivered by 11:06, 83% by 14:00; 6.6 driver hours; not by drone: {'no drop spot': 226, 'no-fly zone': 8, 'too big': 3, 'too heavy': 82} |
| 1000 | 2 | 5 drones: 32% by drone (161 sorties), 1 vans; last parcel at 16:06, half delivered by 13:26, 78% by 14:00; 6.3 driver hours; not by drone: {'no drop spot': 232, 'no-fly zone': 12, 'too big': 5, 'too heavy': 90} |
| 1000 | 2 | 10 drones: 32% by drone (161 sorties), 1 vans; last parcel at 16:04, half delivered by 12:58, 83% by 14:00; 6.3 driver hours; not by drone: {'no drop spot': 232, 'no-fly zone': 12, 'too big': 5, 'too heavy': 90} |
| 1000 | 2 | 20 drones: 32% by drone (161 sorties), 1 vans; last parcel at 16:02, half delivered by 12:58, 83% by 14:00; 6.3 driver hours; not by drone: {'no drop spot': 232, 'no-fly zone': 12, 'too big': 5, 'too heavy': 90} |
| 1000 | 3 | 5 drones: 31% by drone (153 sorties), 1 vans; last parcel at 16:26, half delivered by 13:55, 54% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 256, 'no-fly zone': 12, 'too big': 2, 'too heavy': 77} |
| 1000 | 3 | 10 drones: 31% by drone (153 sorties), 1 vans; last parcel at 16:26, half delivered by 13:25, 61% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 256, 'no-fly zone': 12, 'too big': 2, 'too heavy': 77} |
| 1000 | 3 | 20 drones: 31% by drone (153 sorties), 1 vans; last parcel at 16:26, half delivered by 13:25, 61% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 256, 'no-fly zone': 12, 'too big': 2, 'too heavy': 77} |
| 1000 | 4 | 5 drones: 37% by drone (185 sorties), 1 vans; last parcel at 18:15, half delivered by 12:20, 76% by 14:00; 6.1 driver hours; not by drone: {'no drop spot': 217, 'no-fly zone': 15, 'too heavy': 83} |
| 1000 | 4 | 10 drones: 37% by drone (187 sorties), 1 vans; last parcel at 16:13, half delivered by 13:23, 61% by 14:00; 6.1 driver hours; not by drone: {'no drop spot': 217, 'no-fly zone': 13, 'too heavy': 83} |
| 1000 | 4 | 20 drones: 37% by drone (187 sorties), 1 vans; last parcel at 16:10, half delivered by 12:43, 63% by 14:00; 6.1 driver hours; not by drone: {'no drop spot': 217, 'no-fly zone': 13, 'too heavy': 83} |
| 1001 | 0 | 5 drones: 32% by drone (162 sorties), 1 vans; last parcel at 18:54, half delivered by 14:11, 44% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 241, 'no-fly zone': 8, 'too big': 1, 'too heavy': 88} |
| 1001 | 0 | 10 drones: 32% by drone (162 sorties), 1 vans; last parcel at 16:28, half delivered by 13:02, 68% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 241, 'no-fly zone': 8, 'too big': 1, 'too heavy': 88} |
| 1001 | 0 | 20 drones: 32% by drone (162 sorties), 1 vans; last parcel at 16:28, half delivered by 12:59, 68% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 241, 'no-fly zone': 8, 'too big': 1, 'too heavy': 88} |
| 1001 | 1 | 5 drones: 32% by drone (159 sorties), 1 vans; last parcel at 16:36, half delivered by 11:48, 71% by 14:00; 6.8 driver hours; not by drone: {'no drop spot': 254, 'no-fly zone': 9, 'too heavy': 78} |
| 1001 | 1 | 10 drones: 32% by drone (159 sorties), 1 vans; last parcel at 16:20, half delivered by 11:35, 84% by 14:00; 6.8 driver hours; not by drone: {'no drop spot': 254, 'no-fly zone': 9, 'too heavy': 78} |
| 1001 | 1 | 20 drones: 32% by drone (159 sorties), 1 vans; last parcel at 16:20, half delivered by 11:09, 84% by 14:00; 6.8 driver hours; not by drone: {'no drop spot': 254, 'no-fly zone': 9, 'too heavy': 78} |
| 1001 | 2 | 5 drones: 31% by drone (153 sorties), 1 vans; last parcel at 18:31, half delivered by 13:32, 56% by 14:00; 7.8 driver hours; not by drone: {'no drop spot': 218, 'no-fly zone': 29, 'too big': 3, 'too heavy': 97} |
| 1001 | 2 | 10 drones: 34% by drone (170 sorties), 1 vans; last parcel at 16:47, half delivered by 13:36, 54% by 14:00; 7.3 driver hours; not by drone: {'no drop spot': 218, 'no-fly zone': 12, 'too big': 3, 'too heavy': 97} |
| 1001 | 2 | 20 drones: 34% by drone (170 sorties), 1 vans; last parcel at 16:47, half delivered by 13:09, 54% by 14:00; 7.3 driver hours; not by drone: {'no drop spot': 218, 'no-fly zone': 12, 'too big': 3, 'too heavy': 97} |
| 1001 | 3 | 5 drones: 31% by drone (156 sorties), 1 vans; last parcel at 18:01, half delivered by 14:46, 41% by 14:00; 7.2 driver hours; not by drone: {'no drop spot': 238, 'no-fly zone': 10, 'too big': 1, 'too heavy': 95} |
| 1001 | 3 | 10 drones: 32% by drone (158 sorties), 1 vans; last parcel at 16:33, half delivered by 13:12, 55% by 14:00; 7.1 driver hours; not by drone: {'no drop spot': 238, 'no-fly zone': 8, 'too big': 1, 'too heavy': 95} |
| 1001 | 3 | 20 drones: 32% by drone (158 sorties), 1 vans; last parcel at 16:33, half delivered by 13:12, 55% by 14:00; 7.1 driver hours; not by drone: {'no drop spot': 238, 'no-fly zone': 8, 'too big': 1, 'too heavy': 95} |
| 1001 | 4 | 5 drones: 19% by drone (95 sorties), 1 vans; last parcel at 18:51, half delivered by 14:36, 47% by 14:00; 9.4 driver hours; not by drone: {'no drop spot': 219, 'no time': 49, 'no-fly zone': 18, 'too big': 5, 'too heavy': 104, 'weather': 10} |
| 1001 | 4 | 10 drones: 32% by drone (159 sorties), 1 vans; last parcel at 16:47, half delivered by 12:51, 79% by 14:00; 7.3 driver hours; not by drone: {'no drop spot': 219, 'too big': 5, 'too heavy': 104, 'weather': 13} |
| 1001 | 4 | 20 drones: 32% by drone (159 sorties), 1 vans; last parcel at 16:47, half delivered by 12:51, 79% by 14:00; 7.3 driver hours; not by drone: {'no drop spot': 219, 'no-fly zone': 1, 'too big': 5, 'too heavy': 104, 'weather': 12} |
| 1002 | 0 | 5 drones: 34% by drone (170 sorties), 1 vans; last parcel at 16:28, half delivered by 13:55, 51% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 238, 'no-fly zone': 8, 'too big': 3, 'too heavy': 81} |
| 1002 | 0 | 10 drones: 34% by drone (170 sorties), 1 vans; last parcel at 16:28, half delivered by 13:04, 57% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 238, 'no-fly zone': 8, 'too big': 3, 'too heavy': 81} |
| 1002 | 0 | 20 drones: 34% by drone (170 sorties), 1 vans; last parcel at 16:28, half delivered by 13:04, 57% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 238, 'no-fly zone': 8, 'too big': 3, 'too heavy': 81} |
| 1002 | 1 | 5 drones: 30% by drone (152 sorties), 1 vans; last parcel at 17:16, half delivered by 13:36, 66% by 14:00; 7.8 driver hours; not by drone: {'no drop spot': 245, 'no-fly zone': 6, 'too big': 10, 'too heavy': 87} |
| 1002 | 1 | 10 drones: 30% by drone (152 sorties), 1 vans; last parcel at 17:16, half delivered by 13:22, 67% by 14:00; 7.8 driver hours; not by drone: {'no drop spot': 245, 'no-fly zone': 6, 'too big': 10, 'too heavy': 87} |
| 1002 | 1 | 20 drones: 30% by drone (152 sorties), 1 vans; last parcel at 17:16, half delivered by 13:22, 67% by 14:00; 7.8 driver hours; not by drone: {'no drop spot': 245, 'no-fly zone': 6, 'too big': 10, 'too heavy': 87} |
| 1002 | 2 | 5 drones: 29% by drone (144 sorties), 1 vans; last parcel at 16:52, half delivered by 13:40, 53% by 14:00; 7.4 driver hours; not by drone: {'no drop spot': 251, 'too heavy': 91, 'weather': 14} |
| 1002 | 2 | 10 drones: 29% by drone (144 sorties), 1 vans; last parcel at 16:52, half delivered by 13:22, 53% by 14:00; 7.4 driver hours; not by drone: {'no drop spot': 251, 'too heavy': 91, 'weather': 14} |
| 1002 | 2 | 20 drones: 29% by drone (144 sorties), 1 vans; last parcel at 16:52, half delivered by 13:22, 53% by 14:00; 7.4 driver hours; not by drone: {'no drop spot': 251, 'too heavy': 91, 'weather': 14} |
| 1002 | 3 | 5 drones: 0% by drone (0 sorties), 2 vans; last parcel at 16:00, half delivered by 12:06, 77% by 14:00; 13.0 driver hours; not by drone: {'no drop spot': 243, 'too big': 2, 'too heavy': 84, 'weather': 171} |
| 1002 | 3 | 10 drones: 0% by drone (0 sorties), 2 vans; last parcel at 16:00, half delivered by 12:06, 77% by 14:00; 13.0 driver hours; not by drone: {'no drop spot': 243, 'too big': 2, 'too heavy': 84, 'weather': 171} |
| 1002 | 3 | 20 drones: 0% by drone (0 sorties), 2 vans; last parcel at 16:00, half delivered by 12:06, 77% by 14:00; 13.0 driver hours; not by drone: {'no drop spot': 243, 'too big': 2, 'too heavy': 84, 'weather': 171} |
| 1002 | 4 | 5 drones: 30% by drone (150 sorties), 1 vans; last parcel at 16:09, half delivered by 13:47, 52% by 14:00; 6.5 driver hours; not by drone: {'no drop spot': 241, 'no-fly zone': 10, 'too big': 3, 'too heavy': 96} |
| 1002 | 4 | 10 drones: 30% by drone (150 sorties), 1 vans; last parcel at 16:09, half delivered by 13:18, 53% by 14:00; 6.5 driver hours; not by drone: {'no drop spot': 241, 'no-fly zone': 10, 'too big': 3, 'too heavy': 96} |
| 1002 | 4 | 20 drones: 30% by drone (150 sorties), 1 vans; last parcel at 16:05, half delivered by 13:18, 53% by 14:00; 6.5 driver hours; not by drone: {'no drop spot': 241, 'no-fly zone': 10, 'too big': 3, 'too heavy': 96} |
| 1003 | 0 | 5 drones: 32% by drone (160 sorties), 1 vans; last parcel at 18:48, half delivered by 14:26, 40% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 260, 'no-fly zone': 13, 'too big': 3, 'too heavy': 64} |
| 1003 | 0 | 10 drones: 32% by drone (160 sorties), 1 vans; last parcel at 16:44, half delivered by 14:26, 41% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 260, 'no-fly zone': 13, 'too big': 3, 'too heavy': 64} |
| 1003 | 0 | 20 drones: 32% by drone (160 sorties), 1 vans; last parcel at 16:28, half delivered by 14:26, 43% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 260, 'no-fly zone': 13, 'too big': 3, 'too heavy': 64} |
| 1003 | 1 | 5 drones: 34% by drone (169 sorties), 1 vans; last parcel at 16:11, half delivered by 13:40, 65% by 14:00; 6.7 driver hours; not by drone: {'no drop spot': 235, 'no-fly zone': 4, 'too big': 2, 'too heavy': 90} |
| 1003 | 1 | 10 drones: 34% by drone (169 sorties), 1 vans; last parcel at 16:11, half delivered by 13:15, 73% by 14:00; 6.7 driver hours; not by drone: {'no drop spot': 235, 'no-fly zone': 4, 'too big': 2, 'too heavy': 90} |
| 1003 | 1 | 20 drones: 34% by drone (169 sorties), 1 vans; last parcel at 16:11, half delivered by 13:15, 73% by 14:00; 6.7 driver hours; not by drone: {'no drop spot': 235, 'no-fly zone': 4, 'too big': 2, 'too heavy': 90} |
| 1003 | 2 | 5 drones: 34% by drone (171 sorties), 1 vans; last parcel at 16:14, half delivered by 12:38, 70% by 14:00; 5.8 driver hours; not by drone: {'no drop spot': 251, 'no-fly zone': 9, 'too big': 2, 'too heavy': 67} |
| 1003 | 2 | 10 drones: 34% by drone (171 sorties), 1 vans; last parcel at 16:14, half delivered by 12:21, 80% by 14:00; 5.8 driver hours; not by drone: {'no drop spot': 251, 'no-fly zone': 9, 'too big': 2, 'too heavy': 67} |
| 1003 | 2 | 20 drones: 34% by drone (171 sorties), 1 vans; last parcel at 16:11, half delivered by 12:11, 80% by 14:00; 5.8 driver hours; not by drone: {'no drop spot': 251, 'no-fly zone': 9, 'too big': 2, 'too heavy': 67} |
| 1003 | 3 | 5 drones: 25% by drone (123 sorties), 1 vans; last parcel at 19:23, half delivered by 11:48, 71% by 14:00; 8.3 driver hours; not by drone: {'no drop spot': 237, 'no time': 41, 'no-fly zone': 7, 'too big': 5, 'too heavy': 87} |
| 1003 | 3 | 10 drones: 33% by drone (164 sorties), 1 vans; last parcel at 17:54, half delivered by 12:23, 85% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 237, 'no-fly zone': 7, 'too big': 5, 'too heavy': 87} |
| 1003 | 3 | 20 drones: 33% by drone (164 sorties), 1 vans; last parcel at 18:01, half delivered by 12:23, 85% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 237, 'no-fly zone': 7, 'too big': 5, 'too heavy': 87} |
| 1003 | 4 | 5 drones: 35% by drone (174 sorties), 1 vans; last parcel at 16:44, half delivered by 12:45, 79% by 14:00; 6.6 driver hours; not by drone: {'no drop spot': 223, 'no-fly zone': 6, 'too big': 5, 'too heavy': 92} |
| 1003 | 4 | 10 drones: 35% by drone (174 sorties), 1 vans; last parcel at 16:14, half delivered by 12:31, 89% by 14:00; 6.6 driver hours; not by drone: {'no drop spot': 223, 'no-fly zone': 6, 'too big': 5, 'too heavy': 92} |
| 1003 | 4 | 20 drones: 35% by drone (174 sorties), 1 vans; last parcel at 16:11, half delivered by 12:31, 89% by 14:00; 6.6 driver hours; not by drone: {'no drop spot': 223, 'no-fly zone': 6, 'too big': 5, 'too heavy': 92} |
| 1004 | 0 | 5 drones: 33% by drone (163 sorties), 1 vans; last parcel at 16:15, half delivered by 12:41, 85% by 14:00; 6.8 driver hours; not by drone: {'no drop spot': 230, 'no-fly zone': 9, 'too big': 3, 'too heavy': 95} |
| 1004 | 0 | 10 drones: 33% by drone (163 sorties), 1 vans; last parcel at 16:15, half delivered by 12:05, 87% by 14:00; 6.8 driver hours; not by drone: {'no drop spot': 230, 'no-fly zone': 9, 'too big': 3, 'too heavy': 95} |
| 1004 | 0 | 20 drones: 33% by drone (163 sorties), 1 vans; last parcel at 16:15, half delivered by 11:00, 87% by 14:00; 6.8 driver hours; not by drone: {'no drop spot': 230, 'no-fly zone': 9, 'too big': 3, 'too heavy': 95} |
| 1004 | 1 | 5 drones: 29% by drone (145 sorties), 1 vans; last parcel at 17:49, half delivered by 13:04, 71% by 14:00; 7.7 driver hours; not by drone: {'no drop spot': 257, 'no-fly zone': 15, 'too big': 5, 'too heavy': 78} |
| 1004 | 1 | 10 drones: 29% by drone (145 sorties), 1 vans; last parcel at 17:14, half delivered by 12:42, 82% by 14:00; 7.7 driver hours; not by drone: {'no drop spot': 257, 'no-fly zone': 15, 'too big': 5, 'too heavy': 78} |
| 1004 | 1 | 20 drones: 29% by drone (145 sorties), 1 vans; last parcel at 17:14, half delivered by 12:42, 82% by 14:00; 7.7 driver hours; not by drone: {'no drop spot': 257, 'no-fly zone': 15, 'too big': 5, 'too heavy': 78} |
| 1004 | 2 | 5 drones: 30% by drone (149 sorties), 1 vans; last parcel at 17:04, half delivered by 12:00, 80% by 14:00; 7.6 driver hours; not by drone: {'no drop spot': 243, 'no-fly zone': 9, 'too big': 4, 'too heavy': 95} |
| 1004 | 2 | 10 drones: 30% by drone (149 sorties), 1 vans; last parcel at 17:04, half delivered by 12:43, 81% by 14:00; 7.6 driver hours; not by drone: {'no drop spot': 243, 'no-fly zone': 9, 'too big': 4, 'too heavy': 95} |
| 1004 | 2 | 20 drones: 30% by drone (149 sorties), 1 vans; last parcel at 17:04, half delivered by 12:43, 81% by 14:00; 7.6 driver hours; not by drone: {'no drop spot': 243, 'no-fly zone': 9, 'too big': 4, 'too heavy': 95} |
| 1004 | 3 | 5 drones: 10% by drone (50 sorties), 1 vans; last parcel at 19:25, half delivered by 15:08, 23% by 14:00; 9.6 driver hours; not by drone: {'no drop spot': 247, 'no time': 97, 'no-fly zone': 13, 'too big': 2, 'too heavy': 91} |
| 1004 | 3 | 10 drones: 20% by drone (100 sorties), 1 vans; last parcel at 19:28, half delivered by 15:32, 37% by 14:00; 7.9 driver hours; not by drone: {'no drop spot': 247, 'no time': 45, 'no-fly zone': 15, 'too big': 2, 'too heavy': 91} |
| 1004 | 3 | 20 drones: 29% by drone (144 sorties), 1 vans; last parcel at 19:14, half delivered by 13:06, 61% by 14:00; 6.3 driver hours; not by drone: {'no drop spot': 247, 'no-fly zone': 16, 'too big': 2, 'too heavy': 91} |
| 1004 | 4 | 5 drones: 31% by drone (153 sorties), 1 vans; last parcel at 16:16, half delivered by 13:39, 63% by 14:00; 6.8 driver hours; not by drone: {'no drop spot': 250, 'no-fly zone': 12, 'too big': 2, 'too heavy': 83} |
| 1004 | 4 | 10 drones: 31% by drone (153 sorties), 1 vans; last parcel at 16:16, half delivered by 13:33, 63% by 14:00; 6.8 driver hours; not by drone: {'no drop spot': 250, 'no-fly zone': 12, 'too big': 2, 'too heavy': 83} |
| 1004 | 4 | 20 drones: 31% by drone (153 sorties), 1 vans; last parcel at 16:16, half delivered by 13:33, 63% by 14:00; 6.8 driver hours; not by drone: {'no drop spot': 250, 'no-fly zone': 12, 'too big': 2, 'too heavy': 83} |
| 1005 | 0 | 5 drones: 35% by drone (174 sorties), 1 vans; last parcel at 15:36, half delivered by 11:41, 81% by 14:00; 6.1 driver hours; not by drone: {'no drop spot': 236, 'no-fly zone': 12, 'too big': 3, 'too heavy': 75} |
| 1005 | 0 | 10 drones: 35% by drone (174 sorties), 1 vans; last parcel at 15:36, half delivered by 11:27, 86% by 14:00; 6.1 driver hours; not by drone: {'no drop spot': 236, 'no-fly zone': 12, 'too big': 3, 'too heavy': 75} |
| 1005 | 0 | 20 drones: 35% by drone (174 sorties), 1 vans; last parcel at 15:36, half delivered by 11:03, 86% by 14:00; 6.1 driver hours; not by drone: {'no drop spot': 236, 'no-fly zone': 12, 'too big': 3, 'too heavy': 75} |
| 1005 | 1 | 5 drones: 39% by drone (193 sorties), 1 vans; last parcel at 16:11, half delivered by 11:42, 86% by 14:00; 5.5 driver hours; not by drone: {'no drop spot': 233, 'no-fly zone': 2, 'too big': 1, 'too heavy': 71} |
| 1005 | 1 | 10 drones: 39% by drone (193 sorties), 1 vans; last parcel at 16:03, half delivered by 11:18, 93% by 14:00; 5.5 driver hours; not by drone: {'no drop spot': 233, 'no-fly zone': 2, 'too big': 1, 'too heavy': 71} |
| 1005 | 1 | 20 drones: 39% by drone (193 sorties), 1 vans; last parcel at 16:06, half delivered by 10:56, 93% by 14:00; 5.5 driver hours; not by drone: {'no drop spot': 233, 'no-fly zone': 2, 'too big': 1, 'too heavy': 71} |
| 1005 | 2 | 5 drones: 32% by drone (159 sorties), 1 vans; last parcel at 16:22, half delivered by 12:17, 84% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 240, 'no-fly zone': 9, 'too big': 4, 'too heavy': 88} |
| 1005 | 2 | 10 drones: 32% by drone (159 sorties), 1 vans; last parcel at 16:22, half delivered by 11:54, 87% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 240, 'no-fly zone': 9, 'too big': 4, 'too heavy': 88} |
| 1005 | 2 | 20 drones: 32% by drone (159 sorties), 1 vans; last parcel at 16:22, half delivered by 11:54, 87% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 240, 'no-fly zone': 9, 'too big': 4, 'too heavy': 88} |
| 1005 | 3 | 5 drones: 31% by drone (157 sorties), 1 vans; last parcel at 16:20, half delivered by 12:26, 68% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 259, 'no-fly zone': 5, 'too big': 1, 'too heavy': 78} |
| 1005 | 3 | 10 drones: 31% by drone (157 sorties), 1 vans; last parcel at 16:20, half delivered by 11:46, 70% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 259, 'no-fly zone': 5, 'too big': 1, 'too heavy': 78} |
| 1005 | 3 | 20 drones: 31% by drone (157 sorties), 1 vans; last parcel at 16:20, half delivered by 11:27, 70% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 259, 'no-fly zone': 5, 'too big': 1, 'too heavy': 78} |
| 1005 | 4 | 5 drones: 29% by drone (146 sorties), 1 vans; last parcel at 16:15, half delivered by 13:27, 62% by 14:00; 6.8 driver hours; not by drone: {'no drop spot': 247, 'no-fly zone': 14, 'too big': 3, 'too heavy': 90} |
| 1005 | 4 | 10 drones: 29% by drone (146 sorties), 1 vans; last parcel at 16:15, half delivered by 13:23, 62% by 14:00; 6.8 driver hours; not by drone: {'no drop spot': 247, 'no-fly zone': 14, 'too big': 3, 'too heavy': 90} |
| 1005 | 4 | 20 drones: 29% by drone (146 sorties), 1 vans; last parcel at 16:15, half delivered by 13:23, 62% by 14:00; 6.8 driver hours; not by drone: {'no drop spot': 247, 'no-fly zone': 14, 'too big': 3, 'too heavy': 90} |
| 1006 | 0 | 5 drones: 34% by drone (170 sorties), 1 vans; last parcel at 16:28, half delivered by 12:31, 84% by 14:00; 6.7 driver hours; not by drone: {'no drop spot': 230, 'no-fly zone': 4, 'too big': 2, 'too heavy': 94} |
| 1006 | 0 | 10 drones: 34% by drone (170 sorties), 1 vans; last parcel at 16:29, half delivered by 12:03, 88% by 14:00; 6.7 driver hours; not by drone: {'no drop spot': 230, 'no-fly zone': 4, 'too big': 2, 'too heavy': 94} |
| 1006 | 0 | 20 drones: 34% by drone (170 sorties), 1 vans; last parcel at 16:34, half delivered by 11:56, 88% by 14:00; 6.7 driver hours; not by drone: {'no drop spot': 230, 'no-fly zone': 4, 'too big': 2, 'too heavy': 94} |
| 1006 | 1 | 5 drones: 37% by drone (184 sorties), 1 vans; last parcel at 16:41, half delivered by 13:28, 61% by 14:00; 7.2 driver hours; not by drone: {'no drop spot': 216, 'no-fly zone': 15, 'too big': 3, 'too heavy': 82} |
| 1006 | 1 | 10 drones: 37% by drone (184 sorties), 1 vans; last parcel at 16:41, half delivered by 12:30, 68% by 14:00; 7.2 driver hours; not by drone: {'no drop spot': 216, 'no-fly zone': 15, 'too big': 3, 'too heavy': 82} |
| 1006 | 1 | 20 drones: 37% by drone (184 sorties), 1 vans; last parcel at 16:41, half delivered by 12:30, 68% by 14:00; 7.2 driver hours; not by drone: {'no drop spot': 216, 'no-fly zone': 15, 'too big': 3, 'too heavy': 82} |
| 1006 | 2 | 5 drones: 36% by drone (179 sorties), 1 vans; last parcel at 19:23, half delivered by 13:57, 52% by 14:00; 6.8 driver hours; not by drone: {'no drop spot': 216, 'no time': 17, 'no-fly zone': 7, 'too big': 1, 'too heavy': 80} |
| 1006 | 2 | 10 drones: 39% by drone (196 sorties), 1 vans; last parcel at 17:15, half delivered by 14:02, 48% by 14:00; 6.3 driver hours; not by drone: {'no drop spot': 216, 'no-fly zone': 7, 'too big': 1, 'too heavy': 80} |
| 1006 | 2 | 20 drones: 39% by drone (196 sorties), 1 vans; last parcel at 16:12, half delivered by 13:27, 61% by 14:00; 6.3 driver hours; not by drone: {'no drop spot': 216, 'no-fly zone': 7, 'too big': 1, 'too heavy': 80} |
| 1006 | 3 | 5 drones: 33% by drone (166 sorties), 1 vans; last parcel at 16:13, half delivered by 13:40, 63% by 14:00; 6.5 driver hours; not by drone: {'no drop spot': 231, 'no-fly zone': 4, 'too big': 2, 'too heavy': 97} |
| 1006 | 3 | 10 drones: 33% by drone (166 sorties), 1 vans; last parcel at 16:10, half delivered by 13:28, 68% by 14:00; 6.5 driver hours; not by drone: {'no drop spot': 231, 'no-fly zone': 4, 'too big': 2, 'too heavy': 97} |
| 1006 | 3 | 20 drones: 33% by drone (166 sorties), 1 vans; last parcel at 16:12, half delivered by 13:28, 68% by 14:00; 6.5 driver hours; not by drone: {'no drop spot': 231, 'no-fly zone': 4, 'too big': 2, 'too heavy': 97} |
| 1006 | 4 | 5 drones: 34% by drone (169 sorties), 1 vans; last parcel at 16:14, half delivered by 14:08, 48% by 14:00; 6.4 driver hours; not by drone: {'no drop spot': 236, 'no-fly zone': 5, 'too big': 5, 'too heavy': 85} |
| 1006 | 4 | 10 drones: 34% by drone (169 sorties), 1 vans; last parcel at 16:15, half delivered by 13:21, 53% by 14:00; 6.4 driver hours; not by drone: {'no drop spot': 236, 'no-fly zone': 5, 'too big': 5, 'too heavy': 85} |
| 1006 | 4 | 20 drones: 34% by drone (169 sorties), 1 vans; last parcel at 16:05, half delivered by 13:21, 53% by 14:00; 6.4 driver hours; not by drone: {'no drop spot': 236, 'no-fly zone': 5, 'too big': 5, 'too heavy': 85} |
| 1007 | 0 | 5 drones: 38% by drone (189 sorties), 1 vans; last parcel at 16:01, half delivered by 12:52, 73% by 14:00; 6.5 driver hours; not by drone: {'no drop spot': 211, 'no-fly zone': 8, 'too big': 4, 'too heavy': 88} |
| 1007 | 0 | 10 drones: 38% by drone (189 sorties), 1 vans; last parcel at 16:01, half delivered by 11:37, 87% by 14:00; 6.5 driver hours; not by drone: {'no drop spot': 211, 'no-fly zone': 8, 'too big': 4, 'too heavy': 88} |
| 1007 | 0 | 20 drones: 38% by drone (189 sorties), 1 vans; last parcel at 16:01, half delivered by 11:17, 87% by 14:00; 6.5 driver hours; not by drone: {'no drop spot': 211, 'no-fly zone': 8, 'too big': 4, 'too heavy': 88} |
| 1007 | 1 | 5 drones: 35% by drone (173 sorties), 1 vans; last parcel at 16:27, half delivered by 12:33, 70% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 223, 'no-fly zone': 11, 'too big': 5, 'too heavy': 88} |
| 1007 | 1 | 10 drones: 35% by drone (173 sorties), 1 vans; last parcel at 16:27, half delivered by 11:33, 79% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 223, 'no-fly zone': 11, 'too big': 5, 'too heavy': 88} |
| 1007 | 1 | 20 drones: 35% by drone (173 sorties), 1 vans; last parcel at 16:27, half delivered by 11:14, 79% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 223, 'no-fly zone': 11, 'too big': 5, 'too heavy': 88} |
| 1007 | 2 | 5 drones: 31% by drone (153 sorties), 1 vans; last parcel at 16:08, half delivered by 14:00, 48% by 14:00; 6.3 driver hours; not by drone: {'no drop spot': 240, 'no-fly zone': 17, 'too big': 5, 'too heavy': 85} |
| 1007 | 2 | 10 drones: 31% by drone (153 sorties), 1 vans; last parcel at 16:08, half delivered by 14:00, 49% by 14:00; 6.3 driver hours; not by drone: {'no drop spot': 240, 'no-fly zone': 17, 'too big': 5, 'too heavy': 85} |
| 1007 | 2 | 20 drones: 31% by drone (153 sorties), 1 vans; last parcel at 16:12, half delivered by 14:00, 49% by 14:00; 6.3 driver hours; not by drone: {'no drop spot': 240, 'no-fly zone': 17, 'too big': 5, 'too heavy': 85} |
| 1007 | 3 | 5 drones: 33% by drone (166 sorties), 1 vans; last parcel at 16:09, half delivered by 13:52, 53% by 14:00; 6.7 driver hours; not by drone: {'no drop spot': 236, 'no-fly zone': 8, 'too big': 4, 'too heavy': 86} |
| 1007 | 3 | 10 drones: 33% by drone (166 sorties), 1 vans; last parcel at 16:09, half delivered by 13:24, 56% by 14:00; 6.7 driver hours; not by drone: {'no drop spot': 236, 'no-fly zone': 8, 'too big': 4, 'too heavy': 86} |
| 1007 | 3 | 20 drones: 33% by drone (166 sorties), 1 vans; last parcel at 16:09, half delivered by 13:24, 56% by 14:00; 6.7 driver hours; not by drone: {'no drop spot': 236, 'no-fly zone': 8, 'too big': 4, 'too heavy': 86} |
| 1007 | 4 | 5 drones: 33% by drone (166 sorties), 1 vans; last parcel at 16:52, half delivered by 11:58, 82% by 14:00; 7.4 driver hours; not by drone: {'no drop spot': 235, 'no-fly zone': 6, 'too big': 3, 'too heavy': 90} |
| 1007 | 4 | 10 drones: 33% by drone (166 sorties), 1 vans; last parcel at 16:52, half delivered by 11:28, 85% by 14:00; 7.4 driver hours; not by drone: {'no drop spot': 235, 'no-fly zone': 6, 'too big': 3, 'too heavy': 90} |
| 1007 | 4 | 20 drones: 33% by drone (166 sorties), 1 vans; last parcel at 16:52, half delivered by 11:07, 85% by 14:00; 7.4 driver hours; not by drone: {'no drop spot': 235, 'no-fly zone': 6, 'too big': 3, 'too heavy': 90} |
| 1008 | 0 | 5 drones: 30% by drone (148 sorties), 1 vans; last parcel at 16:26, half delivered by 12:56, 80% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 261, 'no-fly zone': 9, 'too heavy': 82} |
| 1008 | 0 | 10 drones: 30% by drone (148 sorties), 1 vans; last parcel at 16:26, half delivered by 12:41, 87% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 261, 'no-fly zone': 9, 'too heavy': 82} |
| 1008 | 0 | 20 drones: 30% by drone (148 sorties), 1 vans; last parcel at 16:26, half delivered by 12:41, 87% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 261, 'no-fly zone': 9, 'too heavy': 82} |
| 1008 | 1 | 5 drones: 37% by drone (184 sorties), 1 vans; last parcel at 18:20, half delivered by 12:59, 72% by 14:00; 6.6 driver hours; not by drone: {'no drop spot': 234, 'no-fly zone': 6, 'too big': 3, 'too heavy': 73} |
| 1008 | 1 | 10 drones: 37% by drone (184 sorties), 1 vans; last parcel at 16:12, half delivered by 12:30, 84% by 14:00; 6.6 driver hours; not by drone: {'no drop spot': 234, 'no-fly zone': 6, 'too big': 3, 'too heavy': 73} |
| 1008 | 1 | 20 drones: 37% by drone (184 sorties), 1 vans; last parcel at 16:10, half delivered by 12:13, 87% by 14:00; 6.6 driver hours; not by drone: {'no drop spot': 234, 'no-fly zone': 6, 'too big': 3, 'too heavy': 73} |
| 1008 | 2 | 5 drones: 31% by drone (153 sorties), 1 vans; last parcel at 17:16, half delivered by 13:03, 75% by 14:00; 6.5 driver hours; not by drone: {'no drop spot': 261, 'no-fly zone': 12, 'too big': 2, 'too heavy': 72} |
| 1008 | 2 | 10 drones: 31% by drone (153 sorties), 1 vans; last parcel at 16:11, half delivered by 12:51, 88% by 14:00; 6.5 driver hours; not by drone: {'no drop spot': 261, 'no-fly zone': 12, 'too big': 2, 'too heavy': 72} |
| 1008 | 2 | 20 drones: 31% by drone (153 sorties), 1 vans; last parcel at 16:10, half delivered by 12:29, 89% by 14:00; 6.5 driver hours; not by drone: {'no drop spot': 261, 'no-fly zone': 12, 'too big': 2, 'too heavy': 72} |
| 1008 | 3 | 5 drones: 35% by drone (175 sorties), 1 vans; last parcel at 18:04, half delivered by 12:53, 62% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 218, 'no-fly zone': 6, 'too big': 1, 'too heavy': 100} |
| 1008 | 3 | 10 drones: 35% by drone (175 sorties), 1 vans; last parcel at 16:22, half delivered by 12:37, 75% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 218, 'no-fly zone': 6, 'too big': 1, 'too heavy': 100} |
| 1008 | 3 | 20 drones: 35% by drone (175 sorties), 1 vans; last parcel at 16:22, half delivered by 12:34, 75% by 14:00; 6.9 driver hours; not by drone: {'no drop spot': 218, 'no-fly zone': 6, 'too big': 1, 'too heavy': 100} |
| 1008 | 4 | 5 drones: 37% by drone (185 sorties), 1 vans; last parcel at 17:52, half delivered by 12:58, 58% by 14:00; 7.1 driver hours; not by drone: {'no drop spot': 219, 'no-fly zone': 9, 'too big': 3, 'too heavy': 84} |
| 1008 | 4 | 10 drones: 37% by drone (185 sorties), 1 vans; last parcel at 16:38, half delivered by 12:01, 77% by 14:00; 7.1 driver hours; not by drone: {'no drop spot': 219, 'no-fly zone': 9, 'too big': 3, 'too heavy': 84} |
| 1008 | 4 | 20 drones: 37% by drone (185 sorties), 1 vans; last parcel at 16:38, half delivered by 11:29, 77% by 14:00; 7.1 driver hours; not by drone: {'no drop spot': 219, 'no-fly zone': 9, 'too big': 3, 'too heavy': 84} |
| 1009 | 0 | 5 drones: 0% by drone (0 sorties), 2 vans; last parcel at 15:20, half delivered by 11:47, 85% by 14:00; 11.7 driver hours; not by drone: {'no drop spot': 244, 'too big': 4, 'too heavy': 101, 'weather': 151} |
| 1009 | 0 | 10 drones: 0% by drone (0 sorties), 2 vans; last parcel at 15:20, half delivered by 11:47, 85% by 14:00; 11.7 driver hours; not by drone: {'no drop spot': 244, 'too big': 4, 'too heavy': 101, 'weather': 151} |
| 1009 | 0 | 20 drones: 0% by drone (0 sorties), 2 vans; last parcel at 15:20, half delivered by 11:47, 85% by 14:00; 11.7 driver hours; not by drone: {'no drop spot': 244, 'too big': 4, 'too heavy': 101, 'weather': 151} |
| 1009 | 1 | 5 drones: 29% by drone (144 sorties), 1 vans; last parcel at 15:53, half delivered by 12:16, 91% by 14:00; 6.4 driver hours; not by drone: {'no drop spot': 264, 'no-fly zone': 8, 'too big': 2, 'too heavy': 82} |
| 1009 | 1 | 10 drones: 29% by drone (144 sorties), 1 vans; last parcel at 15:53, half delivered by 11:42, 91% by 14:00; 6.4 driver hours; not by drone: {'no drop spot': 264, 'no-fly zone': 8, 'too big': 2, 'too heavy': 82} |
| 1009 | 1 | 20 drones: 29% by drone (144 sorties), 1 vans; last parcel at 15:53, half delivered by 11:31, 91% by 14:00; 6.4 driver hours; not by drone: {'no drop spot': 264, 'no-fly zone': 8, 'too big': 2, 'too heavy': 82} |
| 1009 | 2 | 5 drones: 31% by drone (157 sorties), 1 vans; last parcel at 16:26, half delivered by 11:52, 83% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 255, 'no-fly zone': 7, 'too big': 2, 'too heavy': 79} |
| 1009 | 2 | 10 drones: 31% by drone (157 sorties), 1 vans; last parcel at 16:26, half delivered by 11:29, 85% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 255, 'no-fly zone': 7, 'too big': 2, 'too heavy': 79} |
| 1009 | 2 | 20 drones: 31% by drone (157 sorties), 1 vans; last parcel at 16:26, half delivered by 11:19, 85% by 14:00; 7.0 driver hours; not by drone: {'no drop spot': 255, 'no-fly zone': 7, 'too big': 2, 'too heavy': 79} |
| 1009 | 3 | 5 drones: 29% by drone (143 sorties), 1 vans; last parcel at 15:52, half delivered by 12:23, 91% by 14:00; 6.4 driver hours; not by drone: {'no drop spot': 265, 'no-fly zone': 5, 'too big': 2, 'too heavy': 85} |
| 1009 | 3 | 10 drones: 29% by drone (143 sorties), 1 vans; last parcel at 15:52, half delivered by 12:08, 91% by 14:00; 6.4 driver hours; not by drone: {'no drop spot': 265, 'no-fly zone': 5, 'too big': 2, 'too heavy': 85} |
| 1009 | 3 | 20 drones: 29% by drone (143 sorties), 1 vans; last parcel at 15:52, half delivered by 12:08, 91% by 14:00; 6.4 driver hours; not by drone: {'no drop spot': 265, 'no-fly zone': 5, 'too big': 2, 'too heavy': 85} |
| 1009 | 4 | 5 drones: 0% by drone (0 sorties), 2 vans; last parcel at 15:11, half delivered by 12:30, 87% by 14:00; 11.4 driver hours; not by drone: {'no drop spot': 253, 'too big': 2, 'too heavy': 80, 'weather': 165} |
| 1009 | 4 | 10 drones: 0% by drone (0 sorties), 2 vans; last parcel at 15:11, half delivered by 12:30, 87% by 14:00; 11.4 driver hours; not by drone: {'no drop spot': 253, 'too big': 2, 'too heavy': 80, 'weather': 165} |
| 1009 | 4 | 20 drones: 0% by drone (0 sorties), 2 vans; last parcel at 15:11, half delivered by 12:30, 87% by 14:00; 11.4 driver hours; not by drone: {'no drop spot': 253, 'too big': 2, 'too heavy': 80, 'weather': 165} |
