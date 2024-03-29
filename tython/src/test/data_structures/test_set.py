import unittest
from functools import reduce

from tython.src.main.data_structures.set import set_of, set_from


# noinspection DuplicatedCode
class TestSet(unittest.TestCase):

    def setUp(self):
        self.small_set = set_of(1, 2, 3, 4, 5)
        self.integer_set = set_of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.set_with_none = set_of(1, 2, 3, None, 4, 5, 6, None, 8, 9, None)
        self.set_with_none_edges = set_of(None, 1, 2, 3, None, 4, 5, 6, None, 8, 9, None)
        self.composed_set = set_of(set_of("123"), set_of("45"))

    def test_set_of(self):
        set_a = {1, 2, 3}
        set_b = set_of(1, 2, 3)
        self.assertEqual(set_a, set_b)

    def test_set_from(self):
        set_a = {1, 2, 3}
        self.assertEqual(set_a, set_from(set_a))

    def test_map(self):
        doubled_set = set(map(lambda it: it * 2, self.integer_set))
        functional_doubled_set = self.integer_set.map(lambda it: it * 2)
        self.assertEqual(doubled_set, functional_doubled_set)

    def test_filter_none(self):
        filtered_set = set(filter(lambda it: it is not None, self.set_with_none))
        functional_filtered_set = self.set_with_none.filter_none()
        self.assertEqual(filtered_set, functional_filtered_set)

    def test_filter(self):
        filtered_set = set(filter(lambda it: it > 5, self.integer_set))
        functional_filtered_set = self.integer_set.filter(lambda it: it > 5)
        self.assertEqual(filtered_set, functional_filtered_set)

    def test_fold_without_initial_value(self):
        folded_set = reduce(lambda it, it2: it + it2, self.integer_set)
        functional_folded_set = self.integer_set.fold(lambda it, it2: it + it2)
        self.assertEqual(folded_set, functional_folded_set)

    def test_fold_with_initial_value(self):
        folded_set = reduce(lambda it, it2: it + it2, self.integer_set, 10)
        functional_folded_set = self.integer_set.fold(lambda it, it2: it + it2, 10)
        self.assertEqual(folded_set, functional_folded_set)

    def test_flatten(self):
        flattened_set = self.composed_set.flatten()
        expected = set_of("123", "45")
        self.assertEqual(expected, flattened_set)

    def test_flat_map(self):
        expected_result = set_of(246, 90)
        flattened_set = self.composed_set.flat_map(lambda it: it.map(lambda it: int(it) * 2))
        self.assertEqual(expected_result, flattened_set)

    def test_indexed_map(self):
        indexed_set = self.small_set.map_indexed(lambda index, value: index + value)
        self.assertEqual(set_of(1, 3, 5, 7, 9), indexed_set)

    def test_all(self):
        self.assertTrue(self.small_set.all(lambda it: it < 6))
        self.assertFalse(self.small_set.all(lambda it: it < 5))

    def test_none(self):
        self.assertTrue(self.small_set.none(lambda it: it > 5))
        self.assertFalse(self.small_set.none(lambda it: it > 4))

    def test_any(self):
        self.assertTrue(self.small_set.any(lambda it: it > 4))
        self.assertFalse(self.small_set.any(lambda it: it > 5))

    def test_add(self):
        self.assertEqual(set_of(1, 2, 3, 4, 5, 6), self.small_set.add(6))

    def test_add_all(self):
        self.assertEqual(set_of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), self.small_set.add_all(self.integer_set))

    def test_remove(self):
        self.assertEqual(set_of(1, 2, 3, 4, 5), self.integer_set.remove(6))

    def test_length(self):
        self.assertEqual(5, self.small_set.length())

    def test_map_to_dict(self):
        self.assertEqual({1: 1, 2: 2, 3: 3}, self.small_set.map_to_dict(lambda it: (it, it)))

    def test_map_to_list(self):
        self.assertEqual([1, 2, 3, 4, 5], self.small_set.map_to_list(lambda it: it))

    def test_map_not_none(self):
        self.assertEqual(set_of(1, 2, 3, 4, 5, 6, 8, 9), self.set_with_none.map_not_none(lambda it: it))

    def test_map_not_none_to_dict(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.set_with_none.map_not_none_to_dict(lambda it: (it, it)))

    def test_map_not_none_to_list(self):
        self.assertEqual([1, 2, 3, 4, 5, 6, 8, 9], self.set_with_none.map_not_none_to_list(lambda it: it))

    def test_map_not_none_indexed(self):
        self.assertEqual(set_of((0, 1), (1, 2), (3, 4), (6, 8), (2, 3), (7, 9), (4, 5), (5, 6)), self.set_with_none.map_not_none_indexed(lambda index, value: (index, value)))

    def test_map_not_none_indexed_to_dict(self):
        self.assertEqual({0: 1, 1: 2, 2: 3, 4: 4, 5: 5, 6: 6, 8: 8, 9: 9}, self.set_with_none.map_not_none_indexed_to_dict(lambda index, value: (index, value)))

    def test_map_not_none_indexed_to_list(self):
        self.assertEqual([(0, 1), (1, 2), (3, 4), (6, 8), (2, 3), (7, 9), (4, 5), (5, 6)], self.set_with_none.map_not_none_indexed_to_list(lambda index, value: (index, value)))

    def test_map_indexed_to_dict(self):
        self.assertEqual({0: 1, 1: 2, 2: 3, 3: None, 4: 4, 5: 5, 6: 6, 7: None, 8: 8, 9: 9, 10: None}, self.set_with_none.map_indexed_to_dict(lambda index, value: (index, value)))

    def test_set_with_none_edges(self):
        self.assertEqual(set_of(1, 2, 3, 4, 5, 6, 8, 9), self.set_with_none_edges.map_not_none(lambda it: it))
        self.assertEqual({(0, 1), (1, 2), (3, 4), (6, 8), (2, 3), (7, 9), (4, 5), (5, 6)}, self.set_with_none_edges.map_not_none_indexed(lambda index, value: (index, value)))

    def test_group_by(self):
        self.assertEqual({1: {1, 4, 7, 10}, 2: {2, 5, 8}, 0: {3, 6, 9}}, self.integer_set.group_by(lambda it: it % 3))

    def test_associate_by(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.small_set.associate_by(lambda it: it))

    def test_associate_by_not_none(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.small_set.associate_by_not_none(lambda it: it))

    def test_associate_by_indexed(self):
        self.assertEqual({0: 1, 1: 2, 2: 3, 3: 4, 4: 5}, self.small_set.associate_by_indexed(lambda index, value: (index, value)))

    def test_associate_with(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.small_set.associate_with(lambda it: it))

    def test_associate_with_not_none(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.small_set.associate_with_not_none(lambda it: it))

    def test_associate_with_indexed(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.small_set.associate_with_indexed(lambda index, value: (index, value)))

    def test_associate_with_indexed_not_none(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.small_set.associate_with_indexed_not_none(lambda index, value: (index, value)))

    def test_associate(self):
        self.assertEqual({1: 1, 2: 2, 3: 3}, self.small_set.associate(lambda it: (it, it)))

    def test_associate_not_none(self):
        self.assertEqual({1: 1, 2: 2, 3: 3}, self.small_set.associate_not_none(lambda it: (it, it)))

    def test_associate_indexed(self):
        self.assertEqual({0: 1, 1: 2, 2: 3}, self.small_set.associate_indexed(lambda index, value: (index, value)))

    def test_associate_indexed_not_none(self):
        self.assertEqual({0: 1, 1: 2, 2: 3}, self.small_set.associate_indexed_not_none(lambda index, value: (index, value)))


if __name__ == '__main__':
    unittest.main()
