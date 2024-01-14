import unittest

from tython.src.main.data_structures.set import set_of


class TestSet(unittest.TestCase):

    def test_set_init(self):
        set_a = {1, 2, 3}
        set_b = set_of(1, 2, 3)
        self.assertEqual(set_a, set_b)


if __name__ == '__main__':
    unittest.main()
