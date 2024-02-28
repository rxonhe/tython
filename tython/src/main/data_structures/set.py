from __future__ import annotations

from functools import reduce
from itertools import chain
from typing import Any, TYPE_CHECKING, TypeVar, Callable, Type, Iterable

from tython.src.main.data_structures.placeholder import Placeholder

if TYPE_CHECKING:
    from tython.src.main.data_structures.dict import Dict
    from tython.src.main.data_structures.list import List

T = TypeVar("T")


class Set(set):
    set_type: T = Any

    def __hash__(self):
        return str(self).__hash__()

    def __eq__(self, other):
        return self.all(lambda it: it in other)

    def __add__(self, other):
        return Set(set(self).union(other))

    def __sub__(self, other):
        return Set(set(self).difference(other))

    @staticmethod
    def eval(fun) -> Callable:
        if isinstance(fun, Placeholder):
            return fun.eval
        return fun

    # Base functions =============================================

    def zip(self, other: Set) -> Set:
        return Set(zip(self, other))

    def map(self, fun: Callable[[T], Any]) -> Set:
        return Set(map(self.eval(fun), self))

    def filter(self, fun: Callable[[T], Any]) -> Set:
        return Set(filter(self.eval(fun), self))

    def filter_none(self) -> Set[T]:
        return Set(filter(lambda it: it is not None, self))

    def fold(self, fun: Callable, initial_value=None) -> Any:
        if initial_value is None:
            return reduce(self.eval(fun), self)
        return reduce(self.eval(fun), self, initial_value)

    def flatten(self) -> Set:
        return Set(chain(*self))

    def flat_map(self, fun: Callable[[T], Any]) -> Set:
        return self.map(self.eval(fun)).flatten()

    def nested_map(self, fun: Callable[[T], Any]) -> Set:
        return self.map(lambda it: it.map(self.eval(fun)))

    def map_indexed(self, fun: Callable[[int, T], Any]) -> Set:
        return Set(map(lambda it: self.eval(fun)(it[0], it[1]), enumerate(self)))

    def all(self, fun: Callable[[T], Any]) -> bool:
        return all(self.map(self.eval(fun)))

    def none(self, fun: Callable[[T], Any]) -> bool:
        return not any(self.map(self.eval(fun)))

    def any(self, fun: Callable[[T], Any]) -> bool:
        return any(self.map(self.eval(fun)))

    def first(self, fun: Callable[[T], bool] = None) -> T:
        try:
            if fun:
                return next(filter(self.eval(fun), self), Set())
            return next(iter(self), Set())
        except StopIteration:
            return Set()

    def last(self, fun: Callable[[T], bool] = None) -> T:
        return self.first(self.eval(fun))

    def add(self, element) -> Set:
        return Set(self + [element])

    def add_all(self, elements) -> Set:
        return Set(self + elements)

    def remove(self, element) -> Set:
        return Set(filter(lambda it: it != element, self))

    def remove_all(self, elements) -> Set:
        return Set(filter(lambda it: it not in elements, self))

    def length(self) -> int:
        return len(self)

    # Composite funs ========================================

    def map_to_dict(self, fun: Callable[[T], Any]) -> "Dict":
        from tython.src.main.data_structures.dict import Dict
        return Dict(self.map(self.eval(fun)))

    def map_to_list(self, fun: Callable[[T], Any]) -> "List":
        from tython.src.main.data_structures.list import List
        return List(self.map(self.eval(fun)))

    def map_not_none(self, fun: Callable[[T], Any]) -> Set:
        return self.filter_none().map(self.eval(fun)).filter_none()

    def map_not_none_to_dict(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_not_none(self.eval(fun)).map_to_dict(lambda it: it)

    def map_not_none_to_list(self, fun: Callable[[T], Any]) -> "List":
        return self.map_not_none(self.eval(fun)).map_to_list(lambda it: it)

    def map_not_none_indexed(self, fun: Callable[[int, T], Any]) -> Set:
        filtered_indexed = Set(enumerate(self)).filter(lambda it: it[1] is not None)
        return filtered_indexed.map(lambda value: self.eval(fun)(value[0], value[1])).filter_none()

    def map_not_none_indexed_to_dict(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_not_none_indexed(self.eval(fun)).map_to_dict(lambda it: it)

    def map_not_none_indexed_to_list(self, fun: Callable[[int, T], Any]) -> "List":
        return self.map_not_none_indexed(self.eval(fun)).map_to_list(lambda it: it)

    def map_indexed_to_dict(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_indexed(self.eval(fun)).map_to_dict(lambda it: it)

    def map_indexed_to_list(self, fun: Callable[[int, T], Any]) -> "List":
        return self.map_indexed(self.eval(fun)).map_to_list(lambda it: it)

    def flat_map_not_none(self, fun: Callable[[T], Any]) -> Set:
        return self.map_not_none(self.eval(fun)).flatten()

    def flat_map_not_none_to_dict(self, fun: Callable[[T], Any]) -> "Dict":
        return self.flat_map_not_none(self.eval(fun)).map_to_dict(lambda it: it)

    def flat_map_not_none_to_list(self, fun: Callable[[T], Any]) -> "List":
        return self.flat_map_not_none(self.eval(fun)).map_to_list(lambda it: it)

    def flat_map_indexed(self, fun: Callable[[int, T], Any]) -> Set:
        return self.map_indexed(self.eval(fun)).flatten()

    def flat_map_not_none_indexed(self, fun: Callable[[int, T], Any]) -> Set:
        return self.map_not_none_indexed(self.eval(fun)).flatten()

    def flat_map_not_none_indexed_to_dict(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.flat_map_not_none_indexed(self.eval(fun)).map_to_dict(lambda it: it)

    def flat_map_not_none_indexed_to_list(self, fun: Callable[[int, T], Any]) -> "List":
        return self.flat_map_not_none_indexed(self.eval(fun)).map_to_list(lambda it: it)

    def nested_map_not_none(self, fun: Callable[[T], Any]) -> Set:
        return self.map_not_none(self.eval(fun)).nested_map(lambda it: it)

    def nested_map_not_none_to_dict(self, fun: Callable[[T], Any]) -> "Dict":
        return self.nested_map_not_none(self.eval(fun)).map_to_dict(lambda it: it)

    def nested_map_not_none_to_list(self, fun: Callable[[T], Any]) -> "List":
        return self.nested_map_not_none(self.eval(fun)).map_to_list(lambda it: it)

    def nested_map_indexed(self, fun: Callable[[int, T], Any]) -> Set:
        return self.map_indexed(self.eval(fun)).nested_map(lambda it: it)

    def nested_map_not_none_indexed(self, fun: Callable[[int, T], Any]) -> Set:
        return self.map_not_none_indexed(self.eval(fun)).nested_map(lambda it: it)

    def nested_map_not_none_indexed_to_dict(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.nested_map_not_none_indexed(self.eval(fun)).map_to_dict(lambda it: it)

    def nested_map_not_none_indexed_to_list(self, fun: Callable[[int, T], Any]) -> "List":
        return self.nested_map_not_none_indexed(self.eval(fun)).map_to_list(lambda it: it)

    def first_not_none(self, fun: Callable[[T], Any] = None):
        return self.filter_none().first(self.eval(fun))

    def last_not_none(self, fun: Callable[[T], Any] = None):
        return self.filter_none().last(self.eval(fun))

    def first_indexed(self, fun: Callable[[int, T], Any] = None):
        return self.map_indexed(self.eval(fun)).first()

    def last_indexed(self, fun: Callable[[int, T], Any] = None):
        return self.map_indexed(self.eval(fun)).last()

    def first_indexed_not_none(self, fun: Callable[[T], Any] = None):
        return self.filter_none().first_indexed(self.eval(fun))

    def last_indexed_not_none(self, fun: Callable[[T], Any] = None):
        return self.filter_none().last_indexed(self.eval(fun))

    # Specific funs ========================================

    def group_by(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_to_dict(lambda it: (self.eval(fun)(it), it))

    def group_by_not_none(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_not_none_to_dict(lambda it: (self.eval(fun)(it), it))

    def associate(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_to_dict(self.eval(fun))

    def associate_not_none(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_not_none_to_dict(self.eval(fun))

    def associate_indexed(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_indexed_to_dict(self.eval(fun))

    def associate_indexed_not_none(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_not_none_indexed_to_dict(self.eval(fun))

    def associate_by(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_to_dict(lambda it: (self.eval(fun)(it), it))

    def associate_by_not_none(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_not_none_to_dict(lambda it: (self.eval(fun)(it), it))

    def associate_by_indexed(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_indexed_to_dict(lambda index, value: (self.eval(fun)(index, value), value))

    def associate_with(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_to_dict(lambda it: (it, self.eval(fun)(it)))

    def associate_with_not_none(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_not_none_to_dict(lambda it: (it, self.eval(fun)(it)))

    def associate_with_indexed(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_indexed_to_dict(lambda index, value: (value, self.eval(fun)(index, value)))

    def associate_with_indexed_not_none(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_not_none_indexed_to_dict(lambda index, value: (value, self.eval(fun)(index, value)))

    def of_type(self, set_type: Type[T], check: bool = True) -> Set[T]:
        self.set_type = set_type
        if check:
            if self.any(lambda it: not isinstance(it, set_type)):
                raise TypeError(f"Set contains elements that are not of type {set_type}")
        return self

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return self.__repr__()


# Instantiation

def set_of(*args: T) -> Set[T]:
    return Set(args)


def set_from(iterable: Iterable[T]) -> Set[T]:
    return Set(iterable)
