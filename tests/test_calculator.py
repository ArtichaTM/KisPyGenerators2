from unittest import TestCase

from src.tasks import TaskCalculator, iterations_limit


class TestTaskCalculator(TestCase):
    __slots__ = ()

    def test_check_generator(self):
        iteration = 0
        for value in iterations_limit(TaskCalculator.check_values(), 50):
            gen = TaskCalculator.generator()
            gen.send(None)
            for send, awaited in zip(value.send, value.awaited):
                self.assertEqual(
                    gen.send(send),
                    awaited,
                    f"Error on {iteration} values iteration"
                )
            iteration += 1
