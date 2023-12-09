from typing import Any, Union

__all__ = (
    'CheckHook',
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
    ...        target_method: callable,
    ...        send_value: Any,
    ...        timeout: Union[int, float]
    ...    ) -> Any:
    ...        return function(target_method, self.value, timeout)
    This class simply do nothing. Example of ValueTuple.send with and without:
    without: [1, 2, 3]
    with: [1, Forward(2), 3]
    """
    __slots__ = ()

    def __call__(
        self,
        function: callable,
        target_method: callable,
        send_value: Any,
        timeout: Union[int, float]
    ) -> Any:
        return function(target_method, send_value, timeout)
