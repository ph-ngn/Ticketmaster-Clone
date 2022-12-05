from typing import TypeVar, Type, Union
from .value_objects import *
from .rules import *


class ToDictMixin:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, attrs: dict) -> dict:
        return {k: self._traverse(v) for k, v in attrs.items() if not k.startswith('_')}

    def _traverse(self, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, (list, set)):
            return [self._traverse(v) for v in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value
