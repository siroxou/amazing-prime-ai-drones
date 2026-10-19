import numpy as np
import pytest

from baselines import dsp
from baselines import trucks_only as to
from sim.city import City
from sim.day import Day


@pytest.fixture(scope="module")
def day():
    return Day(City(seed=0), parcels=200)


def test_every_recipient_gets_a_point_they_would_walk_to(day):
    nodes, point, distance = to.pickup_points(day.city, day)
    covered = point >= 0
    assert covered.mean() > 0.95
    assert (distance[covered] <= day.recipient_walk[covered] + 1e-9).all()
    assert len(np.unique(nodes)) == len(nodes) < len(np.unique(day.parcel_address))  # points are shared
    door = day.city.address_door[day.parcel_address[covered], :2]
    crow = np.linalg.norm(door - day.city.nodes[nodes[point[covered]]], axis=1)
    assert distance[covered] == pytest.approx(to.WALK_DETOUR * crow)


def test_lockers_limit_what_each_truck_carries(day, monkeypatch):
    monkeypatch.setattr(to, "LOCKER", 60)
    r = to.baseline(day, seconds=1)
    assert r["trucks"] >= int(np.ceil(len(day.parcel_address) / 60))


def test_collections_happen_while_the_truck_waits(day):
    r = to.baseline(day, seconds=1)
    t = r["parcel_time"]
    ok = ~np.isnan(t)
    assert ok.any() and (t[ok] > dsp.SHIFT_START + dsp.LOADOUT).all() and (t[ok] <= dsp.SHIFT_START + dsp.SHIFT).all()
    assert r["uncollected"] == (~ok).sum() and r["no_point"] <= r["uncollected"]
    slow = day.recipient_reply > to.NOTICE + to.WINDOW  # they can't make it even with no walk
    assert np.isnan(t[slow]).all()


def test_a_longer_wait_collects_more(day):
    short, long = to.baseline(day, window=5.0, seconds=1), to.baseline(day, window=30.0, seconds=1)
    assert long["uncollected"] < short["uncollected"]
    assert long["truck_hours"] > short["truck_hours"]


def test_half_counts_uncollected_parcels_as_never():
    assert to.half(np.array([10.0, 11.0, np.nan, np.nan, np.nan])) == np.inf
    assert to.half(np.array([10.0, 11.0, 12.0, np.nan])) == 12.0
    assert to.half(np.array([10.0, 11.0, 12.0])) == 11.0
