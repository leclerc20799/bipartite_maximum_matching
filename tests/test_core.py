import unittest

from bipartite_maximum_matching import maximum_matching, matching_size


class TestMaximumMatching(unittest.TestCase):
    def test_empty_graph(self):
        self.assertEqual(maximum_matching({}), {})

    def test_no_edges(self):
        # Left vertices exist but have no neighbors.
        self.assertEqual(maximum_matching({"a": [], "b": []}), {})

    def test_single_edge(self):
        self.assertEqual(maximum_matching({"a": ["x"]}), {"x": "a"})

    def test_simple_complete(self):
        # Two-by-two complete bipartite graph: perfect matching of size 2.
        m = maximum_matching({"a": ["x", "y"], "b": ["x", "y"]})
        self.assertEqual(len(m), 2)
        # Each left vertex matched exactly once, each right vertex once.
        self.assertEqual(set(m.values()), {"a", "b"})
        self.assertEqual(set(m.keys()), {"x", "y"})

    def test_augmentation_required(self):
        # a-x, a-y, b-y. Greedy matching a->x then b->? needs augmentation:
        # a moves to y so b can take x. Max size is 2.
        m = maximum_matching({"a": ["x", "y"], "b": ["y"]})
        self.assertEqual(len(m), 2)
        self.assertEqual(set(m.values()), {"a", "b"})

    def test_left_side_larger(self):
        # Three left vertices competing for two right vertices.
        m = maximum_matching({
            "a": ["x", "y"],
            "b": ["x", "y"],
            "c": ["x", "y"],
        })
        self.assertEqual(len(m), 2)
        self.assertEqual(set(m.keys()), {"x", "y"})

    def test_right_side_larger(self):
        m = maximum_matching({
            "a": ["x", "y", "z"],
            "b": ["x", "y", "z"],
        })
        self.assertEqual(len(m), 2)

    def test_disconnected_components(self):
        m = maximum_matching({
            "a": ["x"],
            "b": ["y"],
            "c": ["z"],
        })
        self.assertEqual(m, {"x": "a", "y": "b", "z": "c"})

    def test_integer_vertices(self):
        m = maximum_matching({0: [10, 11], 1: [10, 11]})
        self.assertEqual(len(m), 2)
        self.assertEqual(set(m.values()), {0, 1})

    def test_string_vertices(self):
        m = maximum_matching({"u1": ["v1"], "u2": ["v1", "v2"]})
        self.assertEqual(len(m), 2)

    def test_generator_adjacency_consumed_once(self):
        # Adjacency values may be one-shot generators; the implementation must
        # not exhaust them on the first DFS pass.
        def neighbors():
            yield "x"
            yield "y"

        m = maximum_matching({"a": neighbors(), "b": neighbors()})
        self.assertEqual(len(m), 2)

    def test_matching_size_helper(self):
        m = maximum_matching({"a": ["x"], "b": ["y"]})
        self.assertEqual(matching_size(m), 2)
        self.assertEqual(matching_size({}), 0)

    def test_duplicate_neighbors_in_list(self):
        # Duplicate entries in a neighbor list must not cause double-counting
        # or errors; the seen-set in the DFS guards against revisiting.
        m = maximum_matching({"a": ["x", "x", "x"], "b": ["x", "y"]})
        self.assertEqual(len(m), 2)

    def test_chain_requires_multiple_augmentations(self):
        # Constructed so that each new left vertex forces a reshuffle of all
        # previously matched edges. Max matching size is 4.
        #  a - x
        #  a - y, b - y
        #  a - y, b - z, c - z
        #  ... building a chain that stresses the augmenting-path logic.
        adj = {
            "a": ["x", "y"],
            "b": ["y", "z"],
            "c": ["z", "w"],
            "d": ["w"],
        }
        m = maximum_matching(adj)
        self.assertEqual(len(m), 4)
        self.assertEqual(set(m.keys()), {"x", "y", "z", "w"})


if __name__ == "__main__":
    unittest.main()
