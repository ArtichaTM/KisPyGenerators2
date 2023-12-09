from typing import Any, Type
from random import choice

__all__ = (
    'Checker',
    'AnyValue',
    'AnyValueExcept',
    'AnyValueExceptType',
)


class Checker:
    """
    Checker class, to verify generator correctness
    send_value or output_value can be undefined. In that case, this
    checker should not be used in corresponding lists
    """
    def send_value(self) -> Any:
        """ Called when Checker place in send values list"""
        raise NotImplementedError()

    def output_value(self, generator_output: Any) -> str:
        """ Called when during validating Checker in awaited list
        :param generator_output: Output of generator
        :return: String, containing error. Empty string, if everything correct
        """
        raise NotImplementedError()

    def name(self) -> str:
        """ Called when filling send/awaited values in example for user """
        raise NotImplementedError()

    def description(self) -> str:
        """
        Called after all send/awaited values printed
        to specify checker functionality
        """
        raise NotImplementedError()


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
    __slots__ = ('value',)

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


class AnyValueExceptType(Checker):
    __slots__ = ('dtype', )

    def __init__(self, dtype: Type[Any]):
        self.dtype = dtype

    def send_value(self) -> Any:
        while True:
            value = choice(("123", '1', None, True, False, 12, 2.2, object()))
            if not isinstance(value, self.dtype):
                break
        return value

    def output_value(self, generator_output: Any) -> str:
        if isinstance(generator_output, self.dtype):
            return f'Ожидался любой тип данных кроме {self.dtype}, однако этот тип и получен'
        return ''

    def name(self) -> str:
        return f"Any type except {self.dtype.__qualname__}"

    def description(self) -> str:
        return (f"любое значение любого типа данных кроме одного типа данных "
                f"(здесь: {self.dtype.__qualname__})")
