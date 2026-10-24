"""A planned day as plain data for the 3D renderer: the city's geometry, each truck's drives, every drone
flight that delivered, every locker recipient who walked over, and the weather.

Everything comes from baselines.classical.solve; nothing here plans anything. The checks at the end make
sure every delivered parcel shows up exactly once, as a drone flight or as someone collecting it.
"""
import numpy as np

from baselines import classical, dsp, prime_air, trucks_only
from sim import drone
from sim.roads import Paths


def r1(a):
    return np.round(np.asarray(a, float), 1).tolist()


def city(c):
    obs, ter = c.obstacles, c.terrain
    x0, y0, x1, y1 = -1400.0, -1100.0, c.width + 1100, c.height + 1100  # well past the city, for the horizon
    step = 6.0
    xs, ys = np.arange(x0, x1, step), np.arange(y0, y1, step)
    X, Y = np.meshgrid(xs, ys)
    corners = obs.box_corners(np.arange(obs.nb))  # (n, 4, 2)
    side = corners[:, 1] - corners[:, 0]
    size = np.column_stack([np.linalg.norm(side, axis=1), np.linalg.norm(corners[:, 2] - corners[:, 1], axis=1)])
    zones = [{"kind": z["kind"], "shape": z["shape"], "centre": r1(z["centre"]), "radius": float(z.get("radius", 0)),
              "half": r1(z.get("half", (0, 0))), "yaw": float(z.get("yaw", 0)), "floor": float(z["floor"]),
              "ceiling": float(min(z["ceiling"], drone.MAX_HEIGHT)), "active": bool(z.get("active", True)),
              "ground": float(ter.height(*z["centre"]))} for z in c.airspace.zones]
    wires = obs.kind[obs.nb + obs.nc:]
    return {
        "grid": {"x0": x0, "y0": y0, "step": step, "nx": len(xs), "ny": len(ys), "h": r1(ter.height(X, Y).ravel())},
        "streets": [{"kind": s["kind"], "width": float(s["width"]), "bulb": float(s["bulb"]), "points": r1(s["points"])}
                    for s in c.streets],
        "runway": [r1(c.runway[0]), r1(c.runway[1])],
        "boxes": {"kind": obs.kind[:obs.nb].tolist(), "x": r1(corners.mean(1)[:, 0]), "y": r1(corners.mean(1)[:, 1]),
                  "yaw": np.round(np.arctan2(side[:, 1], side[:, 0]), 3).tolist(), "sx": r1(size[:, 0]),
                  "sy": r1(size[:, 1]), "z0": r1(obs.box_z[:, 0]), "z1": r1(obs.box_z[:, 1])},
        "cyl": {"kind": obs.kind[obs.nb:obs.nb + obs.nc].tolist(), "x": r1(obs.cyl_xy[:, 0]), "y": r1(obs.cyl_xy[:, 1]),
                "r": r1(obs.cyl_r), "z0": r1(obs.cyl_z[:, 0]), "z1": r1(obs.cyl_z[:, 1])},
        "wires": {"kind": wires.tolist(), "p": r1(obs.wire_p), "q": r1(obs.wire_q)},
        "zones": zones,
        "station": r1(c.station_centre),
    }


def truck_legs(c, plan, route, start, truck, second):
    """Each drive of one route: the road polyline, when it starts and ends, and how long the truck stays."""
    nodes = plan["shift"].nodes
    paths = Paths(c, c.edge_length, nodes)
    legs, at, clock = [], 0, start
    for j in route:
        arrive = plan["at"][j - 1]
        if not np.isfinite(arrive):
            continue
        legs.append({"truck": truck, "second": second, "t0": clock, "t1": float(arrive), "stop": int(j),
                     "xy": r1(c.nodes[paths.between(nodes[at], nodes[j])]),
                     "leave": float(arrive) + plan["service"][j] / 3600})
        clock, at = legs[-1]["leave"], j
    back = plan["back"][plan["routes"].index(route)]
    legs.append({"truck": truck, "second": second, "t0": clock, "t1": float(back), "stop": 0, "leave": None,
                 "xy": r1(c.nodes[paths.between(nodes[at], nodes[0])])})
    return legs


def flights(day, plan, delivered, truck_of, second):
    """Drone flights that delivered: the path out (x, y, z) to above the drop spot, the times of launch, drop and
    landing, and how the parcel was put down."""
    c, ground = day.city, day.city.terrain.height
    out = []
    for k, i in enumerate(np.flatnonzero(plan["fly"])):
        stop = plan["drone_stop"][k]
        launch = plan["at"][stop] + plan["start"][k] / 3600
        if not np.isfinite(launch) or stop not in truck_of:
            continue
        a = c.nodes[plan["nodes"][stop]]
        trip = drone.sortie(day, a, i, launch)
        if trip is None or not np.isclose(delivered[i], launch + trip["to_drop"] / 3600, atol=1e-6):
            continue
        b = c.spot_pos[trip["spot"]]
        shape = drone.profile(c, a, b[:2], launch)
        if shape is None:
            continue
        pts, z = shape
        over = b + [0, 0, drone.LOWER_FROM if trip["mode"] == "lower" else max(trip["height"], 1.0)]
        out.append({"truck": truck_of[stop], "second": second, "parcel": int(i), "t0": float(launch),
                    "t1": float(delivered[i]), "t2": float(launch + trip["seconds"] / 3600),
                    "path": r1(np.vstack([[*a, ground(*a) + drone.ROOF], np.column_stack([pts, z]), over])),
                    "mode": trip["mode"], "spot": r1(b), "spot_kind": str(c.spot_kind[trip["spot"]]),
                    "over": round(drone.SECONDS[trip["mode"]] / 3600, 5)})
    return out


def walkers(day, plan, delivered, truck_of):
    """Locker recipients who collected: from their door to the parked truck, arriving when they collect."""
    c = day.city
    out = []
    for k, i in enumerate(np.flatnonzero(plan["locker"])):
        stop, got = plan["point"][k], plan["collected"][k]
        if stop < 0 or not np.isfinite(got) or not np.isclose(delivered[i], got):
            continue
        walk = plan["walk"][k] / trucks_only.WALK_SPEED / 3600
        out.append({"from": r1(c.address_door[day.parcel_address[i]][:2]), "to": r1(c.nodes[plan["nodes"][stop]]),
                    "t0": float(got - walk), "t1": float(got), "parcel": int(i), "truck": truck_of.get(stop, 0)})
    return out


def grounded(day, start, end):
    """Hour-long spans in the shift when it's too gusty or wet to fly, merged."""
    spans = []
    for h in np.arange(np.floor(start), np.ceil(end)):
        if prime_air.flyable(day, h + 0.5):
            continue
        if spans and spans[-1][1] == h:
            spans[-1][1] = float(h + 1)
        else:
            spans.append([float(h), float(h + 1)])
    return spans


def export(day, seconds=dsp.SOLVER_SECONDS):
    """The day planned by the classical solver, with its afternoon second pass, as a dict for render3d/page.html."""
    from optimiser.routes import score

    c = day.city
    r = classical.solve(day, seconds=seconds)
    t = r["parcel_time"]
    start, end = dsp.SHIFT_START + dsp.LOADOUT, dsp.SHIFT_START + dsp.SHIFT
    passes = [(r["plan"], list(range(r["trucks"])), start, False)]
    passes += [(p, [p["truck"]] * p["trucks"], r["plan"]["back"][p["truck"]] + classical.RELOAD, True)
               for p in r["second_plans"]]
    legs, flown, walks = [], [], []
    for plan, trucks, leave, second in passes:
        truck_of = {}
        for route, k in zip(plan["routes"], trucks):
            legs += truck_legs(c, plan, route, leave, k, second)
            truck_of.update({j - 1: k for j in route})
        flown += flights(day, plan, t, truck_of, second)
        walks += walkers(day, plan, t, truck_of)
    by_drone = np.zeros(len(t), bool)
    by_drone[[f["parcel"] for f in flown]] = True
    done = ~np.isnan(t)
    assert len(flown) == by_drone.sum(), "a parcel was flown twice"
    assert len(walks) + len(flown) == done.sum(), "some deliveries are neither a flight nor a pickup"
    w = day.weather
    door = c.address_door[day.parcel_address]
    return {
        "seed": int(c.seed), "day": int(c.day), "city": city(c), "legs": legs, "flights": flown, "walkers": walks,
        "parcels": {"x": r1(door[:, 0]), "y": r1(door[:, 1]), "z": r1(c.terrain.height(door[:, 0], door[:, 1])),
                    "t": [None if np.isnan(v) else round(float(v), 4) for v in t], "drone": by_drone.astype(int).tolist()},
        "weather": {"hour": r1(w["hour"]), "wind": r1(w["wind"]), "gust": r1(w["gust"]),
                    "dir": np.round(w["wind_dir"], 3).tolist(), "rain": r1(w["rain_mm_h"]),
                    "gust_limit": prime_air.GUST_LIMIT, "rain_limit": prime_air.RAIN_LIMIT,
                    "grounded": grounded(day, start, end)},
        "trucks": int(r["trucks"]), "start": start, "end": end,
        "stats": {"score": score(t), "delivered": float(done.mean()), "by_drone": float(by_drone.mean()),
                  "second_pass": int(r["second_pass"]), "last": float(np.nanmax(t)) if done.any() else None},
    }
