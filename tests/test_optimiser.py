import numpy as np
import pytest

from baselines import classical as cl
from optimiser import routes as rt
from optimiser import waits as wt
from sim.city import City
from sim.day import Day


@pytest.fixture(scope="module")
def solved():
    day = Day(City(seed=0), parcels=200)
    r = cl.solve(day, seconds=1)
    return day, r, rt.from_solve(day, r)


def fixed(plan, minutes):
    return [[minutes / 60] * len(r.stops) for r in plan.routes]


def test_replaying_the_plans_own_waits_gives_the_same_day(solved):
    _, r, plan = solved
    replayed = rt.day_times(plan, fixed(plan, cl.WINDOW))
    assert len(replayed) == plan.parcels
    assert np.isnan(replayed).sum() == np.isnan(r["parcel_time"]).sum()
    assert np.allclose(np.sort(replayed[~np.isnan(replayed)]), np.sort(r["parcel_time"][~np.isnan(r["parcel_time"])]))


def test_longer_waits_collect_more_but_finish_later(solved):
    _, _, plan = solved
    short, long = (rt.summary(rt.day_times(plan, fixed(plan, m))) for m in (5, 30))
    assert long["delivered"] > short["delivered"] and long["last"] > short["last"]


def test_score_counts_missed_parcels_as_a_day(solved):
    assert rt.score([rt.START + 1, rt.START + 3]) == pytest.approx(2.0)
    assert rt.score([rt.START + 1, np.nan]) == pytest.approx((1 + rt.MISSED) / 2)


def test_the_training_env_scores_a_route_as_the_replay_does(solved):
    _, _, plan = solved
    env = wt.WaitEnv([plan])
    for route in env.routes:
        env.reset()
        env.route, env.arrive = route, rt.START + rt.leg(route, 0, 1, rt.START)
        total, done = 0.0, False
        while not done:
            obs, reward, done, _, _ = env.step(4)
            total += reward
            assert obs.shape == (wt.FEATURES,) and np.isfinite(obs).all()
        times = rt.replay(route, [wt.WAITS[4]] * len(route.stops))
        assert total == pytest.approx(-np.sum(np.where(np.isnan(times), rt.MISSED, times - rt.START)) / 100)


def test_hand_rule_waits_more_for_more_recipients_and_later_stops(solved):
    _, _, plan = solved
    route = max(plan.routes, key=lambda r: len(r.stops))
    waits = wt.rule(1.0, 10.0)(route)
    assert len(waits) == len(route.stops) and all(0 <= w <= wt.WAITS[-1] for w in waits)
    lockers = [len(s.locker_ready) for s in route.stops]
    assert waits[-1] * 60 == pytest.approx(min(lockers[-1] + 10.0, wt.WAITS[-1] * 60))
