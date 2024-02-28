import unittest
from functools import reduce

from tython.src.main.data_structures.list import list_of, list_from


# noinspection DuplicatedCode
class TestList(unittest.TestCase):

    def setUp(self):
        self.small_list = list_of(1, 2, 3, 4, 5)
        self.integer_list = list_of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.list_with_none = list_of(1, 2, 3, None, 4, 5, 6, None, 8, 9, None)
        self.list_with_none_edges = list_of(None, 1, 2, 3, None, 4, 5, 6, None, 8, 9, None)
        self.composed_list = list_of(list_of("123"), list_of("45"))

    def test_list_of(self):
        list_a = [1, 2, 3]
        list_b = list_of(1, 2, 3)
        self.assertEqual(list_a, list_b)

    def test_list_from(self):
        list_a = [1, 2, 3]
        self.assertEqual(list_a, list_from(list_a))

    def test_map(self):
        doubled_list = list(map(lambda it: it * 2, self.integer_list))
        functional_doubled_list = self.integer_list.map(lambda it: it * 2)
        self.assertEqual(doubled_list, functional_doubled_list)

    def test_filter_none(self):
        filtered_list = list(filter(lambda it: it is not None, self.list_with_none))
        functional_filtered_list = self.list_with_none.filter_none()
        self.assertEqual(filtered_list, functional_filtered_list)

    def test_filter(self):
        filtered_list = list(filter(lambda it: it > 5, self.integer_list))
        functional_filtered_list = self.integer_list.filter(lambda it: it > 5)
        self.assertEqual(filtered_list, functional_filtered_list)

    def test_fold_without_initial_value(self):
        folded_list = reduce(lambda it, it2: it + it2, self.integer_list)
        functional_folded_list = self.integer_list.fold(lambda it, it2: it + it2)
        self.assertEqual(folded_list, functional_folded_list)

    def test_fold_with_initial_value(self):
        folded_list = reduce(lambda it, it2: it + it2, self.integer_list, 10)
        functional_folded_list = self.integer_list.fold(lambda it, it2: it + it2, 10)
        self.assertEqual(folded_list, functional_folded_list)

    def test_flatten(self):
        flattened_list = self.composed_list.flatten()
        expected = list_of("123", "45")
        self.assertEqual(expected, flattened_list)

    def test_flat_map(self):
        expected_result = list_of(90, 246)
        flattened_list = self.composed_list.flat_map(lambda it: it.map(lambda it: int(it) * 2))
        self.assertEqual(expected_result, flattened_list)

    def test_nested_map(self):
        nested_list = list_of(list_of(1, 2), list_of(3, 4))
        doubled_nested_list = nested_list.nested_map(lambda it: it * 2)
        self.assertEqual(list_of(list_of(2, 4), list_of(6, 8)), doubled_nested_list)

    def test_indexed_map(self):
        indexed_list = self.small_list.map_indexed(lambda index, value: index + value)
        self.assertEqual(list_of(1, 3, 5, 7, 9), indexed_list)

    def test_first(self):
        self.assertEqual(1, self.small_list.first())
        self.assertEqual(1, self.small_list.first(lambda it: it % 2 == 1))
        self.assertEqual(3, self.small_list.first(lambda it: it > 2))

    def test_last(self):
        self.assertEqual(5, self.small_list.last())
        self.assertEqual(5, self.small_list.last(lambda it: it % 2 == 1))
        self.assertEqual(4, self.small_list.last(lambda it: it < 5))

    def test_all(self):
        self.assertTrue(self.small_list.all(lambda it: it < 6))
        self.assertFalse(self.small_list.all(lambda it: it < 5))

    def test_none(self):
        self.assertTrue(self.small_list.none(lambda it: it > 5))
        self.assertFalse(self.small_list.none(lambda it: it > 4))

    def test_any(self):
        self.assertTrue(self.small_list.any(lambda it: it > 4))
        self.assertFalse(self.small_list.any(lambda it: it > 5))

    def test_reverse(self):
        self.assertEqual(list_of(5, 4, 3, 2, 1), self.small_list.reverse())

    def test_add(self):
        self.assertEqual(list_of(1, 2, 3, 4, 5, 6), self.small_list.add(6))

    def test_add_all(self):
        self.assertEqual(list_of(1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), self.small_list.add_all(self.integer_list))

    def test_remove(self):
        self.assertEqual(list_of(1, 2, 3, 4, 5, 7, 8, 9, 10), self.integer_list.remove(6))

    def test_remove_all(self):
        self.assertEqual(list_of(6, 7, 8, 9, 10), self.integer_list.remove_all(self.small_list))

    def test_length(self):
        self.assertEqual(5, self.small_list.length())

    def test_map_to_dict(self):
        self.assertEqual({1: 1, 2: 2, 3: 3}, self.small_list.map_to_dict(lambda it: (it, it)))

    def test_map_to_set(self):
        self.assertEqual({1, 2, 3, 4, 5}, self.small_list.map_to_set(lambda it: it))

    def test_map_not_none(self):
        self.assertEqual(list_of(1, 2, 3, 4, 5, 6, 8, 9), self.list_with_none.map_not_none(lambda it: it))

    def test_map_not_none_to_dict(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.list_with_none.map_not_none_to_dict(lambda it: (it, it)))

    def test_map_not_none_to_set(self):
        self.assertEqual({1, 2, 3, 4, 5, 6, 8, 9}, self.list_with_none.map_not_none_to_set(lambda it: it))

    def test_map_not_none_indexed(self):
        self.assertEqual(list_of((0, 1), (1, 2), (2, 3), (4, 4), (5, 5), (6, 6), (8, 8), (9, 9)), self.list_with_none.map_not_none_indexed(lambda index, value: (index, value)))

    def test_map_not_none_indexed_to_dict(self):
        self.assertEqual({0: 1, 1: 2, 2: 3, 4: 4, 5: 5, 6: 6, 8: 8, 9: 9}, self.list_with_none.map_not_none_indexed_to_dict(lambda index, value: (index, value)))

    def test_map_not_none_indexed_to_set(self):
        self.assertEqual({(0, 1), (1, 2), (2, 3), (4, 4), (5, 5), (6, 6), (8, 8), (9, 9)}, self.list_with_none.map_not_none_indexed_to_set(lambda index, value: (index, value)))

    def test_map_indexed_to_dict(self):
        self.assertEqual({0: 1, 1: 2, 2: 3, 3: None, 4: 4, 5: 5, 6: 6, 7: None, 8: 8, 9: 9, 10: None}, self.list_with_none.map_indexed_to_dict(lambda index, value: (index, value)))

    def test_map_indexed_to_set(self):
        self.assertEqual({(0, 1), (1, 2), (2, 3), (3, None), (4, 4), (5, 5), (6, 6), (7, None), (8, 8), (9, 9), (10, None)},
                         self.list_with_none.map_indexed_to_set(lambda index, value: (index, value)))

    def test_list_with_none_edges(self):
        self.assertEqual(list_of(1, 2, 3, 4, 5, 6, 8, 9), self.list_with_none_edges.map_not_none(lambda it: it))
        self.assertEqual(list_of((1, 1), (2, 2), (3, 3), (5, 4), (6, 5), (7, 6), (9, 8), (10, 9)),
                         self.list_with_none_edges.map_not_none_indexed(lambda index, value: (index, value)))
        self.assertEqual({1: 1, 2: 2, 3: 3, 5: 4, 6: 5, 7: 6, 9: 8, 10: 9}, self.list_with_none_edges.map_not_none_indexed_to_dict(lambda index, value: (index, value)))
        self.assertEqual({(1, 1), (2, 2), (3, 3), (5, 4), (6, 5), (7, 6), (9, 8), (10, 9)},
                         self.list_with_none_edges.map_not_none_indexed_to_set(lambda index, value: (index, value)))
        self.assertEqual({0: None, 1: 1, 2: 2, 3: 3, 4: None, 5: 4, 6: 5, 7: 6, 8: None, 9: 8, 10: 9, 11: None},
                         self.list_with_none_edges.map_indexed_to_dict(lambda index, value: (index, value)))
        self.assertEqual({(0, None), (1, 1), (2, 2), (3, 3), (4, None), (5, 4), (6, 5), (7, 6), (8, None), (9, 8), (10, 9), (11, None)},
                         self.list_with_none_edges.map_indexed_to_set(lambda index, value: (index, value)))

    def test_group_by(self):
        self.assertEqual({1: [1, 4, 7, 10], 2: [2, 5, 8], 0: [3, 6, 9]}, self.integer_list.group_by(lambda it: it % 3))

    def test_associate_by(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.small_list.associate_by(lambda it: it))

    def test_associate_by_not_none(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.small_list.associate_by_not_none(lambda it: it))

    def test_associate_by_indexed(self):
        self.assertEqual({0: 1, 1: 2, 2: 3, 3: 4, 4: 5}, self.small_list.associate_by_indexed(lambda index, value: (index, value)))

    def test_associate_with(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.small_list.associate_with(lambda it: it))

    def test_associate_with_not_none(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.small_list.associate_with_not_none(lambda it: it))

    def test_associate_with_indexed(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.small_list.associate_with_indexed(lambda index, value: (index, value)))

    def test_associate_with_indexed_not_none(self):
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, self.small_list.associate_with_indexed_not_none(lambda index, value: (index, value)))

    def test_associate(self):
        self.assertEqual({1: 1, 2: 2, 3: 3}, self.small_list.associate(lambda it: (it, it)))

    def test_associate_not_none(self):
        self.assertEqual({1: 1, 2: 2, 3: 3}, self.small_list.associate_not_none(lambda it: (it, it)))

    def test_associate_indexed(self):
        self.assertEqual({0: 1, 1: 2, 2: 3}, self.small_list.associate_indexed(lambda index, value: (index, value)))

    def test_associate_indexed_not_none(self):
        self.assertEqual({0: 1, 1: 2, 2: 3}, self.small_list.associate_indexed_not_none(lambda index, value: (index, value)))


if __name__ == '__main__':
    unittest.main()
