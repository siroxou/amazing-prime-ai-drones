# Roadmap

Flying a drone to a point is solved. The hard part, and the point of this project, is the whole operation: a city's worth of random parcels every day, a fleet of autonomous trucks each carrying 10 drones, and an optimiser that decides everything in between:

- which truck covers which zone, in what order, and the route it drives
- where along that route each truck launches and recovers drones, and where it parks for locker pickups
- which parcels go by drone, which drone takes which parcel, and when
- the drop spot and release height at each address: yard, porch or balcony, lowered or dropped
- 3D flight paths around power lines, trees and buildings
- all of it adjusted for the day's weather and each parcel's size, weight and fragility

The question: **across random days, does the autonomous fleet deliver faster than Amazon's current last-mile system?** That means delivery station, Delivery Service Partner (DSP) drivers in vans, and Prime Air drones flying from fixed sites, modelled from public figures (see [docs/amazon-baseline.md](docs/amazon-baseline.md)). Both systems get the same days, the same parcels, the same city and the same delivery station, and the Amazon side is given the fast end of every range. A sim result isn't proof about real streets, so every number is reported with its assumptions.

Each phase ends with an exit check that has to pass before the next one starts.

## Design decisions

- **Two levels of fidelity.** Optimising a whole day for several trucks and dozens of drones needs thousands of simulated days. A fast macro sim (road graph travel times, drone time and energy from a cost model) is where the optimiser trains and is scored. A slower micro sim (3D drones, trucks in traffic) checks that the macro plans actually hold, and calibrates the cost model.
- **Classical where it's solved, learned where it pays.** Drone flight uses a hand-written flight stack (cascaded PID, then a geometric controller if needed). Learning goes into planning, and a learned planner is kept only if it beats the classical solver on held-out days.
- **Honest baselines first.** No learned result counts until the Amazon baselines and a classical solver are in place and benchmarked.
- **Settings that carry over from the car project:** for any PPO training, 12 parallel envs, VecNormalize rewards, target KL 0.02, tanh MLP, lower starting action noise, and at least three seeds per result.

## Phase 0: Fork ✓

- [x] Copy the reusable parts of [self-driving-optimized](https://github.com/siroxou/self-driving-optimized): procedural roads, the vehicle model (now the truck and road traffic), IDM traffic, numpy policy runner and the PPO-to-numpy export
- [x] Remove the car-only parts: car sensors and observation layout, driving env, lane follower, hazards, evaluation levels, the browser viewer, the MetaDrive research track, trained models and results
- [x] README and this roadmap

**Exit:** `pytest tests` passes on a fresh install.

## Phase 1: City, parcels and weather ← in progress

- [x] City generator: a street grid as a road graph with speed limits, arterial roads bounding 9 ZIP codes, each ZIP split into 4 delivery zones, and a distribution centre (delivery station) west of the city with 10 truck bays and an access road. Upstream of it (fulfilment centre, sort centre) is the same for both systems, so parcels simply arrive at the station each morning (`sim/city.py`)
- [ ] Traffic levels per street
- [x] Districts: apartment blocks in the centre, small lots around it, suburban lots further out, so stops per route can be compared with what DSP drivers report
- [x] Addresses: houses and apartment flats (one per balcony). Each address gets its candidate drop spots (porch, front yard, back yard, or its balcony) with the clear height above each one. Yards have trees and fences; streets outside the centre have poles with a power line and a lower cable line
- [x] 3D obstacles (boxes, upright cylinders, wires) with raycasts and contact checks, using a coarse grid so queries only look nearby (`sim/geometry.py`)
- [x] Pictures of the city for the README (`sim/render.py`)
- [ ] Parcels: a random set per day, each with an address, size, weight and fragility, drawn from adjustable distributions
- [ ] Recipients: for locker parcels, how far each recipient will walk to the truck and how quickly they turn up after being told it's there, both as adjustable distributions
- [ ] Weather per day, changing through the day: wind speed and direction with gusts, rain, temperature (which changes battery capacity)
- [ ] Day files: every random day is saved by seed, with a fixed held-out set for benchmarks

**Exit:** a city with 2,000 addresses and a 500-parcel day builds in under a second, and the same seed gives the same day.

So far, measured with `python -m sim.city` on an Apple Silicon laptop: the default city (2,058 addresses, 4,622 drop spots, about 14,000 obstacles) builds in **178 ms**, and a 64-ray, 40 m raycast runs **3,271 times a second**. Parcels and weather aren't in yet.

## Phase 2: Baselines

- [ ] **Amazon DSP vans:** loadout at the delivery station, one van and driver per route, routes planned by OR-Tools (so the driver gets a good route for free), driving at the speed limit with traffic, a service time per stop for parking, walking to the door and back, and a shift length cap. Every setting comes from public figures with a range, listed in [docs/amazon-baseline.md](docs/amazon-baseline.md), and results are reported against the fast end
- [ ] **Calibration:** with the DSP settings, a 10-hour route in each density preset should land in the publicly reported range of stops and packages per route. If it doesn't, the city or the settings are wrong, and that gets fixed before anything is compared
- [ ] **Prime Air from fixed sites:** drones flying from the delivery station or a drone site, with the published payload and radius limits. Parcels out of range or too heavy go by DSP van. Shows whether launching from a moving truck beats launching from a fixed site
- [ ] **Autonomous trucks, no drones:** every parcel goes in the truck's locker and recipients collect it at stops along the route. Shows how much of any gain comes from the drones
- [ ] **Classical truck + drone solver:** zone assignment, truck routing and drone sortie scheduling with OR-Tools plus construction heuristics, using the drone cost model from Phase 3 (start with a simple fixed-speed version)
- [ ] Metrics per day: time until the last parcel is delivered, share delivered by a set time, average time from station to doorstep, parcels per hour per vehicle, driver hours, distance driven, drone energy, parcels that went by locker and why, and how long locker recipients waited and walked

**Exit:** the DSP calibration passes, and all baselines run on the full held-out set in under 10 minutes on a laptop, with results in `results/baselines.md`.

## Phase 3: Drone cost model and drop planning

- [ ] 3D path planner over each neighbourhood: shortest safe path between launch, drop and recovery points, keeping clear of power lines, trees and buildings, with separate climb, cruise and descent legs
- [ ] Time and energy per sortie from distance, climb, payload weight, parcel size (drag) and wind along the path. Calibrated against the micro sim in Phase 5
- [ ] Drop planning per parcel: pick the drop spot and release height. Lower and slower for fragile parcels and gusty wind, a winch lowering for balconies and tight yards, and the wind drift on release accounted for. Some drop spots get ruled out in strong wind
- [ ] Payload limits: parcels too big or heavy for a drone go in the truck's locker instead

## Phase 3b: Truck locker

- [ ] Locker on each truck for parcels a drone can't carry. The truck parks at a pickup point, recipients nearby are told when it will be there, and each one walks over and opens their compartment
- [ ] The optimiser picks pickup points (a legal place to stop, within walking distance of as many locker recipients as possible) and how long to wait at each. Drones keep launching and landing while the truck is parked
- [ ] A locker parcel counts as delivered when it's collected. Uncollected parcels after the wait go back to the depot and count against the fleet
- [ ] Locker capacity per truck limits how many oversized parcels a truck can take, which feeds into zone assignment

**Exit:** on held-out days, every oversized parcel is either collected or reported as returned, and the waiting time at pickup points is included in the fleet's delivery time.

**Exit:** the classical solver from Phase 2 using this cost model beats the Amazon DSP baseline on the held-out days, or the gap is written up honestly.

## Phase 4: Learned optimiser

- [ ] Planning env over the macro sim: the optimiser makes the dispatch, routing and sortie decisions as the day goes, and gets scored on delivery time
- [ ] Start with learned improvements to the classical solver (for example, learning which parcels go by drone, or where launch points go), then try a full learned planner, such as an attention-based routing model trained with RL
- [ ] Re-planning during the day: traffic jams, a drone that comes back late, a wind change
- [ ] Benchmark against the classical solver and the Amazon DSP baseline on held-out days, three seeds

**Exit:** the learned optimiser beats the classical solver on held-out days, averaged over three seeds. If it doesn't, the classical solver stays as the main result and this is written up.

## Phase 5: Micro sim check

- [x] 3D neighbourhood from the city generator: houses, yards, trees, fences, power lines, apartment blocks with balconies (built in Phase 1)
- [ ] Wind with gusts
- [ ] Quadrotor model: four rotors with motor lag, drag, ground effect, a parcel that changes the mass when released, battery that drains with thrust
- [ ] Hand-written flight stack following the planned 3D paths, including the drop and the landing on a moving truck's roof dock
- [ ] Sensors with noise, bias, latency and dropout (the full list is in the README)
- [ ] Replay planned days from the macro sim and compare: how close are real sortie times and energy to the cost model, and how many sorties fail

**Exit:** micro sim sortie times are within 10% of the cost model on average, and fewer than 2% of planned sorties fail.

## Phase 6: Autonomous trucks

- [ ] Truck driving in the micro sim: lane following, junctions, traffic, pulling over at launch points. The lane follower and driving work from self-driving-optimized are the starting point
- [ ] Driving the same routes as the Amazon DSP baseline, the autonomous truck must be no slower between stops
- [ ] Launch and recovery while moving, and pulling over when the plan needs a stationary recovery

**Exit:** on replayed held-out days, the full autonomous system (trucks driving themselves, drones flying themselves) still beats the Amazon DSP baseline.

## Phase 7: Hardening

- [ ] Bad days: strong wind, rain, a no-fly window, a truck breakdown, a drone that loses a motor, GPS loss between tall buildings
- [ ] Safe fallbacks: a drone that can't make its recovery lands somewhere safe and gets collected later, and the plan adjusts
- [ ] Results across the whole held-out set, including the days where Amazon's current system wins

**Exit:** no bad-day scenario ends in a crash into people or property in the micro sim, and the fleet's delivery time is reported for every scenario.

## Phase 8: Write-up

- [ ] Renders with matplotlib: a full day over the city map, and a 3D view of one neighbourhood's sorties
- [ ] Docs: city and parcels, baselines, cost model, optimiser, micro sim, results
- [ ] Results tables with every assumption listed, especially the DSP service time per stop

**Exit:** someone new can install, run the tests, and reproduce the published numbers from the docs alone.
