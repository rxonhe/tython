from __future__ import annotations

from functools import reduce
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from tython.src.main.data_structures.dict import Dict
    from tython.src.main.data_structures.list import List


class Set(set):

    # Base functions =============================================
    def map(self, fun) -> Set:
        return Set(map(fun, self))

    def filter(self, fun) -> Set:
        return Set(filter(fun, self))

    def filter_none(self) -> Set:
        return Set(filter(lambda it: it is not None, self))

    def fold(self, fun, initial_value=None) -> Any:
        if initial_value is None:
            return reduce(fun, self)
        return reduce(fun, self, initial_value)

    def flatten(self) -> Set:
        _init_set = Set()
        for it in self:
            _init_set = _init_set.union(it)
        return _init_set

    def flat_map(self, fun) -> Set:
        _init_set = Set()
        for it in self:
            _init_set = _init_set.union(fun(it))
        return _init_set

    def map_indexed(self, fun) -> Set:
        return Set(map(lambda it: fun(it[0], it[1]), enumerate(self)))

    def all(self, fun) -> bool:
        return all(self.map(fun))

    def none(self, fun) -> bool:
        return not any(self.map(fun))

    def any(self, fun) -> bool:
        return any(self.map(fun))

    def first(self, function=None):
        """
        Keep in mind that sets are unordered, so this function is not deterministic.
        """
        try:
            if function:
                return next(filter(function, self), Set())
            return next(iter(self), Set())
        except StopIteration:
            return Set()

    def last(self, function=None):
        """
        Keep in mind that sets are unordered, so this function is not deterministic.
        """
        return self.first(function)

    # Composite functions ========================================

    def map_to_dict(self, fun) -> "Dict":
        from tython.src.main.data_structures.dict import Dict
        return Dict(self.map(fun))

    def map_to_list(self, fun) -> "List":
        from tython.src.main.data_structures.list import List
        return List(self.map(fun))

    def map_not_none(self, fun) -> Set:
        return self.filter_none().map(fun).filter_none()

    def map_not_none_to_dict(self, fun) -> "Dict":
        return self.map_not_none(fun).map_to_dict(lambda it: it)

    def map_not_none_to_list(self, fun) -> "List":
        return self.map_not_none(fun).map_to_list(lambda it: it)

    def map_not_none_indexed(self, fun) -> Set:
        return self.filter_none().map_indexed(lambda index, value: (index, fun(index, value))).filter_none()

    def map_not_none_indexed_to_dict(self, fun) -> "Dict":
        return self.map_not_none_indexed(fun).map_to_dict(lambda it: it)

    def map_not_none_indexed_to_list(self, fun) -> "List":
        return self.map_not_none_indexed(fun).map_to_list(lambda it: it)

    def map_indexed_to_dict(self, fun) -> "Dict":
        return self.map_indexed(fun).map_to_dict(lambda it: it)

    def map_indexed_to_list(self, fun) -> "List":
        return self.map_indexed(fun).map_to_list(lambda it: it)

    def flat_map_not_none(self, fun) -> Set:
        return self.map_not_none(fun).flatten()

    def flat_map_not_none_to_dict(self, fun) -> "Dict":
        return self.flat_map_not_none(fun).map_to_dict(lambda it: it)

    def flat_map_not_none_to_list(self, fun) -> "List":
        return self.flat_map_not_none(fun).map_to_list(lambda it: it)

    def flat_map_indexed(self, fun) -> Set:
        return self.map_indexed(fun).flatten()

    def flat_map_not_none_indexed(self, fun) -> Set:
        return self.map_not_none_indexed(fun).flatten()

    def flat_map_not_none_indexed_to_dict(self, fun) -> "Dict":
        return self.flat_map_not_none_indexed(fun).map_to_dict(lambda it: it)

    def flat_map_not_none_indexed_to_list(self, fun) -> "List":
        return self.flat_map_not_none_indexed(fun).map_to_list(lambda it: it)

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

    def add(self, element) -> Set:
        return Set(self.union({element}))

    def add_all(self, elements) -> Set:
        return Set(self.union(elements))

    def remove(self, element) -> Set:
        return Set(filter(lambda it: it != element, self))

    def remove_all(self, elements) -> Set:
        return Set(filter(lambda it: it not in elements, self))

    def length(self) -> int:
        return len(self)

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

def set_of(*args):
    return Set(args)


def set_from(iterable):
    return Set(iterable)
