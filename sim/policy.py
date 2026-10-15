"""Run an exported policy with plain numpy, no PyTorch needed.

Training (train/) uses PyTorch; train/export.py writes the policy network's
weights to a .npz file that this class loads, so evaluation and rendering
run without torch. tests/test_policy.py checks both give the same actions.
"""
import numpy as np


class Policy:
    def __init__(self, file):
        """`file` is a path or a file-like object."""
        data = np.load(file)
        count = sum(1 for k in data.files if k.startswith("w"))
        self.layers = [(data[f"w{i}"], data[f"b{i}"]) for i in range(count)]

    def act(self, obs):
        """Deterministic action for one observation, clipped to [-1, 1]."""
        h = np.asarray(obs, np.float32)
        for i, (w, b) in enumerate(self.layers):
            h = h @ w.T + b
            if i < len(self.layers) - 1:
                h = np.tanh(h)
        return np.clip(h, -1.0, 1.0)
