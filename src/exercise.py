from io import StringIO
from typing import Generator, List, Callable, Tuple, TypeVar
from random import shuffle
from itertools import combinations
from math import factorial

from .meta import TaskMeta, ValuesTuple
from .tasks import iterations_limit


T = TypeVar('T')


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
        iteration = 0
        try:
            gen.send(None)
            for send, awaited in zip(check_values.send, check_values.awaited):
                output = gen.send(send)
                if type(output) is not type(awaited):
                    return (f'Awaited type {type(awaited)}, '
                            f'got {type(output)} on iteration {iteration}')
                if output != awaited:
                    return (f"Awaited {awaited}, "
                            f"got {output} on iteration {iteration}")
                iteration += 1
        except StopIteration:
            return f'Generator unexpectedly closed on iteration {iteration}'
        except Exception as e:
            return f"Unexpected exception: {type(e).__qualname__}({e.args[0]})"

        # Generator should be closed by now
        try:
            gen.send(None)
        except StopIteration:
            return ''
        else:
            return 'Generator did not stopped after all tasks completed'

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

    def validate(self, factory: Callable[[], Generator], max_iterations: int = 50) -> str:
        assert isinstance(max_iterations, int)
        assert max_iterations > 1

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

    def description(self) -> str:
        assert len(TaskMeta.all_tasks) < 100
        io = StringIO()
        io.write('Перед вами стоит задача построить генератор, который ')
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
        io.write('\nПример ввода и вывода:')
        for example_checks in iterations_limit(self.check_values(), 2):
            io.write(f'\nВходящие в генератор данные:    {example_checks.send} {len(example_checks.send)}')
            io.write(f'\nВыходящие из генератора данные: {example_checks.awaited} {len(example_checks.awaited)}')
        return io.getvalue()
