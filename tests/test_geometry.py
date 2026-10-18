import numpy as np
import pytest

from sim.airspace import UNLIMITED, Airspace
from sim.geometry import Obstacles, Terrain, sphere


def scene(terrain=None):
    return Obstacles(
        boxes=[(11, 0, 1, 2, 0.0, 0, 5, "house")],
        cylinders=[(0, 10, 1.0, 2, 8, "canopy")],
        wires=[(-5, -10, 6, 5, -10, 6, 0.05, "power_line")],
        terrain=terrain,
    )


def tilted(slope=0.1):
    """Ground rising along x: z = slope * x."""
    x = np.arange(-100.0, 101.0, 5.0)
    return Terrain(-100.0, -100.0, 5.0, np.tile(slope * x, (len(x), 1)))


def test_rays_hit_each_shape_at_the_right_distance():
    obs = scene()
    o = np.array([0.0, 0.0, 3.0])
    dist, kind = obs.cast(o, [[1, 0, 0], [0, 1, 0], [0, -1, 0.3], [0, -1, 0], [0, 0, -1], [-1, 0, 0]], 50)
    assert dist[0] == pytest.approx(10) and kind[0] == "house"
    assert dist[1] == pytest.approx(9) and kind[1] == "canopy"
    assert dist[2] == pytest.approx(np.hypot(10, 3), abs=0.1) and kind[2] == "power_line"
    assert dist[3] == 50 and kind[3] == ""  # passes 3 m under the wire
    assert dist[4] == pytest.approx(3) and kind[4] == "ground"
    assert dist[5] == 50 and kind[5] == ""


def test_vertical_rays_hit_cylinder_caps_and_box_tops():
    obs = scene()
    dist, kind = obs.cast([[0, 10, 20], [11, 0, 20], [0, 10, 0.5]], [[0, 0, -1], [0, 0, -1], [0, 0, 1]], 50)
    assert dist == pytest.approx([12, 15, 1.5])
    assert list(kind) == ["canopy", "house", "canopy"]


def test_turned_boxes_are_hit_on_their_own_faces():
    # A 10 x 2 box turned 45 degrees: a ray along x from the left meets its long face, not its bounding box.
    obs = Obstacles(boxes=[(0, 0, 5, 1, np.pi / 4, 0, 3, "wall")])
    dist, kind = obs.cast([-10, 0, 1], [[1, 0, 0]], 50)
    assert dist[0] == pytest.approx(10 - np.sqrt(2)) and kind[0] == "wall"
    dist, _ = obs.cast([-10, 3.0, 1], [[1, 0, 0]], 50)  # inside the bounding box's reach, outside the box
    assert dist[0] == pytest.approx(10 + 3.0 - np.sqrt(2))
    assert obs.touching([3, 3, 1], 0.5) == "wall"
    assert obs.touching([3, -3, 1], 0.5) is None
    corners = obs.box_corners()[0]
    assert np.allclose(np.sort(np.linalg.norm(corners, axis=1)), np.sqrt(26))


def test_rays_and_spheres_meet_hilly_ground():
    obs = Obstacles(terrain=tilted(0.2))
    dist, kind = obs.cast([0, 0, 10], [[0, 0, -1], [1, 0, 0], [-1, 0, 0]], 200)
    assert dist[0] == pytest.approx(10, abs=0.01) and kind[0] == "ground"
    assert dist[1] == pytest.approx(50, abs=0.01) and kind[1] == "ground"  # the slope rises to meet it
    assert dist[2] == 200 and kind[2] == ""
    assert obs.touching([50, 0, 10.3], 0.5) == "ground"
    assert obs.touching([50, 0, 10.7], 0.5) is None
    assert obs.terrain.height(30, 7) == pytest.approx(6.0)


def test_grid_finds_the_same_hits_as_checking_everything():
    rng = np.random.default_rng(0)
    boxes = [(x, y, rng.uniform(0.5, 40), rng.uniform(0.5, 15), rng.uniform(0, np.pi), 0, rng.uniform(2, 30), "b")
             for x, y in rng.uniform(-400, 400, (200, 2))]
    cyls = [(x, y, rng.uniform(0.2, 4), 0, rng.uniform(3, 15), "c") for x, y in rng.uniform(-400, 400, (200, 2))]
    wires = [(*a, *(a + [rng.uniform(-40, 40), rng.uniform(-40, 40), 0]), 0.3, "w")
             for a in np.column_stack([rng.uniform(-400, 400, (100, 2)), rng.uniform(4, 12, 100)])]
    obs = Obstacles(boxes, cyls, wires)
    everything = np.arange(len(obs))
    for o in np.column_stack([rng.uniform(-300, 300, (20, 2)), rng.uniform(1, 40, 20)]):
        fast = obs.cast(o, sphere(64), 60)
        obs.near = lambda lo, hi: everything
        slow = obs.cast(o, sphere(64), 60)
        del obs.near
        assert np.allclose(fast[0], slow[0]) and (fast[1] == slow[1]).all()


def test_overhead_matches_a_ray_straight_up():
    obs = scene()
    pts = np.array([[0, 10, 0.5], [11, 0, 2], [11, 0, 6], [30, 30, 0]], float)
    up = np.array([obs.cast(p, [[0, 0, 1]], 100)[0][0] for p in pts])
    assert obs.overhead(pts) == pytest.approx(up)
    assert obs.overhead(pts) == pytest.approx([1.5, 0, 100, 100])


def test_touching_reports_what_a_sphere_overlaps():
    obs = scene()
    assert obs.touching([9.5, 0, 3], 0.6) == "house"
    assert obs.touching([9.0, 0, 3], 0.6) is None
    assert obs.touching([0, 11.3, 5], 0.4) == "canopy"
    assert obs.touching([0, -10, 6.4], 0.4) == "power_line"
    assert obs.touching([0, -10, 6.6], 0.4) is None
    assert obs.touching([30, 30, 0.2], 0.3) == "ground"


def test_airspace_heights_are_above_the_ground_and_hours_count():
    space = Airspace([
        {"kind": "school", "shape": "rect", "centre": (0, 0), "half": (20, 10), "yaw": np.pi / 2,
         "floor": 0, "ceiling": 60, "hours": (7.5, 16)},
        {"kind": "airport", "shape": "circle", "centre": (60, 0), "radius": 30, "floor": 30, "ceiling": UNLIMITED},
        {"kind": "stadium", "shape": "circle", "centre": (0, 80), "radius": 30, "floor": 0, "ceiling": 300,
         "active": False},
    ], tilted(0.1))
    pts = [[0, 15, 40], [15, 0, 40], [60, 0, 20], [60, 0, 50], [0, 80, 10]]  # the school is turned to run along y
    assert list(space.blocked(pts, hour=9)) == ["school", "", "", "airport", ""]
    assert list(space.blocked(pts, hour=20)) == ["", "", "", "airport", ""]
    assert space.blocked([[60, 0, 35]])[0] == ""  # ground is 6 m up here, so this is only 29 m above it
