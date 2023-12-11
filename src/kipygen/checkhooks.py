from queue import Queue
from typing import Any, Type, Generator

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
    ...        q_in: Queue,
    ...        q_out: Queue,
    ...        gen: Generator
    ...    ) -> Any:
    ...        q_in.put((gen, self.value))
    ...        return q_out.get()
    This class simply do nothing. Example of ValueTuple.send with and without:
    without: [1, 2, 3]
    with: [1, Forward(2), 3]
    """
    __slots__ = ()

    def __repr__(self) -> str:
        return f"<CheckHook {type(self).__qualname__}>"

    def __call__(
        self,
        q_in: Queue,
        q_out: Queue,
        gen: Generator
    ) -> Any:
        """ Called when needed next value from generator
        :param q_in: Queue of value passing to generator
        :param q_out: Queue of value coming from generator
        :param gen: Running generator to validate
        :return: value from generator
        """
        raise NotImplementedError()

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
        q_in: Queue,
        q_out: Queue,
        gen: Generator
    ) -> Any:
        q_in.put((gen.throw, self.exception))
        return q_out.get()

    def name(self) -> str:
        return f"Отправка исключения {self.exception.__qualname__}"

    def description(self) -> str:
        return (
            f"В генератор отправляется исключение с помощью метода Generator.throw()"
            f" (здесь: исключение {self.exception.__qualname__})"
        )
