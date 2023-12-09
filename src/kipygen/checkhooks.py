from typing import Any


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
    ...    def __call__(self, function: callable, *args, **kwargs) -> Any:
    ...        arguments = list(args)
    ...        # Finding self in arguments, because this hook are passing to func
    ...        index = arguments.index(self)
    ...        if index != -1:
    ...            # Found? Replace with real value
    ...            arguments[index] = self.value
    ...        # Call function as nothing happened
    ...        return function(*arguments, **kwargs)
    This class simply do nothing. Example of ValueTuple.send with and without:
    without: [1, 2, 3]
    with: [1, Forward(2), 3]
    """
    __slots__ = ()

    def __call__(self, function: callable, *args, **kwargs) -> Any:
        return function(*args, **kwargs)
