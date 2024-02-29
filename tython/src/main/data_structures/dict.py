from __future__ import annotations

from functools import reduce
from itertools import chain
from typing import Callable, Any, TypeVar

from tython.src.main.data_structures.placeholder import Placeholder

T = TypeVar("T")


class Dict(dict):

    @staticmethod
    def eval(fun) -> Callable:
        if isinstance(fun, Placeholder):
            return fun.eval
        return fun

    # Base functions =============================================
    def map_keys(self, fun: Callable[[T], Any]) -> Dict:
        return Dict({self.eval(fun)(key, value): value for key, value in self.items()})

    def map_values(self, fun: Callable[[T], Any]) -> Dict:
        return Dict({key: self.eval(fun)(key, value) for key, value in self.items()})

    def map(self, fun: Callable[[T], Any]) -> Dict:
        return Dict((self.eval(fun)(key, value) for key, value in self.items()))

    def filter(self, fun: Callable[[T], Any]) -> Dict:
        return Dict(filter(lambda it: self.eval(fun)(it[0], it[1]), self.items()))

    def filter_none(self) -> Dict:
        return Dict(filter(lambda it: it[1] is not None, self.items()))

    def fold(self, fun: Callable, initial_value=None) -> Any:
        if initial_value is None:
            return reduce(self.eval(fun), self)
        return reduce(self.eval(fun), self, initial_value)

    def flatten(self) -> Dict:
        return Dict(chain(*self))

    def flat_map_values(self, fun: Callable[[T], Any]) -> Dict:
        return self.map_values(self.eval(fun)).flatten()

    def flat_map_keys(self, fun: Callable[[T], Any]) -> Dict:
        return self.map_keys(self.eval(fun)).flatten()

    def flat_map(self, fun: Callable[[T], Any]) -> Dict:
        return self.map(self.eval(fun)).flatten()

    def nested_map(self, fun: Callable[[T], Any]) -> Dict:
        return self.map(lambda it: it.map(self.eval(fun)))

    def nested_map_values(self, fun: Callable[[T], Any]) -> Dict:
        return self.map_values(lambda it: it.map_values(self.eval(fun)))

    def nested_map_keys(self, fun: Callable[[T], Any]) -> Dict:
        return self.map_keys(lambda it: it.map_keys(self.eval(fun)))

    def map_indexed(self, fun: Callable[[int, T], Any]) -> Dict:
        return Dict((self.eval(fun)(index, key, value) for index, (key, value) in enumerate(self)))

    def map_indexed_values(self, fun: Callable[[int, T], Any]) -> Dict:
        return Dict({key: self.eval(fun)(index, key, value) for index, (key, value) in enumerate(self)})

    def map_indexed_keys(self, fun: Callable[[int, T], Any]) -> Dict:
        return Dict({self.eval(fun)(index, key, value): value for index, (key, value) in enumerate(self)})

    def all(self, fun: Callable[[T], Any]) -> bool:
        return all((self.eval(fun)(key, value) for key, value in self.items()))

    def none(self, fun: Callable[[T], Any]) -> bool:
        return not any((self.eval(fun)(key, value) for key, value in self.items()))

    def any(self, fun: Callable[[T], Any]) -> bool:
        return any((self.eval(fun)(key, value) for key, value in self.items()))

    def reverse(self) -> Dict:
        return Dict(reversed(self))

    def first(self, fun: Callable[[T], bool] = None) -> T:
        try:
            if fun:
                return next(filter(lambda it: self.eval(fun)(it[0], it[1]), self.items()))
            return next(iter(self.items()), Dict())
        except StopIteration:
            return Dict()

    def last(self, fun: Callable[[T], bool] = None) -> T:
        return self.reverse().first(self.eval(fun))

    def length(self) -> int:
        return len(self)

    # Composite funs ========================================

    def map_not_none(self, fun: Callable[[T], Any]) -> Dict:
        return self.filter_none().map(self.eval(fun)).filter_none()

    def map_not_none_values(self, fun: Callable[[T], Any]) -> Dict:
        return self.filter_none().map_values(self.eval(fun)).filter_none()

    def map_not_none_keys(self, fun: Callable[[T], Any]) -> Dict:
        return self.filter_none().map_keys(self.eval(fun)).filter_none()

    def map_not_none_indexed(self, fun: Callable[[int, T], Any]) -> Dict:
        filtered_indexed = Dict(enumerate(self)).filter(lambda it: it[1] is not None)
        return filtered_indexed.map(lambda value: self.eval(fun)(value[0], value[1])).filter_none()

    def map_not_none_indexed_values(self, fun: Callable[[int, T], Any]) -> Dict:
        filtered_indexed = Dict(enumerate(self)).filter(lambda it: it[1] is not None)
        return filtered_indexed.map_values(lambda value: self.eval(fun)(value[0], value[1])).filter_none()

    def map_not_none_indexed_keys(self, fun: Callable[[int, T], Any]) -> Dict:
        filtered_indexed = Dict(enumerate(self)).filter(lambda it: it[1] is not None)
        return filtered_indexed.map_keys(lambda value: self.eval(fun)(value[0], value[1])).filter_none()

    def flat_map_not_none(self, fun: Callable[[T], Any]) -> Dict:
        return self.map_not_none(self.eval(fun)).flatten()

    def flat_map_not_none_values(self, fun: Callable[[T], Any]) -> Dict:
        return self.map_not_none_values(self.eval(fun)).flatten()

    def flat_map_not_none_keys(self, fun: Callable[[T], Any]) -> Dict:
        return self.map_not_none_keys(self.eval(fun)).flatten()

    def flat_map_indexed(self, fun: Callable[[int, T], Any]) -> Dict:
        return self.map_indexed_values(self.eval(fun)).flatten()

    def flat_map_indexed_values(self, fun: Callable[[int, T], Any]) -> Dict:
        return self.map_indexed_keys(self.eval(fun)).flatten()

    def flat_map_indexed_keys(self, fun: Callable[[int, T], Any]) -> Dict:
        return self.map_indexed(self.eval(fun)).flatten()

    def flat_map_not_none_indexed(self, fun: Callable[[int, T], Any]) -> Dict:
        return self.map_not_none_indexed(self.eval(fun)).flatten()

    def nested_map_not_none(self, fun: Callable[[T], Any]) -> Dict:
        return self.map_not_none(self.eval(fun)).nested_map(lambda it: it)

    def nested_map_indexed(self, fun: Callable[[int, T], Any]) -> Dict:
        return self.map_indexed(self.eval(fun)).nested_map(lambda it: it)

    def nested_map_not_none_indexed(self, fun: Callable[[int, T], Any]) -> Dict:
        return self.map_not_none_indexed(self.eval(fun)).nested_map(lambda it: it)

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
        return self.map(lambda it: (self.eval(fun)(it), it))

    def group_by_not_none(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_not_none(lambda it: (self.eval(fun)(it), it))

    def associate(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map(self.eval(fun))

    def associate_not_none(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_not_none(self.eval(fun))

    def associate_indexed(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_indexed(self.eval(fun))

    def associate_indexed_not_none(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_not_none_indexed(self.eval(fun))

    def associate_by(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_keys(lambda it: self.eval(fun)(it))

    def associate_by_not_none(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_not_none_keys(lambda it: self.eval(fun)(it))

    def associate_by_indexed(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_not_none_indexed_keys(lambda index, value: self.eval(fun)(index, value))

    def associate_with(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_values(lambda it: self.eval(fun)(it))

    def associate_with_not_none(self, fun: Callable[[T], Any]) -> "Dict":
        return self.map_not_none_values(lambda it: self.eval(fun)(it))

    def associate_with_indexed(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_indexed_values(lambda index, value: (value, self.eval(fun)(index, value)))

    def associate_with_indexed_not_none(self, fun: Callable[[int, T], Any]) -> "Dict":
        return self.map_not_none_indexed_values(lambda index, value: self.eval(fun)(index, value))


def dict_of(**kwargs):
    return Dict(**kwargs)


def dict_from(args):
    return Dict(args)
