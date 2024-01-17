from __future__ import annotations

import inspect
from typing import Any


class Nullable:
    _init_type = Any

    def __init__(self, contained=None):
        if isinstance(contained, type):
            self._init_type = contained
            contained = None
        self._contained = contained

    def __getattr__(self, name):
        _contained_vars = dict(vars(self._init_type))
        if name not in _contained_vars:
            raise AttributeError(f"Attribute/Method {name} not found for type {self._init_type}")
        name_ = _contained_vars[name]
        _is_method = inspect.ismethoddescriptor(name_) or inspect.isfunction(name_) or inspect.ismethod(name_)
        if _is_method:
            return getattr(self._contained, name, lambda *args, **kwargs: None)
        return getattr(self._contained, name, None)
