from unittest import TestCase

from core import MultipleErrors


class TestMultipleErrors(TestCase):
    def test_single_error(self):
        e = Exception("Error 1")
        me = MultipleErrors(e)
        self.assertEqual(len(me.errors), 1)
        self.assertEqual(me.errors[0], e)

    def test_multiple_errors(self):
        e1 = Exception("Error 1")
        e2 = Exception("Error 2")
        me = MultipleErrors(e1, e2)
        self.assertEqual(len(me.errors), 2)
        self.assertEqual(me.errors[0], e1)
        self.assertEqual(me.errors[1], e2)

    def test_combine_single_error(self):
        e = Exception("Error 1")
        result = MultipleErrors.combine(e)
        self.assertEqual(result, e)

    def test_combine_multiple_errors(self):
        e1 = Exception("Error 1")
        e2 = Exception("Error 2")
        result = MultipleErrors.combine(e1, e2)
        self.assertIsInstance(result, MultipleErrors)
        self.assertEqual(len(result.errors), 2)
        self.assertEqual(result.errors[0], e1)
        self.assertEqual(result.errors[1], e2)

    def test_combine_no_errors(self):
        result = MultipleErrors.combine()
        self.assertIsNone(result)

    def test_add_errors(self):
        e1 = Exception("Error 1")
        e2 = Exception("Error 2")
        result = MultipleErrors(e1) + e2
        self.assertIsInstance(result, MultipleErrors)
        self.assertEqual(len(result.errors), 2)
        self.assertEqual(result.errors[0], e1)
        self.assertEqual(result.errors[1], e2)
