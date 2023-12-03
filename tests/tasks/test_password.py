from unittest import TestCase, SkipTest

from kipygen import TaskMeta, iterations_limit


class TestTaskPassword(TestCase):
    __slots__ = ('cl', )

    @classmethod
    def setUpClass(cls):
        cls.cl = TaskMeta.find_task('TaskPassword')
        if cls.cl is None:
            raise SkipTest("Can't find task TaskPassword")

    def test_generator(self):
        keys = {'12', '3', '', 0, 1, True, False}
        for real_key in keys:
            gen = self.cl.generator()
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
        for value in iterations_limit(self.cl.check_values(), 500):
            gen = self.cl.generator()
            gen.send(None)
            for iteration, send, awaited in zip(range(len(value.send)), value.send, value.awaited):
                answer = gen.send(send)
                self.assertEqual(answer, awaited, f'Iteration {iteration}')
