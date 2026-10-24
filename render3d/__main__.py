"""Render the README's 3D pictures of planned days with three.js in headless Chrome.

    python -m render3d                 # all shots into docs/images/
    python -m render3d hero stop       # just these
    python -m render3d --fresh         # plan the days again instead of using runs/render3d/

Needs Chrome or Chromium (set CHROME to its path if it isn't found) and a network connection for three.js.
Each shot is rendered at twice its size and scaled down, which smooths every edge.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
CACHE = Path("runs/render3d")
OUT = Path("docs/images")
SIZE, SCALE, FINAL = (1600, 900), 2, (2000, 1125)

LEGEND = [["line", "#ff6a00", "Truck 1: route and drone flights"], ["line", "#8b5cf6", "Truck 2: route and drone flights"],
          ["dash", "#ff6a00", "Afternoon second pass"], ["line", "#e0483e", "No-fly zone outline"]]

SHOTS = {
    "hero": {
        "day": (1007, 3),
        "shot": {"arcs": "all", "droneScale": 7, "truckScale": 3.2, "personScale": 3, "routeWidth": 6, "arcWidth": 1.3,
                 "arcOpacity": 0.9, "offset": [-560, -1180, 600], "fov": 31, "targetHeight": 0, "target": [520, 640],
                 "sun": [-1100, -350, 420],
                 "caption": {"eyebrow": "Amazing Prime AI Drones · simulated delivery day, held-out city {city}",
                             "title": "Two driverless trucks, ten drones each, 500 parcels",
                             "line": "Every drone flight planned for the morning, at its real cruise height over roofs and wires.",
                             "stats": ["{delivered}% delivered today", "{bydrone}% by drone", "last parcel {last}", "0 driver hours"]},
                 "legend": LEGEND},
    },
    "stop": {
        "day": (1007, 3),
        "shot": {"focus": "truck", "truck": 0, "arcs": "aloft", "droneScale": 3, "personScale": 2.4, "parcels": True,
                 "weightDrones": 3, "weightPeople": 0.3, "routeWidth": 3, "arcWidth": 0.45, "offset": [-105, -140, 92], "fov": 36, "shadowReach": 350,
                 "sun": [-500, -260, 300], "fog": 0.0006,
                 "caption": {"eyebrow": "{time} · held-out city {city}, day {day}",
                             "title": "Truck 1 parked: {aloft} drones out",
                             "line": "Drones fly from the truck roof to parcels within 600 m. Bigger parcels wait in its locker: {walking} people are walking over to collect theirs."}},
    },
    "drop": {
        "day": (1007, 3),
        "shot": {"focus": "drop", "arcs": "aloft", "routes": False, "droneScale": 1.5, "personScale": 1.2, "parcels": True,
                 "arcWidth": 0.12, "reach": [24, 0, 0.5], "fov": 46, "shadowReach": 150, "sun": [-300, -160, 190],
                 "fog": 0.0009, "zones": False,
                 "caption": {"eyebrow": "{time} · drop planning",
                             "title": "Lowering a parcel onto a top-floor balcony",
                             "line": "Each parcel gets the quickest way down that fits the spot and the gusts: dropped, set down, or lowered on a line. Only top-floor balconies are open to the sky."}},
    },
    "centre": {
        "day": (0, 0),
        "shot": {"near": "apartment", "routes": False, "arcs": "none", "people": False, "zones": False,
                 "offset": [-190, -250, 150], "fov": 34, "shadowReach": 450, "fog": 0.0005, "sun": [-600, -300, 330],
                 "caption": {"eyebrow": "City {city} · the centre", "title": "Apartment blocks with balconies, next to small lots"}},
    },
    "hazards": {
        "day": (0, 0),
        "shot": {"near": "crane", "routes": False, "arcs": "none", "people": False, "zones": False,
                 "offset": [-150, -210, 115], "fov": 36, "shadowReach": 400, "fog": 0.0005, "sun": [-600, -300, 330],
                 "caption": {"eyebrow": "City {city} · the suburbs", "title": "Cranes, pylons and power lines for the drones to clear"}},
    },
    "grounded": {
        "day": (1002, 3),
        "shot": {"focus": "truck", "truck": 0, "rainy": True, "arcs": "none", "personScale": 4, "truckScale": 2,
                 "weightDrones": 0, "weightPeople": 1,
                 "routeWidth": 4, "parcels": True, "offset": [-150, -200, 125], "fov": 36, "shadowReach": 400,
                 "sun": [-400, -300, 700], "fog": 0.0012, "exposure": 1.1,
                 "caption": {"eyebrow": "{time} · held-out city {city}, day {day}",
                             "title": "Too wet to fly all day: the trucks fall back on their lockers",
                             "line": "{walking} people walking over to truck 1 now. The fleet still delivers {delivered}% today, against 100% for Amazon's vans."}},
    },
}


def chrome():
    for path in (os.environ.get("CHROME"), "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                 "/Applications/Chromium.app/Contents/MacOS/Chromium",
                 *(shutil.which(n) for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"))):
        if path and Path(path).exists():
            return path
    sys.exit("Chrome or Chromium not found: set CHROME to its path")


def day_data(seed, d, fresh=False):
    """The planned day as data, from the cache unless asked to plan it again."""
    path = CACHE / f"city{seed}-day{d}.json"
    if path.exists() and not fresh:
        return json.loads(path.read_text())
    from sim.city import City
    from sim.day import HELD_OUT, Day

    from render3d.scene import export

    held = Path("data/held-out") / f"city{seed}-day{d}.npz"
    day = Day.load(held, City(seed, day=d)) if (seed, d) in HELD_OUT else Day(City(seed, day=d))
    data = export(day)
    CACHE.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, separators=(",", ":")))
    return data


def settle(name, shot, data):
    """Fill in what a shot needs from its day. For the drop: a parcel being lowered onto a balcony, seen from out
    in front of the balcony's facade. Only top-floor balconies are open to the sky, so the drone is above the roof."""
    import numpy as np

    B = data["city"]["boxes"]
    if shot.get("near"):  # a city view: the apartment district, or the crane closest to the high-voltage pylons
        def where(kind):
            return np.array([(B["x"][i], B["y"][i]) for i, k in enumerate(B["kind"]) if k == kind])
        if shot["near"] == "apartment":
            target = where("apartment").mean(0)
        else:
            cranes, pylons = where("crane"), where("pylon")
            target = cranes[np.argmin([np.min(np.hypot(*(pylons - c).T)) for c in cranes])]
        return {**shot, "target": [float(target[0]), float(target[1])]}
    if name != "drop" or "parcel" in shot:
        return shot
    flats = [i for i, k in enumerate(B["kind"]) if k == "apartment"]

    def building(x, y):  # the apartment block this balcony hangs off, and the facade's outward direction
        for i in flats:
            c, s_ = np.cos(B["yaw"][i]), np.sin(B["yaw"][i])
            lx, ly = (x - B["x"][i]) * c + (y - B["y"][i]) * s_, -(x - B["x"][i]) * s_ + (y - B["y"][i]) * c
            hx, hy = B["sx"][i] / 2, B["sy"][i] / 2
            if abs(lx) <= hx + 3 and abs(ly) <= hy + 3:
                n = (np.sign(lx), 0.0) if abs(lx) - hx > abs(ly) - hy else (0.0, np.sign(ly))
                return i, np.array([n[0] * c - n[1] * s_, n[0] * s_ + n[1] * c])
        return None, None

    def clear(a, b):  # no building between two points (x, y, z), sampled every couple of metres
        for k in np.linspace(0, 1, 24):
            x, y, z = np.add(a, np.multiply(np.subtract(b, a), k))
            for i, kind in enumerate(B["kind"]):
                if kind in ("apartment", "house", "station", "school", "hospital", "stadium") and B["z0"][i] - 1 < z < B["z1"][i] + 1:
                    c, s_ = np.cos(B["yaw"][i]), np.sin(B["yaw"][i])
                    lx, ly = (x - B["x"][i]) * c + (y - B["y"][i]) * s_, -(x - B["x"][i]) * s_ + (y - B["y"][i]) * c
                    if abs(lx) < B["sx"][i] / 2 + 1 and abs(ly) < B["sy"][i] / 2 + 1:
                        return False
        return True

    dist, rise, swing = shot.get("reach", (34, 2, 0.5))
    for f in sorted(data["flights"], key=lambda f: -f["spot"][2]):
        if f["mode"] != "lower" or f["spot_kind"] != "balcony":
            continue
        i, normal = building(f["spot"][0], f["spot"][1])
        if i is None:
            continue
        target = np.add(f["spot"], [0, 0, 4])
        for turn in (swing, -swing, 0.0):
            look = normal * np.cos(turn) + np.array([-normal[1], normal[0]]) * np.sin(turn)
            eye = target + [look[0] * dist, look[1] * dist, rise]
            if clear(eye, target + [look[0] * 1.5, look[1] * 1.5, 0]):  # stop just short of the facade itself
                return {**shot, "parcel": f["parcel"], "time": f["t1"] - f["over"] * 0.35,
                        "offset": [float(look[0] * dist), float(look[1] * dist), float(rise)]}
    raise SystemExit("no balcony drop with a clear view")


def render(name, spec, browser, fresh=False):
    data = day_data(*spec["day"], fresh=fresh)
    shot = settle(name, spec["shot"], data)
    page = (HERE / "page.html").read_text().replace(
        "<!-- shot data -->", f"<script>window.SHOT = {json.dumps(shot)}; window.DAY = {json.dumps(data, separators=(',', ':'))};</script>")
    with tempfile.TemporaryDirectory() as tmp:
        html, png = Path(tmp) / f"{name}.html", Path(tmp) / f"{name}.png"
        html.write_text(page)
        flags = ["--headless=new", "--hide-scrollbars", "--enable-gpu", f"--window-size={SIZE[0]},{SIZE[1]}",
                 f"--force-device-scale-factor={SCALE}", "--virtual-time-budget=60000", f"--screenshot={png}"]
        if sys.platform == "darwin":
            flags.append("--use-angle=metal")
        subprocess.run([browser, *flags, html.as_uri()], check=True, capture_output=True, timeout=300)
        OUT.mkdir(parents=True, exist_ok=True)
        out = OUT / f"3d-{name}.jpg"
        Image.open(png).convert("RGB").resize(FINAL, Image.LANCZOS).save(out, quality=88, optimize=True, progressive=True)
    print(f"wrote {out}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("shots", nargs="*", help=f"any of: {', '.join(SHOTS)} (default: all)")
    p.add_argument("--fresh", action="store_true", help="plan the days again")
    a = p.parse_args()
    unknown = set(a.shots) - set(SHOTS)
    if unknown:
        p.error(f"unknown shot: {', '.join(sorted(unknown))}")
    browser = chrome()
    for name in a.shots or SHOTS:
        render(name, SHOTS[name], browser, a.fresh)


if __name__ == "__main__":
    main()
