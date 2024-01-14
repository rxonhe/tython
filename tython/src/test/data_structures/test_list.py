import unittest

from tython.src.main.data_structures.list import list_of


class TestList(unittest.TestCase):

    def test_list_init(self):
        list_a = [1, 2, 3]
        list_b = list_of(1, 2, 3)
        self.assertEqual(list_a, list_b)


if __name__ == '__main__':
    unittest.main()
