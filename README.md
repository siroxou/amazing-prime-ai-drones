# Amazing Prime AI Drones

Self-flying delivery drones that launch from a moving delivery truck, ten at a time.

A truck drives its route with a fleet of 10 drones on its roof. Each drone takes one parcel, flies it to a house or an apartment balcony, drops it, and then flies back to land on the truck, which has kept driving in the meantime. The project builds the simulator for this in Python + numpy and trains the drones with PPO.

This started as a fork of [self-driving-optimized](https://github.com/siroxou/self-driving-optimized), a self-driving car sensor study. The road generator, vehicle model and traffic from that project now drive the truck; everything car-specific was taken out.

**Status:** Phase 0 is done. What's here today is the truck side of the sim (roads, truck, traffic). The 3D world, drone dynamics, sensors and training come in the phases in [ROADMAP.md](ROADMAP.md).

## How it works

Two layers of control:

| Layer | Where it runs | What it decides |
|---|---|---|
| **Fleet controller** | on the truck, one per fleet | which drone takes which parcel, launch order, altitude bands and corridors, where and when each drone meets the truck again, the landing queue on the dock |
| **Drone policy** | on every drone, same network for all 10 | flying: getting to the drop point, avoiding trees, wires, fences and other drones, dealing with wind, releasing the parcel, landing on the moving truck |

The fleet controller starts out hand-written. The drone policy is learned with PPO.

### A delivery

1. The truck drives its route. The fleet controller picks the next parcels and the drones to carry them.
2. A drone lifts off the roof dock while the truck is moving, climbs to its assigned altitude band and heads for the drop point.
3. At the house it comes down into the yard, or up to a balcony, works around whatever is in the way, and releases the parcel.
4. It flies to the rendezvous point the fleet controller gave it, finds the truck and lands on its dock slot while the truck drives.
5. If it's running low on battery or loses the truck, it lands somewhere safe instead and the truck picks it up later.

## Sim

Full 3D. No browser viewer this time: the sim only has to run fast for training, and the README gets matplotlib renders.

- **World:** the procedural roads from the car project, with houses, yards, trees, fences, power lines and apartment blocks with balconies built around them. Wind with gusts.
- **Truck:** kinematic bicycle model driving in IDM traffic, with a roof dock for 10 drones.
- **Drones:** quadrotor rigid-body model with motor lag, drag, ground effect, a parcel that changes the mass when it's released, and a battery that drains with thrust.

## Sensors

Each drone carries everything a real delivery drone could reasonably use. All of them are on all the time; they're modelled with noise, bias, latency and dropout rather than switched off.

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
```

## Layout

```
sim/world.py         procedural roads and a 2D raycaster (3D world comes in Phase 1)
sim/vehicle.py       kinematic bicycle model and collision shape, used by the truck and traffic
sim/traffic.py       IDM traffic and parked cars around the truck
sim/policy.py        runs an exported policy with plain numpy
train/export.py      exports a trained PPO model to .npz for sim/policy.py
tests/               tests
ROADMAP.md           phases and exit criteria
```

## License

MIT
