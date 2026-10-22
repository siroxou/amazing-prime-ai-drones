"""3D obstacles, the ground, and the two queries drones need: raycasts for range sensors,
and contact checks.

Three shapes cover everything built: boxes turned about the vertical (buildings, fences,
balconies, crane jibs), upright cylinders (trunks, canopies, poles, masts) and thin straight
wires (power lines, guy wires, crane cables). The ground is a height grid. A coarse grid
over x, y keeps every query to the obstacles nearby, so cost doesn't grow with the city.
"""
import numpy as np

CELL = 50.0  # grid cell size in metres; anything wider than a cell is checked on every query
EPS = 1e-12


def sphere(n):
    """n roughly even unit directions over the whole sphere (Fibonacci lattice)."""
    i = np.arange(n) + 0.5
    z = 1 - 2 * i / n
    a = np.pi * (1 + 5 ** 0.5) * i
    r = np.sqrt(1 - z ** 2)
    return np.stack([r * np.cos(a), r * np.sin(a), z], 1)


class Terrain:
    """Ground height on a regular grid, bilinear in between and flat beyond the edges.
    heights[j, i] is the height at (x0 + i * cell, y0 + j * cell). The default is flat at 0."""

    def __init__(self, x0=0.0, y0=0.0, cell=1.0, heights=((0.0, 0.0), (0.0, 0.0))):
        self.x0, self.y0, self.cell = float(x0), float(y0), float(cell)
        self.h = np.asarray(heights, float)
        self.flat = bool(np.ptp(self.h) == 0)

    def height(self, x, y):
        ny, nx = self.h.shape
        if np.ndim(x) == 0 and np.ndim(y) == 0:  # one point: plain Python is ten times quicker here
            fx = min(max((float(x) - self.x0) / self.cell, 0.0), nx - 1 - 1e-9)
            fy = min(max((float(y) - self.y0) / self.cell, 0.0), ny - 1 - 1e-9)
            i, j = int(fx), int(fy)
            ax, ay = fx - i, fy - j
            h = self.h
            return float((h[j, i] * (1 - ax) + h[j, i + 1] * ax) * (1 - ay)
                         + (h[j + 1, i] * (1 - ax) + h[j + 1, i + 1] * ax) * ay)
        fx = np.clip((np.asarray(x, float) - self.x0) / self.cell, 0, nx - 1 - 1e-9)
        fy = np.clip((np.asarray(y, float) - self.y0) / self.cell, 0, ny - 1 - 1e-9)
        i, j = fx.astype(int), fy.astype(int)
        ax, ay = fx - i, fy - j
        h = self.h
        return (h[j, i] * (1 - ax) + h[j, i + 1] * ax) * (1 - ay) + (h[j + 1, i] * (1 - ax) + h[j + 1, i + 1] * ax) * ay

    def cast(self, o, d, max_dist, step=2.0):
        """Distance along each ray to the ground, inf if it doesn't get there. o, d: (n, 3), d unit.
        A ray starting under the ground returns 0."""
        if self.flat:
            g = self.h[0, 0]
            down = d[:, 2] < 0
            t = np.where(down, (g - o[:, 2]) / np.where(down, d[:, 2], -1.0), np.inf)
            return np.where(o[:, 2] < g, 0.0, t)
        if (d[:, 2] == 1).all():  # straight up, as for overhead clearance: a height map can't be in the way
            return np.where(o[:, 2] < self.height(o[:, 0], o[:, 1]), 0.0, np.inf)
        # March in steps, then bisect inside the first step that ends underground.
        # ponytail: a ridge thinner than one step can be missed; 2 m is far finer than these hills
        t = np.minimum(np.arange(0.0, max_dist + step, step), max_dist)
        p = o[:, None] + d[:, None] * t[None, :, None]
        below = p[..., 2] < self.height(p[..., 0], p[..., 1])
        k = below.argmax(1)
        lo, hi = t[np.maximum(k - 1, 0)], t[k]
        for _ in range(12):
            mid = (lo + hi) / 2
            q = o + d * mid[:, None]
            under = q[:, 2] < self.height(q[:, 0], q[:, 1])
            lo, hi = np.where(under, lo, mid), np.where(under, mid, hi)
        return np.where(below.any(1), np.where(k == 0, 0.0, hi), np.inf)


class Obstacles:
    def __init__(self, boxes=(), cylinders=(), wires=(), terrain=None):
        """boxes: (x, y, half_length, half_width, yaw, z0, z1, kind): centre, half sizes along the
            box's own axes, turned by yaw about the vertical.
        cylinders: (x, y, radius, z0, z1, kind), upright.
        wires: (x0, y0, z0, x1, y1, z1, radius, kind)."""
        b = np.array([r[:7] for r in boxes], float).reshape(-1, 7)
        c = np.array([r[:5] for r in cylinders], float).reshape(-1, 5)
        w = np.array([r[:7] for r in wires], float).reshape(-1, 7)
        self.box_xy, self.box_half, self.box_z = b[:, :2], b[:, 2:4], b[:, 5:7]
        self.box_cs = np.stack([np.cos(b[:, 4]), np.sin(b[:, 4])], 1)
        self.cyl_xy, self.cyl_r, self.cyl_z = c[:, :2], c[:, 2], c[:, 3:5]
        self.wire_p, self.wire_q, self.wire_r = w[:, :3], w[:, 3:6], w[:, 6]
        self.nb, self.nc = len(b), len(c)
        self.terrain = terrain or Terrain()
        # One kind per primitive, boxes first, then cylinders, then wires. Ids index into this.
        self.kind = np.array([r[-1] for r in (*boxes, *cylinders, *wires)] or [""])[: len(b) + len(c) + len(w)]
        self._names = np.append(self.kind, ["ground", ""])  # id -2 = ground, -1 = nothing

        cs = np.abs(self.box_cs)
        ext = np.stack([cs[:, 0] * self.box_half[:, 0] + cs[:, 1] * self.box_half[:, 1],
                        cs[:, 1] * self.box_half[:, 0] + cs[:, 0] * self.box_half[:, 1]], 1)
        lo = np.vstack([self.box_xy - ext, c[:, :2] - c[:, 2:3], np.minimum(w[:, :2], w[:, 3:5])])
        hi = np.vstack([self.box_xy + ext, c[:, :2] + c[:, 2:3], np.maximum(w[:, :2], w[:, 3:5])])
        self.bounds_lo, self.bounds_hi = lo, hi
        # Small primitives go in the cell holding their centre; a query looks one cell further out
        # in every direction, which covers anything up to one cell wide. Bigger ones are always checked.
        big = ((hi - lo) > CELL).any(1)
        self.origin = lo.min(0) if len(lo) else np.zeros(2)
        cell = np.floor(((lo + hi) / 2 - self.origin) / CELL).astype(int)
        self.ncx, self.ncy = (cell.max(0) + 1) if len(cell) else (1, 1)
        key = cell[:, 1] * self.ncx + cell[:, 0]
        small = np.flatnonzero(~big)
        order = np.argsort(key[small], kind="stable")
        self._ids, self._keys = small[order], key[small][order]
        self._big = np.flatnonzero(big)

    def __len__(self):
        return self.nb + self.nc + len(self.wire_r)

    def box_corners(self, ids=None):
        """x, y of each box's four corners, (k, 4, 2)."""
        ids = np.arange(self.nb) if ids is None else np.asarray(ids)
        (c, s), (hx, hy) = self.box_cs[ids].T, self.box_half[ids].T
        sx, sy = np.array([1, 1, -1, -1]), np.array([1, -1, -1, 1])
        lx, ly = sx * hx[:, None], sy * hy[:, None]
        return np.stack([self.box_xy[ids, :1] + lx * c[:, None] - ly * s[:, None],
                         self.box_xy[ids, 1:] + lx * s[:, None] + ly * c[:, None]], -1)

    def near(self, lo, hi):
        """Ids of every primitive whose x, y bounds might overlap the rectangle lo..hi."""
        i0, j0 = np.floor((np.asarray(lo, float) - self.origin) / CELL).astype(int) - 1
        i1, j1 = np.floor((np.asarray(hi, float) - self.origin) / CELL).astype(int) + 1
        i0, i1 = max(i0, 0), min(i1, self.ncx - 1)
        rows = np.arange(max(j0, 0), min(j1, self.ncy - 1) + 1)
        if i0 > i1 or len(rows) == 0:
            return self._big
        start = np.searchsorted(self._keys, rows * self.ncx + i0, "left")
        end = np.searchsorted(self._keys, rows * self.ncx + i1, "right")
        return np.concatenate([self._ids[s:e] for s, e in zip(start, end)] + [self._big])

    def _local(self, b, x, y):
        """x, y in the frame of boxes b (broadcasts)."""
        c, s = self.box_cs[b, 0], self.box_cs[b, 1]
        return x * c + y * s, -x * s + y * c

    def cast(self, origins, dirs, max_dist):
        """Distance along each ray to the first thing it hits, and the kind of thing.

        `origins` is one point (3,) or one per ray (n, 3); `dirs` is (n, 3), any length.
        Misses return max_dist and "". A ray starting inside something returns 0.
        """
        d = np.asarray(dirs, float).reshape(-1, 3)
        d = d / np.linalg.norm(d, axis=1, keepdims=True)
        o = np.ascontiguousarray(np.broadcast_to(np.asarray(origins, float), d.shape))
        n = len(d)
        end = o + d * max_dist
        lo, hi = np.minimum(o, end).min(0), np.maximum(o, end).max(0)
        ids = self.near(lo[:2], hi[:2])
        ids = ids[(self.bounds_lo[ids] <= hi[:2]).all(1) & (self.bounds_hi[ids] >= lo[:2]).all(1)]
        best = np.full(n, float(max_dist))
        what = np.full(n, -1)

        def keep(t, global_ids):
            j = t.argmin(1)
            tj = t[np.arange(n), j]
            better = tj < best
            best[better] = tj[better]
            what[better] = global_ids[j[better]]

        tg = self.terrain.cast(o, d, max_dist)
        hit = tg < best
        best[hit], what[hit] = tg[hit], -2

        def safe(v):  # avoids 0/0 in the slab tests
            return np.where(np.abs(v) < EPS, EPS, v)

        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            dz = safe(d[:, 2:3])
            b = ids[ids < self.nb]
            if len(b):
                ox, oy = self._local(b[None], o[:, None, 0] - self.box_xy[b, 0], o[:, None, 1] - self.box_xy[b, 1])
                dx, dy = self._local(b[None], d[:, None, 0], d[:, None, 1])
                dx, dy = safe(dx), safe(dy)
                hx, hy = self.box_half[b, 0], self.box_half[b, 1]
                tx1, tx2 = (-hx - ox) / dx, (hx - ox) / dx
                ty1, ty2 = (-hy - oy) / dy, (hy - oy) / dy
                tz1, tz2 = (self.box_z[b, 0] - o[:, 2:3]) / dz, (self.box_z[b, 1] - o[:, 2:3]) / dz
                enter = np.maximum(np.maximum(np.minimum(tx1, tx2), np.minimum(ty1, ty2)), np.minimum(tz1, tz2))
                leave = np.minimum(np.minimum(np.maximum(tx1, tx2), np.maximum(ty1, ty2)), np.maximum(tz1, tz2))
                keep(np.where(leave >= np.maximum(enter, 0), np.maximum(enter, 0), np.inf), b)

            c = ids[(ids >= self.nb) & (ids < self.nb + self.nc)] - self.nb
            if len(c):
                rel = o[:, None, :2] - self.cyl_xy[c][None]
                a = (d[:, None, :2] ** 2).sum(-1)
                bq = 2 * (rel * d[:, None, :2]).sum(-1)
                cq = (rel ** 2).sum(-1) - self.cyl_r[c][None] ** 2
                disc = bq ** 2 - 4 * a * cq
                root = np.sqrt(np.maximum(disc, 0))
                flat = a < EPS  # vertical ray: inside the circle or not, for its whole length
                ta = np.where(flat, -np.inf, (-bq - root) / (2 * a))
                tb = np.where(flat, np.inf, (-bq + root) / (2 * a))
                in_xy = np.where(flat, cq <= 0, disc >= 0)
                z1, z2 = (self.cyl_z[c, 0] - o[:, 2:3]) / dz, (self.cyl_z[c, 1] - o[:, 2:3]) / dz
                enter = np.maximum(ta, np.minimum(z1, z2))
                leave = np.minimum(tb, np.maximum(z1, z2))
                hit = in_xy & (leave >= np.maximum(enter, 0))
                keep(np.where(hit, np.maximum(enter, 0), np.inf), c + self.nb)

            w = ids[ids >= self.nb + self.nc] - self.nb - self.nc
            if len(w):
                # Closest approach between the ray and each wire; a hit if it's within the wire's radius.
                # ponytail: reports the closest-approach distance, off by up to radius / sin(angle); fine for cm-thick wires
                p, v = self.wire_p[w][None], (self.wire_q[w] - self.wire_p[w])[None]
                w0 = o[:, None] - p
                u = d[:, None]
                bb, cc = (u * v).sum(-1), (v * v).sum(-1)
                dd, ee = (u * w0).sum(-1), (v * w0).sum(-1)
                den = cc - bb ** 2
                s = np.where(den > EPS, (bb * ee - cc * dd) / np.where(den > EPS, den, 1.0), 0.0)
                t = np.clip((ee + bb * s) / cc, 0, 1)
                s = np.clip(bb * t - dd, 0, max_dist)
                t = np.clip((ee + bb * s) / cc, 0, 1)
                gap = np.linalg.norm(w0 + u * s[..., None] - v * t[..., None], axis=-1)
                keep(np.where(gap <= self.wire_r[w][None], s, np.inf), w + self.nb + self.nc)

        return best, self._names[what]

    def touching(self, point, radius):
        """Kind of the nearest thing a sphere at `point` overlaps, or None. The ground counts
        (measured straight down, which is close enough on these slopes)."""
        p = np.asarray(point, float)
        if p[2] - self.terrain.height(p[0], p[1]) < radius:
            return "ground"
        ids, gap = self._gaps(p, radius)
        if len(gap) == 0 or gap.min() >= radius:
            return None
        return str(self.kind[ids[gap.argmin()]])

    def room(self, point, upto):
        """Distance from `point` to the nearest obstacle (not the ground), up to `upto`."""
        _, gap = self._gaps(np.asarray(point, float), upto)
        return float(min(gap.min(initial=upto), upto))

    def _gaps(self, p, radius):
        """Ids of the primitives near p, and the gap from p to each."""
        ids = self.near(p[:2] - radius, p[:2] + radius)
        gap = np.full(len(ids), np.inf)
        isb = ids < self.nb
        isc = (ids >= self.nb) & (ids < self.nb + self.nc)
        isw = ids >= self.nb + self.nc
        b = ids[isb]
        lx, ly = self._local(b, p[0] - self.box_xy[b, 0], p[1] - self.box_xy[b, 1])
        out = np.stack([np.abs(lx) - self.box_half[b, 0], np.abs(ly) - self.box_half[b, 1],
                        np.maximum(self.box_z[b, 0] - p[2], p[2] - self.box_z[b, 1])], 1)
        gap[isb] = np.linalg.norm(np.maximum(out, 0), axis=1)
        c = ids[isc] - self.nb
        side = np.maximum(np.linalg.norm(p[:2] - self.cyl_xy[c], axis=1) - self.cyl_r[c], 0)
        up = np.maximum(np.maximum(self.cyl_z[c, 0] - p[2], p[2] - self.cyl_z[c, 1]), 0)
        gap[isc] = np.hypot(side, up)
        w = ids[isw] - self.nb - self.nc
        v = self.wire_q[w] - self.wire_p[w]
        t = np.clip(((p - self.wire_p[w]) * v).sum(1) / (v * v).sum(1), 0, 1)
        gap[isw] = np.linalg.norm(self.wire_p[w] + v * t[:, None] - p, axis=1) - self.wire_r[w]
        return ids, gap

    def overhead(self, points, ceiling=100.0, chunk=32):
        """Clear height straight above each point, up to `ceiling`. Nearby points should be next
        to each other in the list: each chunk only looks at obstacles around the whole chunk.
        Wires are ignored: they're centimetres thick, and this is for 'is there a roof or a tree here'."""
        pts = np.asarray(points, float).reshape(-1, 3)
        out = np.full(len(pts), float(ceiling))
        for i in range(0, len(pts), chunk):
            p = pts[i:i + chunk]
            ids = self.near(p[:, :2].min(0), p[:, :2].max(0))
            b = ids[ids < self.nb]
            lx, ly = self._local(b[None], p[:, None, 0] - self.box_xy[b, 0], p[:, None, 1] - self.box_xy[b, 1])
            over = (np.abs(lx) <= self.box_half[b, 0]) & (np.abs(ly) <= self.box_half[b, 1]) & (self.box_z[b, 1] > p[:, 2:3])
            gap_b = np.where(over, np.maximum(self.box_z[b, 0] - p[:, 2:3], 0), np.inf)
            c = ids[(ids >= self.nb) & (ids < self.nb + self.nc)] - self.nb
            r = np.hypot(p[:, None, 0] - self.cyl_xy[c, 0], p[:, None, 1] - self.cyl_xy[c, 1])
            over = (r <= self.cyl_r[c]) & (self.cyl_z[c, 1] > p[:, 2:3])
            gap_c = np.where(over, np.maximum(self.cyl_z[c, 0] - p[:, 2:3], 0), np.inf)
            out[i:i + chunk] = np.minimum(out[i:i + chunk], np.minimum(gap_b.min(1, initial=np.inf), gap_c.min(1, initial=np.inf)))
        return out
