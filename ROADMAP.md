# Roadmap

The end goal is a fleet of 10 delivery drones that ride on a delivery truck, launch while it drives its route, each drop one parcel at a house or apartment balcony, and fly back to land on the truck wherever it has got to by then.

Control is split in two:

- **Fleet controller** (on the truck, one per fleet): decides which drone takes which parcel, when it launches, which altitude band and corridor it flies in, and when and where it should meet the truck again. It plans with the truck's route and the parcel list.
- **Drone policy** (shared, one copy per drone): flies the drone. It takes the fleet controller's goal plus the drone's own sensors and handles everything local: obstacles at the drop point, wind, other drones close by, the drop itself and the landing on a moving truck.

Each phase ends with an exit check that has to pass before the next one starts.

## Phase 0: Fork ✓

- [x] Copy the reusable parts of [self-driving-optimized](https://github.com/siroxou/self-driving-optimized): procedural roads, the vehicle model (now the truck and road traffic), IDM traffic, numpy policy runner and the PPO-to-numpy export
- [x] Remove the car-only parts: car sensors and observation layout, driving env, lane follower, hazards, evaluation levels, the browser viewer and Pages deploy, the MetaDrive research track, trained car models and results
- [x] README and this roadmap

**Exit:** `pytest tests` passes on a fresh install.

## Phase 1: 3D world

- [ ] Neighbourhood generator on top of the existing roads: houses as boxes with roof heights, front and back yards, trees (cylinders with a canopy), garden fences, street lights and power lines along the road
- [ ] Apartment blocks with balconies on several floors; each balcony is a drop point with a railing and an overhang above it
- [ ] Drop points per house: a clear spot in the yard, or a balcony. Some are partly blocked (a tree over the yard, a washing line, a parked car in the drive)
- [ ] The truck gets its own body (box van, about 7 m long) and a roof dock with room for 10 drones
- [ ] Wind: a steady wind per episode plus gusts, stronger above roof height and in the gaps between apartment blocks
- [ ] 3D raycaster against boxes, cylinders, wires and the ground, vectorised in numpy
- [ ] Tests: raycasts hit hand-built boxes and cylinders at the right distance, every drop point is reachable from above, same seed gives the same neighbourhood

**Exit:** a neighbourhood with 10 drop points builds in under 50 ms, and a 64-ray 3D cast runs at least 5,000 times a second.

## Phase 2: Drone dynamics

- [ ] Quadrotor rigid body: mass, inertia, four rotors with thrust and drag torque, motor lag, body drag, ground effect near the dock and the ground
- [ ] Action: collective thrust plus body rates, all in [-1, 1]. Low-level rate control sits inside the sim, like a flight controller would
- [ ] Payload: one parcel with its own mass, released at the drop point, which changes the drone's mass and centre of gravity mid-flight
- [ ] Battery: energy use from thrust, so a heavy parcel, a climb or a headwind cost more. Voltage sag near empty
- [ ] Collision: drone against buildings, trees, wires, ground, the truck and other drones
- [ ] Reference autopilot: hand-written cascaded PID (position, velocity, attitude) that reads the true state. It's the yardstick, like the lane follower was for the car
- [ ] Tests: hover holds height, the drone falls when thrust is cut, a step in body rate gives the expected attitude, battery drains faster when loaded

**Exit:** at least 3,000 drone-steps/s at 50 Hz for one drone in one process, and the reference autopilot holds a hover within 0.2 m in light wind.

## Phase 3: Sensors

The drone gets every sensor a real delivery drone could reasonably carry. There's no sensor switching this time; the question is whether it can fly well with all of them, including their noise and failures.

- [ ] Fixed observation layout, normalised to [0, 1]
- [ ] Noise, bias, latency and dropout for each sensor, with settings per episode
- [ ] Debug geometry for each sensor so renders can show what it sees
- [ ] Tests: every sensor stays in range under any settings, observation shape never changes, GPS gets worse next to tall buildings, the beacon range matches true distance on average

The sensors are listed in the README.

**Exit:** the reference autopilot, switched to reading only the sensors instead of the true state, still flies a mission it completes with the true state.

## Phase 4: Single-drone mission

- [ ] Gymnasium env for one drone: launch from the moving truck, fly to an assigned drop point, release the parcel, fly back and land on the moving truck
- [ ] Metrics: `delivered`, `docked`, `crash`, `battery_out`, `lost` (out of range of the truck), mission time, energy used
- [ ] The reference autopilot completes missions, with a fixed set of held-out neighbourhoods for benchmarking

**Exit:** the reference autopilot delivers and docks on at least 95% of held-out missions in light wind.

## Phase 5: Shared drone policy

- [ ] PPO with the settings that worked on the car: 12 parallel envs, VecNormalize rewards, target KL 0.02, tanh MLP, lower starting action noise
- [ ] Curriculum: hover, then waypoints, then a drop on an open yard, then a static truck landing, then a moving truck, then balconies and blocked yards, then wind
- [ ] Export to numpy with `train/export.py`, so evaluation and rendering don't need torch
- [ ] Benchmark on held-out neighbourhoods, three seeds per setup. Single runs vary a lot, so no result counts from one run

**Exit:** the trained policy delivers and docks on at least 85% of held-out single-drone missions, averaged over three seeds.

## Phase 6: Fleet controller

- [ ] Fleet env: one truck, 10 drones, 10 parcels per round, all drones running the shared policy
- [ ] Fleet comms in the drone observation: positions and planned paths of nearby drones, with latency and dropout
- [ ] Hand-written fleet controller first: assign parcels to drones by distance along the route, stagger launches, give each drone an altitude band, plan each rendezvous from the truck's route and the drone's battery, queue landings on the dock
- [ ] Replanning when the truck is held up in traffic or a drone is late
- [ ] Metrics: parcels per hour, all delivered, all docked, closest approach between drones, dock wait time, energy per parcel
- [ ] Then try a learned fleet controller and keep it only if it beats the hand-written one on the benchmark

**Exit:** a full round of 10 parcels with no drone-to-drone collisions on at least 90% of held-out rounds.

## Phase 7: Hardening

- [ ] Stress tests: strong gusts, GPS loss in apartment canyons, comms dropout, a beacon failure, a drone that loses a motor and has to land safely
- [ ] Battery reserve rules: a drone that can't make the rendezvous diverts to a safe landing spot and the fleet controller sends the truck back
- [ ] Held-out benchmark across all of the above, published in `results/`

**Exit:** no stress test makes the fleet worse than "drone lands safely and is recovered later".

## Phase 8: Write-up

- [ ] Renders and GIFs with matplotlib for the README: a full fleet round from above and a chase view of one delivery
- [ ] Docs: world, dynamics, sensors, training, fleet controller, results
- [ ] Honest results tables, including what still fails

**Exit:** someone new can install, run the tests, train a policy and reproduce the published numbers from the docs alone.
