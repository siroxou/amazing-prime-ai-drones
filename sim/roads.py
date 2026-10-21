"""Driving times on the city's road graph: shortest paths between road nodes, for any set of
edge times (usually day.travel_time(hour), so traffic counts)."""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra


def nearest_nodes(city, points, chunk=2000):
    """Road node nearest each (x, y) point.
    ponytail: snaps to a node, which on a long straight arterial edge can be up to ~60 m away;
    that's a few seconds of driving, well inside the service-time uncertainty."""
    p = np.asarray(points, float).reshape(-1, 2)
    out = np.empty(len(p), int)
    for i in range(0, len(p), chunk):
        d = ((p[i:i + chunk, None] - city.nodes[None]) ** 2).sum(-1)
        out[i:i + chunk] = d.argmin(1)
    return out


def _graph(city, edge_seconds):
    n = len(city.nodes)
    a, b = city.edges.min(1), city.edges.max(1)
    key = a * n + b
    first = np.lexsort((edge_seconds, key))  # if two edges join the same pair of nodes, keep the quicker
    keep = first[np.r_[True, np.diff(key[first]) != 0]]
    return csr_matrix((edge_seconds[keep], (a[keep], b[keep])), shape=(n, n))


def drive_times(city, edge_seconds, nodes):
    """Shortest driving time in seconds from every one of `nodes` to every one of `nodes`."""
    nodes = np.asarray(nodes)
    sources, row = np.unique(nodes, return_inverse=True)
    return dijkstra(_graph(city, edge_seconds), directed=False, indices=sources)[row][:, nodes]


class Paths:
    """The road nodes a vehicle passes through on the quickest way between any two of `nodes`."""

    def __init__(self, city, edge_seconds, nodes):
        self.nodes = np.asarray(nodes)
        self.sources = {int(v): k for k, v in enumerate(np.unique(self.nodes))}
        _, self.pred = dijkstra(_graph(city, edge_seconds), directed=False, indices=np.unique(self.nodes),
                                return_predecessors=True)

    def between(self, a, b):
        """Road nodes from node a to node b, both included."""
        row, out = self.pred[self.sources[int(a)]], [int(b)]
        while out[-1] != a:
            out.append(int(row[out[-1]]))
        return out[::-1]
