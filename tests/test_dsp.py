import numpy as np
import pytest

from baselines import dsp
from baselines.calibrate import Area
from sim.city import ARTERIAL_SPEED, City
from sim.day import Day
from sim.roads import drive_times, nearest_nodes


@pytest.fixture(scope="module")
def city():
    return City(seed=0)


@pytest.fixture(scope="module")
def day(city):
    return Day(city, parcels=150)


def test_drive_times_are_shortest_paths(city):
    nodes = np.r_[city.station_node, nearest_nodes(city, city.address_street[:40])]
    t = drive_times(city, city.edge_length / city.edge_speed, nodes)
    assert np.allclose(t, t.T) and np.allclose(np.diag(t), 0)
    crow = np.linalg.norm(city.nodes[nodes][:, None] - city.nodes[nodes][None], axis=-1)
    assert (t >= crow / ARTERIAL_SPEED - 1e-6).all()  # can't beat a straight line at the top speed
    via = t[:, :1] + t[:1, :]  # going through the station is never quicker
    assert (t <= via + 1e-6).all()


def test_stops_are_buildings(city, day):
    addresses, packages = np.unique(day.parcel_address, return_counts=True)
    rep, nodes, per_stop, which = dsp.stops(city, addresses, packages)
    assert per_stop.sum() == len(day.parcel_address)
    assert len(rep) == len(np.unique(city.address_building[addresses])) <= len(addresses)
    assert np.array_equal(city.address_building[rep][which], city.address_building[addresses])


def test_planned_routes_cover_every_stop_once_and_fit_the_shift(city, day):
    addresses, packages = np.unique(day.parcel_address, return_counts=True)
    _, nodes, per_stop, _ = dsp.stops(city, addresses, packages)
    shift = dsp.Shift(day, nodes)
    svc = dsp.service_times(per_stop)
    routes = dsp.plan(shift, svc, 2, seconds=1)
    assert sorted(j for r in routes for j in r) == list(range(1, len(nodes) + 1))
    for r in routes:
        legs = [0, *r, 0]
        planned = sum(shift.mean[a, b] + svc[b] for a, b in zip(legs[:-1], legs[1:]))
        assert planned <= (dsp.SHIFT - dsp.LOADOUT) * 3600 + len(legs)  # rounding to whole seconds
        done, back, metres = dsp.drive(shift, r, svc)
        times = [done[j] for j in r if j in done]
        assert times == sorted(times) and times[0] > dsp.SHIFT_START + dsp.LOADOUT
        assert back <= dsp.SHIFT_START + dsp.SHIFT + 1e-9 and metres > 0


def test_a_van_skips_stops_it_cant_fit_and_still_gets_back(city, day):
    addresses, packages = np.unique(day.parcel_address, return_counts=True)
    _, nodes, per_stop, _ = dsp.stops(city, addresses, packages)
    shift = dsp.Shift(day, nodes)
    slow = dsp.service_times(per_stop, service=3600.0)  # an hour a stop
    done, back, _ = dsp.drive(shift, list(range(1, len(nodes) + 1)), slow)
    assert 0 < len(done) <= 9 and back <= dsp.SHIFT_START + dsp.SHIFT + 1e-9


def test_baseline_delivers_the_day_within_the_shift(day):
    r = dsp.baseline(day, seconds=1)
    t = r["parcel_time"]
    assert len(t) == len(day.parcel_address) and r["undelivered"] == np.isnan(t).sum()
    ok = t[~np.isnan(t)]
    assert (ok > dsp.SHIFT_START + dsp.LOADOUT).all() and (ok <= dsp.SHIFT_START + dsp.SHIFT).all()
    assert r["vans"] >= 1 and sum(r["packages"]) == len(day.parcel_address) and r["km"] > 0
    assert r["driver_hours"] <= r["vans"] * dsp.SHIFT


def test_longer_stops_mean_fewer_stops_per_route(city, monkeypatch):
    import baselines.calibrate as cal
    monkeypatch.setattr(cal, "SOLVER_SECONDS", 1)
    area = Area(city, "suburb", 0.3, seed=1)
    quick, slow = area.route(60.0), area.route(400.0)
    assert slow[0] < quick[0] and slow[1] < quick[1]
