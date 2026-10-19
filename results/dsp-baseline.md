# DSP van baseline on the held-out days

Written by `python -m baselines.dsp --held-out`. 50 days, 500 parcels each, service time 166 s per stop plus 10 s per extra package (from [dsp-calibration.md](dsp-calibration.md)), shift 09:30 to 19:30, 30 min loadout, routes by OR-Tools with 5 s per day.

| | mean | best day | worst day |
|---|---|---|---|
| vans | 2.0 | 2 | 2 |
| last parcel delivered | 15:46 | 15:11 | 16:27 |
| half the parcels delivered by | 12:57 | 11:37 | 14:18 |
| delivered by 14:00 | 69% | 87% | 47% |
| driver hours | 12.5 | 11.4 | 13.9 |
| km driven | 24 | 21 | 28 |
| parcels brought back undelivered | 0.0 | 0 | 0 |

## Every day

| city | day | result |
|---|---|---|
| 1000 | 0 | 2 vans, stops [109, 120], packages [342, 158]; last parcel at 16:04, half delivered by 12:32, 75% by 14:00; 0 undelivered; 13.1 driver hours, 28 km |
| 1000 | 1 | 2 vans, stops [106, 114], packages [334, 166]; last parcel at 15:49, half delivered by 13:07, 77% by 14:00; 0 undelivered; 12.6 driver hours, 24 km |
| 1000 | 2 | 2 vans, stops [99, 110], packages [341, 159]; last parcel at 15:35, half delivered by 12:07, 72% by 14:00; 0 undelivered; 12.2 driver hours, 24 km |
| 1000 | 3 | 2 vans, stops [99, 111], packages [341, 159]; last parcel at 15:35, half delivered by 13:45, 57% by 14:00; 0 undelivered; 12.2 driver hours, 23 km |
| 1000 | 4 | 2 vans, stops [112, 106], packages [204, 296]; last parcel at 15:46, half delivered by 11:56, 80% by 14:00; 0 undelivered; 12.5 driver hours, 23 km |
| 1001 | 0 | 2 vans, stops [105, 110], packages [318, 182]; last parcel at 15:42, half delivered by 12:26, 79% by 14:00; 0 undelivered; 12.4 driver hours, 23 km |
| 1001 | 1 | 2 vans, stops [106, 114], packages [326, 174]; last parcel at 15:48, half delivered by 14:05, 49% by 14:00; 0 undelivered; 12.6 driver hours, 22 km |
| 1001 | 2 | 2 vans, stops [107, 116], packages [323, 177]; last parcel at 15:54, half delivered by 12:16, 75% by 14:00; 0 undelivered; 12.8 driver hours, 25 km |
| 1001 | 3 | 2 vans, stops [107, 118], packages [337, 163]; last parcel at 15:55, half delivered by 13:50, 60% by 14:00; 0 undelivered; 12.9 driver hours, 24 km |
| 1001 | 4 | 2 vans, stops [107, 116], packages [339, 161]; last parcel at 15:53, half delivered by 12:22, 69% by 14:00; 0 undelivered; 12.8 driver hours, 24 km |
| 1002 | 0 | 2 vans, stops [111, 121], packages [334, 166]; last parcel at 16:05, half delivered by 13:52, 53% by 14:00; 0 undelivered; 13.2 driver hours, 24 km |
| 1002 | 1 | 2 vans, stops [112, 125], packages [338, 162]; last parcel at 16:10, half delivered by 13:48, 57% by 14:00; 0 undelivered; 13.4 driver hours, 24 km |
| 1002 | 2 | 2 vans, stops [105, 116], packages [335, 165]; last parcel at 15:49, half delivered by 12:57, 80% by 14:00; 0 undelivered; 12.6 driver hours, 22 km |
| 1002 | 3 | 2 vans, stops [109, 119], packages [334, 166]; last parcel at 16:00, half delivered by 12:06, 77% by 14:00; 0 undelivered; 13.0 driver hours, 24 km |
| 1002 | 4 | 2 vans, stops [98, 105], packages [337, 163]; last parcel at 15:27, half delivered by 13:17, 75% by 14:00; 0 undelivered; 11.9 driver hours, 23 km |
| 1003 | 0 | 2 vans, stops [109, 120], packages [337, 163]; last parcel at 16:02, half delivered by 12:42, 65% by 14:00; 0 undelivered; 13.0 driver hours, 25 km |
| 1003 | 1 | 2 vans, stops [107, 115], packages [337, 163]; last parcel at 15:53, half delivered by 12:11, 77% by 14:00; 0 undelivered; 12.8 driver hours, 24 km |
| 1003 | 2 | 2 vans, stops [98, 105], packages [327, 173]; last parcel at 15:27, half delivered by 12:19, 84% by 14:00; 0 undelivered; 11.9 driver hours, 23 km |
| 1003 | 3 | 2 vans, stops [106, 119], packages [343, 157]; last parcel at 15:56, half delivered by 13:26, 68% by 14:00; 0 undelivered; 12.9 driver hours, 25 km |
| 1003 | 4 | 2 vans, stops [104, 113], packages [332, 168]; last parcel at 15:46, half delivered by 14:14, 47% by 14:00; 0 undelivered; 12.6 driver hours, 26 km |
| 1004 | 0 | 2 vans, stops [103, 115], packages [335, 165]; last parcel at 15:48, half delivered by 12:21, 76% by 14:00; 0 undelivered; 12.6 driver hours, 24 km |
| 1004 | 1 | 2 vans, stops [107, 116], packages [330, 170]; last parcel at 15:54, half delivered by 12:53, 72% by 14:00; 0 undelivered; 12.8 driver hours, 25 km |
| 1004 | 2 | 2 vans, stops [103, 113], packages [335, 165]; last parcel at 15:45, half delivered by 14:18, 47% by 14:00; 0 undelivered; 12.5 driver hours, 24 km |
| 1004 | 3 | 2 vans, stops [96, 106], packages [339, 161]; last parcel at 15:22, half delivered by 12:44, 84% by 14:00; 0 undelivered; 11.8 driver hours, 21 km |
| 1004 | 4 | 2 vans, stops [103, 114], packages [337, 163]; last parcel at 15:46, half delivered by 12:23, 80% by 14:00; 0 undelivered; 12.5 driver hours, 25 km |
| 1005 | 0 | 2 vans, stops [102, 111], packages [336, 164]; last parcel at 15:42, half delivered by 11:41, 79% by 14:00; 0 undelivered; 12.4 driver hours, 24 km |
| 1005 | 1 | 2 vans, stops [100, 107], packages [329, 171]; last parcel at 15:35, half delivered by 12:22, 81% by 14:00; 0 undelivered; 12.2 driver hours, 26 km |
| 1005 | 2 | 2 vans, stops [105, 116], packages [349, 151]; last parcel at 15:50, half delivered by 13:53, 55% by 14:00; 0 undelivered; 12.7 driver hours, 24 km |
| 1005 | 3 | 2 vans, stops [102, 109], packages [328, 172]; last parcel at 15:37, half delivered by 12:53, 69% by 14:00; 0 undelivered; 12.3 driver hours, 24 km |
| 1005 | 4 | 2 vans, stops [97, 107], packages [352, 148]; last parcel at 15:28, half delivered by 13:11, 83% by 14:00; 0 undelivered; 11.9 driver hours, 24 km |
| 1006 | 0 | 2 vans, stops [105, 113], packages [337, 163]; last parcel at 15:46, half delivered by 12:55, 78% by 14:00; 0 undelivered; 12.5 driver hours, 24 km |
| 1006 | 1 | 2 vans, stops [111, 118], packages [322, 178]; last parcel at 16:04, half delivered by 12:31, 75% by 14:00; 0 undelivered; 13.1 driver hours, 27 km |
| 1006 | 2 | 2 vans, stops [113, 119], packages [319, 181]; last parcel at 16:11, half delivered by 12:25, 74% by 14:00; 0 undelivered; 13.3 driver hours, 26 km |
| 1006 | 3 | 2 vans, stops [100, 109], packages [327, 173]; last parcel at 15:36, half delivered by 11:41, 82% by 14:00; 0 undelivered; 12.2 driver hours, 24 km |
| 1006 | 4 | 2 vans, stops [104, 114], packages [343, 157]; last parcel at 15:47, half delivered by 13:07, 74% by 14:00; 0 undelivered; 12.6 driver hours, 24 km |
| 1007 | 0 | 2 vans, stops [115, 114], packages [269, 231]; last parcel at 16:02, half delivered by 13:37, 55% by 14:00; 0 undelivered; 13.1 driver hours, 23 km |
| 1007 | 1 | 2 vans, stops [108, 116], packages [317, 183]; last parcel at 15:55, half delivered by 13:29, 63% by 14:00; 0 undelivered; 12.9 driver hours, 25 km |
| 1007 | 2 | 2 vans, stops [102, 105], packages [251, 249]; last parcel at 15:34, half delivered by 13:07, 67% by 14:00; 0 undelivered; 12.1 driver hours, 26 km |
| 1007 | 3 | 2 vans, stops [103, 115], packages [314, 186]; last parcel at 15:46, half delivered by 14:10, 48% by 14:00; 0 undelivered; 12.6 driver hours, 24 km |
| 1007 | 4 | 2 vans, stops [113, 120], packages [332, 168]; last parcel at 16:08, half delivered by 13:14, 64% by 14:00; 0 undelivered; 13.3 driver hours, 26 km |
| 1008 | 0 | 2 vans, stops [103, 111], packages [338, 162]; last parcel at 15:42, half delivered by 13:54, 51% by 14:00; 0 undelivered; 12.4 driver hours, 25 km |
| 1008 | 1 | 2 vans, stops [110, 119], packages [323, 177]; last parcel at 16:02, half delivered by 11:37, 77% by 14:00; 0 undelivered; 13.1 driver hours, 26 km |
| 1008 | 2 | 2 vans, stops [98, 110], packages [344, 156]; last parcel at 15:31, half delivered by 14:11, 47% by 14:00; 0 undelivered; 12.1 driver hours, 22 km |
| 1008 | 3 | 2 vans, stops [107, 116], packages [321, 179]; last parcel at 15:53, half delivered by 13:48, 56% by 14:00; 0 undelivered; 12.8 driver hours, 24 km |
| 1008 | 4 | 2 vans, stops [118, 129], packages [334, 166]; last parcel at 16:27, half delivered by 12:31, 74% by 14:00; 0 undelivered; 13.9 driver hours, 27 km |
| 1009 | 0 | 2 vans, stops [96, 102], packages [323, 177]; last parcel at 15:20, half delivered by 11:47, 85% by 14:00; 0 undelivered; 11.7 driver hours, 24 km |
| 1009 | 1 | 2 vans, stops [93, 101], packages [344, 156]; last parcel at 15:13, half delivered by 13:27, 69% by 14:00; 0 undelivered; 11.5 driver hours, 22 km |
| 1009 | 2 | 2 vans, stops [103, 112], packages [332, 168]; last parcel at 15:41, half delivered by 11:47, 75% by 14:00; 0 undelivered; 12.4 driver hours, 22 km |
| 1009 | 3 | 2 vans, stops [93, 102], packages [322, 178]; last parcel at 15:16, half delivered by 13:43, 53% by 14:00; 0 undelivered; 11.5 driver hours, 23 km |
| 1009 | 4 | 2 vans, stops [94, 99], packages [327, 173]; last parcel at 15:11, half delivered by 12:30, 87% by 14:00; 0 undelivered; 11.4 driver hours, 21 km |
