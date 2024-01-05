from typing import Any, Generator, List, NamedTuple, Callable, Optional, Union

__all__ = (
    'TaskMeta',
    'ValuesTuple',
)


class ValuesTuple(NamedTuple):
    send: List[Any]
    awaited: List[Any]


class TaskMeta(type):
    all_tasks: List['TaskMeta'] = []
    complexity: int
    _gen_annotation: Generator
    generator: Callable
    check_values: Callable[['TaskMeta'], Generator[ValuesTuple, None, None]]

    def __new__(cls, class_name: str, bases: tuple, attrs: dict):
        checker = object()
        ending = f"in class {attrs['__module__']}.{class_name}"

        assert class_name.startswith('Task'), 'All task classes should start with "Task"'
        for base in bases:
            base: type
            assert \
                base.__module__ == attrs['__module__'], \
                f"Multi-file inheritance detected:\n" \
                f" - Base    class: {base.__module__}.{base.__qualname__}\n" \
                f" - Derived class: {attrs['__module__']}.{class_name}\n" \
                'Such inheritance forbidden\n'

        # Task.complexity
        complexity = attrs.get('complexity', checker)
        assert complexity is not checker, f"No complexity attribute found {ending}"

        # Task.generator()
        generator = attrs.get('generator', checker)
        assert generator is not checker, f"No generator method found {ending}"

        # Task.check_values()
        check_values = attrs.get('check_values', checker)
        assert check_values is not checker, f"No check_values method found {ending}"

        # Task.name()
        name = attrs.get('name', checker)
        assert name is not checker, f"No name method found {ending}"
        assert isinstance(name, staticmethod), f"Name method should be static {ending}"

        # Task.short_description()
        short_description = attrs.get('short_description', checker)
        assert short_description is not checker, f"No short_description method found {ending}"

        # Task.save()
        save = attrs.get('save', checker)
        if save is checker:
            attrs['save'] = save_method
        save = save_method
        assert save is not checker, f"No save method found {ending}"

        # Task.init_values()
        init_values = attrs.get('init_values', checker)
        if init_values is checker:
            attrs['init_values'] = init_values_method
        init_values = init_values_method
        assert init_values is not checker, f"No init_values method found {ending}"
        assert isinstance(init_values, classmethod), \
            f"init_values method should be class method {ending}"

        # Task.__init__()
        __init__ = attrs.get('__init__', checker)
        if __init__ is checker:
            attrs['__init__'] = init_method
        __init__ = init_method
        assert __init__ is not checker, f"No __init__ method found {ending}"

        cl = super().__new__(cls, class_name, bases, attrs)
        cls.all_tasks.append(cl)
        return cl

    def __repr__(self):
        return f"<{self.__qualname__} complexity={self.complexity}>"

    @classmethod
    def find_task(cls, name: str) -> Optional['TaskMeta']:
        for task in cls.all_tasks:
            if task.__qualname__ == name:
                return task


@classmethod
def save_method(cls: TaskMeta):
    return (cls.__qualname__, )


@classmethod
def init_values_method(cls: TaskMeta):
    while True:
        yield (cls.__qualname__, )


def init_method(self, values: tuple[str, ...]):
    pass
