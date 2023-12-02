from unittest import TestCase

from src.tasks import TaskConcat, iterations_limit


class TestTaskConcat(TestCase):
    __slots__ = ()

    def test_generator(self):
        gen = TaskConcat.generator()
        gen.send(None)
        gen.send('12')
        gen.send('34')
        gen.send('7722')
        self.assertEqual(gen.send(None), '12347722')

    def test_check_generator(self):
        for value in iterations_limit(TaskConcat.check_values(), 50):
            gen = TaskConcat.generator()
            gen.send(None)
            for send, awaited in zip(value.send, value.awaited):
                self.assertEqual(gen.send(send), awaited)
