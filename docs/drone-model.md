# The drone model

`sim/drone.py` says how long a delivery flight takes, how much battery it uses, and how each parcel is put down. The fleet solver (`baselines/classical.py`, `baselines/moving.py`) plans every flight with it. Prime Air keeps its own simpler model, built from Amazon's published MK30 figures.

None of the numbers below come from a real aircraft. They're a plausible delivery quadcopter of about 9 kg carrying up to 5 kg, picked so the power figures land in the usual range for multirotors (roughly 60–80 W per kg to hover). They get checked against the 3D flight sim in Phase 5. Until then, treat every result that depends on them as provisional.

## Power and battery

Power comes from momentum theory, the standard first model for multirotor delivery energy. It adds up three things:

- the rotors' induced power to hold the drone and parcel up, which falls as the drone picks up speed
- the power to push the drone and the parcel's box through the air
- climbing

On top of that is a fixed draw for the electronics.

| Setting | Value |
|---|---|
| Drone mass with battery | 9 kg |
| Payload | up to 5 kg, one parcel per flight |
| Rotor disc area | 1.8 m² (four 30-inch rotors) |
| Rotor and motor efficiency | 0.7 |
| Drag area of the drone | 0.15 m² |
| Drag of a parcel box | coefficient 1.05 on its two shorter sides (carried long side forward) |
| Electronics | 50 W |
| Cruise airspeed | 15 m/s |
| Climb, descent | 3 m/s, 2 m/s |
| Battery | 600 Wh usable at 20 °C, 20% never used, 1% less per °C below 20 °C |

That gives about 610 W to hover empty, 810 W with a 2 kg parcel and 1,150 W with 5 kg, and about 670 W cruising empty. A typical flight from a truck stop is 2–3 minutes and 30–40 Wh, a small share of the battery, so the battery almost never limits a flight here. The wind does.

## Wind

The drone holds its airspeed, so the wind changes its speed over the ground. A headwind costs time and battery, and a crosswind has to be flown into. Wind at cruise height is the day's 10 m wind scaled up with height (`sim/day.py`). On windy days it can be faster than the drone's 15 m/s airspeed. The drone could then fly out with the wind but not get back, so it isn't sent. That, plus the 12 m/s gust limit, is the main reason parcels planned for a drone end up in the locker.

## Flight height

Each leg follows a height profile along its line:

- at least 30 m above the ground and 10 m above the tallest thing near the path (roofs, trees, power lines, cranes, pylons, cell towers)
- climbing or descending no steeper than the drone's climb rate allows at cruise speed
- never above 120 m
- over school zones while they're on (they end at 60 m)
- under the airfield's 30 m limit, coming down to as low as 15 m there
- round the hospital and stadium zones, which go too high to fly over

Two known limits:

- The heights come from the straight line, even where the route bends round a no-fly zone.
- A leg that would have to cross the high-voltage line under the airfield's limit can't be flown, because the line plus clearance needs 46 m. It isn't routed round; the parcel goes in the locker.

## Putting the parcel down

For each parcel, at the hour it flies, every drop spot at its address with open sky above is considered, and the quickest way of putting it down that has room is used:

| Way | When | Room needed around the spot | Time over the spot |
|---|---|---|---|
| Drop | robust parcels from 3 m, careful ones from 1 m; never fragile ones | 0.3 m, plus drift: 30% of the gust speed over the fall time | 7 s |
| Lower on a line | anything; the only way onto a balcony | 0.3 m plus line swing (0.008 m per m of line per m/s of gust, from 8 m up), and 0.7 m for the drone hovering above | 32 s |
| Set down | anything, in a yard or on a porch | 0.9 m rotor radius plus 0.3 m, plus 0.05 m per m/s of gust | 12 s |

Covered balconies and anything under a tree or overhang can't be reached from above. Spots inside a no-fly zone the drone can't go over or under aren't used. In gusty weather, tight spots and balconies drop out first.

Porches have no roofs in the city model, so almost every house has somewhere a drone can set a parcel down. Real porches often have roofs, so this flatters the drones.

## What it changed

Against the fixed-speed model the fleet used in Phase 2, on the 50 held-out days:

| | fixed-speed model | cost model |
|---|---|---|
| parcels by drone | 46% | 36% |
| delivered today | 90% | 86% |
| last parcel | 11:45 | 12:04 |
| half of all parcels by | 10:58 | 11:09 |

The drones lose about a fifth of their parcels. Most of those go to wind, either too windy to fly back or too gusty for the drop spot. Some go to legs that can't be flown at a legal height, mostly on the airfield side. They move to the locker, where some recipients don't come out in time.
