from unittest import TestCase

from core import (
    HANDLED,
    HANDLED_AND_STOP,
    NOT_HANDLED,
    NOT_HANDLED_AND_STOP
)


class TestHandledOr(TestCase):
    def setUp(self):
        self.result = HANDLED

    def test_handled_should_be_handled(self):
        self.assertEqual(HANDLED, self.result.or_(HANDLED))

    def test_handled_should_be_handled_op(self):
        self.assertEqual(HANDLED, self.result | HANDLED)

    def test_handled_and_stop_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.or_(HANDLED_AND_STOP))

    def test_not_handled_should_be_handled(self):
        self.assertEqual(HANDLED, self.result.or_(NOT_HANDLED))

    def test_not_handled_and_stop_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.or_(NOT_HANDLED_AND_STOP))


class TestHandledErrorOr(TestCase):
    def setUp(self):
        self.result = HANDLED.with_error(Exception("bad"))

    def test_handled_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.or_(HANDLED).without_error())

    def test_handled_and_stop_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.or_(HANDLED_AND_STOP).without_error())

    def test_not_handled_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.or_(NOT_HANDLED).without_error())

    def test_not_handled_and_stop_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.or_(NOT_HANDLED_AND_STOP).without_error())


class TestHandleResultErrors(TestCase):
    def test_combines_multiple_errors(self):
        result = HANDLED.with_error(Exception("bad")).or_(NOT_HANDLED.with_error(Exception("argument")))

        self.assertTrue(result.is_error)

        err = result.error
        self.assertIsNotNone(err)
        self.assertEqual(2, len(err.args))


class TestHandledAndStopOr(TestCase):
    def setUp(self):
        self.result = HANDLED_AND_STOP

    def test_handled_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.or_(HANDLED))

    def test_handled_and_stop_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.or_(HANDLED_AND_STOP))

    def test_not_handled_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.or_(NOT_HANDLED))

    def test_not_handled_and_stop_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.or_(NOT_HANDLED_AND_STOP))


class TestNotHandledOr(TestCase):
    def setUp(self):
        self.result = NOT_HANDLED

    def test_handled_should_be_handled(self):
        self.assertEqual(HANDLED, self.result.or_(HANDLED))

    def test_handled_should_be_handled_op(self):
        self.assertEqual(HANDLED, self.result | HANDLED)

    def test_handled_and_stop_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.or_(HANDLED_AND_STOP))

    def test_not_handled_should_be_not_handled(self):
        self.assertEqual(NOT_HANDLED, self.result.or_(NOT_HANDLED))

    def test_not_handled_and_stop_should_be_not_handled_and_stop(self):
        self.assertEqual(NOT_HANDLED_AND_STOP, self.result.or_(NOT_HANDLED_AND_STOP))


class TestNotHandledAndStopOr(TestCase):
    def setUp(self):
        self.result = NOT_HANDLED_AND_STOP

    def test_handled_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.or_(HANDLED))

    def test_handled_and_stop_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.or_(HANDLED_AND_STOP))

    def test_not_handled_should_be_not_handled_and_stop(self):
        self.assertEqual(NOT_HANDLED_AND_STOP, self.result.or_(NOT_HANDLED))

    def test_not_handled_and_stop_should_be_not_handled_and_stop(self):
        self.assertEqual(NOT_HANDLED_AND_STOP, self.result.or_(NOT_HANDLED_AND_STOP))


class TestHandledAnd(TestCase):
    def setUp(self):
        self.result = HANDLED

    def test_handled_should_be_handled(self):
        self.assertEqual(HANDLED, self.result.and_(HANDLED))

    def test_handled_should_be_handled_op(self):
        self.assertEqual(HANDLED, self.result & HANDLED)

    def test_handled_and_stop_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.and_(HANDLED_AND_STOP))

    def test_not_handled_should_be_not_handled(self):
        self.assertEqual(NOT_HANDLED, self.result.and_(NOT_HANDLED))

    def test_not_handled_and_stop_should_be_not_handled_and_stop(self):
        self.assertEqual(NOT_HANDLED_AND_STOP, self.result.and_(NOT_HANDLED_AND_STOP))


class TestHandledAndStopAnd(TestCase):
    def setUp(self):
        self.result = HANDLED_AND_STOP

    def test_handled_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.and_(HANDLED))

    def test_handled_and_stop_should_be_handled_and_stop(self):
        self.assertEqual(HANDLED_AND_STOP, self.result.and_(HANDLED_AND_STOP))

    def test_not_handled_should_be_not_handled_and_stop(self):
        self.assertEqual(NOT_HANDLED_AND_STOP, self.result.and_(NOT_HANDLED))

    def test_not_handled_and_stop_should_be_not_handled_and_stop(self):
        self.assertEqual(NOT_HANDLED_AND_STOP, self.result.and_(NOT_HANDLED_AND_STOP))


class TestNotHandledAnd(TestCase):
    def setUp(self):
        self.result = NOT_HANDLED

    def test_handled_should_be_not_handled(self):
        self.assertEqual(NOT_HANDLED, self.result.and_(HANDLED))

    def test_handled_should_be_not_handled_op(self):
        self.assertEqual(NOT_HANDLED, self.result & HANDLED)

    def test_handled_and_stop_should_be_not_handled_and_stop(self):
        self.assertEqual(NOT_HANDLED_AND_STOP, self.result.and_(HANDLED_AND_STOP))

    def test_not_handled_should_be_not_handled(self):
        self.assertEqual(NOT_HANDLED, self.result.and_(NOT_HANDLED))

    def test_not_handled_and_stop_should_be_not_handled_and_stop(self):
        self.assertEqual(NOT_HANDLED_AND_STOP, self.result.and_(NOT_HANDLED_AND_STOP))


class TestNotHandledAndStopAnd(TestCase):
    def setUp(self):
        self.result = NOT_HANDLED_AND_STOP

    def test_handled_should_be_not_handled_and_stop(self):
        self.assertEqual(NOT_HANDLED_AND_STOP, self.result.and_(HANDLED))

    def test_handled_and_stop_should_be_not_handled_and_stop(self):
        self.assertEqual(NOT_HANDLED_AND_STOP, self.result.and_(HANDLED_AND_STOP))

    def test_not_handled_should_be_not_handled_and_stop(self):
        self.assertEqual(NOT_HANDLED_AND_STOP, self.result.and_(NOT_HANDLED))

    def test_not_handled_and_stop_should_be_not_handled_and_stop(self):
        self.assertEqual(NOT_HANDLED_AND_STOP, self.result.and_(NOT_HANDLED_AND_STOP))
