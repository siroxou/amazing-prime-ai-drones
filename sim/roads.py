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


def drive_times(city, edge_seconds, nodes):
    """Shortest driving time in seconds from every one of `nodes` to every one of `nodes`."""
    n = len(city.nodes)
    a, b = city.edges.min(1), city.edges.max(1)
    key = a * n + b
    first = np.lexsort((edge_seconds, key))  # if two edges join the same pair of nodes, keep the quicker
    keep = first[np.r_[True, np.diff(key[first]) != 0]]
    graph = csr_matrix((edge_seconds[keep], (a[keep], b[keep])), shape=(n, n))
    nodes = np.asarray(nodes)
    sources, row = np.unique(nodes, return_inverse=True)
    return dijkstra(graph, directed=False, indices=sources)[row][:, nodes]
