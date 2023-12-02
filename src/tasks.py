from typing import Generator, Any, Tuple, TypeVar, Union
from io import StringIO
from random import choices, triangular

from .meta import TaskMeta, ValuesTuple


__all__ = (
    'TaskPassword',
    'TaskRange',
    'TaskConcat',
    'TaskCalculator',
    'iterations_limit',
)


T = TypeVar('T')


def triangular_int(low: int, high: int, mode: int) -> int:
    return int(triangular(low, high, mode))


def iterations_limit(gen: Generator[T, None, None], limit: int) -> Generator[T, None, None]:
    assert isinstance(limit, int)
    try:
        for _ in range(limit):
            yield next(gen)
    except StopIteration:
        return


class TaskRange(metaclass=TaskMeta):
    complexity = 1
    _gen_annotation = Generator[int, int, None]

    @staticmethod
    def generator() -> _gen_annotation:
        start = yield
        start -= 1
        end = yield
        while start <= end:
            yield start
            start += 1

    @classmethod
    def check_values(cls) -> Generator[ValuesTuple, None, None]:
        yield from (
            ValuesTuple(
                [1, 3, None, None, None],
                [None, 0, 1, 2, 3]
            ),
            ValuesTuple(
                [1, 4, None, None, None, None],
                [None, 0, 1, 2, 3, 4]
            ),
            ValuesTuple(
                [123, 127, None, None, None, None, None],
                [None, 122, 123, 124, 125, 126, 127]
            ),
        )


class TaskConcat(metaclass=TaskMeta):
    complexity = 3
    _gen_annotation = Generator[str, str, None]
    _all_values: str = None
    _choices_max: int = None

    @classmethod
    def _random_string(cls) -> str:
        return ''.join(choices(cls._all_values, k=triangular_int(0, cls._choices_max, 10)))

    @staticmethod
    def generator() -> _gen_annotation:
        string = StringIO()
        value = yield
        while isinstance(value, str):
            string.write(value)
            value = yield
        yield string.getvalue()

    @classmethod
    def check_values(cls) -> Generator[ValuesTuple, None, None]:
        if cls._all_values is None:
            cls._all_values = ''.join([chr(i) for i in range(0, 50000)])
            cls._choices_max = int(len(cls._all_values) ** 0.5)

        while True:
            output = ValuesTuple([], [])
            local_io = StringIO()
            for _ in range(triangular_int(0, 20, 2)):
                value = cls._random_string()
                local_io.write(value)
                output.send.append(value)
                output.awaited.append(None)
            output.send.append(None)
            output.awaited.append(local_io.getvalue())
            yield output


class TaskPassword(metaclass=TaskMeta):
    complexity = 2
    _gen_annotation = Generator[bool, Any, None]

    @staticmethod
    def generator() -> _gen_annotation:
        password = yield
        new_password = yield
        while True:
            if new_password == password:
                break
            new_password = yield False
        yield True

    @classmethod
    def check_values(cls) -> Generator[ValuesTuple, None, None]:
        checker = object()
        yield from (
            ValuesTuple(
                ["Password", 2, '', "Password"],
                [None, False, False, True]
            ),
            ValuesTuple(
                [1, 2, '', 1],
                [None, False, False, True]
            ),
            ValuesTuple(
                [1, 1],
                [None, True]
            ),
            ValuesTuple(
                ['', ''],
                [None, True]
            ),
            ValuesTuple(
                [checker, checker],
                [None, True]
            ),
        )


class TaskCalculator(metaclass=TaskMeta):
    complexity = 5
    _number = Union[float, int]
    _gen_annotation = Generator[_number, Tuple[str, _number], None]

    @staticmethod
    def generator() -> _gen_annotation:
        output = yield 0
        while True:
            values = yield output
            if values is None:
                break
            operation, new_number = values
            if operation == '+':
                output += new_number
            elif operation == '-':
                output -= new_number
            elif operation == '/':
                if new_number == 0:
                    continue
                output /= new_number
            elif operation == '*':
                output *= new_number
            if output == int(output):
                output = int(output)

    @classmethod
    def check_values(cls) -> Generator[ValuesTuple, None, None]:
        yield from (
            ValuesTuple(
                [0, ('+', 5), None],
                [0, 5]
            ),
            ValuesTuple(
                [70, ('*', 2), None],
                [70, 140]
            ),
            ValuesTuple(
                [70, ('*', 2), ('-', 2), None],
                [70, 140, 138]
            ),
            ValuesTuple(
                [3, ('/', 2), ('*', 2), None],
                [3, 1.5, 3]
            ),
            ValuesTuple(
                [3, ('/', 2), ('*', 2), None],
                [3, 1.5, 3]
            ),
            ValuesTuple(
                [70, ('/', 0), ('+', 1), None],
                [70, 70, 71]
            ),
        )
