from __future__ import annotations

from functools import reduce
from itertools import chain
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from tython.src.main.data_structures.dict import Dict
    from tython.src.main.data_structures.set import Set


class List(list):

    # Base functions =============================================
    def map(self, fun) -> List:
        return List(map(fun, self))

    def filter(self, fun) -> List:
        return List(filter(fun, self))

    def filter_none(self) -> List:
        return List(filter(lambda it: it is not None, self))

    def fold(self, fun, initial_value=None) -> Any:
        if initial_value is None:
            return reduce(fun, self)
        return reduce(fun, self, initial_value)

    def flatten(self) -> List:
        return List(chain(*self))

    def flat_map(self, fun) -> List:
        return self.map(fun).flatten()

    def nested_map(self, fun) -> List:
        return self.map(lambda it: it.map(fun))

    def map_indexed(self, fun) -> List:
        return List(map(lambda it: fun(it[0], it[1]), enumerate(self)))

    def all(self, fun) -> bool:
        return all(self.map(fun))

    def none(self, fun) -> bool:
        return not any(self.map(fun))

    def any(self, fun) -> bool:
        return any(self.map(fun))

    def reverse(self) -> List:
        return List(reversed(self))

    def first(self, function=None):
        try:
            if function:
                return next(filter(function, self), List())
            return next(iter(self), List())
        except StopIteration:
            return List()

    def last(self, function=None) -> List:
        return self.reverse().first(function)

    def add(self, element) -> List:
        return List(self + [element])

    def add_all(self, elements) -> List:
        return List(self + elements)

    def remove(self, element) -> List:
        return List(filter(lambda it: it != element, self))

    def remove_all(self, elements) -> List:
        return List(filter(lambda it: it not in elements, self))

    def length(self) -> int:
        return len(self)

    # Composite functions ========================================

    def map_to_dict(self, fun) -> "Dict":
        from tython.src.main.data_structures.dict import Dict
        return Dict(self.map(fun))

    def map_to_set(self, fun) -> "Set":
        from tython.src.main.data_structures.set import Set
        return Set(self.map(fun))

    def map_not_none(self, fun) -> List:
        return self.filter_none().map(fun).filter_none()

    def map_not_none_to_dict(self, fun) -> "Dict":
        return self.map_not_none(fun).map_to_dict(lambda it: it)

    def map_not_none_to_set(self, fun) -> "Set":
        return self.map_not_none(fun).map_to_set(lambda it: it)

    def map_not_none_indexed(self, fun) -> List:
        return self.filter_none().map_indexed(lambda index, value: (index, fun(index, value))).filter_none()

    def map_not_none_indexed_to_dict(self, fun) -> "Dict":
        return self.map_not_none_indexed(fun).map_to_dict(lambda it: it)

    def map_not_none_indexed_to_set(self, fun) -> "Set":
        return self.map_not_none_indexed(fun).map_to_set(lambda it: it)

    def map_indexed_to_dict(self, fun) -> "Dict":
        return self.map_indexed(fun).map_to_dict(lambda it: it)

    def map_indexed_to_set(self, fun) -> "Set":
        return self.map_indexed(fun).map_to_set(lambda it: it)

    def flat_map_not_none(self, fun) -> List:
        return self.map_not_none(fun).flatten()

    def flat_map_not_none_to_dict(self, fun) -> "Dict":
        return self.flat_map_not_none(fun).map_to_dict(lambda it: it)

    def flat_map_not_none_to_set(self, fun) -> "Set":
        return self.flat_map_not_none(fun).map_to_set(lambda it: it)

    def flat_map_indexed(self, fun) -> List:
        return self.map_indexed(fun).flatten()

    def flat_map_not_none_indexed(self, fun) -> List:
        return self.map_not_none_indexed(fun).flatten()

    def flat_map_not_none_indexed_to_dict(self, fun) -> "Dict":
        return self.flat_map_not_none_indexed(fun).map_to_dict(lambda it: it)

    def flat_map_not_none_indexed_to_set(self, fun) -> "Set":
        return self.flat_map_not_none_indexed(fun).map_to_set(lambda it: it)

    def nested_map_not_none(self, fun) -> List:
        return self.map_not_none(fun).nested_map(lambda it: it)

    def nested_map_not_none_to_dict(self, fun) -> "Dict":
        return self.nested_map_not_none(fun).map_to_dict(lambda it: it)

    def nested_map_not_none_to_set(self, fun) -> "Set":
        return self.nested_map_not_none(fun).map_to_set(lambda it: it)

    def nested_map_indexed(self, fun) -> List:
        return self.map_indexed(fun).nested_map(lambda it: it)

    def nested_map_not_none_indexed(self, fun) -> List:
        return self.map_not_none_indexed(fun).nested_map(lambda it: it)

    def nested_map_not_none_indexed_to_dict(self, fun) -> "Dict":
        return self.nested_map_not_none_indexed(fun).map_to_dict(lambda it: it)

    def nested_map_not_none_indexed_to_set(self, fun) -> "Set":
        return self.nested_map_not_none_indexed(fun).map_to_set(lambda it: it)

    def first_not_none(self, function=None):
        return self.filter_none().first(function)

    def last_not_none(self, function=None):
        return self.filter_none().last(function)

    def first_indexed(self, function=None):
        return self.map_indexed(function).first()

    def last_indexed(self, function=None):
        return self.map_indexed(function).last()

    def first_indexed_not_none(self, function=None):
        return self.filter_none().first_indexed(function)

    def last_indexed_not_none(self, function=None):
        return self.filter_none().last_indexed(function)

    # Specific functions ========================================

    def group_by(self, fun) -> "Dict":
        return self.map_to_dict(lambda it: (fun(it), it))

    def group_by_not_none(self, fun) -> "Dict":
        return self.map_not_none_to_dict(lambda it: (fun(it), it))

    def associate(self, fun) -> "Dict":
        return self.map_to_dict(fun)

    def associate_not_none(self, fun) -> "Dict":
        return self.map_not_none_to_dict(fun)

    def associate_indexed(self, fun) -> "Dict":
        return self.map_indexed_to_dict(fun)

    def associate_indexed_not_none(self, fun) -> "Dict":
        return self.map_not_none_indexed_to_dict(fun)

    def associate_by(self, fun) -> "Dict":
        return self.map_to_dict(lambda it: (fun(it), it))

    def associate_by_not_none(self, fun) -> "Dict":
        return self.map_not_none_to_dict(lambda it: (fun(it), it))

    def associate_by_indexed(self, fun) -> "Dict":
        return self.map_indexed_to_dict(lambda index, value: (fun(index, value), value))

    def associate_with(self, fun) -> "Dict":
        return self.map_to_dict(lambda it: (it, fun(it)))

    def associate_with_not_none(self, fun) -> "Dict":
        return self.map_not_none_to_dict(lambda it: (it, fun(it)))

    def associate_with_indexed(self, fun) -> "Dict":
        return self.map_indexed_to_dict(lambda index, value: (value, fun(index, value)))

    def associate_with_indexed_not_none(self, fun) -> "Dict":
        return self.map_not_none_indexed_to_dict(lambda index, value: (value, fun(index, value)))

    def __hash__(self):
        return super

    def __eq__(self, other):
        return super


# Instantiation

def list_of(*args):
    return List(args)


def list_from(iterable):
    return List(iterable)
