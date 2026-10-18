"""City layout: streets, ZIP codes, delivery zones, the distribution centre, and the 3D
houses, apartment blocks, trees, fences and power lines the drones fly around.

Streets form a grid along x and y and every building is an axis-aligned box. Arterial
roads run every ZIP_BLOCKS blocks and bound the ZIP codes; each ZIP splits into zones of
ZONE_BLOCKS x ZONE_BLOCKS blocks. The middle of the city is apartment blocks with
balconies, around that are small lots, and further out bigger suburban lots. The
distribution centre sits west of the city with an access road onto the middle arterial.

Everything is stored as flat numpy arrays per address, drop spot, block, zone and ZIP.
Units are metres and z is up.

    python -m sim.city       # build a city, print what's in it and time the queries
"""
from time import perf_counter

import numpy as np

from .geometry import Obstacles, sphere

ZIP_BLOCKS, ZONE_BLOCKS = 4, 2
LOCAL_WIDTH, ARTERIAL_WIDTH, SIDEWALK = 10.0, 18.0, 2.5  # street widths are kerb to kerb
LOCAL_SPEED, ARTERIAL_SPEED = 30 / 3.6, 50 / 3.6  # speed limits, m/s
STOREY = 3.0
DISTRICTS = ("centre", "dense", "suburb")
SPOT_KINDS = ("porch", "front_yard", "back_yard", "balcony")
LOT_WIDTH = {"dense": (12.0, 16.0), "suburb": (20.0, 28.0)}
POLE_SPACING, POLE_HEIGHT = 40.0, 10.0
POWER_Z, CABLE_Z = 9.5, 6.0  # the power line, and the lower phone/cable line on the same poles
STATION_ROAD, BAYS = 80.0, 10  # access road length, truck bays at the distribution centre


class City:
    def __init__(self, seed=0, blocks=12):
        if blocks % ZIP_BLOCKS:
            raise ValueError(f"blocks must be a multiple of {ZIP_BLOCKS}")
        rng = np.random.default_rng(seed)
        self.seed, self.blocks = seed, blocks
        self.arterial = np.arange(blocks + 1) % ZIP_BLOCKS == 0  # per street line; same pattern along x and y
        self.line_width = np.where(self.arterial, ARTERIAL_WIDTH, LOCAL_WIDTH)
        self.xs = np.concatenate([[0.0], np.cumsum(rng.uniform(100, 140, blocks))])  # north-south streets
        self.ys = np.concatenate([[0.0], np.cumsum(rng.uniform(85, 115, blocks))])  # east-west streets

        self._boxes, self._cyls, self._wires, self._addr, self._spots = [], [], [], [], []
        self._roads()
        self._blocks(rng)
        self._station()
        self._power_lines()
        self.obstacles = Obstacles(self._boxes, self._cyls, self._wires)
        self._finish()

    # Road graph: one node per junction plus the distribution centre's gate.

    def _roads(self):
        n = self.blocks
        gx, gy = np.meshgrid(self.xs, self.ys)
        idx = np.arange((n + 1) ** 2).reshape(n + 1, n + 1)  # node idx[j, i] sits at (xs[i], ys[j])
        along_x = np.stack([idx[:, :-1].ravel(), idx[:, 1:].ravel()], 1)
        along_y = np.stack([idx[:-1].ravel(), idx[1:].ravel()], 1)
        self.station_row = ZIP_BLOCKS * int(round(n / 2 / ZIP_BLOCKS))  # the arterial nearest the middle
        gate = [-STATION_ROAD, self.ys[self.station_row]]
        self.nodes = np.vstack([np.stack([gx.ravel(), gy.ravel()], 1), [gate]])
        self.station_node = len(self.nodes) - 1
        self.edges = np.vstack([along_x, along_y, [[self.station_node, idx[self.station_row, 0]]]])
        self.edge_arterial = np.concatenate([np.repeat(self.arterial, n), np.tile(self.arterial, n), [True]])
        self.edge_length = np.linalg.norm(self.nodes[self.edges[:, 1]] - self.nodes[self.edges[:, 0]], axis=1)
        self.edge_speed = np.where(self.edge_arterial, ARTERIAL_SPEED, LOCAL_SPEED)

    # Blocks, zones and ZIP codes, then what's built on each block.

    def _blocks(self, rng):
        n, xs, ys = self.blocks, self.xs, self.ys
        bi, bj = (a.ravel() for a in np.meshgrid(np.arange(n), np.arange(n)))  # block b = bj * n + bi
        inset = self.line_width / 2 + SIDEWALK
        self.block_bounds = np.stack(
            [xs[bi] + inset[bi], ys[bj] + inset[bj], xs[bi + 1] - inset[bi + 1], ys[bj + 1] - inset[bj + 1]], 1)
        centre = self._centre_dist((self.block_bounds[:, 0] + self.block_bounds[:, 2]) / 2,
                                   (self.block_bounds[:, 1] + self.block_bounds[:, 3]) / 2)
        self.block_district = np.where(centre < 0.2, "centre",
                                       np.where(centre + rng.uniform(-0.08, 0.08, n * n) < 0.6, "dense", "suburb"))

        zones, zips = n // ZONE_BLOCKS, n // ZIP_BLOCKS  # per row
        self.block_zone = (bj // ZONE_BLOCKS) * zones + bi // ZONE_BLOCKS
        self.block_zip = (bj // ZIP_BLOCKS) * zips + bi // ZIP_BLOCKS
        zi, zj = (a.ravel() for a in np.meshgrid(np.arange(zones), np.arange(zones)))
        k = ZONE_BLOCKS
        self.zone_zip = (zj * k // ZIP_BLOCKS) * zips + zi * k // ZIP_BLOCKS
        self.zone_bounds = np.stack([xs[zi * k], ys[zj * k], xs[(zi + 1) * k], ys[(zj + 1) * k]], 1)  # street centrelines
        pi, pj = (a.ravel() for a in np.meshgrid(np.arange(zips), np.arange(zips)))
        k = ZIP_BLOCKS
        self.zip_bounds = np.stack([xs[pi * k], ys[pj * k], xs[(pi + 1) * k], ys[(pj + 1) * k]], 1)
        self.zip_codes = [f"{101 + i:05d}" for i in range(zips * zips)]  # made up: real ZIP codes start at 00501

        for b in range(n * n):
            x0, y0, x1, y1 = self.block_bounds[b]
            depth = (y1 - y0) / 2
            # The north half faces the street to its north, the south half the street to its south.
            for front, s, street_y in ((y1, -1.0, ys[bj[b] + 1]), (y0, 1.0, ys[bj[b]])):
                if self.block_district[b] == "centre":
                    self._apartments(rng, b, x0, x1, front, s, depth, street_y)
                else:
                    self._houses(rng, b, x0, x1, front, s, depth, street_y, LOT_WIDTH[self.block_district[b]])

    def _houses(self, rng, b, x0, x1, front, s, depth, street_y, lot_width):
        """One side of a block: a row of lots, each with a house, front and back yard, maybe trees
        and fences. `u` is distance in from the street, so y = front + s * u."""
        count = max(1, int((x1 - x0) // np.mean(lot_width)))
        w = rng.uniform(*lot_width, count)
        cuts = x0 + np.concatenate([[0.0], np.cumsum(w)]) * (x1 - x0) / w.sum()
        for lx0, lx1 in zip(cuts[:-1], cuts[1:]):
            setback, house_depth, gap = rng.uniform(5, 8), rng.uniform(9, 13), rng.uniform(1.2, 2.5)
            cx, back = (lx0 + lx1) / 2, setback + house_depth
            height = rng.integers(1, 3) * STOREY + 1.0
            house = self._box(lx0 + gap, lx1 - gap, front + s * setback, front + s * back, 0.0, height, "house")
            a = self._address("house", b, (cx, front + s * setback, 0.0), (cx, street_y), 0, house)
            quarter = (lx1 - lx0) / 4
            spots = [("porch", cx, setback - 1.2),
                     ("front_yard", cx + rng.choice([-1, 1]) * quarter, setback / 2),
                     ("back_yard", cx + rng.uniform(-1, 1) * quarter, (back + depth) / 2)]
            for kind, x, u in spots:
                self._spots.append((a, kind, x, front + s * u, 0.0))

            # Trees anywhere in the yards, but never with the trunk on a drop spot. Canopies can hang over one.
            for (ua, ub), trees, (r0, r1) in (((0.8, setback - 2.0), rng.integers(0, 2), (1.5, 2.5)),
                                              ((back + 1.5, depth - 0.8), rng.integers(0, 4), (1.5, 3.5))):
                for _ in range(trees):
                    x, y = rng.uniform(lx0 + 1, lx1 - 1), front + s * rng.uniform(ua, ub)
                    if all(np.hypot(x - sx, y - (front + s * su)) > 2.0 for _, sx, su in spots):
                        self._tree(x, y, rng.uniform(r0, r1), rng.uniform(5, 13))

            if rng.random() < 0.7:  # side fence along the back yard, plus the back fence once per pair of lots
                self._box(lx0, lx0 + 0.1, front + s * back, front + s * depth, 0.0, 1.8, "fence")
                if s < 0:
                    self._box(lx0, lx1, front + s * depth - 0.05, front + s * depth + 0.05, 0.0, 1.8, "fence")

    def _apartments(self, rng, b, x0, x1, front, s, depth, street_y):
        """One side of a centre block: one or two apartment buildings with balconies facing the street.
        Each balcony is one flat: its own address, and its drop spot."""
        spans = [(x0 + 2, x1 - 2)]
        if x1 - x0 > 80 and rng.random() < 0.5:
            m = (x0 + x1) / 2
            spans = [(x0 + 2, m - 5), (m + 5, x1 - 2)]
        face = front + s * 4.0  # facade, 4 m back from the pavement
        out = face - s * 1.5  # balconies stick out 1.5 m towards the street
        for bx0, bx1 in spans:
            floors = int(rng.integers(4, 11))
            building = self._box(bx0, bx1, face, face + s * rng.uniform(14, 18), 0.0, floors * STOREY, "apartment")
            for f in range(1, floors):
                z = f * STOREY
                for x in np.arange(bx0 + 3.5, bx1 - 3.0, 6.0):
                    self._box(x - 1.6, x + 1.6, face, out, z - 0.2, z, "balcony")
                    self._box(x - 1.6, x + 1.6, out, out + s * 0.05, z, z + 1.1, "railing")
                    self._box(x - 1.6, x - 1.55, face, out, z, z + 1.1, "railing")
                    self._box(x + 1.55, x + 1.6, face, out, z, z + 1.1, "railing")
                    a = self._address("apartment", b, (x, face, z), (x, street_y), f, building)
                    self._spots.append((a, "balcony", x, face - s * 0.75, z))

    def _station(self):
        """Distribution centre west of the city: a warehouse, and a yard with truck bays in front of it.
        Trucks start backed onto the warehouse wall, facing the gate (heading 0, along +x)."""
        y = self.ys[self.station_row]
        self.station_building = self._box(-320.0, -220.0, y - 90, y + 90, 0.0, 14.0, "station")
        self.bays = np.array([[-214.0, y - 54.0 + 12.0 * k, 0.0] for k in range(BAYS)])  # x, y, heading

    def _power_lines(self):
        """Poles and two overhead lines down one side of every street, except in the centre."""
        for horizontal, lines, cross in ((True, self.ys, self.xs), (False, self.xs, self.ys)):
            # Poles along each stretch between junctions, so none stand in a crossing street.
            gaps = zip(cross[:-1] + self.line_width[:-1] / 2 + 1.0, cross[1:] - self.line_width[1:] / 2 - 1.0)
            along = np.concatenate([np.linspace(a, b, max(2, int(np.ceil((b - a) / POLE_SPACING)) + 1)) for a, b in gaps])
            for k, c in enumerate(lines):
                side = np.full_like(along, c + self.line_width[k] / 2 + 1.0)  # in the pavement, north or east side
                pts = np.stack([along, side] if horizontal else [side, along], 1)
                mid = (pts[:-1] + pts[1:]) / 2
                span = self._centre_dist(mid[:, 0], mid[:, 1]) >= 0.22  # the centre's lines are underground
                used = np.zeros(len(pts), bool)
                used[:-1] |= span
                used[1:] |= span
                for x, y in pts[used]:
                    self._cyls.append((x, y, 0.15, 0.0, POLE_HEIGHT, "pole"))
                for (xa, ya), (xb, yb) in zip(pts[:-1][span], pts[1:][span]):
                    self._wires.append((xa, ya, POWER_Z, xb, yb, POWER_Z, 0.02, "power_line"))
                    self._wires.append((xa, ya, CABLE_Z, xb, yb, CABLE_Z, 0.02, "cable"))

    def _finish(self):
        a, sp = self._addr, self._spots
        self.address_kind = np.array([r[0] for r in a])
        self.address_block = np.array([r[1] for r in a], int)
        self.address_door = np.array([r[2] for r in a], float)
        self.address_street = np.array([r[3] for r in a], float)  # point on the street centreline out front
        self.address_floor = np.array([r[4] for r in a], int)
        self.address_building = np.array([r[5] for r in a], int)  # box index in self.obstacles
        self.address_zone = self.block_zone[self.address_block]
        self.address_zip = self.block_zip[self.address_block]
        self.spot_address = np.array([r[0] for r in sp], int)
        self.spot_kind = np.array([r[1] for r in sp])
        self.spot_pos = np.array([r[2:] for r in sp], float)
        self.spot_overhead = self.obstacles.overhead(self.spot_pos + [0, 0, 0.1])  # clear height above each spot
        del self._boxes, self._cyls, self._wires, self._addr, self._spots

    # Helpers

    def _box(self, xa, xb, ya, yb, za, zb, kind):
        self._boxes.append((min(xa, xb), min(ya, yb), za, max(xa, xb), max(ya, yb), zb, kind))
        return len(self._boxes) - 1

    def _tree(self, x, y, r, h):
        self._cyls.append((x, y, 0.2, 0.0, 2.5, "trunk"))
        self._cyls.append((x, y, r, 2.5, h, "canopy"))

    def _address(self, kind, block, door, street, floor, building):
        self._addr.append((kind, block, door, street, floor, building))
        return len(self._addr) - 1

    def _centre_dist(self, x, y):
        """0 in the middle of the city, 1 at the middle of each edge."""
        w, h = self.xs[-1] / 2, self.ys[-1] / 2
        return np.hypot((np.asarray(x) - w) / w, (np.asarray(y) - h) / h)

    def summary(self):
        district = self.block_district[self.address_block]
        lines = [f"city seed {self.seed}: {self.xs[-1]:.0f} x {self.ys[-1]:.0f} m, {self.blocks}x{self.blocks} blocks",
                 f"{len(self.zip_codes)} ZIP codes, {len(self.zone_zip)} zones, {len(self.nodes)} road nodes, {len(self.edges)} road edges",
                 f"{len(self.address_kind)} addresses: " + ", ".join(f"{(district == d).sum()} {d}" for d in DISTRICTS),
                 f"{len(self.spot_kind)} drop spots: " + ", ".join(f"{(self.spot_kind == k).sum()} {k}" for k in SPOT_KINDS),
                 f"{(self.spot_overhead < 100).mean():.0%} of drop spots have something overhead",
                 f"{len(self.obstacles)} obstacles: " + ", ".join(
                     f"{c} {k}" for k, c in zip(*np.unique(self.obstacles.kind, return_counts=True)))]
        return "\n".join(lines)


if __name__ == "__main__":
    start = perf_counter()
    city = City(0)
    built = perf_counter() - start
    print(city.summary())
    print(f"built in {built * 1000:.0f} ms")

    dirs = sphere(64)
    x0, y0, x1, y1 = city.block_bounds[np.flatnonzero(city.block_district == "dense")[0]]
    origin = np.array([(x0 + x1) / 2, y1 - 2, 12.0])  # 12 m up over the back yards
    reps = 2000
    start = perf_counter()
    for _ in range(reps):
        city.obstacles.cast(origin, dirs, 40.0)
    print(f"64-ray cast, 40 m range: {reps / (perf_counter() - start):.0f} per second")
