from unittest import IsolatedAsyncioTestCase
import asyncio
import time


async def some_function():
    await asyncio.sleep(.5)
    return 1


class TestFuture(IsolatedAsyncioTestCase):
    async def test_async(self):
        future = asyncio.ensure_future(some_function())

        # Now you can await the future to get the result
        result = await future
        print(f"async {result}")

    def test_sync(self):
        loop = asyncio.get_event_loop()

        # Create a Future object from the coroutine
        future = asyncio.ensure_future(some_function())

        # Alternatively, you can use the loop.create_task method
        # future = loop.create_task(some_function())

        # Now you can await the future to get the result
        result = loop.run_until_complete(future)
        print(f"sync {result}")


class TestGather(IsolatedAsyncioTestCase):
    async def test_all(self):
        values = await asyncio.gather(
            some_function(),
            some_function()
        )
        print(values)  # [1, 1]


class TestTask(IsolatedAsyncioTestCase):
    async def test_group(self):
        # Schedule nested() to run soon concurrently
        # with "main()".
        task = asyncio.create_task(self.nested())

        print("doing more work")

        # "task" can now be used to cancel "nested()", or
        # can simply be awaited to wait until it is complete:
        await task
        print(f"finished at {time.strftime('%X')}")

    @staticmethod
    async def nested():
        print(f"started nested at {time.strftime('%X')}")
        await asyncio.sleep(.1)
        return 42


class TestTaskGroup(IsolatedAsyncioTestCase):
    async def test_group(self):
        await self.foo(asyncio.TaskGroup())

    async def foo(self, task_group):
        async with task_group as tg:
            # Adding tasks to the task group
            task1 = tg.create_task(self.do_something(1))
            task2 = tg.create_task(self.do_something(2))

            print(f"started at {time.strftime('%X')}")

        # The task group ensures that all tasks have completed before reaching this point
        print(f"finished at {time.strftime('%X')}")

    @staticmethod
    async def do_something(name):
        print(f"Task {name} started")
        await asyncio.sleep(.5)
        print(f"Task {name} completed")
