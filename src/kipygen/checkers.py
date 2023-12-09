from typing import Any
from random import choice

from .meta import Checker

__all__ = (
    'AnyValue',
    'AnyValueExcept',
)


class AnyValue(Checker):
    __slots__ = ()

    def send_value(self) -> Any:
        return choice(("123", '1', None, True, False, 12, 2.2, object()))

    def output_value(self, generator_output: Any) -> str:
        return ''

    def name(self) -> str:
        return "Any"

    def description(self) -> str:
        return "любое значение любого типа данных"


class AnyValueExcept(Checker):
    __slots__ = ()

    def __init__(self, value: Any):
        self.value = value

    def send_value(self) -> Any:
        value = self.value
        while value == self.value:
            value = choice(("123", '1', None, True, False, 12, 2.2, object()))
        return value

    def output_value(self, generator_output: Any) -> str:
        if generator_output == self.value:
            return f'Ожидалось любое значение кроме {self.value}, однако оно и получено'
        return ''

    def name(self) -> str:
        return f"Any except {self.value}"

    def description(self) -> str:
        return f"любое значение любого типа данных кроме одного (здесь: {self.value})"
