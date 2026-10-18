"""City layout: streets, ZIP codes, delivery zones, the distribution centre, hills, and the
3D houses, apartment blocks, trees, power lines and other hazards the drones fly around.

Straight arterial roads every ZIP_BLOCKS grid lines bound the ZIP codes, and each ZIP
splits into four delivery zones (its quarters). The middle ZIP keeps a street grid, with
apartment blocks in its centre and a hospital. The ZIPs around it get curving collector
streets with cul-de-sacs off them, and houses face whatever street they're on.

Hazards: poles with power and cable lines along every street outside the centre, a
high-voltage line on pylons across one corner, guyed cell towers, construction cranes that
change from day to day, and no-fly airspace over schools, around the hospital's helipad,
around the stadium on event days, and around a small airfield east of the city. The
distribution centre, where the trucks start, sits west of the city.

The ground is hilly and everything sits on it. Units are metres, z is up, hours are 0-24.
`seed` fixes the city; `day` changes only what changes day to day (cranes, stadium events).

    python -m sim.city       # build a city, print what's in it and time the queries
"""
from time import perf_counter

import numpy as np

from .airspace import UNLIMITED, Airspace
from .geometry import Obstacles, Terrain, sphere

ZIP_BLOCKS, ZONE_BLOCKS = 4, 2  # grid lines per ZIP code and per zone; arterials run every ZIP_BLOCKS lines
LOCAL_WIDTH, COLLECTOR_WIDTH, ARTERIAL_WIDTH, ACCESS_WIDTH = 10.0, 12.0, 18.0, 14.0  # kerb to kerb
SIDEWALK = 2.5
LOCAL_SPEED, ARTERIAL_SPEED = 30 / 3.6, 50 / 3.6  # speed limits, m/s
STOREY = 3.0
BULB = 11.0  # cul-de-sac turning circle radius
DISTRICTS = ("centre", "dense", "suburb")
SPOT_KINDS = ("porch", "front_yard", "back_yard", "balcony")
LOT_WIDTH = {"dense": (12.0, 16.0), "suburb": (20.0, 28.0)}
LOT_DEPTH = {"dense": (26.0, 32.0), "suburb": (32.0, 42.0)}
POLE_SPACING, POLE_HEIGHT = 40.0, 10.0
POWER_Z, CABLE_Z = 9.5, 6.0  # the power line, and the lower phone/cable line on the same poles
STATION_ROAD, BAYS = 80.0, 10  # access road length, truck bays at the distribution centre
TERRAIN_CELL = 5.0
STREET_ORDER = {"culdesac": 0, "collector": 1, "local": 2, "arterial": 3, "access": 4}  # who gets lots first


class City:
    def __init__(self, seed=0, blocks=12, day=0):
        if blocks % ZIP_BLOCKS:
            raise ValueError(f"blocks must be a multiple of {ZIP_BLOCKS}")
        rng, today = np.random.default_rng(seed), np.random.default_rng([seed, day])
        self.seed, self.blocks, self.day = seed, blocks, day
        self.arterial = np.arange(blocks + 1) % ZIP_BLOCKS == 0  # per grid line; same pattern along x and y
        self.line_width = np.where(self.arterial, ARTERIAL_WIDTH, LOCAL_WIDTH)
        self.xs = np.concatenate([[0.0], np.cumsum(rng.uniform(100, 140, blocks))])  # north-south grid lines
        self.ys = np.concatenate([[0.0], np.cumsum(rng.uniform(85, 115, blocks))])  # east-west grid lines
        self.width, self.height = self.xs[-1], self.ys[-1]
        self.station_row = ZIP_BLOCKS * int(round(blocks / 2 / ZIP_BLOCKS))  # the arterial nearest the middle
        self.station_centre = np.array([-270.0, self.ys[self.station_row]])
        self.runway_centre = np.array([self.width + 700.0, self.height / 2])
        self.terrain = self._terrain(rng)
        self.ground = self.terrain.height

        self._boxes, self._cyls, self._wires, self._addr, self._spots, self._zones = [], [], [], [], [], []
        self.streets, self.sites = [], []
        self._space = _Raster(-360.0, -40.0, self.width + 40, self.height + 40)  # anything built or reserved
        self.road_mask = _Raster(-360.0, -40.0, self.width + 40, self.height + 40)  # road surfaces only
        self._space.mark_outside(0.0, 0.0, self.width, self.height)  # the city ends at the outer arterials

        self._zip_setup()
        self._main_roads()
        self._station()
        self._corridor(rng)
        self._collectors(rng)
        self._grid_blocks(rng)
        self._sites(rng)
        self._culdesacs(rng)
        for s in sorted(self.streets, key=lambda s: STREET_ORDER[s["kind"]]):
            if s["kind"] != "access":
                self._lots(rng, s)
        self._power_lines()
        self._pylons()
        self._airport()
        self._today(today)
        self._graph()
        self.obstacles = Obstacles(self._boxes, self._cyls, self._wires, terrain=self.terrain)
        self.airspace = Airspace(self._zones, self.terrain)
        self._finish()

    # Ground

    def _terrain(self, rng):
        """Rolling hills: a few broad bumps and dips plus a gentle tilt, flattened at the
        distribution centre and the airfield. Slopes reach about 15%."""
        gx = np.arange(-500.0, self.width + 1300 + TERRAIN_CELL, TERRAIN_CELL)
        gy = np.arange(-700.0, self.height + 700 + TERRAIN_CELL, TERRAIN_CELL)
        X, Y = np.meshgrid(gx, gy)
        h = rng.uniform(-0.015, 0.015) * X + rng.uniform(-0.015, 0.015) * Y
        for _ in range(int(rng.integers(4, 7))):
            cx, cy = rng.uniform(-100, self.width + 100), rng.uniform(-100, self.height + 100)
            h += rng.uniform(-20, 35) * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * rng.uniform(150, 320) ** 2))
        for (cx, cy), inner, outer in ((self.station_centre, 160, 320), (self.runway_centre, 550, 800)):
            r = np.hypot(X - cx, Y - cy)
            w = np.clip((r - inner) / (outer - inner), 0, 1)
            w = w * w * (3 - 2 * w)
            level = h[np.unravel_index(np.argmin(r), r.shape)]
            h = level + w * (h - level)
        h -= h[np.unravel_index(np.argmin(np.hypot(X - self.station_centre[0], Y - self.station_centre[1])), X.shape)]
        return Terrain(gx[0], gy[0], TERRAIN_CELL, h)

    # ZIP codes, zones and the roads between them

    def _zip_setup(self):
        k, nz = ZIP_BLOCKS, self.blocks // ZIP_BLOCKS
        pi, pj = (a.ravel() for a in np.meshgrid(np.arange(nz), np.arange(nz)))  # ZIP z = pj * nz + pi
        self.zip_bounds = np.stack([self.xs[pi * k], self.ys[pj * k], self.xs[(pi + 1) * k], self.ys[(pj + 1) * k]], 1)
        self.zip_codes = [f"{101 + i:05d}" for i in range(nz * nz)]  # made up: real ZIP codes start at 00501
        mid = (self.zip_bounds[:, :2] + self.zip_bounds[:, 2:]) / 2
        self.zip_grid = self._centre_dist(mid[:, 0], mid[:, 1]) < 0.3  # ZIPs that keep a street grid
        k, nz = ZONE_BLOCKS, self.blocks // ZONE_BLOCKS
        zi, zj = (a.ravel() for a in np.meshgrid(np.arange(nz), np.arange(nz)))
        self.zone_bounds = np.stack([self.xs[zi * k], self.ys[zj * k], self.xs[(zi + 1) * k], self.ys[(zj + 1) * k]], 1)
        self.zone_zip = self._zip_at((self.zone_bounds[:, :2] + self.zone_bounds[:, 2:]) / 2)

    def _main_roads(self):
        """Arterials along every ZIP_BLOCKS-th grid line, and a plain grid inside the middle ZIP."""
        xs, ys = self.xs, self.ys
        for k in np.flatnonzero(self.arterial):
            self._street([[xs[0], ys[k]], [xs[-1], ys[k]]], ARTERIAL_WIDTH, "arterial")
            self._street([[xs[k], ys[0]], [xs[k], ys[-1]]], ARTERIAL_WIDTH, "arterial")
        k, nz = ZIP_BLOCKS, self.blocks // ZIP_BLOCKS
        for z in np.flatnonzero(self.zip_grid):
            zi, zj = z % nz, z // nz
            for i in range(zi * k + 1, (zi + 1) * k):
                self._street([[xs[i], ys[zj * k]], [xs[i], ys[(zj + 1) * k]]], LOCAL_WIDTH, "local")
            for j in range(zj * k + 1, (zj + 1) * k):
                self._street([[xs[zi * k], ys[j]], [xs[(zi + 1) * k], ys[j]]], LOCAL_WIDTH, "local")

    def _station(self):
        """Distribution centre west of the city: a warehouse, a yard with truck bays in front of it,
        and an access road onto the middle arterial. Trucks start backed onto the warehouse wall,
        facing the gate (heading 0, along +x)."""
        cx, cy = self.station_centre
        self._space.mark_rect(np.array([-200.0, cy]), (1.0, 0.0), 145.0, 110.0)
        self._street([[-STATION_ROAD, cy], [self.xs[0], cy]], ACCESS_WIDTH, "access")
        self.station_building, _ = self._building((cx, cy), (1.0, 0.0), 50.0, 90.0, 14.0, "station")
        self.bays = np.array([[-214.0, cy - 54.0 + 12.0 * k, 0.0] for k in range(BAYS)])  # x, y, heading

    def _corridor(self, rng):
        """A high-voltage line across one of the city's eastern corners, with a 40 m strip
        kept clear of buildings under it. The pylons go up once the streets are in."""
        a, b = rng.uniform(350, 650, 2)
        w, h = self.width, self.height
        if rng.random() < 0.5:
            start, end = np.array([w - a, 0.0]), np.array([w, b])
        else:
            start, end = np.array([w - a, h]), np.array([w, h - b])
        u = (end - start) / np.linalg.norm(end - start)
        self.hv_line = (start - u * 250, end + u * 250)
        self._space.mark_segment(*self.hv_line, 20.0)

    def _collectors(self, rng):
        """In each outer ZIP: two curving streets across it from the west arterial to the east one,
        and curving links between them and out to the south and north arterials."""
        for z in np.flatnonzero(~self.zip_grid):
            x0, y0, x1, y1 = self.zip_bounds[z]
            W, H = x1 - x0, y1 - y0
            f = np.linspace(0, 1, int(W // 8) + 1)
            across = []
            for lo, hi in ((0.27, 0.36), (0.64, 0.73)):
                ya, yb = y0 + H * rng.uniform(lo, hi, 2)
                y = ya + (yb - ya) * f + rng.uniform(8, 22) * rng.choice([-1, 1]) * np.sin(np.pi * f) \
                    + rng.uniform(-6, 6) * np.sin(2 * np.pi * f)
                across.append(np.stack([x0 + W * f, y], 1))
                self._street(across[-1], COLLECTOR_WIDTH, "collector")
            south, north = across
            # Links: south arterial -> south street, south street -> north street, north street -> north arterial.
            # Each ends exactly on a vertex of the street it meets, so they share a junction.
            for a, b, chance in ((None, south, 0.8), (south, north, 1.0), (north, None, 0.8)):
                if rng.random() > chance:
                    continue
                k = int(rng.integers(int(len(f) * 0.25), int(len(f) * 0.75)))
                start = a[k] if a is not None else np.array([np.clip(b[k, 0] + rng.uniform(-40, 40), x0 + 70, x1 - 70), y0])
                stop = b[k] if b is not None else np.array([np.clip(a[k, 0] + rng.uniform(-40, 40), x0 + 70, x1 - 70), y1])
                g = np.linspace(0, 1, max(int(abs(stop[1] - start[1]) // 8), 2) + 1)[:, None]
                pts = start + (stop - start) * g + np.array([1.0, 0.0]) * rng.uniform(-20, 20) * np.sin(np.pi * g)
                pts[0], pts[-1] = start, stop
                self._street(pts, COLLECTOR_WIDTH, "collector")

    def _grid_blocks(self, rng):
        """Apartment blocks in the blocks nearest the middle of the city, and a hospital on one
        other block of the grid ZIP. Their blocks are reserved whole; the rest get house lots."""
        k, nz = ZIP_BLOCKS, self.blocks // ZIP_BLOCKS
        blocks = []
        for z in np.flatnonzero(self.zip_grid):
            zi, zj = z % nz, z // nz
            blocks += [(bi, bj) for bj in range(zj * k, (zj + 1) * k) for bi in range(zi * k, (zi + 1) * k)]
        bounds = np.array([self._block(bi, bj) for bi, bj in blocks])
        centre = self._centre_dist((bounds[:, 0] + bounds[:, 2]) / 2, (bounds[:, 1] + bounds[:, 3]) / 2)
        for i in np.flatnonzero(centre < 0.2):
            self._apartments(rng, *bounds[i])
        others = np.flatnonzero(centre >= 0.2)
        x0, y0, x1, y1 = bounds[others[int(rng.integers(len(others)))]]
        c = np.array([(x0 + x1) / 2, (y0 + y1) / 2])
        self._space.mark_rect(c, (1.0, 0.0), (x1 - x0) / 2, (y1 - y0) / 2)
        self._building(c, (1.0, 0.0), (x1 - x0) / 2 - 6, (y1 - y0) / 2 - 6, 7 * STOREY, "hospital")
        self.sites.append({"kind": "hospital", "centre": c})
        # Helicopters come and go from the roof, so keep well clear of it all the time.
        self._zones.append({"kind": "hospital", "shape": "circle", "centre": c, "radius": 150.0,
                            "floor": 0.0, "ceiling": 150.0})

    def _apartments(self, rng, x0, y0, x1, y1):
        """A centre block: on each side, one or two apartment buildings with balconies facing the
        street. Each balcony is one flat: its own address, and its drop spot."""
        self._space.mark_rect(np.array([(x0 + x1) / 2, (y0 + y1) / 2]), (1.0, 0.0), (x1 - x0) / 2, (y1 - y0) / 2)
        street_ys = self.ys[np.argmin(np.abs(self.ys - y1))], self.ys[np.argmin(np.abs(self.ys - y0))]
        for front, s, street_y in ((y1, -1.0, street_ys[0]), (y0, 1.0, street_ys[1])):
            spans = [(x0 + 2, x1 - 2)]
            if x1 - x0 > 80 and rng.random() < 0.5:
                m = (x0 + x1) / 2
                spans = [(x0 + 2, m - 5), (m + 5, x1 - 2)]
            face = front + s * 4.0  # facade, 4 m back from the pavement
            out = face - s * 1.5  # balconies stick out 1.5 m towards the street
            depth = rng.uniform(14, 18)
            for bx0, bx1 in spans:
                floors = int(rng.integers(4, 11))
                columns = np.arange(bx0 + 3.5, bx1 - 3.0, 6.0)
                # Floors count up from the highest ground under the building and its balconies, so on
                # a slope the lowest balconies still clear the ground (the downhill side gets taller).
                xs = np.concatenate([columns, [bx0, bx1, bx0, bx1]])
                ys = np.concatenate([np.full(len(columns), out), [out, out, face + s * depth, face + s * depth]])
                level = float(self.ground(xs, ys).max())
                building, g = self._building(((bx0 + bx1) / 2, face + s * depth / 2), (1.0, 0.0), (bx1 - bx0) / 2,
                                             depth / 2, floors * STOREY, "apartment", level=level)
                for f in range(1, floors):
                    z = g + f * STOREY
                    for x in columns:
                        mid = face - s * 0.75
                        self._box((x, mid), (1, 0), 1.6, 0.75, z - 0.2, z, "balcony")
                        self._box((x, out + s * 0.025), (1, 0), 1.6, 0.025, z, z + 1.1, "railing")
                        self._box((x - 1.575, mid), (1, 0), 0.025, 0.75, z, z + 1.1, "railing")
                        self._box((x + 1.575, mid), (1, 0), 0.025, 0.75, z, z + 1.1, "railing")
                        a = self._address("apartment", "centre", (x, face, z), (x, street_y), f, building)
                        self._spots.append((a, "balcony", x, mid, z))

    def _sites(self, rng):
        """Schools, a stadium, cell towers and construction sites, each on a plot facing a street
        in one of the outer ZIPs. They go in before the cul-de-sacs and houses so they fit."""
        for _ in range(2):
            site = self._plot(rng, 110, 80)
            if site is None:
                continue
            c, t, n, front = site
            self._building(front + n * 20, t, 30.0, 12.0, 8.0, "school")
            self.sites.append({"kind": "school", "centre": c})
            # Over the school and its grounds, while children are there.
            self._zones.append({"kind": "school", "shape": "rect", "centre": c, "half": (85.0, 70.0),
                                "yaw": float(np.arctan2(t[1], t[0])), "floor": 0.0, "ceiling": 60.0,
                                "hours": (7.5, 16.0)})
        site = self._plot(rng, 150, 110)
        if site is not None:
            c, t, n, _ = site
            for off, axis, hx, hy in ((45, n, 65, 9), (-45, n, 65, 9), (65, t, 9, 36), (-65, t, 9, 36)):
                self._building(c + axis * off, t, hx, hy, 22.0, "stadium")
            self.sites.append({"kind": "stadium", "centre": c})
            self._zones.append({"kind": "stadium", "shape": "circle", "centre": c, "radius": 300.0, "floor": 0.0,
                                "ceiling": 300.0, "hours": (17.0, 23.0), "active": False})  # _today switches it on
        for _ in range(2):
            site = self._plot(rng, 60, 60)
            if site is None:
                continue
            c, _, _, _ = site
            g, tall = self.ground(*c), rng.uniform(45, 60)
            self._cyls.append((c[0], c[1], 0.8, g - 0.5, g + tall, "cell_tower"))
            for a in rng.uniform(0, 2 * np.pi) + np.arange(3) * 2 * np.pi / 3:
                anchor = c + 0.45 * tall * np.array([np.cos(a), np.sin(a)])
                ga = self.ground(*anchor) + 0.3
                for frac in (0.55, 0.9):
                    self._wires.append((c[0], c[1], g + frac * tall, anchor[0], anchor[1], ga, 0.015, "guy_wire"))
            self.sites.append({"kind": "cell_tower", "centre": c})
        for _ in range(4):
            site = self._plot(rng, 34, 40)
            if site is not None:
                self.sites.append({"kind": "construction", "centre": site[0]})

    def _culdesacs(self, rng):
        """Dead-end streets off the collectors and arterials, alternating sides, each ending in a
        turning circle. Each one grows until it gets too close to another street or runs into
        something reserved (the grid ZIP's blocks and anything outside the city count)."""
        for parent in [s for s in self.streets if s["kind"] in ("collector", "arterial")]:
            pts = parent["points"]
            arc = _arc(pts)
            pos, side = rng.uniform(40, 80), rng.choice([-1.0, 1.0])
            while pos < arc[-1] - 60:
                root, tangent = _at(pts, arc, pos)  # the road graph splits the parent here later
                heading = np.arctan2(*(side * _left(tangent))[::-1]) + rng.uniform(-0.3, 0.3)
                bend = rng.uniform(-0.006, 0.006)
                others = [s for s in self.streets if s is not parent]
                a = np.vstack([s["points"][:-1] for s in others])
                b = np.vstack([s["points"][1:] for s in others])
                path, gap = [root], _seg_dist(root, a, b).min()
                for step in range(28):  # up to 140 m
                    heading += bend * 5
                    q = path[-1] + 5 * np.array([np.cos(heading), np.sin(heading)])
                    # Stop short of other streets, leaving room for a row of houses on each,
                    # but don't mind one nearby that it's heading away from.
                    near = _seg_dist(q, a, b).min()
                    if near < 40 or (near < 70 and near < gap):
                        break
                    gap = near
                    if step >= 3 and not self._space.free_disc(q, LOCAL_WIDTH / 2 + SIDEWALK + 1):
                        break
                    path.append(q)
                while len(path) > 8 and not self._space.free_disc(path[-1], BULB + SIDEWALK + 1):
                    path.pop()  # back off until the turning circle fits
                if len(path) > 8:  # at least 40 m long
                    self._street(path, LOCAL_WIDTH, "culdesac", bulb=BULB)
                pos += rng.uniform(70, 110)
                side = -side

    # Houses

    def _lots(self, rng, s):
        """House lots down both sides of a street, and round the turning circle of a cul-de-sac."""
        pts, arc = s["points"], _arc(s["points"])
        off = s["width"] / 2 + SIDEWALK
        end = arc[-1] - (s["bulb"] + SIDEWALK if s["bulb"] else 0)
        for side in (1.0, -1.0):
            pos = 2.0
            while pos < end - 8:
                district = self._district(_at(pts, arc, pos)[0])
                w, depth = rng.uniform(*LOT_WIDTH[district]), rng.uniform(*LOT_DEPTH[district])
                p, t = _at(pts, arc, pos + w / 2)
                n = side * _left(t)
                if pos + w <= end and self._try_lot(rng, p + n * off, t, n, w, depth, p, district):
                    pos += w
                else:
                    pos += 3.0
        if s["bulb"]:
            c = pts[-1]
            r = s["bulb"] + SIDEWALK
            back = np.arctan2(*(pts[-2] - c)[::-1])  # where the street comes in
            ang = back + 0.9
            while ang < back + 2 * np.pi - 0.9:
                district = self._district(c)
                w, depth = rng.uniform(*LOT_WIDTH[district]), rng.uniform(*LOT_DEPTH[district])
                step = 2 * np.arcsin(min(w / 2 / r, 1.0))
                mid = ang + step / 2
                n = np.array([np.cos(mid), np.sin(mid)])
                if mid + step / 2 <= back + 2 * np.pi - 0.9 and self._try_lot(rng, c + n * r, _left(n) * -1, n, w,
                                                                               depth, c, district):
                    ang += step
                else:
                    ang += 0.15

    def _try_lot(self, rng, front, t, n, w, depth, street_pt, district):
        centre = front + n * depth / 2
        if not self._space.free_rect(centre, t, w / 2, depth / 2):
            return False
        self._space.mark_rect(centre, t, w / 2, depth / 2)
        self._house(rng, front, t, n, w, depth, street_pt, district)
        return True

    def _house(self, rng, front, t, n, w, depth, street_pt, district):
        """A house set back from the street, with a front and back yard, maybe trees and fences.
        Positions in the lot are (v, u): v along the street from the lot's middle, u in from the front."""
        def at(v, u):
            return front + t * v + n * u

        setback, gap = rng.uniform(4, 7), rng.uniform(1.2, 2.5)
        hd = min(rng.uniform(9, 13), depth - setback - 8)
        back = setback + hd
        house, _ = self._building(at(0, setback + hd / 2), t, w / 2 - gap, hd / 2,
                                  rng.integers(1, 3) * STOREY + 1.0, "house")
        door = at(0, setback)
        a = self._address("house", district, (*door, self.ground(*door)), street_pt, 0, house)
        spots = [("porch", 0.0, setback - 1.2), ("front_yard", rng.choice([-1, 1]) * w / 4, setback / 2),
                 ("back_yard", rng.uniform(-1, 1) * w / 4, (back + depth) / 2)]
        for kind, v, u in spots:
            p = at(v, u)
            self._spots.append((a, kind, p[0], p[1], self.ground(*p)))

        # Trees anywhere in the yards, but never with the trunk on a drop spot. Canopies can hang over one.
        for (ua, ub), trees, (r0, r1) in (((0.8, setback - 2.0), rng.integers(0, 2), (1.5, 2.5)),
                                          ((back + 1.5, depth - 0.8), rng.integers(0, 4), (1.5, 3.5))):
            for _ in range(trees):
                v, u = rng.uniform(-w / 2 + 1, w / 2 - 1), rng.uniform(ua, ub)
                if all(np.hypot(v - sv, u - su) > 2.0 for _, sv, su in spots):
                    self._tree(at(v, u), rng.uniform(r0, r1), rng.uniform(5, 13))

        if rng.random() < 0.7:  # a side fence along the back yard, and the back fence
            self._building(at(-w / 2 + 0.05, (back + depth) / 2), t, 0.05, (depth - back) / 2, 1.8, "fence")
            self._building(at(0, depth - 0.05), t, w / 2, 0.05, 1.8, "fence")

    # Overhead lines and the day's changes

    def _power_lines(self):
        """Poles 1 m in from the kerb down the left side of every street outside the centre, with a
        power line and a cable line between them. Poles that would stand in another street are left out."""
        a = np.vstack([s["points"][:-1] for s in self.streets])
        b = np.vstack([s["points"][1:] for s in self.streets])
        half = np.concatenate([np.full(len(s["points"]) - 1, s["width"] / 2) for s in self.streets])
        for s in self.streets:
            if s["kind"] == "access":
                continue
            pts, arc = s["points"], _arc(s["points"])
            end = arc[-1] - (s["bulb"] + 3 if s["bulb"] else 0)
            poles = []
            for pos in np.linspace(0, end, max(2, int(np.ceil(end / POLE_SPACING)) + 1)):
                p, t = _at(pts, arc, pos)
                q = p + _left(t) * (s["width"] / 2 + 1.0)
                ok = self._centre_dist(*q) >= 0.22 and not (_seg_dist(q, a, b) < half + 0.5).any()
                poles.append(q if ok else None)
            for q in poles:
                if q is not None:
                    g = self.ground(*q)
                    self._cyls.append((q[0], q[1], 0.15, g - 0.5, g + POLE_HEIGHT, "pole"))
            for p, q in zip(poles[:-1], poles[1:]):
                if p is not None and q is not None:
                    gp, gq = self.ground(*p), self.ground(*q)
                    self._wires.append((*p, gp + POWER_Z, *q, gq + POWER_Z, 0.02, "power_line"))
                    self._wires.append((*p, gp + CABLE_Z, *q, gq + CABLE_Z, 0.02, "cable"))

    def _pylons(self):
        """Lattice pylons every ~220 m along the high-voltage line, nudged off any street, with two
        conductors on each of two crossarms and an earth wire on top."""
        start, end = self.hv_line
        length = np.linalg.norm(end - start)
        u = (end - start) / length
        across = _left(u)
        a = np.vstack([s["points"][:-1] for s in self.streets])
        b = np.vstack([s["points"][1:] for s in self.streets])
        half = np.concatenate([np.full(len(s["points"]) - 1, s["width"] / 2) for s in self.streets])
        towers = []
        for pos in np.linspace(0, length, int(length // 220) + 2):
            for nudge in (0, 10, -10, 20, -20, 30, -30):
                p = start + u * np.clip(pos + nudge, 0, length)
                if not (_seg_dist(p, a, b) < half + 4).any():
                    towers.append(p)
                    break
        for p in towers:
            g = self.ground(*p)
            self._box(p, u, 1.5, 1.5, g - 0.5, g + 36, "pylon")
            for z in (25.0, 31.0):
                self._box(p, u, 0.5, 9.0, g + z, g + z + 1, "pylon")
        for p, q in zip(towers[:-1], towers[1:]):
            gp, gq = self.ground(*p), self.ground(*q)
            for off, z in ((8, 24.8), (-8, 24.8), (8, 30.8), (-8, 30.8)):
                self._wires.append((*(p + across * off), gp + z, *(q + across * off), gq + z, 0.03, "hv_line"))
            self._wires.append((*p, gp + 36.3, *q, gq + 36.3, 0.01, "hv_line"))

    def _airport(self):
        """A small airfield east of the city: a runway along y and a terminal. Drones may only fly
        low near it (below 30 m within 1.2 km) and never over the runway or its approaches."""
        c = self.runway_centre
        self.runway = (c, np.array([22.0, 450.0]))  # centre, half width and half length, along y
        self._building(c + (-120.0, 0.0), (1.0, 0.0), 30.0, 15.0, 10.0, "airport")
        self._zones.append({"kind": "airport", "shape": "circle", "centre": c, "radius": 1200.0,
                            "floor": 30.0, "ceiling": UNLIMITED})
        self._zones.append({"kind": "runway", "shape": "rect", "centre": c, "half": (150.0, 750.0),
                            "yaw": 0.0, "floor": 0.0, "ceiling": UNLIMITED})

    def _today(self, rng):
        """What changes from day to day: whether the stadium has an event tonight, and which
        construction sites have a crane up, where its jib points and where its hook hangs."""
        for z in self._zones:
            if z["kind"] == "stadium":
                z["active"] = bool(rng.random() < 0.35)
        self.cranes = []
        for site in [s for s in self.sites if s["kind"] == "construction"]:
            if rng.random() > 0.75:
                continue
            c = site["centre"]
            g, tall, yaw = self.ground(*c), rng.uniform(35, 50), rng.uniform(0, 2 * np.pi)
            u = np.array([np.cos(yaw), np.sin(yaw)])
            self._box(c, (1.0, 0.0), 1.0, 1.0, g - 0.5, g + tall, "crane")
            self._box(c + u * 16.5, u, 28.5, 0.8, g + tall, g + tall + 1.6, "crane")  # jib, 45 m out and 12 m back
            self._box(c - u * 10, u, 2.0, 1.5, g + tall - 3, g + tall, "crane")  # counterweight
            hook = c + u * rng.uniform(12, 42)
            self._wires.append((*hook, g + tall, *hook, self.ground(*hook) + rng.uniform(3, 20), 0.03, "crane_cable"))
            self.cranes.append({"centre": c, "height": tall, "yaw": yaw})

    # Road graph

    def _graph(self):
        """Every street vertex is a node. Where a street ends partway along another, or two grid
        streets cross, the other street is split there too, so all junctions are shared nodes."""
        xs, ys = np.meshgrid(self.xs, self.ys)
        joins = np.vstack([np.array([s["points"][0], s["points"][-1]]) for s in self.streets]
                          + [np.stack([xs.ravel(), ys.ravel()], 1)])
        index, nodes, edges, arterial = {}, [], [], []

        def node(p):
            key = (round(float(p[0]), 3), round(float(p[1]), 3))
            if key not in index:
                index[key] = len(nodes)
                nodes.append(p)
            return index[key]

        for s in self.streets:
            pts = [s["points"][0]]
            for a, b in zip(s["points"][:-1], s["points"][1:]):
                ab = b - a
                t = (joins - a) @ ab / (ab @ ab)
                on = (t > 1e-9) & (t < 1 - 1e-9) & (np.linalg.norm(a + t[:, None] * ab - joins, axis=1) < 1e-6)
                pts += [a + tt * ab for tt in np.unique(t[on])]
                pts.append(b)
            ids = [node(p) for p in pts]
            for i, j in zip(ids[:-1], ids[1:]):
                if i != j:
                    edges.append((i, j))
                    arterial.append(s["kind"] in ("arterial", "access"))
        self.nodes = np.array(nodes, float)
        self.edges = np.array(edges, int)
        self.edge_arterial = np.array(arterial, bool)
        self.edge_length = np.linalg.norm(self.nodes[self.edges[:, 1]] - self.nodes[self.edges[:, 0]], axis=1)
        self.edge_speed = np.where(self.edge_arterial, ARTERIAL_SPEED, LOCAL_SPEED)
        self.station_node = index[(round(-STATION_ROAD, 3), round(float(self.station_centre[1]), 3))]

    def _finish(self):
        a, sp = self._addr, self._spots
        self.address_kind = np.array([r[0] for r in a])
        self.address_district = np.array([r[1] for r in a])
        self.address_door = np.array([r[2] for r in a], float)
        self.address_street = np.array([r[3] for r in a], float)  # point on the street centreline out front
        self.address_floor = np.array([r[4] for r in a], int)
        self.address_building = np.array([r[5] for r in a], int)  # box index in self.obstacles
        self.address_zip = self._zip_at(self.address_door[:, :2])
        self.address_zone = self._zone_at(self.address_door[:, :2])
        self.spot_address = np.array([r[0] for r in sp], int)
        self.spot_kind = np.array([r[1] for r in sp])
        self.spot_pos = np.array([r[2:] for r in sp], float)
        self.spot_overhead = self.obstacles.overhead(self.spot_pos + [0, 0, 0.1])  # clear height above each spot
        self.bays[:, 2] = 0.0
        del self._boxes, self._cyls, self._wires, self._addr, self._spots, self._zones, self._space

    # Helpers

    def _street(self, points, width, kind, bulb=0.0):
        pts = np.asarray(points, float)
        self.streets.append({"points": pts, "width": width, "kind": kind, "bulb": bulb})
        for a, b in zip(pts[:-1], pts[1:]):
            self._space.mark_segment(a, b, width / 2 + SIDEWALK)
            self.road_mask.mark_segment(a, b, width / 2)
        if bulb:
            self._space.mark_disc(pts[-1], bulb + SIDEWALK)
            self.road_mask.mark_disc(pts[-1], bulb)

    def _plot(self, rng, width, depth, kinds=("collector", "arterial"), tries=400):
        """Room for a width x depth plot facing a street in an outer ZIP: (centre, t, n, front) or None."""
        streets = [s for s in self.streets if s["kind"] in kinds]
        for _ in range(tries):
            s = streets[int(rng.integers(len(streets)))]
            arc = _arc(s["points"])
            p, t = _at(s["points"], arc, rng.uniform(0, arc[-1]))
            n = rng.choice([-1.0, 1.0]) * _left(t)
            front = p + n * (s["width"] / 2 + SIDEWALK)
            c = front + n * depth / 2
            if self.zip_grid[self._zip_at(c[None])[0]] or not self._space.free_rect(c, t, width / 2, depth / 2):
                continue
            self._space.mark_rect(c, t, width / 2, depth / 2)
            return c, t, n, front
        return None

    def _block(self, bi, bj):
        """Buildable area of grid block (bi, bj), inside the pavements."""
        inset = self.line_width / 2 + SIDEWALK
        return (self.xs[bi] + inset[bi], self.ys[bj] + inset[bj],
                self.xs[bi + 1] - inset[bi + 1], self.ys[bj + 1] - inset[bj + 1])

    def _box(self, c, t, hx, hy, z0, z1, kind):
        self._boxes.append((c[0], c[1], hx, hy, float(np.arctan2(t[1], t[0])), z0, z1, kind))
        return len(self._boxes) - 1

    def _building(self, c, t, hx, hy, height, kind, level=None):
        """A box standing on the ground: its base goes just below the lowest corner, its top is
        `height` above `level` (default: the ground at its centre). Returns (box index, level)."""
        c, t = np.asarray(c, float), np.asarray(t, float)
        n = _left(t)
        corners = c + np.array([sx * hx * t + sy * hy * n for sx in (-1, 1) for sy in (-1, 1)])
        g = float(self.ground(*c)) if level is None else level
        return self._box(c, t, hx, hy, float(self.ground(corners[:, 0], corners[:, 1]).min()) - 0.3, g + height, kind), g

    def _tree(self, p, r, h):
        g = float(self.ground(*p))
        self._cyls.append((p[0], p[1], 0.2, g - 0.3, g + 2.5, "trunk"))
        self._cyls.append((p[0], p[1], r, g + 2.5, g + h, "canopy"))

    def _address(self, kind, district, door, street, floor, building):
        self._addr.append((kind, district, door, street, floor, building))
        return len(self._addr) - 1

    def _centre_dist(self, x, y):
        """0 in the middle of the city, 1 at the middle of each edge."""
        w, h = self.width / 2, self.height / 2
        return np.hypot((np.asarray(x) - w) / w, (np.asarray(y) - h) / h)

    def _district(self, p):
        return "dense" if self._centre_dist(*p) < 0.6 else "suburb"

    def _zip_at(self, p):
        k, nz = ZIP_BLOCKS, self.blocks // ZIP_BLOCKS
        i = np.clip(np.searchsorted(self.xs[::k], p[:, 0]) - 1, 0, nz - 1)
        j = np.clip(np.searchsorted(self.ys[::k], p[:, 1]) - 1, 0, nz - 1)
        return j * nz + i

    def _zone_at(self, p):
        k, nz = ZONE_BLOCKS, self.blocks // ZONE_BLOCKS
        i = np.clip(np.searchsorted(self.xs[::k], p[:, 0]) - 1, 0, nz - 1)
        j = np.clip(np.searchsorted(self.ys[::k], p[:, 1]) - 1, 0, nz - 1)
        return j * nz + i

    def on_road(self, x, y):
        """True where (x, y) is on a road surface."""
        return self.road_mask.get(x, y)

    def summary(self):
        kinds = lambda a: ", ".join(f"{c} {k}" for k, c in zip(*np.unique(a, return_counts=True)))  # noqa: E731
        degree = np.bincount(self.edges.ravel(), minlength=len(self.nodes))
        inside = (self.terrain.height(*np.meshgrid(np.linspace(0, self.width, 60), np.linspace(0, self.height, 50))))
        gy, gx = np.gradient(self.terrain.h, self.terrain.cell)
        def zone(z):
            top = "up" if z["ceiling"] >= UNLIMITED else f"{z['ceiling']:.0f} m"
            return f"{z['kind']} ({z['floor']:.0f} m to {top}{'' if z.get('active', True) else ', not today'})"

        zones = [zone(z) for z in self.airspace.zones]
        return "\n".join([
            f"city seed {self.seed}, day {self.day}: {self.width:.0f} x {self.height:.0f} m",
            f"{len(self.zip_codes)} ZIP codes, {len(self.zone_zip)} zones",
            f"streets: {kinds([s['kind'] for s in self.streets])}",
            f"road graph: {len(self.nodes)} nodes, {len(self.edges)} edges, {(degree == 1).sum()} dead ends",
            f"{len(self.address_kind)} addresses: {kinds(self.address_district)}",
            f"{len(self.spot_kind)} drop spots: {kinds(self.spot_kind)}",
            f"{(self.spot_overhead < 100).mean():.0%} of drop spots have something overhead",
            f"ground: {inside.max() - inside.min():.0f} m from lowest to highest point in the city, "
            f"steepest slope {np.hypot(gx, gy).max():.0%}",
            f"sites: {kinds([s['kind'] for s in self.sites])}; {len(self.cranes)} cranes up today",
            f"no-fly zones: {', '.join(zones)}",
            f"{len(self.obstacles)} obstacles: {kinds(self.obstacles.kind)}",
        ])


class _Raster:
    """1 m grid of booleans over the city, used to keep things from being built on top of each other."""

    def __init__(self, x0, y0, x1, y1):
        self.x0, self.y0 = x0, y0
        self.grid = np.zeros((int(y1 - y0), int(x1 - x0)), bool)

    def mark_outside(self, x0, y0, x1, y1):
        x = self.x0 + np.arange(self.grid.shape[1]) + 0.5
        y = self.y0 + np.arange(self.grid.shape[0]) + 0.5
        self.grid |= (x[None] < x0) | (x[None] > x1) | (y[:, None] < y0) | (y[:, None] > y1)

    def get(self, x, y):
        i = np.clip(np.floor(np.asarray(x) - self.x0).astype(int), 0, self.grid.shape[1] - 1)
        j = np.clip(np.floor(np.asarray(y) - self.y0).astype(int), 0, self.grid.shape[0] - 1)
        return self.grid[j, i]

    def _window(self, lo, hi):
        """Slice and cell-centre coordinates covering lo..hi, and whether it all lies inside the grid."""
        i0, j0 = int(np.floor(lo[0] - self.x0)), int(np.floor(lo[1] - self.y0))
        i1, j1 = int(np.floor(hi[0] - self.x0)), int(np.floor(hi[1] - self.y0))
        ny, nx = self.grid.shape
        inside = i0 >= 0 and j0 >= 0 and i1 < nx and j1 < ny
        i0, j0, i1, j1 = max(i0, 0), max(j0, 0), min(i1, nx - 1), min(j1, ny - 1)
        X = (self.x0 + np.arange(i0, i1 + 1) + 0.5)[None]  # broadcasts against Y to the window's shape
        Y = (self.y0 + np.arange(j0, j1 + 1) + 0.5)[:, None]
        return (slice(j0, j1 + 1), slice(i0, i1 + 1)), X, Y, inside

    def _rect(self, c, t, hx, hy, shrink=0.0):
        ext = np.array([abs(t[0]) * hx + abs(t[1]) * hy, abs(t[1]) * hx + abs(t[0]) * hy])
        win, X, Y, inside = self._window(c - ext, c + ext)
        u = (X - c[0]) * t[0] + (Y - c[1]) * t[1]
        v = -(X - c[0]) * t[1] + (Y - c[1]) * t[0]
        return win, (np.abs(u) <= hx - shrink) & (np.abs(v) <= hy - shrink), inside

    def free_rect(self, c, t, hx, hy):
        win, m, inside = self._rect(c, t, hx, hy, shrink=0.5)
        return inside and not self.grid[win][m].any()

    def mark_rect(self, c, t, hx, hy):
        win, m, _ = self._rect(c, t, hx, hy)
        self.grid[win] |= m

    def free_disc(self, c, r):
        win, X, Y, inside = self._window(c - r, c + r)
        return inside and not self.grid[win][np.hypot(X - c[0], Y - c[1]) <= r].any()

    def mark_disc(self, c, r):
        win, X, Y, _ = self._window(c - r, c + r)
        self.grid[win] |= np.hypot(X - c[0], Y - c[1]) <= r

    def mark_segment(self, a, b, r):
        win, X, Y, _ = self._window(np.minimum(a, b) - r, np.maximum(a, b) + r)
        ab = b - a
        t = np.clip(((X - a[0]) * ab[0] + (Y - a[1]) * ab[1]) / max(ab @ ab, 1e-12), 0, 1)
        self.grid[win] |= np.hypot(X - a[0] - t * ab[0], Y - a[1] - t * ab[1]) <= r


def _arc(points):
    """Distance along a polyline at each vertex."""
    return np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(points, axis=0), axis=1))])


def _at(points, arc, s):
    """Point and unit tangent at distance s along a polyline."""
    k = min(max(int(np.searchsorted(arc, s)) - 1, 0), len(points) - 2)
    t = (points[k + 1] - points[k]) / (arc[k + 1] - arc[k])
    return points[k] + t * (s - arc[k]), t


def _left(t):
    return np.array([-t[1], t[0]])


def _seg_dist(p, a, b):
    """Distance from point p to each segment a[i] -> b[i]."""
    ab = b - a
    t = np.clip(((p - a) * ab).sum(1) / np.maximum((ab * ab).sum(1), 1e-12), 0, 1)
    return np.linalg.norm(a + t[:, None] * ab - p, axis=1)


if __name__ == "__main__":
    start = perf_counter()
    city = City(0)
    built = perf_counter() - start
    print(city.summary())
    print(f"built in {built * 1000:.0f} ms")

    dirs = sphere(64)
    door = city.address_door[np.flatnonzero(city.address_district == "dense")[0]]
    origin = door + [0, 0, 12.0]  # 12 m above a front door
    reps = 2000
    start = perf_counter()
    for _ in range(reps):
        city.obstacles.cast(origin, dirs, 40.0)
    print(f"64-ray cast, 40 m range: {reps / (perf_counter() - start):.0f} per second")
