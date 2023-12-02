from unittest import TestCase
from io import StringIO

from src.tasks import TaskRange, TaskConcat, TaskPassword
from src.exercise import Exercise


class TestTaskRange(TestCase):
    __slots__ = ()

    def test_range_password_1(self):
        e = Exercise([TaskRange, TaskPassword])

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
        e = Exercise([TaskRange, TaskConcat])

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
