from typing import Any, Type
from random import choice

__all__ = (
    'Raised',
    'Checker',
    'AnyValue',
    'AnyValueExcept',
    'AnyValueExceptType',
)


class Raised:
    __slots__ = ('exception',)

    def __init__(self, e: BaseException):
        self.exception = e

    def __repr__(self) -> str:
        return f"<Raised {type(self.exception).__qualname__}({self.exception.args})>"


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


class Except(Checker):
    __slots__ = ('exception',)

    def __init__(self, exception: Type[BaseException]):
        assert issubclass(exception, BaseException)
        self.exception = exception

    def output_value(self, exception: Raised) -> str:
        assert isinstance(exception, Raised)
        exception = exception.exception
        assert isinstance(exception, BaseException)
        v = (
            f'Ожидалось исключение {self.exception.__qualname__}, '
            f'однако получено {type(exception).__qualname__}'
        )
        if not isinstance(exception, self.exception):
            return v
        elif type(exception) is not self.exception:
            return v
        return 'FINISH'

    def name(self) -> str:
        return f"Raised {type(self.exception).__qualname__}"

    def description(self) -> str:
        return (
            "Вызванное генератором исключение нужного класса "
            f"(здесь: {type(self.exception)})"
        )


class ExceptWithArgs(Checker):
    __slots__ = ('exception',)

    def __init__(self, exception: BaseException):
        self.exception = exception

    def output_value(self, exception: BaseException) -> str:
        v = (
            f'Ожидалось исключение {type(self.exception).__qualname__}, '
            f'однако получено {type(exception).__qualname__}'
        )
        if not isinstance(exception, type(self.exception)):
            return v
        elif type(exception) is not type(self.exception):
            return v
        expected_arguments = self.exception.args
        got_arguments = exception.args
        if len(expected_arguments) != len(got_arguments):
            return (
                f"Ожидалось исключение с {len(expected_arguments)} аргументами, "
                f"однако исключение {type(exception).__qualname__} "
                f"имеет {len(got_arguments)} аргументов"
            )
        for i in range(len(expected_arguments)):
            expected = expected_arguments[i]
            got = got_arguments[i]
            if expected != got:
                return f"{i+1} аргумент исключения должен быть {expected}, однако получено {got}"
        return ''

    def name(self) -> str:
        return f"Raised {type(self.exception).__qualname__}({self.exception.args})"

    def description(self) -> str:
        return (
            "Вызванное генератором исключение нужного класса и с нужными аргументами "
            f"(здесь: исключение={type(self.exception)}, аргументы={self.exception.args})"
        )
