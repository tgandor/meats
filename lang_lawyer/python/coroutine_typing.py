# https://stackoverflow.com/questions/49360480/python-type-hinting-for-async-function-as-function-argument

from typing import Optional, Coroutine, Any, Callable


async def test(*args, **kwargs):
    return args, kwargs

# instead of Coroutine[Any, Any, Any], Awaitable[Any] could be OK


def consumer(function_: Optional[Callable[..., Coroutine[Any, Any, Any]]] = None):
    func = function_
    return func


consumer(test)
