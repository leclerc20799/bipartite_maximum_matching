# bipartite-maximum-matching

Finds a maximum-cardinality matching in a bipartite graph using augmenting-path depth-first search. Standard library only, no dependencies.

## Usage

```python
from bipartite_maximum_matching import maximum_matching, matching_size

# adjacency maps each LEFT vertex to an iterable of RIGHT vertices.
# Left and right vertex sets must be disjoint.
adjacency = {
    "a": ["x", "y"],
    "b": ["y"],
    "c": ["z"],
}

matching = maximum_matching(adjacency)   # dict: right_vertex -> left_vertex
print(matching)        # e.g. {'y': 'a', 'x': 'b', 'z': 'c'} -- exact assignment may vary
print(matching_size(matching))  # 3
```

`maximum_matching(adjacency)` returns a dict keyed by right vertex, valued by the matched left vertex. `matching_size(matching)` returns the edge count.

## Why this exists

The problem is maximum bipartite matching: pair as many left vertices to right vertices as possible such that no vertex is used twice. The implementation uses the classic augmenting-path DFS approach, giving O(V * E) worst-case time. This is simpler and shorter than Hopcroft-Karp's O(E * sqrt(V)) and needs no third-party libraries. The trade-off is performance on very large graphs — if you need to match millions of vertices, use a dedicated native library.

## Edge cases worth knowing

- **Disjoint partite sets required.** A vertex must not appear on both sides. The matching dict is keyed by right vertex, so a vertex appearing on both sides would be ambiguous. The library does not check this; passing overlapping sets produces undefined results.
- **Adjacency values may be generators.** They are materialised once internally, so one-shot iterables work correctly.
- **Isolated vertices.** Left vertices with empty neighbor lists never match. Right vertices that no left vertex references never appear in the output.
- **Non-determinism of assignment.** The size of the returned matching is always maximum, but which specific vertices are paired can vary depending on dict iteration order. Compare sizes, not exact pairings, unless the matching is unique.

## Running the tests

```
PYTHONPATH=src python -m unittest discover -s tests
```
