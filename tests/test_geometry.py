import numpy as np
import pytest

from sim.geometry import Obstacles, sphere


def scene():
    return Obstacles(
        boxes=[(10, -2, 0, 12, 2, 5, "house")],
        cylinders=[(0, 10, 1.0, 2, 8, "canopy")],
        wires=[(-5, -10, 6, 5, -10, 6, 0.05, "power_line")],
    )


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


def test_grid_finds_the_same_hits_as_checking_everything():
    rng = np.random.default_rng(0)
    boxes = [(x, y, 0, x + rng.uniform(1, 80), y + rng.uniform(1, 30), rng.uniform(2, 30), "b")
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


def test_touching_reports_what_a_sphere_overlaps():
    obs = scene()
    assert obs.touching([9.5, 0, 3], 0.6) == "house"
    assert obs.touching([9.0, 0, 3], 0.6) is None
    assert obs.touching([0, 11.3, 5], 0.4) == "canopy"
    assert obs.touching([0, -10, 6.4], 0.4) == "power_line"
    assert obs.touching([0, -10, 6.6], 0.4) is None
    assert obs.touching([30, 30, 0.2], 0.3) == "ground"
