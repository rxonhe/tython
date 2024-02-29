import unittest

from tython.src.main.data_structures.dict import dict_of, dict_from


class TestDict(unittest.TestCase):

    def test_dict_init(self):
        map_a = {'a': 1, 'b': 2, 'c': 3}
        map_b = dict_of(a=1, b=2, c=3)
        map_c = dict_from({'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(map_a, map_b)
        self.assertEqual(map_a, map_c)


if __name__ == '__main__':
    unittest.main()
