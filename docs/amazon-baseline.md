# Amazon baseline

The fleet is compared against a model of how Amazon delivers today. Amazon doesn't publish its route data, so the model is built from public figures only: Amazon's own articles first, then driver reports and trade press. Every number is a setting with a range, and results are reported at the end of the range that favours Amazon.

This is an independent project and isn't affiliated with or endorsed by Amazon.

## How Amazon's last mile works

A parcel goes through a chain of buildings before it reaches a vehicle:

1. **Fulfilment centre:** stock is stored, picked and packed.
2. **Sort centre:** parcels are sorted by destination, roughly by ZIP code, and loaded onto trucks.
3. **Delivery station:** the last building. Parcels are staged into routes and loaded into vans.
4. **Van and driver:** most routes are run by Delivery Service Partners (DSPs), small independent companies that employ the drivers and run Amazon-branded vans. Some areas use other contracted couriers.

On top of that, Prime Air delivers small parcels by drone from fixed sites in a growing number of areas.

## What the sim models

Steps 1 and 2 happen the same way for both systems, so they're left out: parcels arrive at the delivery station each morning. The comparison starts at the station.

| | Amazon baseline | This project |
|---|---|---|
| Leaves from | delivery station | the same delivery station |
| Vehicle | one van and driver per route | autonomous truck with 10 drones and a locker |
| Routes | planned by OR-Tools for the van | planned by the fleet optimiser |
| At each address | driver parks, walks to the door, walks back | drone drop, or locker pickup for oversized parcels |
| Drones | Prime Air, from a fixed site, within its payload and radius limits | launched and recovered by the moving truck |

## Settings and sources

| Setting | Range used | Where it comes from |
|---|---|---|
| Stops per DSP route | 150–190 | Amazon: a DSP owner says drivers typically have at least 150 stops [1]; a DSP driver reports 170–190 [2] |
| Packages per DSP route | 200–300 | Amazon: 200–300 a day, more in dense areas such as apartment blocks [1]; a driver reports 250–300 [2] |
| Shift length | 10 hours | common in DSP job listings and driver reports [3]. Real days sometimes run longer; the sim uses 10 hours, which favours Amazon |
| Service time per stop | 166 s, the fast end of a calibrated 166–209 s window | not published. Calibrated: with a 10-hour shift and the city's driving times, it's what gives 150–190 stops ([results/dsp-calibration.md](../results/dsp-calibration.md)). Reported results use the fast end |
| Extra time per extra package at a stop | 10 s | guess |
| What counts as a stop | one building: a house, or a whole apartment block | how drivers count stops |
| Station loadout | 30 minutes | not published; reported with every result |
| Shift start | 9:30, out of the station by 10:00 | guess; only affects which hours' traffic the vans meet |
| Breaks | none modelled | the service time absorbs them, since the public stop counts include them |
| Prime Air site | at the distribution centre | Prime Air flies from Amazon delivery facilities [6] |
| Prime Air payload | 5 lb (about 2.3 kg), one parcel per flight | reported specs for the MK30 drone [4][5] |
| Prime Air parcel size | envelope, small and medium boxes; not large or oversize | guess: no cargo box size is published |
| Prime Air radius | 7.5 miles (about 12 km) from the site | Amazon: up to 7.5 miles from an Amazon facility [6]. The whole sim city is inside it |
| Prime Air cruise | 30 m/s (58 knots) at 61 m (200 ft), never above 122 m (400 ft) | FAA environmental filings for Prime Air sites [9][10] |
| Prime Air drop | lowers to 4 m (13 ft) over the yard and lets go; needs open sky and 3 m (10 ft) clear around | FAA filing and press coverage [9][11]. Houses only: the MK30 delivers to yards, not balconies |
| Climb, descent, drop and turnaround | 3 m/s up, 2 m/s down, 15 s to let go, 5 min at the site to reload and change battery | guess |
| Weather | flies in light rain (up to 2.5 mm/h) and gusts up to 12 m/s | Amazon says the MK30 flies in light rain [11]; 2.5 mm/h is where "light rain" ends. No wind limit is published; 12 m/s is a guess, and it grounds the drones on about 10% of days |
| No-fly zones | flies over school zones (they end at 60 m) and under the airfield's 30 m limit; goes round the hospital and stadium zones; won't drop inside an active zone | the sim's airspace rules |
| Drones at the site | 5, 10 and 20 | not published; all three are reported |
| Flying hours | 10:00 to 19:30, the same as the vans | guess |
| Prime Air promise | delivery within 60 minutes | Amazon [6]. Expansion coverage talks about 30 minutes as a goal [7]; the sim uses actual flight time, which is shorter than either |

## Calibration check

Before any comparison, the DSP van model has to reproduce the public figures: in each density preset, a 10-hour route should land in the 150–190 stop and 200–300 package range. If it doesn't, the city or the settings get fixed first. This stops the fleet from looking good just because the van model is slow.

**Result: passed** ([results/dsp-calibration.md](../results/dsp-calibration.md), `python -m baselines.calibrate`). In a 24 x 24-block city, with 15% of houses getting parcels, a service time of 166–209 s puts routes in both the dense and suburban districts inside 150–190 stops and 200–300 packages. That's inside the plausible 30–228 s. With 10% or 25% of houses getting parcels, the fast end moves only to 157–171 s. Apartment blocks aren't calibrated, because Amazon gives no stop figures for them.

## Known gaps

- Real routes depend on season, weather, traffic and how a station is run. The sim covers weather and traffic but not peak-season loads or late trucks from the sort centre.
- Driver reports vary a lot and most aren't audited. The ranges above lean on Amazon's own figures where they exist.
- Amazon keeps changing its network, vans and drones. These figures are as of October 2026 and should be rechecked before publishing results.

## Sources

1. Amazon, [I'm an Amazon Delivery Service Partner. Follow me on a typical day](https://www.aboutamazon.com/news/transportation/amazon-delivery-service-partner-diary-photos)
2. Amazon, [I deliver packages to Amazon customers. Follow me on a typical day as a delivery driver in a Rivian van](https://www.aboutamazon.com/news/transportation/photos-day-in-the-life-amazon-delivery-driver)
3. Routerra, [How many stops does an Amazon driver make a day?](https://routerra.io/blog/amazon-driver-stops-per-day)
4. Wikipedia, [Amazon Prime Air](https://en.wikipedia.org/wiki/Amazon_Prime_Air)
5. DroneXL, [Amazon Prime Air MK30 at XPONENTIAL Europe](https://dronexl.co/2026/04/02/amazon-prime-air-mk30-drone-2/)
6. AWS, [Air delivery](https://aws.amazon.com/solutions/amazon/one-amazon-lane/air-delivery/)
7. TechSpot, [Amazon to bring 30-minute drone delivery to 500 US locations by the end of 2026](https://www.techspot.com/news/113543-amazon-drones-soon-deliver-nearly-500-us-cities.html)
8. Amazon, [Our fulfillment centers](https://www.aboutamazon.com/amazon-fulfillment/our-fulfillment-centers), for the network description above
9. FAA, [Technical noise report, Amazon Prime Air, Omaha](https://www.faa.gov/uas/advanced_operations/nepa_and_drones/Amazon_Omaha_NE_Appendix_E_ADA_508_Final.pdf)
10. FAA, [Amazon Prime Air operations specifications re-evaluation, Pendleton](https://www.faa.gov/uas/advanced_operations/nepa_and_drones/20250827_Amazon_Pendleton_OR_Written_ReEvaluation.pdf)
11. Amazon, [Photos of the MK30 drone](https://www.aboutamazon.com/news/transportation/amazon-prime-air-drone-delivery-mk30-photos)
