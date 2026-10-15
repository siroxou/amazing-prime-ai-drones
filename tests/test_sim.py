import numpy as np
import pytest

from sim.traffic import Traffic
from sim.vehicle import Vehicle, collides
from sim.world import Road, raycast


def test_raycast_hits_wall_at_right_distance():
    p, q = np.array([[10.0, -5.0]]), np.array([[10.0, 5.0]])
    dist, idx = raycast(np.zeros(2), np.array([0.0, np.pi, np.pi / 4, np.arctan2(4, 10)]), 50, p, q)
    assert dist[0] == pytest.approx(10)
    assert dist[1] == 50 and idx[1] == -1  # facing away
    assert dist[2] == 50  # passes above the wall's end
    assert dist[3] == pytest.approx(np.hypot(10, 4))


def test_roads_never_double_back_and_coordinates_round_trip():
    for seed in range(20):
        road = Road(np.random.default_rng(seed), lanes=3, complexity=1.0)
        assert np.all(np.diff(road.pts[:, 0]) > 0)  # heading stays within +-80 deg, so x always grows
        s = np.array([10.0, road.length / 2, road.length - 10])
        x, y, _ = road.pose_at(s, 2.0)
        for i in range(3):
            _, s2, lat2 = road.project(np.array([x[i], y[i]]))
            assert s2 == pytest.approx(s[i], abs=0.1) and lat2 == pytest.approx(2.0, abs=0.1)


def test_truck_drives_straight_and_detects_contact():
    truck = Vehicle(0, 0, 0)
    for _ in range(50):
        truck.step([0.0, 1.0])
    assert truck.v > 0 and truck.x > 0 and truck.y == pytest.approx(0)
    assert collides(truck, np.array([truck.x + 3.0]), np.array([0.0]), np.array([0.0]))
    assert not collides(truck, np.array([truck.x + 10.0]), np.array([0.0]), np.array([0.0]))


def test_traffic_keeps_moving_and_never_hits_the_truck():
    road = Road(np.random.default_rng(1), lanes=2, complexity=0.5)
    traffic = Traffic(road, np.random.default_rng(1), density=0.2, parked=0.0)
    assert len(traffic) > 0
    for _ in range(300):  # truck parked at the start of lane 0
        traffic.step(5.0, road.lane_center(0), 0.0)
    assert len(traffic) > 0 and traffic.v.max() > 5
    x, y, yaw, _, _ = traffic.poses()
    tx, ty, tyaw = road.pose_at(5.0, road.lane_center(0))
    assert not collides(Vehicle(tx, ty, tyaw), x, y, yaw)
