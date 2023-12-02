from unittest import TestCase

from src.tasks import TaskRange, iterations_limit


class TestTaskRange(TestCase):
    __slots__ = ()

    def test_generator(self):
        gen = TaskRange.generator()
        gen.send(None)
        gen.send(5)
        gen.send(10)
        for i in range(5, 11):
            answer = gen.send(None)
            self.assertEqual(answer, i)

    def test_check_generator(self):
        counter = 0
        for value in iterations_limit(TaskRange.check_values(), 50):
            gen = TaskRange.generator()
            gen.send(None)
            for send, awaited in zip(value.send, value.awaited):
                self.assertEqual(gen.send(send), awaited, f"Error on {counter} values iteration")
            counter += 1
