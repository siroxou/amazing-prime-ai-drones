"""3D obstacles and the two queries drones need: raycasts for range sensors, and contact checks.

Three shapes cover the whole city: axis-aligned boxes (buildings, fences, balconies),
vertical cylinders (tree trunks and canopies, poles) and thin straight wires (power
lines). The ground is the plane z = 0. A coarse grid over x, y keeps every query to the
obstacles nearby, so cost doesn't grow with the size of the city.
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


class Obstacles:
    def __init__(self, boxes=(), cylinders=(), wires=()):
        """boxes: (x0, y0, z0, x1, y1, z1, kind) with x0 <= x1 etc.
        cylinders: (x, y, radius, z0, z1, kind), upright.
        wires: (x0, y0, z0, x1, y1, z1, radius, kind)."""
        b = np.array([r[:6] for r in boxes], float).reshape(-1, 6)
        c = np.array([r[:5] for r in cylinders], float).reshape(-1, 5)
        w = np.array([r[:7] for r in wires], float).reshape(-1, 7)
        self.lo, self.hi = b[:, :3], b[:, 3:]
        self.cyl_xy, self.cyl_r, self.cyl_z = c[:, :2], c[:, 2], c[:, 3:5]
        self.wire_p, self.wire_q, self.wire_r = w[:, :3], w[:, 3:6], w[:, 6]
        self.nb, self.nc = len(b), len(c)
        # One kind per primitive, boxes first, then cylinders, then wires. Ids index into this.
        self.kind = np.array([r[-1] for r in (*boxes, *cylinders, *wires)] or [""])[: len(b) + len(c) + len(w)]
        self._names = np.append(self.kind, ["ground", ""])  # id -2 = ground, -1 = nothing

        lo = np.vstack([b[:, :2], c[:, :2] - c[:, 2:3], np.minimum(w[:, :2], w[:, 3:5])])
        hi = np.vstack([b[:, 3:5], c[:, :2] + c[:, 2:3], np.maximum(w[:, :2], w[:, 3:5])])
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

    def cast(self, origins, dirs, max_dist):
        """Distance along each ray to the first thing it hits, and the kind of thing.

        `origins` is one point (3,) or one per ray (n, 3); `dirs` is (n, 3), any length.
        Misses return max_dist and "". A ray starting inside a box or cylinder returns 0.
        """
        d = np.asarray(dirs, float).reshape(-1, 3)
        d = d / np.linalg.norm(d, axis=1, keepdims=True)
        o = np.broadcast_to(np.asarray(origins, float), d.shape)
        n = len(d)
        end = o + d * max_dist
        lo, hi = np.minimum(o, end).min(0), np.maximum(o, end).max(0)
        ids = self.near(lo[:2], hi[:2])
        ids = ids[(self.bounds_lo[ids] <= hi[:2]).all(1) & (self.bounds_hi[ids] >= lo[:2]).all(1)]
        best = np.full(n, float(max_dist))
        what = np.full(n, -1)
        ds = np.where(np.abs(d) < EPS, EPS, d)  # avoids 0/0 in the slab tests

        def keep(t, global_ids):
            j = t.argmin(1)
            tj = t[np.arange(n), j]
            better = tj < best
            best[better] = tj[better]
            what[better] = global_ids[j[better]]

        down = d[:, 2] < 0
        tg = np.where(down, -o[:, 2] / np.where(down, d[:, 2], -1.0), np.inf)
        hit = tg < best
        best[hit], what[hit] = tg[hit], -2

        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            b = ids[ids < self.nb]
            if len(b):
                t1 = (self.lo[b][None] - o[:, None]) / ds[:, None]
                t2 = (self.hi[b][None] - o[:, None]) / ds[:, None]
                enter, leave = np.minimum(t1, t2).max(2), np.maximum(t1, t2).min(2)
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
                z1 = (self.cyl_z[c, 0][None] - o[:, 2:3]) / ds[:, 2:3]
                z2 = (self.cyl_z[c, 1][None] - o[:, 2:3]) / ds[:, 2:3]
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
        """Kind of the nearest thing a sphere at `point` overlaps, or None. The ground counts."""
        p = np.asarray(point, float)
        if p[2] < radius:
            return "ground"
        ids = self.near(p[:2] - radius, p[:2] + radius)
        gap = np.full(len(ids), np.inf)
        isb = ids < self.nb
        isc = (ids >= self.nb) & (ids < self.nb + self.nc)
        isw = ids >= self.nb + self.nc
        b = ids[isb]
        gap[isb] = np.linalg.norm(np.maximum(np.maximum(self.lo[b] - p, p - self.hi[b]), 0), axis=1)
        c = ids[isc] - self.nb
        side = np.maximum(np.linalg.norm(p[:2] - self.cyl_xy[c], axis=1) - self.cyl_r[c], 0)
        up = np.maximum(np.maximum(self.cyl_z[c, 0] - p[2], p[2] - self.cyl_z[c, 1]), 0)
        gap[isc] = np.hypot(side, up)
        w = ids[isw] - self.nb - self.nc
        v = self.wire_q[w] - self.wire_p[w]
        t = np.clip(((p - self.wire_p[w]) * v).sum(1) / (v * v).sum(1), 0, 1)
        gap[isw] = np.linalg.norm(self.wire_p[w] + v * t[:, None] - p, axis=1) - self.wire_r[w]
        if len(gap) == 0 or gap.min() >= radius:
            return None
        return str(self.kind[ids[gap.argmin()]])

    def overhead(self, points, ceiling=100.0, chunk=64):
        """Clear height straight above each point, up to `ceiling`. Nearby points should be next
        to each other in the list: each chunk only looks at obstacles around the whole chunk."""
        pts = np.asarray(points, float).reshape(-1, 3)
        out = np.empty(len(pts))
        for i in range(0, len(pts), chunk):
            part = pts[i:i + chunk]
            out[i:i + chunk] = self.cast(part, np.tile([0.0, 0.0, 1.0], (len(part), 1)), ceiling)[0]
        return out
