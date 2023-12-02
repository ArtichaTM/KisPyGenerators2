from unittest import TestCase

from src.tasks import TaskPassword, iterations_limit


class TestTaskPassword(TestCase):
    __slots__ = ()

    def test_generator(self):
        keys = {'12', '3', '', 0, 1, True, False}
        for real_key in keys:
            gen = TaskPassword.generator()
            gen.send(None)
            gen.send(real_key)
            for i in keys.difference({real_key}):
                answer = gen.send(i)
                self.assertIsInstance(answer, bool)
                self.assertFalse(answer)
            answer = gen.send(real_key)
            self.assertIsInstance(answer, bool)
            self.assertTrue(answer)
            with self.assertRaises(StopIteration):
                gen.send(None)

    def test_check_generator(self):
        for value in iterations_limit(TaskPassword.check_values(), 50):
            gen = TaskPassword.generator()
            gen.send(None)
            for iteration, send, awaited in zip(range(len(value.send)), value.send, value.awaited):
                answer = gen.send(send)
                self.assertEqual(answer, awaited, f'Iteration {iteration}')
