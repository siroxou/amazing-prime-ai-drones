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

## Phase 1: City, parcels and weather ✓

- [x] City generator: straight arterial roads bounding 9 ZIP codes, each split into 4 delivery zones; a street grid in the middle ZIP and curving streets with cul-de-sacs in the others; all of it as a road graph with speed limits; and a distribution centre (delivery station) west of the city with 10 truck bays and an access road. Upstream of it (fulfilment centre, sort centre) is the same for both systems, so parcels simply arrive at the station each morning (`sim/city.py`)
- [x] Traffic levels per street: rush hours, a fixed busyness per street, busier and quieter days, rain (`sim/day.py`)
- [x] Districts: apartment blocks in the centre, small lots around it, suburban lots further out, so stops per route can be compared with what DSP drivers report
- [x] Addresses: houses and apartment flats (one per balcony). Each address gets its candidate drop spots (porch, front yard, back yard, or its balcony) with the clear height above each one. Yards have trees and fences; streets outside the centre have poles with a power line and a lower cable line
- [x] Hills: a ground height grid that everything stands on, up to 15% steep
- [x] Hazards: power and cable lines on every street outside the centre, a high-voltage line on pylons, guyed cell towers, and construction cranes that change from day to day
- [x] No-fly airspace with floors, ceilings and hours: schools, the hospital's helipad, the stadium on event days, and an airfield east of the city (`sim/airspace.py`)
- [x] 3D obstacles (turned boxes, upright cylinders, wires) and the ground, with raycasts and contact checks, using a coarse grid so queries only look nearby (`sim/geometry.py`)
- [x] Pictures of the city for the README (`sim/render.py`)
- [x] Parcels: a random set per day, each with an address, size, weight and fragility, drawn from adjustable distributions (`sim/day.py`, settings and sources in [docs/days.md](docs/days.md))
- [x] Recipients: for locker parcels, how far each recipient will walk to the truck and how quickly they turn up after being told it's there, both as adjustable distributions
- [x] Weather per day, hour by hour: wind speed and direction with gusts, wind growing with height, rain, temperature (which will change battery capacity)
- [x] Day files: any day can be saved and loaded back exactly, tied to its city, with a fixed held-out set of 50 days in `data/held-out/`

**Exit:** a city with 2,000 addresses and a 500-parcel day builds in under a second, and the same seed gives the same day.

Measured with `python -m sim.day` on an Apple Silicon laptop: the default city (seed 0: 2,038 addresses, 4,252 drop spots, about 12,000 obstacles) plus a 500-parcel day builds in **734 ms**, of which the day takes 4 ms. Tests check that the same seed gives the same day. A 64-ray, 40 m raycast runs **1,893 times a second**.

Caveat: other seeds give 1,700–2,000 addresses, so not every city reaches 2,000. Curving streets leave more open ground than a grid. Most of the day's settings are reasoned guesses rather than public figures; [docs/days.md](docs/days.md) marks which are which.

## Phase 2: Baselines ✓

- [x] **Amazon DSP vans:** loadout at the delivery station, one van and driver per route, routes planned by OR-Tools (so the driver gets a good route for free), driving at the speed limit with traffic, a service time per stop for parking, walking to the door and back, and a shift length cap. Every setting comes from public figures with a range, listed in [docs/amazon-baseline.md](docs/amazon-baseline.md), and results are reported against the fast end (`baselines/dsp.py`, results in [results/dsp-baseline.md](results/dsp-baseline.md))
- [x] **Calibration:** with the DSP settings, a 10-hour route in each density preset should land in the publicly reported range of stops and packages per route. If it doesn't, the city or the settings are wrong, and that gets fixed before anything is compared. **Passed**: 166–209 s per stop puts both districts in range ([results/dsp-calibration.md](results/dsp-calibration.md))
- [x] **Prime Air from fixed sites:** drones flying from the delivery station or a drone site, with the published payload and radius limits. Parcels out of range or too heavy go by DSP van. Shows whether launching from a moving truck beats launching from a fixed site (`baselines/prime_air.py`, results in [results/prime-air-baseline.md](results/prime-air-baseline.md))
- [x] **Autonomous trucks, no drones:** every parcel goes in the truck's locker and recipients collect it at stops along the route. Shows how much of any gain comes from the drones (`baselines/trucks_only.py`, results in [results/trucks-only-baseline.md](results/trucks-only-baseline.md))
- [x] **Classical truck + drone solver:** launch stops, drone sortie scheduling and truck routing with OR-Tools plus construction heuristics, first with a fixed-speed drone model and now with the Phase 3 cost model (`baselines/classical.py`, results in [results/classical-solver.md](results/classical-solver.md))
- [x] Drones that launch from a moving truck and land on it further along the route (`baselines/moving.py`, results in [results/moving-launch.md](results/moving-launch.md)). It saves only a few minutes here, because the trucks spend most of their time parked for the locker
- [x] Metrics per day: time until the last parcel is delivered, share delivered by a set time, average time from station to doorstep, parcels per hour per vehicle, driver hours, distance driven, drone energy, parcels that went by locker and why, and how long locker recipients waited and walked

**Exit:** the DSP calibration passes, and all baselines run on the full held-out set in under 10 minutes on a laptop, with results in `results/baselines.md`.

**Passed.** The calibration passes, and `python -m baselines.run` runs every baseline on all 50 held-out days in **6.3 minutes on 6 workers** (2.1 minutes on 18), writing the side-by-side table in [results/baselines.md](results/baselines.md). Run to run, OR-Tools' fixed time per solve moves the vans' results by up to about 10 minutes, so smaller gaps between systems don't count.

## Phase 3: Drone cost model and drop planning ✓

- [x] Flight paths: climb, cruise and descent legs, with a height profile that clears roofs, trees, wires, cranes and pylons by 10 m and follows the airspace rules, bent round no-fly zones (`sim/drone.py`)
- [ ] A full 3D search for paths that go round obstacles sideways instead of over them
- [x] Time and energy per sortie from distance, climb, payload weight, parcel size (drag) and wind, with a battery that holds less in the cold ([docs/drone-model.md](docs/drone-model.md)). To be calibrated against the micro sim in Phase 5
- [x] Drop planning per parcel: pick the drop spot and release height. Lower and slower for fragile parcels and gusty wind, a winch lowering for balconies and tight yards, and the wind drift on release accounted for. Some drop spots get ruled out in strong wind
- [x] Payload limits: parcels too big or heavy for a drone go in the truck's locker instead
- [x] The classical solver and moving launches use all of it

## Phase 3b: Truck locker

- [ ] Locker on each truck for parcels a drone can't carry. The truck parks at a pickup point, recipients nearby are told when it will be there, and each one walks over and opens their compartment
- [ ] The optimiser picks pickup points (a legal place to stop, within walking distance of as many locker recipients as possible) and how long to wait at each. Drones keep launching and landing while the truck is parked
- [ ] A locker parcel counts as delivered when it's collected. Uncollected parcels after the wait go back to the depot and count against the fleet
- [ ] Locker capacity per truck limits how many oversized parcels a truck can take, which feeds into zone assignment

**Exit:** on held-out days, every oversized parcel is either collected or reported as returned, and the waiting time at pickup points is included in the fleet's delivery time.

**Exit:** the classical solver from Phase 2 using this cost model beats the Amazon DSP baseline on the held-out days, or the gap is written up honestly.

**Result: a split verdict, written up.** On the 50 held-out days the fleet gets 86% of parcels out by 14:00, against about 65–70% for the vans, and finishes around noon instead of mid-afternoon. But it leaves 14% behind, while the vans deliver everything. Wind is the main limit: drones take 36% of parcels, down from 46% with the fixed-speed model ([results/baselines.md](results/baselines.md), [docs/drone-model.md](docs/drone-model.md)).

## Phase 4: Learned optimiser ← in progress

- [x] Planning env over the macro sim, scored on delivery time, with a parcel left for tomorrow counting 24 hours (`optimiser/routes.py`). So far it covers one decision, how long each truck waits at each stop
- [ ] The same env for dispatch, routing and sortie decisions
- [x] First learned improvement to the classical solver: locker waits per stop, trained with PPO (`optimiser/waits.py`, [results/learned-waits.md](results/learned-waits.md)). It beats the classical solver, but a two-setting hand rule matches it
- [x] Afternoon second pass: each truck goes out again with what it couldn't deliver (`baselines/classical.py`). The fleet goes from 86% to 96% delivered today and from 4.13 h to 2.15 h, ahead of both Amazon baselines, if everyone who missed the truck comes out the second time. If nobody does, it's 3.73 h ([results/baselines.md](results/baselines.md))
- [ ] Learn the locker waits again with the second pass in: the policies trained without it score 2.23 h with it, against 2.00 h for a re-tuned hand rule
- [ ] Learned decisions without an obvious rule: which parcels go by drone, where launch points go
- [ ] A full learned planner, such as an attention-based routing model trained with RL
- [ ] Re-planning during the day: traffic jams, a drone that comes back late, a wind change
- [x] Benchmark against the classical solver and the Amazon baselines on held-out days, three seeds

**Exit:** the learned optimiser beats the classical solver on held-out days, averaged over three seeds. If it doesn't, the classical solver stays as the main result and this is written up.

**Passed, with a caveat.** Learned locker waits score 3.03 h on the held-out days (three seeds, 3.01 to 3.05), against 4.13 h for the classical solver's 10-minute wait and 3.64 h for the best fixed wait. But a two-setting hand rule tuned the same way scores 3.02 h, so learning isn't needed for this decision. Against Amazon on the same score, the fleet tied the DSP vans (3.01 h) and was behind Prime Air with vans (2.71 h). Adding the afternoon second pass then mattered more than the waits: the classical solver scores 2.15 h with it, and the learned waits no longer help. The rest of this phase is about decisions where a simple rule isn't obvious, learned with the second pass in.

## Phase 5: Micro sim check

- [x] 3D neighbourhood from the city generator: houses, yards, trees, fences, power lines, pylons, cell towers, cranes, apartment blocks with balconies, hills (built in Phase 1)
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
