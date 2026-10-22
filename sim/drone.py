"""Delivery drone cost model: how long a flight takes, how much battery it uses, and how each
parcel is put down.

Power comes from momentum theory for a multirotor, the usual first model for delivery drone
energy: the rotors' induced power to hold the drone and its parcel up, which falls as the
drone picks up speed, plus the power to push the drone and the parcel's box through the air,
plus climbing, plus a fixed draw for the electronics. The drone flies at a fixed AIRSPEED, so
the day's wind changes its speed over the ground, and headwinds cost time and battery. The
battery holds less in the cold, and a RESERVE is never used.

Each leg follows a height profile along its line: at least MIN_HEIGHT above the ground and
CLEARANCE above the tallest thing near the path (roofs, trees, wires, cranes, pylons, cell
towers), climbing or descending no steeper than GRADE, never above MAX_HEIGHT. It flies over
no-fly zones that end low enough (schools, while they're on) and under ones that start high
enough (the airfield's 30 m limit); it goes round the rest. ponytail: the heights come from
the straight line even where the route bends round a zone.

At the address the drone either drops the parcel from a few metres, lowers it on a line, or
sets it down, depending on how fragile it is, how gusty it is, and how much room there is
around the spot. A spot without enough room for any of them isn't used.

Every number here is a guess at a plausible delivery quadcopter of about 9 kg carrying up to
5 kg, until the 3D flight sim (ROADMAP Phase 5) calibrates them.
"""
import numpy as np

G, RHO = 9.81, 1.225
MASS = 9.0  # kg, drone and battery
DISC = 1.8  # m² of rotor disc: four 30-inch rotors
EFFICIENCY = 0.7  # rotor figure of merit times motor and controller efficiency
BODY_DRAG = 0.15  # m², drag coefficient times frontal area of the drone
BOX_DRAG = 1.05  # drag coefficient of a parcel box
AVIONICS = 50.0  # W
AIRSPEED = 15.0  # m/s
CLIMB, DESCEND = 3.0, 2.0  # m/s straight up and down
BATTERY = 600.0  # Wh usable at 20 °C
RESERVE = 0.2  # share of the battery never used
COLD = 0.01  # share of capacity lost per °C below 20 °C
MIN_HEIGHT, LOW_HEIGHT, CLEARANCE, MAX_HEIGHT = 30.0, 15.0, 10.0, 120.0  # m above the ground
ROOF = 3.0  # m: the truck roof, where drones take off and land
GRADE = CLIMB / AIRSPEED  # steepest climb or descent while cruising
STEP, SKY_CELL = 5.0, 10.0  # m between height samples, and the size of the obstacle-height map's squares

# Putting the parcel down
POSITION = 0.3  # m the drone can be off where it means to be
DROP_FROM = {"robust": 3.0, "careful": 1.0}  # m it lets go from; fragile parcels are never dropped
DRIFT = 0.3  # how much of the gust a falling parcel picks up
LOWER_FROM, SWING = 8.0, 0.008  # m it hovers at to lower on a line, and line swing per m of line per m/s of gust
DRONE_RADIUS, ROTOR_RADIUS = 0.7, 0.9  # m: room it needs around itself hovering, and setting down
SET_FROM = 5.0  # m it slows down from to set a parcel down
SECONDS = {"drop": 7.0, "lower": 5 + LOWER_FROM / 0.5 + 3 + LOWER_FROM / 1.0, "set": SET_FROM / 1.0 + 5 + SET_FROM / CLIMB}


def power(payload=0.0, frontal=0.0, airspeed=0.0, climb=0.0):
    """Electrical power (W) to fly level at `airspeed` (m/s), or climb at `climb`, carrying `payload` kg
    in a box with `frontal` m² facing forward."""
    weight = (MASS + payload) * G
    drag = 0.5 * RHO * (BODY_DRAG + BOX_DRAG * frontal) * airspeed ** 2
    thrust = np.hypot(weight, drag)
    hover = thrust / (2 * RHO * DISC)  # induced velocity squared in a hover
    induced = np.sqrt(-airspeed ** 2 / 2 + np.sqrt(airspeed ** 4 / 4 + hover ** 2))
    return float((thrust * (induced + max(climb, 0.0)) + drag * airspeed) / EFFICIENCY + AVIONICS)


def usable_wh(temp_c):
    return BATTERY * (1 - COLD * max(0.0, 20.0 - temp_c)) * (1 - RESERVE)


def frontal_area(dims):
    """Box carried long side forward: the two shorter sides face the air."""
    a, b, _ = np.sort(dims)
    return float(a * b)


def ground_speed(wind_xy, heading):
    """Speed over the ground along `heading` (unit vector) at AIRSPEED in this wind, or None if the
    wind across the track is too strong to hold it."""
    along = float(wind_xy @ heading)
    across = abs(wind_xy[0] * heading[1] - wind_xy[1] * heading[0])
    if across >= AIRSPEED:
        return None
    v = along + np.sqrt(AIRSPEED ** 2 - across ** 2)
    return v if v > 1.0 else None


def skyline(city):
    """Height of the tallest obstacle top in each SKY_CELL square (absolute, -inf where there's none).
    Built once per city."""
    if getattr(city, "_skyline", None) is not None:
        return city._skyline
    obs = city.obstacles
    origin = obs.bounds_lo.min(0) - SKY_CELL
    shape = (np.ceil((obs.bounds_hi.max(0) - origin) / SKY_CELL).astype(int) + 2)[::-1]
    grid = np.full(shape, -np.inf)
    solid = obs.nb + obs.nc
    lo = np.floor((obs.bounds_lo[:solid] - origin) / SKY_CELL).astype(int)
    hi = np.floor((obs.bounds_hi[:solid] - origin) / SKY_CELL).astype(int)
    tops = np.r_[obs.box_z[:, 1], obs.cyl_z[:, 1]]
    for (i0, j0), (i1, j1), top in zip(lo, hi, tops):
        cell = grid[j0:j1 + 1, i0:i1 + 1]
        np.maximum(cell, top, out=cell)
    for p, q in zip(obs.wire_p, obs.wire_q):  # wires go in along their length, not their bounding box
        n = int(np.linalg.norm(q[:2] - p[:2]) / (SKY_CELL / 2)) + 2
        pts = p + np.linspace(0, 1, n)[:, None] * (q - p)
        i, j = np.floor((pts[:, :2] - origin) / SKY_CELL).astype(int).T
        np.maximum.at(grid, (j, i), pts[:, 2])
    city._skyline = (origin, grid)
    return city._skyline


def tallest(city, xy):
    origin, grid = skyline(city)
    i, j = np.floor((np.asarray(xy) - origin) / SKY_CELL).astype(int).T
    ok = (i >= 0) & (j >= 0) & (i < grid.shape[1]) & (j < grid.shape[0])
    out = np.full(len(i), -np.inf)
    out[ok] = grid[j[ok], i[ok]]
    return out


def profile(city, a, b, hour):
    """Cruise heights (absolute) at points every STEP along the line a -> b, or None if no height works."""
    n = max(int(np.linalg.norm(b - a) / STEP), 1) + 1
    pts = a + np.linspace(0, 1, n)[:, None] * (b - a)
    ground = city.terrain.height(pts[:, 0], pts[:, 1])
    obstacle = tallest(city, pts) + CLEARANCE
    need = np.maximum(ground + MIN_HEIGHT, obstacle)
    limit = ground + MAX_HEIGHT
    sky = city.airspace
    if len(sky):
        inside = sky.inside(pts) & sky.on(hour)
        over = inside & (sky.floor < LOW_HEIGHT) & (sky.ceiling < MAX_HEIGHT - CLEARANCE)  # fly over it
        under = inside & (sky.floor >= LOW_HEIGHT)  # stay under it
        need = np.maximum(need, ground + np.where(over, sky.ceiling + 1, -np.inf).max(1, initial=-np.inf))
        low = under.any(1)
        need[low] = np.maximum(ground[low] + LOW_HEIGHT, obstacle[low])
        limit = np.minimum(limit, ground + np.where(under, sky.floor - 1, np.inf).min(1, initial=np.inf))
    z = need.copy()
    for i in range(1, n):  # no steeper than GRADE either way: raise the lower side
        z[i] = max(z[i], z[i - 1] - GRADE * STEP)
    for i in range(n - 2, -1, -1):
        z[i] = max(z[i], z[i + 1] - GRADE * STEP)
    if (z > limit + 1e-6).any():
        return None
    return pts, z


def leg(day, a, b, hour, start_z, end_z, payload=0.0, frontal=0.0):
    """Take off at height start_z over a, fly to b and come down to end_z (absolute heights).
    Returns {"seconds", "wh", "cruise" (seconds cruising), "distance" (m)} or None if it can't be flown."""
    city = day.city
    a, b = np.asarray(a, float), np.asarray(b, float)
    shape = profile(city, a, b, hour)
    distance = city.airspace.route_length(a, b, hour, LOW_HEIGHT, MAX_HEIGHT) if len(city.airspace) else \
        float(np.linalg.norm(b - a))
    if shape is None or distance is None:
        return None
    _, z = shape
    cruise_s, climbed = 0.0, float(np.maximum(np.diff(z), 0).sum())
    if distance > 1e-6:
        mid = np.append((a + b) / 2, z.mean())
        speed = ground_speed(day.wind_at([mid], hour)[0, :2], (b - a) / np.linalg.norm(b - a))
        if speed is None:
            return None
        cruise_s = distance / speed
    up, down = max(z[0] - start_z, 0.0) / CLIMB, max(z[-1] - end_z, 0.0) / DESCEND
    joules = (power(payload, frontal, AIRSPEED) * cruise_s + power(payload, frontal, 0, CLIMB) * up
              + power(payload, frontal) * down + (MASS + payload) * G * climbed / EFFICIENCY)
    return {"seconds": up + cruise_s + down, "wh": joules / 3600, "cruise": cruise_s, "distance": distance}


def _room(city):
    """For every drop spot: room around it 1 m up, and room for the drone hovering LOWER_FROM above it.
    Built once per city."""
    if getattr(city, "_drop_room", None) is None:
        obs = city.obstacles
        low = np.array([obs.room(p + [0, 0, 1.0], 5.0) for p in city.spot_pos])
        high = np.array([obs.room(p + [0, 0, LOWER_FROM], 5.0) for p in city.spot_pos])
        city._drop_room = (low, high)
    return city._drop_room


def drop_options(day, parcel, hour):
    """Ways to put this parcel down at its address at this hour, quickest first:
    (seconds over the spot, spot index, mode, height it's released or lowered from, above the spot)."""
    city = day.city
    gust = day.weather_at(hour)["gust"]
    fragility = str(day.parcel_fragility[parcel])
    low, high = _room(city)
    centres, radii = city.airspace.walls(hour, LOW_HEIGHT, MAX_HEIGHT) if len(city.airspace) else ([], [])
    out = []
    for s in np.flatnonzero(city.spot_address == day.parcel_address[parcel]):
        if city.spot_overhead[s] < 100:  # something overhead: nothing can come straight down onto it
            continue
        if any(np.linalg.norm(city.spot_pos[s, :2] - c) < r for c, r in zip(centres, radii)):
            continue  # inside a no-fly zone it can't go over or under
        lower_ok = high[s] >= DRONE_RADIUS and low[s] >= POSITION + SWING * LOWER_FROM * gust
        if city.spot_kind[s] == "balcony":
            if lower_ok:
                out.append((SECONDS["lower"], s, "lower", LOWER_FROM))
            continue
        if fragility in DROP_FROM:
            h = DROP_FROM[fragility]
            if low[s] >= POSITION + DRIFT * gust * np.sqrt(2 * h / G):
                out.append((SECONDS["drop"], s, "drop", h))
        if lower_ok:
            out.append((SECONDS["lower"], s, "lower", LOWER_FROM))
        if low[s] >= ROTOR_RADIUS + POSITION + 0.05 * gust:
            out.append((SECONDS["set"], s, "set", SET_FROM))
    return sorted(out)


def sortie(day, start, parcel, hour, back=None, options=None):
    """Fly a parcel from `start` (x, y, taking off from a truck roof there), put it down, and fly back to
    `back` (default `start`), landing on the truck roof. Uses the quickest drop option that the battery
    allows. Returns a dict, or None if nothing works:
        to_drop, seconds: seconds to the moment it's put down, and in the air altogether
        wh: battery used; watts: average draw
        spot, mode, height: the drop option used
        speed_out, speed_back: ground speeds cruising out and back (m/s)
        fixed_out, fixed_back: seconds not spent cruising, before and after the drop"""
    city = day.city
    start = np.asarray(start, float)
    back = start if back is None else np.asarray(back, float)
    payload, frontal = float(day.parcel_weight[parcel]), frontal_area(day.parcel_dims[parcel])
    battery = usable_wh(day.weather_at(hour)["temp_c"])
    for seconds, s, mode, height in (drop_options(day, parcel, hour) if options is None else options):
        spot = city.spot_pos[s]
        out = leg(day, start, spot[:2], hour, city.terrain.height(*start) + ROOF, spot[2] + height, payload, frontal)
        if out is None:
            continue
        home = leg(day, spot[:2], back, hour + out["seconds"] / 3600, spot[2] + height,
                   city.terrain.height(*back) + ROOF)
        if home is None:
            continue
        wh = out["wh"] + home["wh"] + power(payload, frontal) * seconds / 3600
        if wh > battery:
            continue
        total = out["seconds"] + seconds + home["seconds"]

        def speed(part):
            return part["distance"] / part["cruise"] if part["cruise"] > 0 else AIRSPEED

        return {"to_drop": out["seconds"] + seconds / 2, "seconds": total, "wh": wh, "watts": wh * 3600 / total,
                "spot": s, "mode": mode, "height": height, "speed_out": speed(out), "speed_back": speed(home),
                "fixed_out": out["seconds"] - out["cruise"] + seconds / 2,
                "fixed_back": home["seconds"] - home["cruise"] + seconds / 2}
    return None
