from __future__ import annotations

from functools import reduce
from typing import Optional, List, Callable, TypeVar, Type

T = TypeVar("T")


class Placeholder:

    def __init__(self, operations: Optional[List[EvalPair]] = None, placeholder_type: [Type[T]] = None):
        if placeholder_type:
            self.placeholder_type = placeholder_type
        self.operations = operations

    def eval(self, value):
        if self.operations:
            return reduce(lambda acc, operation: operation.eval(acc), self.operations, value)
        return value

    def monad(self, operation, other=None):
        if self.operations is None:
            return Placeholder([EvalPair(operation, other)])
        return Placeholder(self.operations + [EvalPair(operation, other)])

    def __add__(self, other):
        return self.monad(lambda x: x + other, other)

    def __radd__(self, other):
        return self.monad(lambda x: other + x, other)

    def __sub__(self, other):
        return self.monad(lambda x: x - other, other)

    def __rsub__(self, other):
        return self.monad(lambda x: other - x, other)

    def __mul__(self, other):
        return self.monad(lambda x: x * other, other)

    def __rmul__(self, other):
        return self.monad(lambda x: other * x, other)

    def __truediv__(self, other):
        return self.monad(lambda x: x / other, other)

    def __rtruediv__(self, other):
        return self.monad(lambda x: other / x, other)

    def __floordiv__(self, other):
        return self.monad(lambda x: x // other, other)

    def __rfloordiv__(self, other):
        return self.monad(lambda x: other // x, other)

    def __mod__(self, other):
        return self.monad(lambda x: x % other, other)

    def __rmod__(self, other):
        return self.monad(lambda x: other % x, other)

    def __pow__(self, other):
        return self.monad(lambda x: x ** other, other)

    def __rpow__(self, other):
        return self.monad(lambda x: other ** x, other)

    def __lshift__(self, other):
        return self.monad(lambda x: x << other, other)

    def __rlshift__(self, other):
        return self.monad(lambda x: other << x, other)

    def __rshift__(self, other):
        return self.monad(lambda x: x >> other, other)

    def __rrshift__(self, other):
        return self.monad(lambda x: other >> x, other)

    def __and__(self, other):
        return self.monad(lambda x: x & other, other)

    def __rand__(self, other):
        return self.monad(lambda x: other & x, other)

    def __xor__(self, other):
        return self.monad(lambda x: x ^ other, other)

    def __rxor__(self, other):
        return self.monad(lambda x: other ^ x, other)

    def __or__(self, other):
        return self.monad(lambda x: x | other, other)

    def __ror__(self, other):
        return self.monad(lambda x: other | x, other)

    def __neg__(self):
        return self.monad(lambda x: -x)

    def __pos__(self):
        return self.monad(lambda x: +x)

    def __abs__(self):
        return self.monad(lambda x: abs(x))

    def __invert__(self):
        return self.monad(lambda x: ~x)

    def __lt__(self, other):
        return self.monad(lambda x: x < other, other)

    def __le__(self, other):
        return self.monad(lambda x: x <= other, other)

    def __eq__(self, other):
        return self.monad(lambda x: x == other, other)

    def __ne__(self, other):
        return self.monad(lambda x: x != other, other)

    def __gt__(self, other):
        return self.monad(lambda x: x > other, other)

    def __ge__(self, other):
        return self.monad(lambda x: x >= other, other)

    def __contains__(self, other):
        return self.monad(lambda x: other in x, other)

    def __getitem__(self, other):
        return self.monad(lambda x: x[other], other)

    def __getattr__(self, other):
        return self.monad(lambda x: getattr(x, other), other)

    def __call__(self, *args, **kwargs):
        return self.monad(lambda x: x(*args, **kwargs))

    def __iter__(self):
        return self.monad(lambda x: iter(x))

    def __next__(self):
        return self.monad(lambda x: next(x))

    def __len__(self):
        return self.monad(lambda x: len(x))

    @property
    def iter(self):
        """
        Callable iter() alternative
        """
        return self.monad(lambda x: iter(x))

    @property
    def size(self):
        """
        Callable len() alternative
        """
        return self.monad(lambda x: len(x))

    @property
    def next(self):
        """
        Callable next() alternative
        """
        return self.monad(lambda x: next(x))

    @property
    def reversed(self):
        """
        Callable reversed() alternative
        """
        return self.monad(lambda x: reversed(x))

    def __bool__(self):
        return self.monad(lambda x: bool(x))

    def __repr__(self):
        if not self.operations:
            return "self"
        operations_repr = ".".join(list(map(str, self.operations)))
        return f"self.{operations_repr}"

    def __str__(self):
        return self.__repr__()

    def __format__(self, format_spec):
        return self.__repr__()


class EvalPair:
    def __init__(self, operation: Callable, value):
        self.operation = operation
        self.value = value

    def __repr__(self):
        value_repr = self.value or ""
        return f"{self.get_op_name()}({value_repr})"

    def eval(self, other):
        try:
            return self.operation(other)
        except Exception:
            raise Exception(f"Error evaluating {self.get_op_name()}({other})")

    def get_op_name(self):
        try:
            return str(self.operation).split(".")[1]
        except Exception:
            str(self.operation)
