import numpy as np
import pytest

from baselines import classical as cl
from baselines import dsp
from sim.city import City
from sim.day import Day


@pytest.fixture(scope="module")
def day():
    return Day(City(seed=0), parcels=200)


def calm(day, monkeypatch):
    w = {k: v.copy() for k, v in day.weather.items()}
    w["wind"][:], w["gust"][:], w["rain_mm_h"][:] = 0.0, 0.0, 0.0
    monkeypatch.setattr(day, "weather", w)


def test_drop_spots_need_open_sky(day):
    city = day.city
    spots = cl.drone_spots(city)
    has = spots >= 0
    assert (city.spot_overhead[spots[has]] >= 100).all()
    assert (city.spot_address[spots[has]] == np.flatnonzero(has)).all()
    flats = has & (city.address_kind == "apartment")
    assert flats.any() and (city.spot_kind[spots[flats]] == "balcony").all()  # top floors only
    assert not (has & (city.address_kind == "apartment") & (city.address_floor < 3)).all()


def test_sorties_are_shared_out_longest_first():
    cycles = np.array([100.0, 400.0, 300.0, 200.0])
    start, busy = cl.share_out(cycles, drones=2)
    assert busy == pytest.approx(500 - cl.TURNAROUND)  # 400 + 100 on one drone, 300 + 200 on the other
    assert start[1] == 0 and start[2] == 0 and sorted(start[[0, 3]]) == [300.0, 400.0]
    assert cl.share_out(np.zeros(0))[1] == 0


def test_every_drone_parcel_has_a_stop_within_range(day):
    city = day.city
    targets = city.address_door[day.parcel_address[:80], :2]
    base = city.station_node + np.zeros(0, int)
    nodes, stop = cl.launch_stops(city, targets, base, 400.0)
    assert len(stop) == 80 and stop.max() < len(nodes)
    assert (np.linalg.norm(targets - city.nodes[nodes[stop]], axis=1) <= 400.0 + 1e-9).mean() > 0.95


def test_a_calm_day_goes_mostly_by_drone_and_early(day, monkeypatch):
    calm(day, monkeypatch)
    r = cl.solve(day, seconds=1)
    t = r["parcel_time"]
    ok = ~np.isnan(t)
    assert r["by_drone"] > 0.3 and ok.mean() > 0.8
    assert (t[ok] > dsp.SHIFT_START + dsp.LOADOUT).all() and (t[ok] <= dsp.SHIFT_START + dsp.SHIFT).all()
    heavy = day.parcel_weight > cl.PAYLOAD
    assert r["undelivered"] == (~ok).sum() and heavy.any()


def test_a_grounded_day_falls_back_to_the_locker(day, monkeypatch):
    w = {k: v.copy() for k, v in day.weather.items()}
    w["rain_mm_h"][:] = 10.0
    monkeypatch.setattr(day, "weather", w)
    r = cl.solve(day, seconds=1)
    assert r["by_drone"] == 0 and r["replanned"] == 1
    assert np.mean(~np.isnan(r["parcel_time"])) > 0.5  # people still collect from the lockers
