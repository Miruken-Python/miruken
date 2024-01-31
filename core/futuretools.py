from typing import (
    Any,
    Callable,
    Coroutine,
    TypeVar,
    TypeAlias
)
import asyncio

T = TypeVar('T')
R = TypeVar('R')
AsyncSource: TypeAlias = Coroutine[Any, Any, T] | asyncio.Future[T]
AsyncResult: TypeAlias = Coroutine[Any, Any, R] | asyncio.Future[R]


def then(
        async_source: AsyncSource,
        continuation: Callable[[T], R | AsyncResult]
) -> asyncio.Future[R]:
    future = asyncio.ensure_future(async_source)

    async def callback():
        result = await future
        new_result = continuation(result)
        if isinstance(new_result, asyncio.Future):
            return await new_result
        elif asyncio.iscoroutine(new_result):
            return await new_result
        return new_result

    return asyncio.create_task(callback())


def catch(
        async_source: AsyncSource,
        continuation: Callable[[Exception], R | AsyncResult]
) -> asyncio.Future[R]:
    future = asyncio.ensure_future(async_source)

    async def callback():
        try:
            return await future
        except Exception as e:
            new_result = continuation(e)
            if isinstance(new_result, asyncio.Future):
                return await new_result
            elif asyncio.iscoroutine(new_result):
                return await new_result
            return new_result

    return asyncio.create_task(callback())


def always(
        async_source: AsyncSource,
        continuation: Callable[[], None]
) -> asyncio.Future[R]:
    future = asyncio.ensure_future(async_source)

    async def callback():
        try:
            return await future
        finally:
            continuation()

    return asyncio.create_task(callback())
