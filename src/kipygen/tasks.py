from itertools import chain
from typing import Generator, Any, Tuple, TypeVar, Union
from io import StringIO
from random import choices, choice, randint, triangular

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
        end = yield
        while start <= end:
            yield start
            start += 1

    @classmethod
    def check_values(cls) -> Generator[ValuesTuple, None, None]:
        # while True:
        #     start = randint(-65536, 65536)
        #     end = start + randint(0, 65536)
        yield from (
            ValuesTuple(
                [1, 3, None, None],
                [None, 1, 2, 3]
            ),
            ValuesTuple(
                [1, 4, None, None, None],
                [None, 1, 2, 3, 4]
            ),
            ValuesTuple(
                [123, 127, None, None, None, None],
                [None, 123, 124, 125, 126, 127]
            ),
            ValuesTuple(
                [1, 1],
                [None, 1]
            ),
            ValuesTuple(
                [0, 0],
                [None, 0]
            ),
        )

    @staticmethod
    def name() -> str:
        return 'Диапазон'

    @staticmethod
    def short_description() -> tuple:
        return (
            "Нужно вернуть все целые числа в диапазоне [start, end]",
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
        yield from (
            ValuesTuple(
                ['123', '45', '6789', None],
                [None, None, None, '123456789']
            ),
            ValuesTuple(
                ['Very', ' simple', ' example', None],
                [None, None, None, 'Very simple example']
            ),
            ValuesTuple(
                ['', '', None],
                [None, None, '']
            ),
            ValuesTuple(
                [None],
                ['']
            )
        )

        if cls._all_values is None:
            cls._all_values = ''.join([chr(i) for i in chain(
                range(48, 58),
                range(65, 91),
                range(100, 123)
            )])
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

    @staticmethod
    def name() -> str:
        return 'Конкатенация строк'

    @staticmethod
    def short_description() -> tuple:
        return (
            "В генератор передаются строки, которые нужно сложить. "
            "При получении значения None вернуть полученную строку "
            "и закончить работу",
        )


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

    @staticmethod
    def name() -> str:
        return 'Пароль'

    @staticmethod
    def short_description() -> tuple:
        return (
            "В генератор передаётся пароль. Возвращать False до тех пор, "
            "пока генератору не будет передан тот же пароль. В этом случае "
            "вернуть True и закончить работу",
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
            ValuesTuple(
                [70, None],
                [70, ]
            ),
        )
        while True:
            number = randint(-100, 100)
            send = []
            awaited = []

            send.append(number)
            awaited.append(number)

            for _ in range(randint(0, 10)):
                new_number = randint(-100, 100)
                operation = choice(('+', '-', '*', '/'))
                if operation == '+':
                    number += new_number
                elif operation == '-':
                    number -= new_number
                elif operation == '*':
                    number *= new_number
                else:
                    if new_number == 0:
                        continue
                    number /= new_number
                if int(number) == number:
                    number = int(number)
                send.append((operation, new_number))
                awaited.append(number)

            send.append(None)
            yield ValuesTuple(send, awaited)

    @staticmethod
    def name() -> str:
        return 'Калькулятор'

    @staticmethod
    def short_description() -> tuple:
        return (
            "В первую очередь в генератор передаётся изначальное число, "
            "над которым будут производится операции, возвращая его обратно. "
            "Дальше в генератор будут передаваться пары (операция, число), где:",
            "> число: любое число типа float или int",
            "> операция: символ +, -, *, / для выполнения соответствующих операций"
        )
