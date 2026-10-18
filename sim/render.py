"""Pictures of the city for the README, drawn with matplotlib.

    python -m sim.render                 # writes docs/images/city-*.png
    python -m sim.render --seed 3 --day 2 --out /tmp
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.collections import LineCollection, PatchCollection, PolyCollection  # noqa: E402
from matplotlib.colors import LightSource  # noqa: E402
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection  # noqa: E402

from .airspace import UNLIMITED  # noqa: E402
from .city import City  # noqa: E402

COLOURS = {"house": "#d8b48e", "apartment": "#a3aebd", "station": "#7f8b99", "balcony": "#6c7480",
           "railing": "#4b5058", "fence": "#9a7752", "trunk": "#6b4f3a", "canopy": "#5f9f5b", "pole": "#5a5a5a",
           "school": "#c9a0dc", "hospital": "#e8e8f0", "stadium": "#b0b6bf", "airport": "#8f9aa6",
           "cell_tower": "#d35400", "crane": "#f1c40f", "pylon": "#6e6e6e"}
WIRES = {"power_line": "#333333", "cable": "#555555", "hv_line": "#8e2c2c", "guy_wire": "#d35400",
         "crane_cable": "#b7950b"}
GROUND, ROAD = "#dfe6cf", "#a8a8a8"


def city_map(city, path, view=None):
    """Top-down map: hills, zones and ZIP codes, streets, buildings, trees, overhead lines, no-fly zones."""
    obs, ter = city.obstacles, city.terrain
    x0, y0, x1, y1 = view or (-380, -260, city.width + 960, city.height + 260)
    fig, ax = plt.subplots(figsize=(14, 9))
    X, Y = np.meshgrid(np.arange(x0, x1, 5.0), np.arange(y0, y1, 5.0))
    H = ter.height(X, Y)
    shade = LightSource(azdeg=315, altdeg=45).shade(H, cmap=plt.cm.Greys, vert_exag=3, blend_mode="soft")
    ax.imshow(shade, extent=(x0, x1, y0, y1), origin="lower", alpha=0.35, zorder=0)
    ax.contour(X, Y, H, levels=np.arange(np.floor(H.min() / 5) * 5, H.max(), 5), colors="#8a7f6a",
               linewidths=0.3, alpha=0.5, zorder=1)
    ax.add_collection(PatchCollection([Rectangle((a, b), c - a, d - b) for a, b, c, d in city.zone_bounds],
                                      facecolors=plt.cm.tab20(np.arange(len(city.zone_bounds)) % 20), alpha=0.16,
                                      edgecolors="none", zorder=1))
    scale = fig.get_figwidth() * 72 * 0.8 / (x1 - x0)  # points per metre, roughly
    for s in city.streets:
        ax.plot(*s["points"].T, color=ROAD, linewidth=s["width"] * scale, solid_capstyle="round", zorder=2)
        if s["bulb"]:
            ax.add_patch(Circle(s["points"][-1], s["bulb"], color=ROAD, zorder=2))
    c, r = city.runway
    ax.add_patch(Rectangle(c - r, *(2 * r), color="#9a9a9a", zorder=2))

    kinds = obs.kind[:obs.nb]
    show = np.flatnonzero(np.isin(kinds, ["house", "apartment", "station", "school", "hospital", "stadium",
                                          "airport", "crane", "pylon"]))
    ax.add_collection(PolyCollection(obs.box_corners(show), facecolors=[COLOURS[k] for k in kinds[show]],
                                     edgecolors="none", zorder=3))
    cyl = obs.kind[obs.nb:obs.nb + obs.nc]
    trees = np.flatnonzero(cyl == "canopy")
    ax.add_collection(PatchCollection([Circle(obs.cyl_xy[k], obs.cyl_r[k]) for k in trees],
                                      facecolors=COLOURS["canopy"], alpha=0.7, edgecolors="none", zorder=3))
    towers = np.flatnonzero(cyl == "cell_tower")
    ax.plot(*obs.cyl_xy[towers].T, "^", color=COLOURS["cell_tower"], markersize=9, zorder=5)
    wk = obs.kind[obs.nb + obs.nc:]
    for kind, width, style in (("power_line", 0.4, (0, (2, 2))), ("hv_line", 1.2, "-"), ("guy_wire", 0.6, "-"),
                               ("crane_cable", 0.6, "-")):
        w = np.flatnonzero(wk == kind)
        ax.add_collection(LineCollection(np.stack([obs.wire_p[w, :2], obs.wire_q[w, :2]], 1), colors=WIRES[kind],
                                         linewidths=width, linestyles=style, zorder=4))

    for z in city.airspace.zones:
        on = z.get("active", True)
        style = {"facecolor": "#e74c3c", "alpha": 0.10 if on else 0.04, "edgecolor": "#c0392b",
                 "linestyle": "-" if on else ":", "linewidth": 1.2, "zorder": 4}
        if z["shape"] == "circle":
            ax.add_patch(Circle(z["centre"], z["radius"], **style))
        else:
            cs = np.array([np.cos(z["yaw"]), np.sin(z["yaw"])])
            n = np.array([-cs[1], cs[0]])
            hx, hy = z["half"]
            ax.add_patch(Polygon([z["centre"] + sx * hx * cs + sy * hy * n for sx, sy in
                                  ((1, 1), (1, -1), (-1, -1), (-1, 1))], **style))
        top = "" if z["ceiling"] >= UNLIMITED else f" below {z['ceiling']:.0f} m"
        label = {"airport": "airfield: stay below 30 m", "runway": "runway: no drones"}.get(
            z["kind"], f"{z['kind']}: no drones{top}" + (" (event days)" if z["kind"] == "stadium" else ""))
        lx, ly = z["centre"] + ((0, z["radius"] * 0.55) if z["kind"] == "airport" else (0, 0))
        ax.text(lx, ly, label, ha="center", va="center", fontsize=8, color="#922b21", zorder=6,
                bbox={"facecolor": "white", "alpha": 0.7, "edgecolor": "none", "pad": 1})

    for code, (a, b, c_, d) in zip(city.zip_codes, city.zip_bounds):
        ax.add_patch(Rectangle((a, b), c_ - a, d - b, fill=False, edgecolor="#222222", linewidth=1.6, zorder=5))
        ax.text(a + 12, d - 14, f"ZIP {code}", fontsize=10, weight="bold", va="top", zorder=6,
                bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none", "pad": 2})
    for z, (a, b, c_, d) in enumerate(city.zone_bounds):
        ax.text((a + c_) / 2, (b + d) / 2, f"zone {z}", fontsize=7, ha="center", va="center", color="#333333", zorder=6)
    ax.text(*(city.station_centre + (0, 110)), "distribution centre", ha="center", fontsize=10, weight="bold", zorder=6)
    ax.plot(*city.bays[:, :2].T, "s", color="#c0392b", markersize=3, zorder=5)
    for s in city.sites:
        if s["kind"] in ("school", "stadium", "cell_tower", "construction"):
            ax.text(*(s["centre"] + (0, -12)), s["kind"].replace("_", " "), ha="center", va="top", fontsize=7,
                    zorder=6, bbox={"facecolor": "white", "alpha": 0.6, "edgecolor": "none", "pad": 1})
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)


def _box_faces(corners, z0, z1):
    top = [(x, y, z1) for x, y in corners]
    sides = [[(*corners[k], z0), (*corners[(k + 1) % 4], z0), (*corners[(k + 1) % 4], z1), (*corners[k], z1)]
             for k in range(4)]
    return [top] + sides


def _prism_faces(x, y, r, z0, z1, sides=8):
    a = np.linspace(0, 2 * np.pi, sides + 1)
    px, py = x + r * np.cos(a), y + r * np.sin(a)
    faces = [[(px[k], py[k], z0), (px[k + 1], py[k + 1], z0), (px[k + 1], py[k + 1], z1), (px[k], py[k], z1)]
             for k in range(sides)]
    return faces + [list(zip(px[:-1], py[:-1], [z1] * sides))]


def view_3d(city, path, bounds, kinds=None, elev=30, azim=-60, size=(12, 8), mesh=2.5):
    """3D view of everything inside bounds (x0, y0, x1, y1), on the hills. `kinds` limits what's drawn."""
    obs = city.obstacles
    x0, y0, x1, y1 = bounds
    centre = (obs.bounds_lo + obs.bounds_hi) / 2
    inside = (centre[:, 0] >= x0) & (centre[:, 0] <= x1) & (centre[:, 1] >= y0) & (centre[:, 1] <= y1)
    if kinds is not None:
        inside &= np.isin(obs.kind, kinds)
    faces, colours = [], []
    b = np.flatnonzero(inside[:obs.nb])
    for i, corners in zip(b, obs.box_corners(b)):
        faces += _box_faces(corners, *obs.box_z[i])
        colours += [COLOURS[obs.kind[i]]] * 5
    for i in np.flatnonzero(inside[obs.nb:obs.nb + obs.nc]):
        f = _prism_faces(*obs.cyl_xy[i], obs.cyl_r[i], *obs.cyl_z[i], sides=8 if obs.cyl_r[i] > 0.5 else 4)
        faces += f
        colours += [COLOURS[obs.kind[obs.nb + i]]] * len(f)
    w = np.flatnonzero(inside[obs.nb + obs.nc:])

    fig = plt.figure(figsize=size)
    ax = fig.add_subplot(projection="3d", computed_zorder=False)
    X, Y = np.meshgrid(np.arange(x0, x1 + mesh, mesh), np.arange(y0, y1 + mesh, mesh))
    Z = city.terrain.height(X, Y)
    road = city.on_road((X[:-1, :-1] + X[1:, 1:]) / 2, (Y[:-1, :-1] + Y[1:, 1:]) / 2)
    rgb = np.where(road[..., None], matplotlib.colors.to_rgb(ROAD), matplotlib.colors.to_rgb(GROUND))
    rgb = LightSource(azdeg=315, altdeg=50).shade_rgb(rgb, Z[:-1, :-1], vert_exag=2, blend_mode="soft")
    ax.plot_surface(X, Y, Z, facecolors=rgb, shade=False, linewidth=0, antialiased=False, zorder=0)
    if mesh > 4:  # too coarse to show the roads in the ground colour, so draw them as lines on it
        lines, widths = [], []
        for s in city.streets:
            pts = s["points"]
            dense = np.concatenate([np.linspace(a, b, max(int(np.linalg.norm(b - a) // 10), 1) + 1)[:-1]
                                    for a, b in zip(pts[:-1], pts[1:])] + [pts[-1:]])
            lines.append(np.column_stack([dense, city.terrain.height(dense[:, 0], dense[:, 1]) + 0.5]))
            widths.append(s["width"] / 8)
        ax.add_collection3d(Line3DCollection(lines, colors=ROAD, linewidths=widths, zorder=1))
    ax.add_collection3d(Poly3DCollection(faces, facecolors=colours, edgecolors="#00000030", linewidths=0.2, zorder=2))
    if len(w):
        ax.add_collection3d(Line3DCollection(np.stack([obs.wire_p[w], obs.wire_q[w]], 1),
                                             colors=[WIRES[k] for k in obs.kind[obs.nb + obs.nc + w]],
                                             linewidths=0.6, zorder=3))
    bottom = Z.min()
    top = max(obs.box_z[b, 1].max(initial=bottom + 10), obs.cyl_z[inside[obs.nb:obs.nb + obs.nc], 1].max(
        initial=bottom + 10), bottom + 10)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_zlim(bottom, top)
    ax.set_box_aspect((x1 - x0, y1 - y0, top - bottom))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--day", type=int, default=0)
    p.add_argument("--out", default="docs/images")
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    city = City(a.seed, day=a.day)
    city_map(city, out / "city-map.png")
    view_3d(city, out / "city-overview.png", (-340, -20, city.width + 20, city.height + 20),
            kinds=["house", "apartment", "station", "school", "hospital", "stadium", "canopy", "crane", "pylon",
                   "cell_tower", "hv_line"], elev=38, azim=-70, size=(14, 9), mesh=10.0)
    # The zone with the most apartments: the edge of the centre, next to small lots.
    zones = np.bincount(city.address_zone[city.address_district == "centre"], minlength=len(city.zone_bounds))
    view_3d(city, out / "city-centre.png", city.zone_bounds[zones.argmax()])
    # Hazards up close: the zone with the most cul-de-sacs, cranes, cell towers and pylons.
    obs = city.obstacles
    hazards = np.concatenate([obs.box_xy[np.isin(obs.kind[:obs.nb], ["crane", "pylon"])],
                              obs.cyl_xy[obs.kind[obs.nb:obs.nb + obs.nc] == "cell_tower"],
                              np.array([s["points"][-1] for s in city.streets if s["kind"] == "culdesac"]).reshape(-1, 2)])
    zone = np.bincount(city._zone_at(hazards), minlength=len(city.zone_bounds)).argmax()
    view_3d(city, out / "city-suburb.png", city.zone_bounds[zone], elev=38)
    print("wrote", ", ".join(str(out / f) for f in ("city-map.png", "city-overview.png", "city-centre.png",
                                                     "city-suburb.png")))


if __name__ == "__main__":
    main()
