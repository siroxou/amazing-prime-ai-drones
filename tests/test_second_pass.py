import numpy as np
import pytest

from baselines import classical as cl
from baselines import dsp
from sim.city import City
from sim.day import Day


@pytest.fixture(scope="module")
def solved():
    day = Day(City(seed=0), parcels=200)
    return day, cl.solve(day, seconds=1, second=False), cl.solve(day, seconds=1)


def test_second_notices_are_fresh_but_repeatable(solved):
    day, _, _ = solved
    again = day.second_reply()
    assert np.array_equal(again, day.second_reply())
    assert not np.allclose(again, day.recipient_reply)
    for a in np.unique(day.parcel_address)[:20]:  # one person per address
        assert np.ptp(again[day.parcel_address == a]) == 0


def test_second_pass_only_adds_deliveries_later_in_the_day(solved):
    day, morning, both = solved
    plan = morning["plan"]
    t = morning["parcel_time"]
    after, added = cl.second_pass(day, cl.trucks_of(plan), t)
    done_before = ~np.isnan(t)
    assert np.array_equal(after[done_before], t[done_before])  # nothing delivered in the morning moves
    new = np.isnan(t) & ~np.isnan(after)
    assert new.any() and added["hours"] > 0
    earliest = min(back for back, _ in cl.trucks_of(plan)) + cl.RELOAD
    assert (after[new] > earliest).all() and (after[new] <= dsp.SHIFT_START + dsp.SHIFT).all()
    carried = np.concatenate([p for _, p in cl.trucks_of(plan)])
    assert np.isin(np.flatnonzero(new), carried).all()  # only parcels a truck had on board


def test_solve_with_second_pass_delivers_more(solved):
    _, morning, both = solved
    assert both["undelivered"] < morning["undelivered"]
    assert both["second_pass"] == morning["undelivered"] - both["undelivered"]
    assert both["truck_hours"] > morning["truck_hours"]


def test_no_second_pass_when_the_shift_is_over(solved):
    day, morning, _ = solved
    late = [(dsp.SHIFT_START + dsp.SHIFT - 0.2, parcels) for _, parcels in cl.trucks_of(morning["plan"])]
    after, added = cl.second_pass(day, late, morning["parcel_time"])
    assert np.array_equal(np.isnan(after), np.isnan(morning["parcel_time"])) and added["hours"] == 0


def test_recipients_who_dont_come_back_leave_only_the_drones(solved, monkeypatch):
    day, morning, both = solved
    assert np.isinf(day.second_reply(show=0.0)).all()
    assert np.array_equal(day.second_reply(show=1.0), day.second_reply())
    monkeypatch.setattr(day, "second_reply", lambda: np.full(len(day.parcel_address), np.inf))
    after, added = cl.second_pass(day, cl.trucks_of(morning["plan"]), morning["parcel_time"])
    assert (~np.isnan(after)).sum() - (~np.isnan(morning["parcel_time"])).sum() == added["by_drone"]
    assert added["by_drone"] <= both["second_pass"]
