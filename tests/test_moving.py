import numpy as np
import pytest

from baselines import classical as cl
from baselines import dsp, moving
from sim import drone
from sim.city import City
from sim.day import Day


@pytest.fixture(scope="module")
def calm_day():
    day = Day(City(seed=0), parcels=200)
    w = {k: v.copy() for k, v in day.weather.items()}
    w["wind"][:], w["gust"][:], w["rain_mm_h"][:] = 0.0, 0.0, 0.0
    day.weather = w
    return day


@pytest.fixture(scope="module")
def flown(calm_day):
    city = calm_day.city
    spot = cl.drop_spots(calm_day)
    target = city.spot_pos[np.maximum(spot, 0), :2]
    fly = spot >= 0
    plan = cl._plan(calm_day, fly, target, cl.LAUNCH_RADIUS, cl.WINDOW, 1, parked=False)
    drop, failed, extra = moving.fly(calm_day, plan, spot, target)
    return plan, target, drop, failed, extra


def position(trajectory, t):
    times, places = trajectory
    return np.array([np.interp(t, times, places[:, 0]), np.interp(t, times, places[:, 1])])


def test_the_truck_drives_its_route_on_the_roads(calm_day, flown):
    plan, *_ = flown
    nodes = calm_day.city.nodes
    for (times, places), route in zip(plan["trajectories"], plan["routes"]):
        assert (np.diff(times) >= -1e-12).all()
        assert times[0] == pytest.approx(dsp.SHIFT_START + dsp.LOADOUT)
        station = nodes[plan["shift"].nodes[0]]
        assert np.allclose(places[0], station) and np.allclose(places[-1], station)
        for j in route:  # passes through every stop it plans to
            assert (np.linalg.norm(places - nodes[plan["shift"].nodes[j]], axis=1) < 1e-6).any()
        hops = np.linalg.norm(np.diff(places, axis=0), axis=1)
        assert hops.max() < 300  # one road edge at a time, not straight lines across the city


def test_drones_meet_the_truck_within_range_and_battery(flown):
    plan, target, drop, failed, _ = flown
    assert len(plan["flights"]) == (~failed).sum() > 20
    moving_launches = 0
    for parcel, route, launch, at, land in plan["flights"]:
        traj = plan["trajectories"][route]
        start, end = position(traj, launch), position(traj, land)
        out = np.linalg.norm(target[parcel] - start)
        assert out <= cl.RANGE + 1e-6
        assert launch < at < land <= dsp.SHIFT_START + dsp.SHIFT + 1e-9
        assert (land - launch) * 60 <= moving.ENDURANCE + 1e-6
        # it can get from the drop to where the truck is when it lands, even in still air
        back = (land - at) * 3600
        assert np.linalg.norm(target[parcel] - end) <= drone.AIRSPEED * back + drone.AIRSPEED * moving.TICK + 1e-6
        moving_launches += not np.allclose(start, position(traj, launch + 10 / 3600))
    assert moving_launches > 0  # some take off while the truck is driving


def test_each_drone_flies_one_parcel_at_a_time(flown):
    plan, *_ = flown
    for r in range(len(plan["routes"])):
        mine = sorted((launch, land) for _, route, launch, _, land in plan["flights"] if route == r)
        busy = np.zeros(cl.DRONES)
        for launch, land in mine:
            k = int(np.argmin(busy))
            assert launch >= busy[k] - 1e-9  # some drone is free by then
            busy[k] = land + cl.TURNAROUND / 3600


def test_moving_launches_keep_the_trucks_no_longer_and_deliver_as_much(calm_day):
    # Not that they're faster: with real flight times they can be slower per parcel (see results/moving-launch.md).
    parked = cl.solve(calm_day, seconds=1)
    on_the_move = cl.solve(calm_day, seconds=1, moving=True)
    assert on_the_move["truck_hours"] <= parked["truck_hours"] + 0.25
    delivered = [np.mean(~np.isnan(r["parcel_time"])) for r in (parked, on_the_move)]
    assert delivered[1] >= delivered[0] - 0.02
