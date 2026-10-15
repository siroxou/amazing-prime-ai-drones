import gymnasium as gym
import numpy as np
import pytest

pytest.importorskip("stable_baselines3")

from stable_baselines3 import PPO  # noqa: E402

from sim.policy import Policy  # noqa: E402
from train.export import export  # noqa: E402


def test_numpy_policy_matches_torch(tmp_path):
    # Stand-in until the drone env exists; actions rescaled to [-1, 1] like ours.
    env = gym.wrappers.RescaleAction(gym.make("Pendulum-v1"), -1.0, 1.0)
    model = PPO("MlpPolicy", env, policy_kwargs={"net_arch": {"pi": [64, 32], "vf": [16]}}, device="cpu", seed=0)
    export(model, tmp_path / "p.npz")
    policy = Policy(tmp_path / "p.npz")
    obs = np.random.default_rng(0).uniform(-1, 1, (50, env.observation_space.shape[0])).astype(np.float32)
    expected, _ = model.predict(obs, deterministic=True)
    got = np.array([policy.act(o) for o in obs])
    assert np.allclose(got, expected, atol=1e-5)
