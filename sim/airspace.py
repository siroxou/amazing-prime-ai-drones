"""No-fly airspace: volumes drones must stay out of, some only at certain hours.

Each zone is a circle or a turned rectangle on the map, closed between a floor and a
ceiling measured above the ground under the drone. A zone over a school from 0 to 60 m
means "don't fly over it below 60 m"; a zone around an airfield from 30 m up means "stay
below 30 m here". Hours are 0-24 on the sim clock; zones that aren't on today (a stadium
with no event) have active False.
"""
import numpy as np

UNLIMITED = 1e9


class Airspace:
    def __init__(self, zones, terrain):
        """zones: dicts with kind, shape ("circle" or "rect"), centre (x, y), radius (circle) or
        half (half length, half width) and yaw (rect), floor, ceiling, hours (start, end), active."""
        self.zones, self.terrain = list(zones), terrain
        z = self.zones
        n = len(z)
        self.kind = np.array([q["kind"] for q in z] or [""])[:n]
        self.circle = np.array([q["shape"] == "circle" for q in z], bool)
        self.centre = np.array([q["centre"] for q in z], float).reshape(-1, 2)
        self.half = np.array([q.get("half", (q.get("radius", 0.0),) * 2) for q in z], float).reshape(-1, 2)
        yaw = np.array([q.get("yaw", 0.0) for q in z], float)
        self.cs = np.stack([np.cos(yaw), np.sin(yaw)], 1)
        self.floor = np.array([q["floor"] for q in z], float)
        self.ceiling = np.array([q["ceiling"] for q in z], float)
        self.hours = np.array([q.get("hours", (0.0, 24.0)) for q in z], float).reshape(-1, 2)
        self.active = np.array([q.get("active", True) for q in z], bool)

    def __len__(self):
        return len(self.zones)

    def blocked(self, points, hour=None):
        """Kind of the zone each point is inside, or "". hour=None counts every zone that's
        active today, whatever its hours."""
        p = np.asarray(points, float).reshape(-1, 3)
        if len(self) == 0:
            return np.full(len(p), "")
        agl = p[:, 2] - self.terrain.height(p[:, 0], p[:, 1])
        rx, ry = p[:, None, 0] - self.centre[:, 0], p[:, None, 1] - self.centre[:, 1]
        u = rx * self.cs[:, 0] + ry * self.cs[:, 1]
        v = -rx * self.cs[:, 1] + ry * self.cs[:, 0]
        inside = np.where(self.circle, np.hypot(u, v) <= self.half[:, 0],
                          (np.abs(u) <= self.half[:, 0]) & (np.abs(v) <= self.half[:, 1]))
        on = self.active.copy()
        if hour is not None:
            on &= (self.hours[:, 0] <= hour) & (hour < self.hours[:, 1])
        hit = inside & on & (agl[:, None] >= self.floor) & (agl[:, None] <= self.ceiling)
        return np.where(hit.any(1), self.kind[hit.argmax(1)], "")
