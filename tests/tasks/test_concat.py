from unittest import TestCase, SkipTest

from kipygen import TaskMeta


class TestTaskConcat(TestCase):
    __slots__ = ('cl', )

    @classmethod
    def setUpClass(cls):
        cls.cl = TaskMeta.find_task('TaskConcat')
        if cls.cl is None:
            raise SkipTest("Can't find task TaskConcat")

    def test_generator(self):
        gen = self.cl.generator()
        gen.send(None)
        gen.send('12')
        gen.send('34')
        gen.send('7722')
        self.assertEqual(gen.send(None), '12347722')
