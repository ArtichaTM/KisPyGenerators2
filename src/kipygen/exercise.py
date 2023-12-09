from functools import partial
from io import StringIO
from typing import Dict, Generator, List, Callable, Tuple, TypeVar, Union
from random import shuffle
from itertools import combinations
from math import factorial
from threading import Thread

from .meta import TaskMeta, ValuesTuple, Checker
from .tasks import iterations_limit


T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')


def _timeout_call(
        function: Callable[[T1], T2],
        values: list,
        *args: T1,
        **kwargs: T1
) -> None:
    values.append(function(*args, **kwargs))


def timeout_call(
        _function: Callable[[T1], T2],
        *args: T1,
        timeout: Union[float, int] = 3,
        **kwargs: T1
) -> T2:
    output = []
    function = partial(_timeout_call, _function, output)

    thread = Thread(
        target=function,
        args=args,
        kwargs=kwargs, name='Function check thread',
        daemon=True
    )
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        raise TimeoutError()
    return output[0]


class Exercise:
    __slots__ = ('tasks', 'complexity')

    def __init__(self, tasks: List[TaskMeta]):
        assert isinstance(tasks, (tuple, list))
        assert tasks
        self.tasks = tuple(tasks)
        self.complexity = sum((t.complexity for t in tasks))

    def __repr__(self) -> str:
        return f"<Exercise with {len(self.tasks)} tasks and {self.complexity} complexity>"

    def _validate_iteration(
            self,
            gen: Generator,
            check_values: ValuesTuple
    ) -> str:
        """
        Validates just started generator. Method calls "gen.send(None) on start

        :param gen: Collective generator of all tasks contained in `tasks` variable
        :return: String with error message. If len(str) == 0, no error occured
        """
        TIMEOUT = 3
        iteration = 0
        output = StringIO()
        # indexes = dict()
        send, awaited = None, None
        try:
            timeout_call(gen.send, None, timeout=TIMEOUT)
            for send, awaited in zip(check_values.send, check_values.awaited):
                gen_out = timeout_call(gen.send, send, timeout=TIMEOUT)
                if isinstance(awaited, Checker):
                    gen_out = awaited.output_value(gen_out)
                    if gen_out:
                        output.write(gen_out)
                        break
                elif gen_out != awaited:
                    output.write(
                        f"От генератора ожидалось значение {awaited}, "
                        f"однако получено {gen_out}"
                    )
                    break
                elif type(gen_out) is not type(awaited):
                    output.write(
                        f'От генератора ожидался тип данных '
                        f'{type(awaited).__qualname__} ({awaited}), '
                        f'однако получен {type(gen_out).__qualname__} ({gen_out})'
                    )
                    break
                iteration += 1
        except StopIteration:
            output.write('Генератор неожиданно завершился')
        except TimeoutError:
            output.write(f'Генератор не дал ответ после {TIMEOUT} секунд')
        except Exception as e:
            output.write(
                f"Неожиданное исключение: "
                f"{type(e).__qualname__}({e.args[0]})"
            )

        # Error happened
        if output.tell() != 0:
            indexes: dict = dict()
            send, awaited = self._cute_in_out(check_values.send, check_values.awaited, indexes)
            indexes: Tuple[int, int] = indexes[iteration]
            output.write(f'\nSend:    {send}\nAwaited: {awaited}\n')
            output.write(' ' * 9)
            output.write(' ' * indexes[0])
            output.write('^' * indexes[1])
            return output.getvalue()

        if output.tell() == 0:
            # Generator should be closed by now
            try:
                gen.send(None)
            except StopIteration:
                pass
            else:
                return 'Генератор не остановился после выполнения всех задач'

    def check_values(self) -> Generator[ValuesTuple, None, None]:
        """
        Returns generator of ValuesTuple based on all current tasks
        :return: Generator of ValuesTuple[list, list]
        """
        all_check_values = [task.check_values() for task in self.tasks]
        for values_tuples in zip(*all_check_values):
            values_tuples: Tuple[ValuesTuple]
            send = []
            awaited = []
            for value_tuple in values_tuples:
                send.extend(value_tuple.send)
                awaited.extend(value_tuple.awaited)
            yield ValuesTuple(send, awaited)

    def validate(self, factory: Callable[[], Generator], max_iterations: int = 500) -> str:
        assert isinstance(max_iterations, int)
        assert max_iterations > 1
        output = StringIO()

        for check_values in iterations_limit(self.check_values(), max_iterations):
            gen = factory()
            output = self._validate_iteration(gen, check_values)
            if output:
                return output
        return ''

    @staticmethod
    def combinations_amount() -> int:
        n = len(TaskMeta.all_tasks)
        amount = 0
        for r in range(1, n+1):
            left = factorial(n)
            middle = factorial(r)
            right = factorial(n-r)
            amount += int(left / middle / right)
        return amount

    @classmethod
    def _random_all_length_recursive(
            cls,
            values: List[type(T)],
            r: int
    ) -> Generator[List[type(T)], None, None]:
        if r == len(values):
            yield values
            return
        for i in combinations(values, r):
            yield i
        yield from cls._random_all_length_recursive(values, r+1)

    @classmethod
    def _random_all_length(cls, values: List[type(T)]) -> Generator[List[type(T)], None, None]:
        return cls._random_all_length_recursive(values, 1)

    @classmethod
    def random(cls) -> Generator['Exercise', None, None]:
        new_tasks = TaskMeta.all_tasks
        shuffle(new_tasks)
        for tasks in cls._random_all_length(new_tasks):
            yield Exercise(tasks)

    @classmethod
    def random_range(
            cls,
            complexity_min: int = None,
            complexity_max: int = None
    ) -> Generator['Exercise', None, None]:
        for e in cls.random():
            if complexity_min <= e.complexity <= complexity_max:
                yield e

    def name(self) -> str:
        return (
            f"Упражнение с "
            f"{len(self.tasks)} заданиями и "
            f"{self.complexity} уровнем сложности")

    @staticmethod
    def _cute_in_out(
        _send: List[T],
        _awaited: List[T],
        indexes: Dict[int, List[int]],
        checkers: Dict[str, Checker]
    ) -> Tuple[str, str]:
        """ Returns send and awaited values in cute string form, aligned to left
        :param _send: ValuesTuple.send
        :param _awaited: ValuesTuple.awaited
        :param indexes: Dictionary, where indexes and lengths of values is placed
        :return: Send and awaited values

        indexes variable will be like this on function end:
        >>> {
        ...     0: [4, 2],
        ...     1: [9, 5],
        ...     2: [17, 3]
        ... }
        """
        assert isinstance(indexes, dict)

        iter_send = iter(_send)
        iter_awaited = iter(_awaited)

        send = StringIO()
        awaited = StringIO()

        send.write('[ ')
        awaited.write('[ ')

        for index, left, right in zip(range(0, len(_send)), iter_send, iter_awaited):
            indexes[index] = [send.tell()]
            if isinstance(left, str):
                left = f"'{left}'"
            elif isinstance(left, Checker):
                checkers[type(left).__qualname__] = left
                left = left.name()
            else:
                left = str(left)
            if isinstance(right, str):
                right = f"'{right}'"
            elif isinstance(right, Checker):
                checkers[type(right).__qualname__] = right
                right = right.name()
            else:
                right = str(right)
            length = max(len(left), len(right))
            send.write(left.ljust(length))
            awaited.write(right.ljust(length))
            send.write(', ')
            awaited.write(', ')
            indexes[index].append(length)

        # Leftovers
        for left in iter_send:
            send.write(str(left))
            send.write(', ')

        for right in iter_awaited:
            awaited.write(str(right))
            send.write(', ')

        # Removing last ", "
        send.seek(send.truncate(send.tell()-2))
        awaited.seek(awaited.truncate(awaited.tell()-2))

        send.write(' ]')
        awaited.write(' ]')

        return send.getvalue(), awaited.getvalue()

    def description(self) -> str:
        assert len(TaskMeta.all_tasks) < 100
        io = StringIO()
        io.write('> Перед вами стоит задача построить генератор, который ')
        io.write('выполняет несколько последовательных задач:')
        tabulation_amount = 2

        # For numbers over 9
        if len(self.tasks) // 10:
            tabulation_amount += 1

        for index, task in enumerate(self.tasks, start=1):
            io.write('\n')
            prefix = f"{index}. ".rjust(tabulation_amount+1)
            io.write(prefix)
            io.write(f"\n{' '*len(prefix)}".join(task.short_description()))
        io.write('\n> Пример ввода и вывода (списки выровнены по элементам):')
        checkers: Dict[str, Checker] = dict()
        for example_checks in iterations_limit(self.check_values(), 2):
            indexes = dict()
            send, awaited = self._cute_in_out(
                example_checks.send,
                example_checks.awaited,
                indexes,
                checkers
            )
            io.write(f'\nВходящие в генератор данные:    '
                     f'{send}')
            io.write(f'\nВыходящие из генератора данные: '
                     f'{awaited}')
        checkers: list[str] = [f"{c.name()} - {c.description()}" for c in checkers.values()]
        if checkers:
            io.write('\n> Информация об уникальных значениях:')
            for checker_info in checkers:
                io.write('\n')
                io.write(checker_info)
        return io.getvalue()
