import unittest
from dataclasses import dataclass
from typing import Union

from tython.src.main.nullable.nullable import Nullable


class ChildClass:
    my_property = "property"

    @staticmethod
    def my_method():
        return "method"


@dataclass
class ParentClass:
    my_int: int
    my_child: Union[ChildClass, Nullable] = Nullable(ChildClass)


class TestNullable(unittest.TestCase):

    def test_property_access_on_nullable(self):
        parent = ParentClass(1)
        self.assertEqual(parent.my_child.my_property, None)

    def test_method_access_on_nullable(self):
        parent = ParentClass(1)
        self.assertEqual(parent.my_child.my_method(), None)

    def test_property_access_on_valid(self):
        parent = ParentClass(1, ChildClass())
        self.assertEqual(parent.my_child.my_property, "property")

    def test_method_access_on_valid(self):
        parent = ParentClass(1, ChildClass())
        self.assertEqual(parent.my_child.my_method(), "method")
