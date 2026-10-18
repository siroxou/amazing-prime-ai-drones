"""Pictures of the city for the README, drawn with matplotlib.

    python -m sim.render                 # writes docs/images/city-*.png
    python -m sim.render --seed 3 --out /tmp
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.collections import LineCollection, PatchCollection  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection  # noqa: E402

from .city import ARTERIAL_WIDTH, LOCAL_WIDTH, City  # noqa: E402

COLOURS = {"house": "#d8b48e", "apartment": "#a3aebd", "station": "#7f8b99", "balcony": "#6c7480",
           "railing": "#4b5058", "fence": "#9a7752", "trunk": "#6b4f3a", "canopy": "#5f9f5b", "pole": "#5a5a5a"}
GROUND, ROAD = "#e6eadb", "#b9b9b9"


def city_map(city, path):
    """Top-down map: zones shaded, ZIP codes outlined, roads, buildings, trees, power lines."""
    obs = city.obstacles
    fig, ax = plt.subplots(figsize=(11, 9))
    zone_colours = plt.cm.tab20(np.arange(len(city.zone_bounds)) % 20)
    ax.add_collection(PatchCollection([Rectangle((x0, y0), x1 - x0, y1 - y0) for x0, y0, x1, y1 in city.zone_bounds],
                                      facecolors=zone_colours, alpha=0.22, edgecolors="none"))
    roads = city.nodes[city.edges]
    ax.add_collection(LineCollection(roads[~city.edge_arterial], colors=ROAD, linewidths=1.2))
    ax.add_collection(LineCollection(roads[city.edge_arterial], colors="#8c8c8c", linewidths=3))
    for kind in ("house", "apartment", "station"):
        i = np.flatnonzero(obs.kind[:obs.nb] == kind)
        ax.add_collection(PatchCollection([Rectangle(obs.lo[k, :2], *(obs.hi[k, :2] - obs.lo[k, :2])) for k in i],
                                          facecolors=COLOURS[kind], edgecolors="none"))
    c = np.flatnonzero(obs.kind[obs.nb:obs.nb + obs.nc] == "canopy")
    ax.add_collection(PatchCollection([Circle(obs.cyl_xy[k], obs.cyl_r[k]) for k in c],
                                      facecolors=COLOURS["canopy"], alpha=0.7, edgecolors="none"))
    w = np.flatnonzero(obs.kind[obs.nb + obs.nc:] == "power_line")
    ax.add_collection(LineCollection(np.stack([obs.wire_p[w, :2], obs.wire_q[w, :2]], 1), colors="#333333",
                                     linewidths=0.4, linestyles=(0, (2, 2))))
    for code, (x0, y0, x1, y1) in zip(city.zip_codes, city.zip_bounds):
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, edgecolor="#222222", linewidth=1.6))
        ax.text(x0 + 12, y1 - 14, f"ZIP {code}", fontsize=10, weight="bold", va="top",
                bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none", "pad": 2})
    for z, (x0, y0, x1, y1) in enumerate(city.zone_bounds):
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, f"zone {z}", fontsize=7, ha="center", va="center", color="#333333")
    sx0, sy0 = obs.lo[city.station_building, :2]
    sx1, sy1 = obs.hi[city.station_building, :2]
    ax.text((sx0 + sx1) / 2, sy1 + 15, "distribution centre", ha="center", fontsize=10, weight="bold")
    ax.plot(*city.bays[:, :2].T, "s", color="#c0392b", markersize=3)
    ax.autoscale_view()
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)


def _box_faces(lo, hi):
    (x0, y0, z0), (x1, y1, z1) = lo, hi
    return [[(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
            [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
            [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)],
            [(x1, y1, z0), (x0, y1, z0), (x0, y1, z1), (x1, y1, z1)],
            [(x0, y1, z0), (x0, y0, z0), (x0, y0, z1), (x0, y1, z1)]]


def _prism_faces(x, y, r, z0, z1, sides=8):
    a = np.linspace(0, 2 * np.pi, sides + 1)
    px, py = x + r * np.cos(a), y + r * np.sin(a)
    faces = [[(px[k], py[k], z0), (px[k + 1], py[k + 1], z0), (px[k + 1], py[k + 1], z1), (px[k], py[k], z1)]
             for k in range(sides)]
    return faces + [list(zip(px[:-1], py[:-1], [z1] * sides))]


def view_3d(city, path, bounds, kinds=None, elev=30, azim=-60, size=(12, 8)):
    """3D view of everything inside bounds (x0, y0, x1, y1). `kinds` limits what's drawn."""
    obs = city.obstacles
    x0, y0, x1, y1 = bounds
    centre = (obs.bounds_lo + obs.bounds_hi) / 2
    inside = (centre[:, 0] >= x0) & (centre[:, 0] <= x1) & (centre[:, 1] >= y0) & (centre[:, 1] <= y1)
    if kinds is not None:
        inside &= np.isin(obs.kind, kinds)
    faces, colours = [], []
    for i in np.flatnonzero(inside[:obs.nb]):
        faces += _box_faces(obs.lo[i], obs.hi[i])
        colours += [COLOURS[obs.kind[i]]] * 5
    for i in np.flatnonzero(inside[obs.nb:obs.nb + obs.nc]):
        f = _prism_faces(*obs.cyl_xy[i], obs.cyl_r[i], *obs.cyl_z[i], sides=8 if obs.cyl_r[i] > 0.5 else 4)
        faces += f
        colours += [COLOURS[obs.kind[obs.nb + i]]] * len(f)
    w = np.flatnonzero(inside[obs.nb + obs.nc:])

    fig = plt.figure(figsize=size)
    ax = fig.add_subplot(projection="3d", computed_zorder=False)
    ax.add_collection3d(Poly3DCollection([[(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)]],
                                         facecolors=GROUND, zorder=0))
    roads = []
    for (a, b), art in zip(city.edges, city.edge_arterial):
        h = (ARTERIAL_WIDTH if art else LOCAL_WIDTH) / 2
        lo, hi = np.minimum(city.nodes[a], city.nodes[b]) - h, np.maximum(city.nodes[a], city.nodes[b]) + h
        rx0, ry0 = np.maximum(lo, (x0, y0))
        rx1, ry1 = np.minimum(hi, (x1, y1))
        if rx1 > rx0 and ry1 > ry0:
            roads.append([(rx0, ry0, 0.01), (rx1, ry0, 0.01), (rx1, ry1, 0.01), (rx0, ry1, 0.01)])
    ax.add_collection3d(Poly3DCollection(roads, facecolors=ROAD, zorder=1))
    ax.add_collection3d(Poly3DCollection(faces, facecolors=colours, edgecolors="#00000030", linewidths=0.2, zorder=2))
    if len(w):
        ax.add_collection3d(Line3DCollection(np.stack([obs.wire_p[w], obs.wire_q[w]], 1), colors="#222222",
                                             linewidths=0.5, zorder=3))
    top = max(obs.hi[:obs.nb, 2][inside[:obs.nb]].max(initial=10.0), 10.0)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_zlim(0, top)
    ax.set_box_aspect((x1 - x0, y1 - y0, top))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--out", default="docs/images")
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    city = City(a.seed)
    city_map(city, out / "city-map.png")
    obs = city.obstacles
    sx0 = obs.lo[city.station_building, 0] - 20
    view_3d(city, out / "city-overview.png", (sx0, city.ys[0] - 20, city.xs[-1] + 20, city.ys[-1] + 20),
            kinds=["house", "apartment", "station", "canopy"], elev=38, azim=-70, size=(14, 9))
    # A zone at the edge of the centre: apartments with balconies next to small lots.
    edge = np.flatnonzero(city.block_district == "centre")[0]
    view_3d(city, out / "city-zone.png", city.zone_bounds[city.block_zone[edge]])
    # A suburban zone in the corner, with yards, trees, fences and power lines.
    view_3d(city, out / "city-suburb.png", city.zone_bounds[0], elev=40)
    print("wrote", ", ".join(str(out / f) for f in ("city-map.png", "city-overview.png", "city-zone.png", "city-suburb.png")))


if __name__ == "__main__":
    main()
