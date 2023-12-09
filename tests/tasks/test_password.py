from unittest import TestCase, SkipTest

from kipygen import TaskMeta


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
