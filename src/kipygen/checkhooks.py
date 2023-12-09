from typing import Any, Union, Type, Generator

__all__ = (
    'CheckHook',
    'GenThrow',
)


class CheckHook:
    """
    Checker class, but in comparison with Checker, this class invoked with generator
    and corresponding arguments. This class can be placed ONLY in send list

    Example:
    >>>class Forward(CheckHook):
    ...    __slots__ = ('value', )
    ...
    ...    def __init__(self, value: Any):
    ...        self.value = value
    ...
    ...    def __call__(
    ...        self,
    ...        function: callable,
    ...        gen: Generator,
    ...        send_value: Any,
    ...        timeout: Union[int, float]
    ...    ) -> Any:
    ...        return function(gen.send, self.value, timeout)
    This class simply do nothing. Example of ValueTuple.send with and without:
    without: [1, 2, 3]
    with: [1, Forward(2), 3]
    """
    __slots__ = ()

    def __call__(
        self,
        function: callable,
        gen: Generator,
        send_value: Any,
        timeout: Union[int, float]
    ) -> Any:
        """ Called when needed next value from generator
        :param function: Intermediate function to call generator methods
        :param gen: Running generator to validate
        :param send_value: Value, passing to generator (send_value == self)
        :param timeout: how many second wait answer from generator thread
        :return: value from generator
        """
        return function(gen.send, send_value, timeout)

    def name(self) -> str:
        raise NotImplementedError()

    def description(self) -> str:
        raise NotImplementedError()


class GenThrow(CheckHook):
    __slots__ = ('exception',)

    def __init__(self, exception: Type[BaseException]):
        isinstance(exception, BaseException)
        self.exception = exception

    def __call__(
        self,
        function: callable,
        gen: Generator,
        send_value: Any,
        timeout: Union[int, float]
    ) -> Any:
        return function(gen.throw, self.exception, timeout)

    def name(self) -> str:
        return f"Отправка исключения {self.exception.__qualname__}"

    def description(self) -> str:
        return (
            f"В генератор отправляется исключение с помощью метода Generator.throw()"
            f" (здесь: исключение {self.exception.__qualname__})"
        )
