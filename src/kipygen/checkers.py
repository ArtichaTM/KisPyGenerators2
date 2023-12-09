from typing import Any
from random import choice

from .meta import Checker

__all__ = (
    'Any',
)


class AnyValue(Checker):
    def send_value(self) -> Any:
        return choice(("123", '1', None, True, False, 12, 2.2, object()))

    def output_value(self, generator_output: Any) -> str:
        return ''

    @staticmethod
    def name() -> str:
        return "Any"

    @staticmethod
    def description() -> str:
        return "любое значение любого типа данных"
