from unittest import TestCase, SkipTest

from kipygen import TaskMeta


class TestTaskRange(TestCase):
    __slots__ = ('cl', )

    @classmethod
    def setUpClass(cls):
        cls.cl = TaskMeta.find_task('TaskRange')
        if cls.cl is None:
            raise SkipTest("Can't find task TaskRange")

    def test_generator(self):
        gen = self.cl.generator()
        self.assertEqual(gen.send(None), None)
        self.assertEqual(gen.send(5), None)
        self.assertEqual(gen.send(11), None)
        for i in range(5, 12):
            answer = gen.send(None)
            self.assertEqual(answer, i)
