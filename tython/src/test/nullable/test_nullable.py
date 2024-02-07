import unittest

from pydantic.dataclasses import dataclass

from tython.src.main.nullable.nullable import Nullable


@dataclass
class MyCustomSubClass:
    str_attr: Nullable[str] = "custom string"
    str_none_attr: Nullable[str] = Nullable(str)


@dataclass
class MyCustomTestClass:
    int_attr: Nullable[int] = 10
    float_attr: Nullable[float] = 10.5
    str_attr: Nullable[str] = "test"
    bool_attr: Nullable[bool] = False

    none_int_attr: Nullable[int] = Nullable(int)
    none_float_attr: Nullable[float] = Nullable(float)
    none_str_attr: Nullable[str] = Nullable(str)
    none_bool_attr: Nullable[bool] = Nullable(bool)

    assigned_attr: Nullable[str] = Nullable(str)
    subclass_attr: Nullable[MyCustomSubClass] = MyCustomSubClass()
    subclass_none_attr: Nullable[MyCustomSubClass] = Nullable(MyCustomSubClass)


# noinspection PyUnresolvedReferences
class TestNullable(unittest.TestCase):

    def setUp(self):
        self.test_class = MyCustomTestClass(assigned_attr="test")

    def test_str(self):
        my_none_str = self.test_class.none_str_attr.replace("t", "a")
        my_str = self.test_class.str_attr.replace("t", "a")
        assigned_str = self.test_class.assigned_attr
        direct_assignment = Nullable("test")

        self.assertEqual(my_str, "aesa")
        self.assertEqual(direct_assignment, "test")

        self.assertEqual(my_none_str, None)

        self.assertEqual(assigned_str, "test")

    def test_assert_subclass_access(self):
        # Subclass access
        self.assertIsInstance(self.test_class.subclass_attr, MyCustomSubClass)
        self.assertIsNone(self.test_class.subclass_none_attr.str_none_attr)

        # Subclass attrs
        self.assertEqual(self.test_class.subclass_attr.str_attr, "custom string")
        self.assertEqual(self.test_class.subclass_attr.str_none_attr, None)


if __name__ == "__main__":
    unittest.main()
