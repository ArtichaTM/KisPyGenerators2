from unittest import TestCase
from io import StringIO

from src.meta import TaskMeta
from src.exercise import Exercise


class TestTaskRange(TestCase):
    __slots__ = ()

    def test_range_password_1(self):
        cl_range = TaskMeta.find_task('TaskRange')
        cl_password = TaskMeta.find_task('TaskPassword')
        if cl_range is None:
            self.skipTest("Can't find task TaskRange")
        if cl_password is None:
            self.skipTest("Can't find task TaskPassword")
        e = Exercise([cl_range, cl_password])
        self.assertEqual(cl_range.complexity + cl_password.complexity, e.complexity)

        def gen():
            start = yield
            start -= 1
            end = yield
            while start <= end:
                password = yield start
                start += 1
            new_password = yield
            while True:
                if new_password == password:
                    break
                new_password = yield False
            yield True

        self.assertEqual('', e.validate(gen))

    def test_range_concat(self):
        cl_range = TaskMeta.find_task('TaskRange')
        cl_concat = TaskMeta.find_task('TaskConcat')
        if cl_range is None:
            self.skipTest("Can't find task TaskRange")
        if cl_concat is None:
            self.skipTest("Can't find task TaskConcat")
        e = Exercise([cl_range, cl_concat])
        self.assertEqual(cl_range.complexity + cl_concat.complexity, e.complexity)

        def gen():
            start = yield
            start -= 1
            end = yield
            while start <= end:
                value = yield start
                start += 1
            if start < end:
                value = yield
            string = StringIO()
            while isinstance(value, str):
                string.write(value)
                value = yield
            yield string.getvalue()

        e.validate(gen)

    def test_range_calculator(self):
        cl_range = TaskMeta.find_task('TaskRange')
        cl_calculator = TaskMeta.find_task('TaskCalculator')
        if cl_range is None:
            self.skipTest("Can't find task TaskRange")
        if cl_calculator is None:
            self.skipTest("Can't find task TaskCalculator")
        e = Exercise([cl_range, cl_calculator])
        self.assertEqual(cl_range.complexity + cl_calculator.complexity, e.complexity)
