from typing import Any, Generator, List, NamedTuple, Callable

__all__ = (
    'TaskMeta',
    'ValuesTuple',
)


class ValuesTuple(NamedTuple):
    send: List[Any]
    awaited: List[Any]


def task_repr(self: 'TaskMeta') -> str:
    return f"<{type(self).__qualname__} complexity={self.complexity}>"


class TaskMeta(type):
    all_tasks: List['TaskMeta'] = []
    complexity: int
    _gen_annotation: Generator
    generator: Callable
    check_values: Callable[['TaskMeta'], Generator[ValuesTuple, None, None]]

    def __new__(cls, name: str, bases: tuple, attrs: dict):
        checker = object()
        ending = f"in class {attrs['__module__']}.{name}"

        assert name.startswith('Task'), 'All task classes should start with "Task"'
        for base in bases:
            base: type
            assert \
                base.__module__ == attrs['__module__'], \
                f"Multi-file inheritance detected:\n" \
                f" - Base    class: {base.__module__}.{base.__qualname__}\n" \
                f" - Derived class: {attrs['__module__']}.{name}\n" \
                'Such inheritance forbidden\n'

        # Task.complexity
        complexity = attrs.get('complexity', checker)
        assert complexity is not checker, f"No complexity attribute found {ending}"
        assert isinstance(complexity, int), f"Complexity is not type of int {ending}"

        # Task.generator()
        generator = attrs.get('generator', checker)
        assert generator is not checker, f"No generator method found {ending}"
        assert isinstance(generator, staticmethod), f"Generator method should be static {ending}"

        # Task.check_values()
        check_values = attrs.get('check_values', checker)
        assert check_values is not checker, f"No check_values method found {ending}"
        assert \
            isinstance(check_values, classmethod), \
            f"Check_values method should be classmethod {ending}"

        # Implementing repr, if not overriden
        attrs.setdefault('__repr__', task_repr)

        cl = super().__new__(cls, name, bases, attrs)
        cls.all_tasks.append(cl)
        return cl
