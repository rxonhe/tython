from __future__ import annotations

import inspect
from typing import Any, Union
from typing import Generic, TypeVar

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

T = TypeVar("T")
IGNORE = {Any}


class Nullable(Generic[T]):
    _init_type = Any
    _contained: T = None

    def __init__(self, contained: T = None):
        if isinstance(contained, type):
            self._init_type = contained
            contained = None
        self._contained = contained

    def __call__(self, *args, **kwargs):
        if self._contained is None:
            return self._init_type(*args, **kwargs)
        return self._contained(*args, **kwargs)

    def __getitem__(self, item: T) -> T:
        return Union[T, Nullable]

    def __getattr__(self, name):
        _contained_vars = dict(self._init_type.__dict__)
        if name not in _contained_vars:
            raise AttributeError(f"Attribute/Method {name} not found for type {self._init_type}")
        name_ = _contained_vars[name]
        _is_method = inspect.ismethoddescriptor(name_) or inspect.isfunction(name_) or inspect.ismethod(name_)
        if _is_method:
            return getattr(self._contained, name, lambda *args, **kwargs: None)
        return getattr(self._contained, name, None)

    def __str__(self) -> str:
        return ""

    def __int__(self) -> int:
        return 0

    def __float__(self) -> float:
        return 0.0

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return repr(self._contained)

    def __hash__(self):
        return hash(self._contained)

    def __eq__(self, other):
        return self._contained == other

    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            _: Any,
            handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(cls._init_type))
