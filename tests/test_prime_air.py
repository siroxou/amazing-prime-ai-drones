import numpy as np
import pytest

from baselines import prime_air as pa
from sim.city import City
from sim.day import Day


@pytest.fixture(scope="module")
def city():
    return City(seed=0)


@pytest.fixture(scope="module")
def day(city):
    return Day(city, parcels=200)


def calm(day, monkeypatch):
    """No wind, no rain, all day."""
    w = {k: v.copy() for k, v in day.weather.items()}
    w["wind"][:], w["gust"][:], w["rain_mm_h"][:] = 0.0, 0.0, 0.0
    monkeypatch.setattr(day, "weather", w)


def test_drop_spots_are_open_yards_at_houses(city):
    spots = pa.drop_spots(city)
    has = spots >= 0
    assert (city.address_kind[has] == "house").all()
    assert np.isin(city.spot_kind[spots[has]], ["front_yard", "back_yard"]).all()
    assert (city.spot_overhead[spots[has]] >= 100).all()
    assert 0.3 < has[city.address_kind == "house"].mean() < 1.0  # trees and sheds rule some yards out


def test_paths_go_round_walls_but_not_into_them(city):
    hospital = next(s["centre"] for s in city.sites if s["kind"] == "hospital")
    a, b = hospital + [-400.0, 5.0], hospital + [400.0, 5.0]
    assert pa.path_length(city, a, b, 10.0) > np.linalg.norm(b - a) + 10  # the helipad zone is in the way
    assert pa.path_length(city, a, a + [0, -400.0], 10.0) == pytest.approx(400.0)
    assert pa.path_length(city, a, hospital, 10.0) is None


def test_headwind_slows_one_way_and_speeds_the_other(day, monkeypatch):
    calm(day, monkeypatch)
    site = day.city.station_centre
    assert pa.ground_speeds(day, site, np.array([1.0, 0.0]), 12.0) == pytest.approx((pa.CRUISE_SPEED,) * 2)
    w = dict(day.weather)
    w["wind"] = np.full(25, 8.0)
    w["wind_dir"] = np.zeros(25)  # blowing along +x
    monkeypatch.setattr(day, "weather", w)
    out, back = pa.ground_speeds(day, site, np.array([1.0, 0.0]), 12.0)
    assert out > pa.CRUISE_SPEED > back


def test_drones_take_light_parcels_to_yards_and_vans_take_the_rest(day, monkeypatch):
    calm(day, monkeypatch)
    times, reason, sorties, hours = pa.schedule(day, drones=10)
    flown = ~np.isnan(times)
    assert sorties == flown.sum() > 0 and hours > 0
    assert (day.parcel_weight[flown] <= pa.PAYLOAD).all() and np.isin(day.parcel_size[flown], pa.SIZES).all()
    assert (day.city.address_kind[day.parcel_address[flown]] == "house").all()
    assert ((times[flown] > pa.OPEN) & (times[flown] < pa.CLOSE)).all()
    assert (reason[flown] == "").all() and (reason[~flown] != "").all()
    assert set(reason[day.parcel_weight > pa.PAYLOAD]) == {"too heavy"}
    r = pa.baseline(day, drones=10, seconds=1)
    assert r["undelivered"] == 0 and r["by_drone"] == pytest.approx(flown.mean())


def test_more_drones_get_parcels_out_sooner(day, monkeypatch):
    calm(day, monkeypatch)
    few, _, _, _ = pa.schedule(day, drones=2)
    many, _, _, _ = pa.schedule(day, drones=20)
    assert np.nanmean(many) < np.nanmean(few)


def test_drones_stay_grounded_in_heavy_rain(day, monkeypatch):
    w = {k: v.copy() for k, v in day.weather.items()}
    w["rain_mm_h"][:] = 10.0
    monkeypatch.setattr(day, "weather", w)
    times, reason, sorties, _ = pa.schedule(day, drones=10)
    assert sorties == 0 and "weather" in set(reason)
