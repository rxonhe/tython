import unittest

from tython.src.main.data_structures.map import map_of


class TestMap(unittest.TestCase):

    def test_map_init(self):
        map_a = {'a': 1, 'b': 2, 'c': 3}
        map_b = map_of(a=1, b=2, c=3)
        self.assertEqual(map_a, map_b)


if __name__ == '__main__':
    unittest.main()
