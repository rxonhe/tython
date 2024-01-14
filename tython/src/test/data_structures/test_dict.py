import unittest


class TestDict(unittest.TestCase):

    def test_dict_init(self):
        map_a = {'a': 1, 'b': 2, 'c': 3}
        map_b = dict_of(a=1, b=2, c=3)
        self.assertEqual(map_a, map_b)


def dict_of(**kwargs):
    return kwargs


def dict_from(*args):
    return dict(args)


if __name__ == '__main__':
    unittest.main()
