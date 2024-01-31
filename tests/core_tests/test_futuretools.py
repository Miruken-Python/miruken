import asyncio
from unittest import IsolatedAsyncioTestCase
from core import futuretools as ft


class TestFutureThen(IsolatedAsyncioTestCase):
    async def test_then(self):
        def func(value):
            return value * 2

        future = asyncio.Future()
        future.set_result(5)
        result = await ft.then(future, func)
        self.assertEqual(result, 10)

    async def test_then_lambda(self):
        future = asyncio.Future()
        future.set_result(5)
        result = await ft.then(future, lambda x: x * 3)
        self.assertEqual(result, 15)

    async def test_then_async(self):
        async def func(value):
            await asyncio.sleep(.1)
            return value * 2

        future = asyncio.Future()
        future.set_result(5)
        result = await ft.then(future, func)
        self.assertEqual(result, 10)

    async def test_then_exception(self):
        def func(value):
            if value % 2 == 1:
                raise ValueError("value cannot be odd")
            return value * 2

        future = asyncio.Future()
        future.set_result(5)
        with self.assertRaises(ValueError) as context:
            await ft.then(future, func)

        self.assertEqual(str(context.exception), "value cannot be odd")

    async def test_then_lambda_exception(self):
        def func(value):
            if value % 2 == 1:
                raise ValueError("value cannot be odd")
            return value * 2

        future = asyncio.Future()
        future.set_result(5)
        with self.assertRaises(ValueError) as context:
            await ft.then(future, lambda ex: func(3))

        self.assertEqual(str(context.exception), "value cannot be odd")

    async def test_then_exception_async(self):
        async def func(value):
            if value % 2 == 1:
                raise ValueError("value cannot be odd")
            await asyncio.sleep(.1)
            return value * 2

        future = asyncio.Future()
        future.set_result(5)
        with self.assertRaises(ValueError) as context:
            await ft.then(future, func)

        self.assertEqual(str(context.exception), "value cannot be odd")

    async def test_then_unwrap(self):
        def func(value):
            f = asyncio.Future()
            f.set_result(value * 2)
            return f

        future = asyncio.Future()
        future.set_result(5)
        result = await ft.then(future, func)
        self.assertEqual(result, 10)

    async def test_then_unwrap_lambda(self):
        future = asyncio.Future()
        future.set_result(5)
        result = await ft.then(future, lambda x: 2 ** x)
        self.assertEqual(result, 32)

    async def test_then_unwrap_exception(self):
        def func(value):
            f = asyncio.Future()
            f.set_exception(ValueError("value cannot be even"))
            return f

        future = asyncio.Future()
        future.set_result(5)
        with self.assertRaises(ValueError) as context:
            await ft.then(future, func)

        self.assertEqual(str(context.exception), "value cannot be even")


class TestFutureCatch(IsolatedAsyncioTestCase):
    async def test_catch(self):
        def func(ex):
            raise TimeoutError("connection failed")

        future = asyncio.Future()
        future.set_exception(ValueError("An error occurred"))
        with self.assertRaises(TimeoutError) as context:
            await ft.catch(future, func)

        self.assertEqual(str(context.exception), "connection failed")

    async def test_catch_async(self):
        async def func(ex):
            await asyncio.sleep(.1)
            raise TimeoutError("connection failed")

        future = asyncio.Future()
        future.set_exception(ValueError("An error occurred"))
        with self.assertRaises(TimeoutError) as context:
            await ft.catch(future, func)

        self.assertEqual(str(context.exception), "connection failed")

    async def test_catch_result(self):
        def func(ex):
            return str(ex)

        future = asyncio.Future()
        future.set_exception(ValueError("An error occurred"))
        result = await ft.catch(future, func)

        self.assertEqual(result, "An error occurred")

    async def test_catch_result_lambda(self):
        future = asyncio.Future()
        future.set_exception(ValueError("An error occurred"))
        result = await ft.catch(future, lambda ex: str(ex))

        self.assertEqual(result, "An error occurred")

    async def test_catch_lambda_exception(self):
        def func(ex):
            raise RuntimeError("cpu overheating")

        future = asyncio.Future()
        future.set_exception(ValueError("An error occurred"))
        with self.assertRaises(RuntimeError) as context:
            await ft.catch(future, lambda ex: func(ex))

        self.assertEqual(str(context.exception), "cpu overheating")

    async def test_catch_unwrap(self):
        def func(ex):
            f = asyncio.Future()
            f.set_result(2)
            return f

        future = asyncio.Future()
        future.set_exception(ValueError("An error occurred"))
        result = await ft.catch(future, func)
        self.assertEqual(result, 2)

    async def test_catch_unwrap_result(self):
        def func(ex):
            f = asyncio.Future()
            f.set_result(22)
            return f

        future = asyncio.Future()
        future.set_exception(ValueError("An error occurred"))
        result = await ft.catch(future, func)
        self.assertEqual(result, 22)


class TestFutureAlways(IsolatedAsyncioTestCase):
    async def test_always(self):
        was_called = False

        def func():
            nonlocal was_called
            was_called = True

        future = asyncio.Future()
        future.set_result(5)
        await ft.always(future, func)
        self.assertTrue(was_called)

    async def test_always_exception(self):
        was_called = False

        def func():
            nonlocal was_called
            was_called = True

        future = asyncio.Future()
        future.set_exception(ValueError("An error occurred"))
        with self.assertRaises(ValueError) as context:
            await ft.always(future, func)

        self.assertTrue(was_called)
        self.assertEqual(str(context.exception), "An error occurred")

    async def test_always_exception_replace(self):
        was_called = False

        def func():
            nonlocal was_called
            was_called = True
            raise RuntimeError("Out of memory")

        future = asyncio.Future()
        future.set_exception(ValueError("An error occurred"))
        with self.assertRaises(RuntimeError) as context:
            await ft.always(future, func)

        self.assertTrue(was_called)
        self.assertEqual(str(context.exception), "Out of memory")
