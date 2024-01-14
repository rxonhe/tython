from typing import TypeVar, Type

T = TypeVar("T")


class AbstractKey:
    _delegated_attrs = dict()

    @classmethod
    def delegate(cls, delegated_class: Type[T]) -> T:
        """
        Use this decorator to delegate attributes from the delegated_class to the Key class.
        """
        class_items = dict(delegated_class.__dict__).get("__annotations__")
        for key in class_items.keys():
            setattr(delegated_class, key, key)
        cls._delegated_attrs.update(class_items)
        return delegated_class()

    @classmethod
    def get_type(cls, key):
        return cls._delegated_attrs.get(key)
