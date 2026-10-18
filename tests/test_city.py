from collections import deque

import numpy as np
import pytest

from sim.city import SIDEWALK, STOREY, City


@pytest.fixture(scope="module")
def city():
    return City(seed=0)


def segments(city):
    a = np.vstack([s["points"][:-1] for s in city.streets])
    b = np.vstack([s["points"][1:] for s in city.streets])
    half = np.concatenate([np.full(len(s["points"]) - 1, s["width"] / 2) for s in city.streets])
    return a, b, half


def gap_to_streets(points, city):
    """For each point, the smallest distance to a street's kerb (negative means on the road)."""
    a, b, half = segments(city)
    ab = b - a
    t = np.clip(((points[:, None] - a) * ab).sum(-1) / (ab * ab).sum(-1), 0, 1)
    d = np.linalg.norm(a + t[..., None] * ab - points[:, None], axis=-1)
    return (d - half).min(1)


def test_same_seed_same_city_and_days_only_change_cranes():
    a, b = City(3), City(3)
    assert np.array_equal(a.spot_pos, b.spot_pos) and np.array_equal(a.obstacles.box_xy, b.obstacles.box_xy)
    assert not np.allclose(City(4).xs, a.xs)
    days = [City(3, day=d) for d in range(4)]
    assert all(np.array_equal(d.spot_pos, a.spot_pos) for d in days)  # same houses every day
    assert len({tuple(np.round([c["yaw"] for c in d.cranes], 6)) for d in days}) > 1  # cranes move


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


def test_centre_is_a_grid_and_the_rest_curves_with_cul_de_sacs(city):
    kinds = [s["kind"] for s in city.streets]
    assert kinds.count("culdesac") >= 10 and kinds.count("collector") >= 8
    for s in city.streets:
        d = np.diff(s["points"], axis=0)
        straight = np.allclose(d[:, 0], 0) or np.allclose(d[:, 1], 0)
        assert straight == (s["kind"] in ("arterial", "local", "access"))
    degree = np.bincount(city.edges.ravel(), minlength=len(city.nodes))
    assert (degree == 1).sum() == kinds.count("culdesac") + 1  # every cul-de-sac, plus the station gate


def test_buildings_stay_off_the_streets_and_apart(city):
    obs = city.obstacles
    built = np.flatnonzero(np.isin(obs.kind[:obs.nb], ["house", "apartment", "school", "hospital", "stadium"]))
    corners = obs.box_corners(built)
    pts = np.vstack([corners.reshape(-1, 2), obs.box_xy[built]])
    assert gap_to_streets(pts, city).min() > SIDEWALK - 1.0
    houses = np.flatnonzero(obs.kind[:obs.nb] == "house")
    hc = obs.box_corners(houses) * 0.999 + obs.box_xy[houses, None] * 0.001  # pull corners in a hair
    pts, owner = hc.reshape(-1, 2), np.repeat(houses, 4)
    rx, ry = pts[:, None, 0] - obs.box_xy[houses, 0], pts[:, None, 1] - obs.box_xy[houses, 1]
    lx, ly = obs._local(houses[None], rx, ry)
    inside = (np.abs(lx) < obs.box_half[houses, 0]) & (np.abs(ly) < obs.box_half[houses, 1])
    inside[np.arange(len(pts)), np.searchsorted(houses, owner)] = False
    assert not inside.any()


def test_everything_stands_on_the_ground(city):
    obs = city.obstacles
    houses = np.flatnonzero(obs.kind[:obs.nb] == "house")
    corners = obs.box_corners(houses)
    ground = city.terrain.height(corners[..., 0], corners[..., 1])
    assert (obs.box_z[houses, 0, None] <= ground).all() and (obs.box_z[houses, 1, None] > ground + 2).all()
    yard = city.spot_kind != "balcony"
    assert city.spot_pos[yard, 2] == pytest.approx(city.terrain.height(*city.spot_pos[yard, :2].T))
    relief = np.ptp(city.terrain.height(*np.meshgrid(np.linspace(0, city.width, 40), np.linspace(0, city.height, 30))))
    assert relief > 15  # it really is hilly


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
    assert len(city.bays) == 10 and (city.bays[:, 0] > city.obstacles.box_xy[city.station_building, 0]).all()


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


def test_tall_hazards_are_there_and_wired(city):
    obs = city.obstacles
    kinds = set(obs.kind)
    assert {"hv_line", "pylon", "cell_tower", "guy_wire", "power_line", "cable"} <= kinds
    hv = np.flatnonzero(obs.kind == "hv_line") - obs.nb - obs.nc
    assert (obs.wire_p[hv, 2] - city.terrain.height(*obs.wire_p[hv, :2].T) > 20).all()  # well above the houses
    houses = np.flatnonzero(obs.kind[:obs.nb] == "house")
    a, b = city.hv_line
    u = (b - a) / np.linalg.norm(b - a)
    off = obs.box_xy[houses] - a
    assert (np.abs(off[:, 0] * u[1] - off[:, 1] * u[0]) > 15).all()  # nobody lives under the line


def test_no_fly_zones_cover_their_sites(city):
    by_kind = {s["kind"]: s["centre"] for s in city.sites}
    school = np.append(by_kind["school"], city.terrain.height(*by_kind["school"]) + 30)
    hospital = np.append(by_kind["hospital"], city.terrain.height(*by_kind["hospital"]) + 100)
    assert city.airspace.blocked([school], hour=10)[0] == "school"
    assert city.airspace.blocked([school], hour=20)[0] == ""
    assert city.airspace.blocked([hospital], hour=3)[0] == "hospital"
    near_airfield = np.append(city.runway_centre + (-600, 0), 0.0)
    near_airfield[2] = city.terrain.height(*near_airfield[:2])
    assert city.airspace.blocked([near_airfield + [0, 0, 20]])[0] == ""
    assert city.airspace.blocked([near_airfield + [0, 0, 50]])[0] == "airport"
