"""Maximum-cardinality matching in a bipartite graph.

The graph is given as an adjacency mapping from each left vertex to an
iterable of right vertices it is adjacent to. Left and right vertices may
be any hashable, comparable objects; the only constraint is that the two
partite sets be disjoint (a vertex must not appear on both sides), because
otherwise the matching dictionary could not distinguish which side a vertex
belongs to.

Algorithm: Hopcroft-style augmenting-path search. For each left vertex we
run a depth-first search looking for an alternating path that ends at an
unmatched right vertex. If one is found, we flip matched/unmatched edges
along the path, growing the matching by one. Each DFS visits each edge at
most once per outer iteration, giving O(V * E) worst case.

We deliberately use the simple O(V*E) form rather than Hopcroft-Karp's
O(E * sqrt(V)): the code is short, dependency-free, and fast enough for the
moderate graphs this library targets. For very large graphs, a dedicated
library would be the better choice.
"""

from typing import Dict, Hashable, Iterable, Mapping, Set


def _augment(
    u: Hashable,
    adj: Mapping[Hashable, Iterable[Hashable]],
    match_r: Dict[Hashable, Hashable],
    seen: Set[Hashable],
) -> bool:
    """Try to find an augmenting path starting from left vertex ``u``.

    Mutates ``match_r`` in place when a path is found. ``seen`` tracks right
    vertices already considered in this DFS round so we never revisit them;
    this keeps the round O(E) and prevents infinite loops on cycles.
    """
    for v in adj[u]:
        if v in seen:
            continue
        seen.add(v)
        # If v is unmatched, we extend the path. Otherwise we recurse through
        # v's current match; if that subtree yields an augmenting path, v gets
        # rematched to u as part of the flip.
        if v not in match_r or _augment(match_r[v], adj, match_r, seen):
            match_r[v] = u
            return True
    return False


def maximum_matching(adjacency: Mapping[Hashable, Iterable[Hashable]]) -> Dict[Hashable, Hashable]:
    """Return a maximum-cardinality matching as a dict mapping right -> left.

    ``adjacency`` maps each left vertex to an iterable of adjacent right
    vertices. Left and right vertex sets must be disjoint. The returned dict
    has one entry per matched edge, keyed by the right vertex.

    An empty adjacency yields an empty dict. Left vertices with no neighbors
    simply never match. Isolated right vertices never appear as keys.
    """
    # Materialise each adjacency list once so repeated DFS rounds don't
    # re-consume a generator (which would be exhausted after the first pass).
    adj: Dict[Hashable, list] = {u: list(vs) for u, vs in adjacency.items()}
    match_r: Dict[Hashable, Hashable] = {}
    for u in adj:
        _augment(u, adj, match_r, set())
    return match_r


def matching_size(matching: Mapping[Hashable, Hashable]) -> int:
    """Return the number of edges in ``matching``.

    ``matching`` is expected to be a dict in the form produced by
    :func:`maximum_matching` (right -> left). The size is simply the number
    of keys; this helper exists so callers don't reach into the dict shape
    directly.
    """
    return len(matching)
