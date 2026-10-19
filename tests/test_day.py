from pathlib import Path

import numpy as np
import pytest

from sim.city import City
from sim.day import FRAGILITY, HELD_OUT, SIZES, Day, _weather


@pytest.fixture(scope="module")
def city():
    return City(seed=0)


@pytest.fixture(scope="module")
def day(city):
    return Day(city, parcels=2000)


def test_same_seed_and_day_give_the_same_parcels_and_weather(city):
    a, b = Day(city, 300), Day(city, 300)
    assert np.array_equal(a.parcel_address, b.parcel_address) and np.array_equal(a.parcel_weight, b.parcel_weight)
    assert np.array_equal(a.weather["wind"], b.weather["wind"]) and np.array_equal(a.busy, b.busy)
    other = Day(City(0, day=1), 300)
    assert not np.array_equal(other.parcel_address, a.parcel_address)
    assert not np.allclose(other.weather["temp_c"], a.weather["temp_c"])
    assert np.array_equal(other.busy, a.busy)  # how busy each street is belongs to the city


def test_parcels_go_to_real_addresses_a_few_per_stop(city, day):
    assert len(day.parcel_address) == 2000
    assert day.parcel_address.min() >= 0 and day.parcel_address.max() < len(city.address_kind)
    per_stop = len(day.parcel_address) / len(np.unique(day.parcel_address))
    assert 1.3 < per_stop < 1.6  # DSP routes: 200-300 packages over 150-190 stops
    with pytest.raises(ValueError):
        Day(city, parcels=10 * len(city.address_kind))


def test_parcel_sizes_weights_and_fragility(day):
    assert set(day.parcel_size) == set(SIZES) and set(day.parcel_fragility) == set(FRAGILITY)
    assert 0.75 < (day.parcel_weight <= 2.27).mean() < 0.9  # Amazon's 2013 estimate: 86% under 5 lb
    assert (day.parcel_weight > 0).all() and day.parcel_weight.max() <= 30
    envelope, large = day.parcel_size == "envelope", day.parcel_size == "large"
    assert np.median(day.parcel_weight[envelope]) < np.median(day.parcel_weight[large])
    assert (day.parcel_dims[envelope].prod(1).max() < day.parcel_dims[large].prod(1).min())


def test_everyone_at_an_address_is_the_same_recipient(day):
    for a in np.unique(day.parcel_address)[:50]:
        same = day.parcel_address == a
        assert np.ptp(day.recipient_walk[same]) == 0 and np.ptp(day.recipient_reply[same]) == 0
    assert (day.recipient_walk > 0).all() and day.recipient_walk.max() <= 800


def test_weather_is_hourly_and_sensible_on_many_days():
    days = [_weather(np.random.default_rng(d)) for d in range(200)]
    assert 0.15 < np.mean([w["rain_mm_h"].sum() > 0 for w in days]) < 0.45
    for w in days:
        assert len(w["hour"]) == 25
        assert (-30 < w["temp_c"]).all() and (w["temp_c"] < 45).all()
        assert (w["wind"] >= 0).all() and (w["gust"] >= w["wind"]).all() and (w["rain_mm_h"] >= 0).all()


def test_weather_between_hours_and_wind_with_height(city, day):
    w = day.weather
    mid = day.weather_at(10.5)
    assert mid["temp_c"] == pytest.approx((w["temp_c"][10] + w["temp_c"][11]) / 2)
    x, y = city.address_door[0, :2]
    g = city.terrain.height(x, y)
    low, high = day.wind_at([[x, y, g + 10], [x, y, g + 40]], 10.5)
    assert np.linalg.norm(low) == pytest.approx(mid["wind"])
    assert np.linalg.norm(high) > np.linalg.norm(low)


def test_rush_hour_slows_the_roads(city, day):
    night, rush = day.travel_time(3.0), day.travel_time(8.0)
    free = city.edge_length / city.edge_speed
    assert (night >= free).all() and (rush > night).all()
    arterial = city.edge_arterial
    assert (rush / night)[arterial].mean() > (rush / night)[~arterial].mean()


def test_day_files_round_trip_and_refuse_the_wrong_city(city, day, tmp_path):
    path = tmp_path / "day.npz"
    day.save(path)
    back = Day.load(path, city)
    for k in ("parcel_address", "parcel_size", "parcel_dims", "parcel_weight", "parcel_fragility", "recipient_walk"):
        assert np.array_equal(getattr(back, k), getattr(day, k))
    assert np.array_equal(back.travel_time(8.0), day.travel_time(8.0))
    assert back.weather_at(13.2) == day.weather_at(13.2)
    with pytest.raises(ValueError):
        Day.load(path, City(1))


def test_held_out_days_are_fixed_and_apart_from_training():
    assert len(HELD_OUT) == 50 and len(set(HELD_OUT)) == 50
    assert min(seed for seed, _ in HELD_OUT) >= 1000
    saved = Path(__file__).parent.parent / "data" / "held-out"
    assert sorted(p.name for p in saved.glob("*.npz")) == sorted(f"city{s}-day{d}.npz" for s, d in HELD_OUT)
    seed, d = HELD_OUT[0]
    assert len(Day.load(saved / f"city{seed}-day{d}.npz", City(seed, day=d)).parcel_address) == 500
