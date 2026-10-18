from collections import deque

import numpy as np
import pytest

from sim.city import STOREY, City


@pytest.fixture(scope="module")
def city():
    return City(seed=0)


def test_same_seed_same_city():
    a, b = City(3), City(3)
    assert np.array_equal(a.spot_pos, b.spot_pos) and np.array_equal(a.obstacles.lo, b.obstacles.lo)
    assert not np.allclose(City(4).xs, a.xs)


def test_houses_sit_in_zones_inside_zip_codes(city):
    assert len(city.zip_codes) == 9 and len(city.zone_bounds) == 36
    assert np.array_equal(city.zone_zip[city.address_zone], city.address_zip)
    for zone, zip_ in enumerate(city.zone_zip):
        zx0, zy0, zx1, zy1 = city.zone_bounds[zone]
        px0, py0, px1, py1 = city.zip_bounds[zip_]
        assert px0 <= zx0 < zx1 <= px1 and py0 <= zy0 < zy1 <= py1
    assert set(city.address_zone) == set(range(len(city.zone_bounds)))  # every zone has addresses
    door = city.address_door
    x0, y0, x1, y1 = city.zone_bounds[city.address_zone].T
    assert ((door[:, 0] >= x0) & (door[:, 0] <= x1) & (door[:, 1] >= y0) & (door[:, 1] <= y1)).all()


def test_buildings_stay_off_the_streets_and_apart(city):
    obs = city.obstacles
    built = np.flatnonzero(np.isin(obs.kind[:obs.nb], ["house", "apartment", "balcony", "railing", "fence"]))
    centre = (obs.lo[built, :2] + obs.hi[built, :2]) / 2
    b = (np.searchsorted(city.ys, centre[:, 1]) - 1) * city.blocks + np.searchsorted(city.xs, centre[:, 0]) - 1
    x0, y0, x1, y1 = city.block_bounds[b].T
    lo, hi = obs.lo[built], obs.hi[built]
    tol = 1e-9
    assert ((lo[:, 0] >= x0 - tol) & (hi[:, 0] <= x1 + tol) & (lo[:, 1] >= y0 - tol) & (hi[:, 1] <= y1 + tol)).all()
    houses = np.flatnonzero(obs.kind[:obs.nb] == "house")
    l, h = obs.lo[houses, :2], obs.hi[houses, :2]
    overlap = ((l[:, None] < h[None]) & (h[:, None] > l[None])).all(-1)
    np.fill_diagonal(overlap, False)
    assert not overlap.any()


def test_trucks_can_drive_from_the_distribution_centre_to_every_junction(city):
    links = {i: [] for i in range(len(city.nodes))}
    for a, b in city.edges:
        links[a].append(b)
        links[b].append(a)
    seen, todo = {city.station_node}, deque([city.station_node])
    while todo:
        for nxt in links[todo.popleft()]:
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    assert len(seen) == len(city.nodes)
    assert len(city.bays) == 10 and (city.bays[:, 0] > city.obstacles.hi[city.station_building, 0]).all()


def test_drop_spots_have_room_for_a_parcel(city):
    for pos in city.spot_pos:
        assert city.obstacles.touching(pos + [0, 0, 0.35], 0.3) is None


def test_balconies_are_covered_except_on_the_top_floor(city):
    balcony = city.spot_kind == "balcony"
    addr = city.spot_address[balcony]
    top = np.zeros(city.address_building.max() + 1, int)
    np.maximum.at(top, city.address_building, city.address_floor)
    is_top = city.address_floor[addr] == top[city.address_building[addr]]
    overhead = city.spot_overhead[balcony]
    assert overhead[~is_top] == pytest.approx(STOREY - 0.2 - 0.1)  # slab above, measured from 0.1 m up
    assert (overhead[is_top] == 100).all()


def test_some_yards_are_under_trees(city):
    yard = np.isin(city.spot_kind, ["front_yard", "back_yard"])
    covered = (city.spot_overhead[yard] < 100).mean()
    assert 0.02 < covered < 0.5
