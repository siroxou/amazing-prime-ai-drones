import json

import numpy as np
import pytest

from render3d import scene
from render3d.__main__ import SHOTS, settle
from sim.city import City
from sim.day import Day


@pytest.fixture(scope="module")
def data():
    return scene.export(Day(City(seed=0), parcels=200), seconds=1)


def test_every_delivery_shows_up_once(data):
    delivered = sum(t is not None for t in data["parcels"]["t"])
    parcels = [f["parcel"] for f in data["flights"]] + [w["parcel"] for w in data["walkers"]]
    assert len(parcels) == len(set(parcels)) == delivered
    assert json.loads(json.dumps(data)) == data  # plain data the page can read


def test_drives_and_flights_run_forwards_in_time(data):
    for leg in data["legs"]:
        assert leg["t0"] <= leg["t1"] + 1e-9
        assert len(leg["xy"]) >= 1
    for f in data["flights"]:
        assert f["t0"] < f["t1"] <= f["t2"]
        assert f["mode"] in ("drop", "lower", "set")
        assert f["path"][-1][2] >= f["spot"][2]  # the drone ends up above the spot it puts the parcel on
    for w in data["walkers"]:
        assert w["t0"] <= w["t1"]


def test_city_shots_aim_at_what_they_show(data):
    centre = settle("centre", SHOTS["centre"]["shot"], data)
    flats = [(x, y) for k, x, y in zip(data["city"]["boxes"]["kind"], data["city"]["boxes"]["x"], data["city"]["boxes"]["y"])
             if k == "apartment"]
    assert np.allclose(centre["target"], np.mean(flats, 0))
