from typing import Generator, List, Callable, Tuple

from .meta import TaskMeta, ValuesTuple
from .tasks import iterations_limit


class Exercise:
    __slots__ = ('tasks', 'complexity')

    def __init__(self, tasks: List[TaskMeta]):
        self.tasks = tasks
        self.complexity = sum((t.complexity for t in tasks))

    def __repr__(self) -> str:
        return f"<Exercise with {len(self.tasks)} tasks and {self.complexity} complexity"

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
                assert len(value_tuple.send) == len(value_tuple.awaited)
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
