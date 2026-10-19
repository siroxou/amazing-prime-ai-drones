# Delivery days

A day is everything that changes from one morning to the next: the parcels waiting at the distribution centre, the people they're for, the weather, how busy the roads are, and which cranes are up. `Day(City(seed, day=d))` always gives the same day for the same seed and day number.

Every number below is a setting at the top of `sim/day.py`. Where a public figure exists it's listed. Where it doesn't, the setting is a reasoned guess, it's marked as one, and results should be checked for how much they depend on it.

## Parcels

| Setting | Value | Where it comes from |
|---|---|---|
| Parcels per address | 1 + Poisson(0.45), about 1.45 on average | DSP routes carry 200–300 packages over 150–190 stops, so 1.3–1.8 per stop ([amazon-baseline.md](amazon-baseline.md)) |
| Which addresses | any address in the city, equally likely | guess. Real demand isn't even, but there's no public data to shape it |
| Size | envelope 30%, small 35%, medium 22%, large 10%, oversize 3% | guess, tuned so the weights below come out near the one public figure |
| Dimensions | per size, from 30 x 22 x 2 cm (envelope) to 100 x 60 x 50 cm (oversize), each side ±20% | guess, typical box sizes |
| Weight | log-normal per size, medians 0.2, 0.8, 1.5, 5 and 12 kg, capped at 30 kg | tuned to the figure below. About 82–85% of parcels come out at 5 lb (2.27 kg) or less |
| Fragility | robust 70%, careful 20%, fragile 10% | guess |

The one public figure on parcel weight is old: when Amazon announced Prime Air in 2013, Jeff Bezos said its drones could carry up to 5 lb, which covered about 86% of what Amazon delivered ([AP via The Spokesman-Review, 2013](https://www.spokesman.com/stories/2013/dec/02/amazoncom-sees-delivery-drones-future/)). That was his estimate, not published data, and it's more than ten years old. 5 lb is also the payload of Amazon's current MK30 drone, so the share of parcels under 5 lb matters a lot for the Prime Air baseline.

## Recipients

Only matters for parcels too big for a drone, which go in the truck's locker. Everyone at one address counts as the same person.

| Setting | Value | Where it comes from |
|---|---|---|
| How far they'll walk to the truck | log-normal, median 250 m, capped at 800 m | guess |
| How soon they turn up after being told the truck is there | log-normal, median 10 minutes | guess |

These two decide how well the locker works and have no public data behind them, so locker results get reported across a range of them.

The trucks-only baseline adds four more guesses: 10 minutes' warning before the truck arrives, a wait of 10, 20 or 30 minutes at each pickup point (all three are reported), walking at 1.3 m/s, and pavements 1.3 times the straight-line distance. Each locker has 200 compartments.

## Weather

Hourly from 0:00 to 24:00, interpolated in between.

| Setting | Value | Where it comes from |
|---|---|---|
| Temperature | a random season (mean 2 °C in midwinter to 22 °C in midsummer, ±3 °C), a daily swing of 3–7 °C peaking at 15:00 | guess, a temperate climate |
| Wind at 10 m | Weibull with shape 2 and scale 5 m/s for the day, a little stronger in the afternoon, varying hour to hour | guess, typical inland wind |
| Gusts | 1.3–1.6 times the mean wind, varying hour to hour | guess, typical gust factors over towns |
| Wind direction | random for the day, drifting about 9° an hour | guess |
| Wind with height | grows as (height / 10 m)^0.25 | the usual power law over suburbs |
| Rain | 30% of days have one or two showers of 1–5 hours, averaging 2 mm/h | guess |

Not modelled yet: wind sheltering behind buildings and speeding up between them, fog, snow and ice. Those come with the micro sim (ROADMAP Phase 5).

## Traffic

`day.travel_time(hour)` gives the seconds to drive each road edge at that time.

| Setting | Value | Where it comes from |
|---|---|---|
| Free flow | edge length / speed limit (50 km/h arterials, 30 km/h side streets) | the city |
| Rush hours | extra delay peaking at 8:00 (+60%) and 17:30 (+80%), plus 10% all day | guess |
| How much each street feels it | arterials 1.0, side streets 0.4, times a random factor per street that stays the same every day | guess |
| Busier and quieter days | the whole day's delay times 0.8–1.2 | guess |
| Rain | 15% slower while it's raining more than 0.5 mm/h | guess |

The DSP calibration check in Phase 2 tests these against the public stops-per-route figures. If a 10-hour van route doesn't land in the reported range, these settings are among the first suspects.

## Day files and the held-out set

`day.save(path)` writes a day to a `.npz` file, and `Day.load(path, city)` reads it back exactly as saved, even if the generator has changed since. Each file carries a fingerprint of the city's addresses and refuses to load against a different city.

The benchmark days are fixed: city seeds 1000–1009, days 0–4, 500 parcels each, saved in `data/held-out/`. Training only ever uses city seeds below 1000. To rebuild them after a change to the city:

```bash
python -m sim.day --held-out data/held-out
```

Rebuilding changes the benchmark, so any results published before it no longer compare.
