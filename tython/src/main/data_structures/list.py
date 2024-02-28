from __future__ import annotations

from functools import reduce
from itertools import chain
from typing import Any, TYPE_CHECKING, TypeVar, Callable, Type

from tython.src.main.data_structures.placeholder import Placeholder

if TYPE_CHECKING:
    from tython.src.main.data_structures.dict import Dict
    from tython.src.main.data_structures.set import Set

T = TypeVar("T")


class List(list):
    list_type: T = Any

    @staticmethod
    def eval(fun) -> Callable:
        if isinstance(fun, Placeholder):
            return fun.eval
        return fun

    # Base functions =============================================
    def map(self, fun: Callable[[T], Any]) -> List:
        return List(map(self.eval(fun), self))

    def filter(self, fun: Callable[[T], Any]) -> List:
        return List(filter(self.eval(fun), self))

    def filter_none(self) -> List[T]:
        return List(filter(lambda it: it is not None, self))

    def fold(self, fun: Callable, initial_value=None) -> Any:
        if initial_value is None:
            return reduce(self.eval(fun), self)
        return reduce(self.eval(fun), self, initial_value)

    def flatten(self) -> List:
        return List(chain(*self))

    def flat_map(self, fun: Callable[[T], Any]) -> List:
        return self.map(self.eval(fun)).flatten()

    def nested_map(self, fun: Callable[[T], Any]) -> List:
        return self.map(lambda it: it.map(self.eval(fun)))

    def map_indexed(self, fun: Callable[[int, T], Any]) -> List:
        return List(map(lambda it: self.eval(fun)(it[0], it[1]), enumerate(self)))

    def all(self, fun: Callable[[T], Any]) -> bool:
        return all(self.map(self.eval(fun)))

    def none(self, fun: Callable[[T], Any]) -> bool:
        return not any(self.map(self.eval(fun)))

    def any(self, fun: Callable[[T], Any]) -> bool:
        return any(self.map(self.eval(fun)))

    def reverse(self) -> List:
        return List(reversed(self))

    def first(self, fun: Callable[[T], bool] = None) -> T:
        try:
            if fun:
                return next(filter(self.eval(fun), self), List())
            return next(iter(self), List())
        except StopIteration:
            return List()

    def last(self, fun: Callable[[T], bool] = None) -> T:
        return self.reverse().first(self.eval(fun))

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

    # Composite funs ========================================

    def map_to_dict(self, fun: Callable[[T], Any]) -> "Dict":
        from tython.src.main.data_structures.dict import Dict
        return Dict(self.map(self.eval(fun)))

    def map_to_set(self, fun: Callable[[T], Any]) -> "Set":
        from tython.src.main.data_structures.set import Set
        return Set(self.map(self.eval(fun)))

    def map_not_none(self, fun: Callable[[T], Any]) -> List:
        return self.filter_none().map(self.eval(fun)).filter_none()

    def map_not_none_to_dict(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_not_none(self.eval(fun)).map_to_dict(lambda it: it)

    def map_not_none_to_set(self, fun: Callable[[T], Any]) -> "Set":
        return self.map_not_none(self.eval(fun)).map_to_set(lambda it: it)

    def map_not_none_indexed(self, fun: Callable[[int, T], Any]) -> List:
        filtered_indexed = List(enumerate(self)).filter(lambda it: it[1] is not None)
        return filtered_indexed.map(lambda value: self.eval(fun)(value[0], value[1])).filter_none()

    def map_not_none_indexed_to_dict(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_not_none_indexed(self.eval(fun)).map_to_dict(lambda it: it)

    def map_not_none_indexed_to_set(self, fun: Callable[[int, T], Any]) -> "Set":
        return self.map_not_none_indexed(self.eval(fun)).map_to_set(lambda it: it)

    def map_indexed_to_dict(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_indexed(self.eval(fun)).map_to_dict(lambda it: it)

    def map_indexed_to_set(self, fun: Callable[[int, T], Any]) -> "Set":
        return self.map_indexed(self.eval(fun)).map_to_set(lambda it: it)

    def flat_map_not_none(self, fun: Callable[[T], Any]) -> List:
        return self.map_not_none(self.eval(fun)).flatten()

    def flat_map_not_none_to_dict(self, fun: Callable[[T], Any]) -> "Dict":
        return self.flat_map_not_none(self.eval(fun)).map_to_dict(lambda it: it)

    def flat_map_not_none_to_set(self, fun: Callable[[T], Any]) -> "Set":
        return self.flat_map_not_none(self.eval(fun)).map_to_set(lambda it: it)

    def flat_map_indexed(self, fun: Callable[[int, T], Any]) -> List:
        return self.map_indexed(self.eval(fun)).flatten()

    def flat_map_not_none_indexed(self, fun: Callable[[int, T], Any]) -> List:
        return self.map_not_none_indexed(self.eval(fun)).flatten()

    def flat_map_not_none_indexed_to_dict(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.flat_map_not_none_indexed(self.eval(fun)).map_to_dict(lambda it: it)

    def flat_map_not_none_indexed_to_set(self, fun: Callable[[int, T], Any]) -> "Set":
        return self.flat_map_not_none_indexed(self.eval(fun)).map_to_set(lambda it: it)

    def nested_map_not_none(self, fun: Callable[[T], Any]) -> List:
        return self.map_not_none(self.eval(fun)).nested_map(lambda it: it)

    def nested_map_not_none_to_dict(self, fun: Callable[[T], Any]) -> "Dict":
        return self.nested_map_not_none(self.eval(fun)).map_to_dict(lambda it: it)

    def nested_map_not_none_to_set(self, fun: Callable[[T], Any]) -> "Set":
        return self.nested_map_not_none(self.eval(fun)).map_to_set(lambda it: it)

    def nested_map_indexed(self, fun: Callable[[int, T], Any]) -> List:
        return self.map_indexed(self.eval(fun)).nested_map(lambda it: it)

    def nested_map_not_none_indexed(self, fun: Callable[[int, T], Any]) -> List:
        return self.map_not_none_indexed(self.eval(fun)).nested_map(lambda it: it)

    def nested_map_not_none_indexed_to_dict(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.nested_map_not_none_indexed(self.eval(fun)).map_to_dict(lambda it: it)

    def nested_map_not_none_indexed_to_set(self, fun: Callable[[int, T], Any]) -> "Set":
        return self.nested_map_not_none_indexed(self.eval(fun)).map_to_set(lambda it: it)

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

    def of_type(self, list_type: Type[T], check: bool = True) -> List[T]:
        self.list_type = list_type
        if check:
            if self.any(lambda it: not isinstance(it, list_type)):
                raise TypeError(f"List contains elements that are not of type {list_type}")
        return self


# Instantiation

def list_of(*args: T) -> List[T]:
    return List(args)


def list_from(iterable: list[T]) -> List[T]:
    return List(iterable)
