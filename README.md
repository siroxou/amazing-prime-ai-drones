# Amazing Prime AI Drones

Can a fleet of autonomous trucks, each launching 10 delivery drones, deliver a city's parcels faster than Amazon does today?

Flying one drone to one point is solved. This project is about the operation around it: every day brings a random set of parcels across the city, and an optimiser has to decide which truck covers which zone, the route each truck drives, where it launches and recovers its drones, which drone takes which parcel, where and from what height each parcel is put down, and the 3D path each drone flies around power lines, trees and buildings. All of that changes with the weather and with each parcel's size, weight and fragility.

It's scored against a model of Amazon's current last mile: parcels arriving at a delivery station, Delivery Service Partner drivers in vans, and Prime Air drones flying from fixed sites. Both systems start from the same delivery station, with the same days, parcels and city. The Amazon model is built only from public figures and is deliberately generous: good routes for free and the fast end of every range. How it's built, and where each number comes from, is in [docs/amazon-baseline.md](docs/amazon-baseline.md).

This is an independent project and isn't affiliated with or endorsed by Amazon.

This started as a fork of [self-driving-optimized](https://github.com/siroxou/self-driving-optimized), a self-driving car sensor study. The road generator, vehicle model and traffic from that project now drive the trucks; everything car-specific was taken out.

**Status:** Phase 1 is done. The 3D city is in (streets, ZIP codes, delivery zones, the distribution centre, hills, houses, apartment blocks, hazards and no-fly airspace), and so are random delivery days: parcels, recipients, weather and traffic. Next are the Amazon baselines, then the optimiser and the drone sim, in the phases in [ROADMAP.md](ROADMAP.md).

## The city

![Top-down map: 9 ZIP codes outlined, each split into 4 shaded zones, curving streets and cul-de-sacs around a grid centre, the distribution centre to the west, no-fly zones in red](docs/images/city-map.png)

Each seed gives a different city, about 1.5 x 1.2 km:

- **ZIP codes and zones:** straight arterial roads mark out 9 ZIP codes. Each ZIP splits into 4 delivery zones (its quarters), and every address belongs to one zone and one ZIP.
- **Streets:** the middle ZIP keeps a street grid. The ZIPs around it get two curving streets across each one, curving links between them and out to the arterials, and cul-de-sacs with turning circles off all of those. Houses face whatever street they're on.
- **Distribution centre:** a warehouse west of the city with 10 truck bays in its yard and an access road onto the middle arterial. Trucks start here.
- **Districts:** apartment blocks in the middle, with a balcony per flat on the street side. Small lots around them, bigger suburban lots further out.
- **Houses:** each lot has a house, a front and back yard, sometimes trees and fences. Every address has drop spots (porch, front yard, back yard, or its balcony) and the sim knows the clear height above each one, so a yard under a tree or a balcony under the one above is known in advance.
- **Hills:** broad hills and dips, about 60 m from the lowest point to the highest and up to 15% steep. Everything stands on the ground, and apartment floors are levelled from the high side so balconies clear the slope.

### Hazards and airspace

| Hazard | What's there |
|---|---|
| Power lines | poles down one side of every street outside the centre, with a power line at 9.5 m and a cable line at 6 m |
| High-voltage line | lattice pylons about 36 m tall across one corner of the city, 5 conductors from 25 to 36 m, with a 40 m strip under it kept clear of houses |
| Cell towers | two masts of 45–60 m, each held up by six guy wires anchored out to about half its height |
| Construction cranes | four building sites; on any given day most have a tower crane up, with its jib pointing a different way and its hook hanging at a different height. `City(seed, day=...)` changes only these and the stadium |
| Schools | no drones below 60 m over the school and its grounds, 7:30 to 16:00 |
| Hospital | no drones below 150 m within 150 m of the roof helipad, at any time |
| Stadium | no drones below 300 m within 300 m, 17:00 to 23:00 on event days |
| Airfield | east of the city: stay below 30 m within 1.2 km, and never over the runway or its approaches |

Airspace heights are above the ground under the drone. `city.airspace.blocked(points, hour)` says which zone, if any, each point is in.

| Edge of the centre | A suburban zone with a crane, pylons and power lines |
|---|---|
| ![3D view of apartment blocks with balconies next to small lots with trees and fences, on a slope](docs/images/city-centre.png) | ![3D view of suburban houses on curving streets with a tower crane, high-voltage pylons and power lines](docs/images/city-suburb.png) |

![3D overview of the whole city on its hills, with the distribution centre on the left, the stadium, schools, hospital, cranes and the high-voltage line](docs/images/city-overview.png)

The default city (seed 0) has 2,038 addresses, 4,252 drop spots and about 12,000 obstacles, and builds in about 0.7 s. Other seeds give 1,700 to 2,000 addresses. Drones see the city through raycasts: about 1,900 casts of 64 rays a second on a laptop, against buildings, trees, wires and the hills.

```python
from sim.city import City

city = City(seed=0, day=0)
print(city.summary())
city.zip_codes[city.address_zip[0]], city.address_zone[0]   # ZIP code and zone of address 0
city.spot_pos[city.spot_address == 0]                      # its drop spots
city.terrain.height(x, y)                                  # ground height
city.obstacles.cast(origin, directions, 40.0)              # distances and what each ray hit
city.obstacles.touching(point, 0.5)                        # what a 0.5 m sphere at point is touching, or None
city.airspace.blocked(points, hour=10.5)                   # which no-fly zone each point is in, or ""
```

## A delivery day

Each morning a random set of parcels is waiting at the distribution centre. `Day(city, parcels=500)` gives:

- **Parcels:** each one has an address, a size (envelope to oversize), dimensions, a weight and a fragility (robust, careful, fragile). Addresses get about 1.45 parcels each, in line with what DSP routes report, and about 82–85% of parcels weigh 5 lb or less, close to the 86% Amazon gave when it announced Prime Air.
- **Recipients:** for parcels that go in the truck's locker, how far each person will walk to the truck and how soon they turn up.
- **Weather, hour by hour:** temperature, wind speed and direction with gusts, wind growing with height, and rain on about 30% of days.
- **Traffic:** `day.travel_time(hour)` gives the time to drive every road edge, with rush hours, busier and quieter streets, and rain.

```
$ python -m sim.day
city seed 0, day 0: 500 parcels to 328 addresses (1.52 per stop)
sizes: 30% envelope, 34% small, 24% medium, 10% large, 2% oversize
weight: median 0.9 kg, 82% at 5 lb (2.27 kg) or less, heaviest 20.5 kg
fragility: 70% robust, 21% careful, 9% fragile
recipients walk up to a median 251 m and turn up after a median 9 min
weather: 5 to 18 C, wind 5.1 m/s average with gusts to 11.1 m/s, 0.0 mm of rain
traffic: arterials take 1.64x as long at 8:00 as at 3:00
city built in 730 ms, city + day in 734 ms
```

Most of these settings are reasoned guesses, because there's little public data on parcel mixes or recipients. [docs/days.md](docs/days.md) lists every setting, where each one comes from, and which are guesses. The 50 benchmark days are saved in `data/held-out/` (city seeds 1000–1009, which training never uses), so benchmark results stay comparable.

## How it works

| Decision | Made by | Depends on |
|---|---|---|
| Zones per truck, and their order | optimiser | parcel locations, traffic, depot |
| Truck route, launch and recovery points | optimiser | road graph, traffic, drone range in today's wind |
| Drone or truck locker for each parcel | optimiser | size, weight, fragility, drop spot, weather |
| Locker pickup points and how long to wait | optimiser | where locker recipients live, legal places to stop |
| Which drone, and when it launches | optimiser | battery, distance, other sorties, the truck's route |
| Drop spot and release height | drop planner | yard, porch or balcony, obstacles, wind drift, fragility |
| 3D flight path | path planner | power lines, trees, buildings, wind |
| Flying and landing on the moving truck | flight stack (hand-written) | the drone's sensors |
| Driving the truck | autonomous driver | traffic, the route |

The optimiser starts as a classical solver (OR-Tools plus heuristics). A learned optimiser replaces it only where it beats it on held-out days.

Two sims share the same city:

- **Macro sim:** road graph travel times plus a drone time and energy model. Fast enough to run thousands of days, so this is where planners are trained and scored.
- **Micro sim:** full 3D drones with a quadrotor model and trucks driving in traffic. It replays planned days to check the plans hold and to calibrate the macro sim's drone model.

### A delivery

1. The truck drives to its zone. The optimiser has already picked which parcels go by drone and where each drone launches.
2. A drone lifts off the roof dock while the truck is moving and follows its planned path, above the power lines and around trees.
3. At the address it goes to the chosen drop spot, comes down to the planned height, and releases or lowers the parcel.
4. It flies to its recovery point and lands on the truck, which has kept driving.
5. If it's running low on battery or loses the truck, it lands somewhere safe instead and the plan adjusts.

Parcels too big or heavy for a drone ride in a locker on the truck. The truck parks at a pickup point near those addresses, the recipients are told it's there, and they walk over and collect them while the drones keep working.

## Sensors

In the micro sim, each drone carries everything a real delivery drone could reasonably use. All of them are on all the time; they're modelled with noise, bias, latency and dropout rather than switched off.

| Sensor | What the drone gets |
|---|---|
| GNSS (GPS) | position and velocity, with drift, and much worse next to tall buildings |
| IMU | acceleration and rotation rate, with bias |
| Magnetometer | heading, disturbed near the truck and power lines |
| Barometer | altitude, with drift |
| Airspeed | airspeed, which together with GNSS gives a wind estimate |
| Downward rangefinder | height above whatever is directly below |
| Optical flow | ground speed from the downward camera, for low flight and landing |
| 3D lidar / depth camera | distances in sectors all around, for buildings, trees, fences and wires |
| Truck beacon (UWB) | range and bearing to the truck's dock, plus the truck's speed and heading |
| Dock marker camera | exact relative position of the dock slot once it's in view |
| Fleet comms | positions and planned paths of nearby drones, with latency and dropout |
| Battery monitor | charge left, voltage, current draw |
| Payload sensor | whether the parcel is still attached and its weight |
| Motor telemetry | rotor speeds, to notice a failing motor |

## Quickstart

Tested on Python 3.11.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-train.txt
pytest tests
python -m sim.city       # build a city, print what's in it, time the raycasts
python -m sim.day        # build a delivery day: parcels, weather, traffic
python -m sim.render     # redraw the pictures in docs/images
```

## Layout

```
sim/city.py          city layout: streets, ZIP codes, zones, distribution centre, hills, houses, hazards, airspace
sim/geometry.py      3D obstacles and hilly ground: raycasts and contact checks
sim/airspace.py      no-fly zones with heights and hours
sim/day.py           a delivery day: parcels, recipients, weather, traffic; day files
sim/render.py        matplotlib pictures of the city
sim/world.py         single procedural roads and a 2D raycaster, from the car project
sim/vehicle.py       kinematic bicycle model and collision shape, used by the truck and traffic
sim/traffic.py       IDM traffic and parked cars around the truck
sim/policy.py        runs an exported policy with plain numpy
train/export.py      exports a trained PPO model to .npz for sim/policy.py
tests/               tests
docs/amazon-baseline.md  how Amazon's current last mile is modelled, with sources
docs/days.md         every setting for parcels, weather and traffic, and where it comes from
data/held-out/       the 50 fixed benchmark days
ROADMAP.md           phases and exit criteria
```

## License

MIT
