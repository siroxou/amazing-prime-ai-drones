import numpy as np
import pytest

from sim import drone
from sim.city import City
from sim.day import Day


@pytest.fixture(scope="module")
def day():
    return Day(City(seed=0), parcels=200)


def windy(day, monkeypatch, speed, towards=0.0, gust=None):
    w = {k: v.copy() for k, v in day.weather.items()}
    w["wind"][:], w["wind_dir"][:] = speed, towards
    w["gust"][:] = speed if gust is None else gust
    w["rain_mm_h"][:], w["temp_c"][:] = 0.0, 20.0
    monkeypatch.setattr(day, "weather", w)


def test_power_grows_with_payload_drag_and_climb():
    assert drone.power(5.0) > drone.power(2.0) > drone.power(0.0) > drone.AVIONICS
    assert drone.power(2.0, 0.2, 15) > drone.power(2.0, 0.0, 15)  # a bigger box is harder to push
    extra = drone.power(2.0, 0, 0, drone.CLIMB) - drone.power(2.0)
    assert extra == pytest.approx((drone.MASS + 2.0) * drone.G * drone.CLIMB / drone.EFFICIENCY, rel=0.01)
    # induced power falls with speed, so cruising empty costs about what hovering does
    assert 0.8 < drone.power(0, 0, drone.AIRSPEED) / drone.power() < 1.3


def test_battery_holds_less_in_the_cold():
    assert drone.usable_wh(25) == drone.usable_wh(20) > drone.usable_wh(0) > drone.usable_wh(-10)


def test_wind_changes_ground_speed():
    east = np.array([1.0, 0.0])
    assert drone.ground_speed(np.array([5.0, 0.0]), east) == pytest.approx(drone.AIRSPEED + 5)
    assert drone.ground_speed(np.array([-5.0, 0.0]), east) == pytest.approx(drone.AIRSPEED - 5)
    assert drone.ground_speed(np.array([0.0, 5.0]), east) == pytest.approx(np.sqrt(drone.AIRSPEED ** 2 - 25))
    assert drone.ground_speed(np.array([0.0, 20.0]), east) is None


def test_flight_heights_clear_everything_and_respect_airspace(day):
    city = day.city
    checked = 0
    for a, b in ((np.array([100.0, 100.0]), np.array([city.width * 0.5, city.height * 0.5])),
                 (np.array([city.width * 0.5, city.height * 0.5]), np.array([city.width * 0.2, city.height * 0.8])),
                 (np.array([city.width * 0.3, city.height * 0.1]), np.array([city.width * 0.5, city.height * 0.3]))):
        shape = drone.profile(city, a, b, 10.0)
        if shape is None:
            continue
        checked += 1
        pts, z = shape
        ground = city.terrain.height(*pts.T)
        assert (z >= ground + drone.LOW_HEIGHT - 1e-6).all()
        assert (z >= drone.tallest(city, pts) + drone.CLEARANCE - 1e-6).all()
        assert (np.abs(np.diff(z)) <= drone.GRADE * np.linalg.norm(b - a) / (len(z) - 1) + 1e-6).all()
        sky = city.airspace
        inside = sky.inside(pts) & sky.on(10.0)
        for k in np.flatnonzero(inside.any(0)):
            agl = (z - ground)[inside[:, k]]
            if sky.floor[k] >= drone.LOW_HEIGHT:
                assert (agl < sky.floor[k]).all()  # under the airfield's limit
            elif sky.ceiling[k] < drone.MAX_HEIGHT - drone.CLEARANCE:
                assert (agl > sky.ceiling[k]).all()  # over the school
    assert checked >= 2


def test_a_leg_that_needs_to_be_higher_than_the_airfield_allows_cant_be_flown(day):
    city = day.city
    sky = city.airspace
    airfield = int(np.flatnonzero(sky.kind == "airport")[0])
    a = np.array([city.width - 50.0, city.height / 2])  # inside the airfield's 30 m limit
    assert sky.inside([a])[0, airfield]
    tall = drone.tallest(city, [a])[0] - city.terrain.height(*a)
    assert drone.profile(city, a, a + [1.0, 0.0], 10.0) is not None or tall + drone.CLEARANCE >= sky.floor[airfield] - 1


def test_headwind_costs_time_and_battery(day, monkeypatch):
    city = day.city
    a = np.array([city.width * 0.3, city.height * 0.2])
    b = a + [500.0, 0.0]
    z = city.terrain.height(*a) + drone.ROOF
    windy(day, monkeypatch, 8.0, towards=0.0)  # blowing east, the way it's going
    tail = drone.leg(day, a, b, 12.0, z, z, payload=2.0, frontal=0.06)
    windy(day, monkeypatch, 8.0, towards=np.pi)
    head = drone.leg(day, a, b, 12.0, z, z, payload=2.0, frontal=0.06)
    assert head["seconds"] > tail["seconds"] and head["wh"] > tail["wh"]
    assert head["distance"] == pytest.approx(tail["distance"])


def test_drop_planning_follows_fragility_and_gusts(day, monkeypatch):
    windy(day, monkeypatch, 2.0)
    calm = [drone.drop_options(day, i, 12.0) for i in range(len(day.parcel_address))]
    windy(day, monkeypatch, 10.0, gust=14.0)
    gusty = [drone.drop_options(day, i, 12.0) for i in range(len(day.parcel_address))]
    assert sum(map(len, gusty)) < sum(map(len, calm))
    for i, options in enumerate(calm):
        for _, s, mode, height in options:
            if day.parcel_fragility[i] == "fragile":
                assert mode != "drop"
            if day.city.spot_kind[s] == "balcony":
                assert mode == "lower"
            if mode == "drop":
                assert height == drone.DROP_FROM[str(day.parcel_fragility[i])]


def test_a_flight_the_battery_cant_manage_isnt_made(day, monkeypatch):
    windy(day, monkeypatch, 2.0)
    city = day.city
    i = next(i for i in range(len(day.parcel_address)) if drone.drop_options(day, i, 12.0))
    start = city.address_street[day.parcel_address[i]]
    trip = drone.sortie(day, start, i, 12.0)
    assert trip is not None and 0 < trip["wh"] <= drone.usable_wh(20.0)
    assert trip["to_drop"] < trip["seconds"]
    monkeypatch.setattr(drone, "BATTERY", trip["wh"] / (1 - drone.RESERVE) * 0.5)
    assert drone.sortie(day, start, i, 12.0) is None
