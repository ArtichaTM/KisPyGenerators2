from unittest import TestCase, SkipTest

from kipygen import TaskMeta, iterations_limit


class TestTaskRange(TestCase):
    __slots__ = ('cl', )

    @classmethod
    def setUpClass(cls):
        cls.cl = TaskMeta.find_task('TaskRange')
        if cls.cl is None:
            raise SkipTest("Can't find task TaskRange")

    def test_generator(self):
        gen = self.cl.generator()
        gen.send(None)
        gen.send(5)
        gen.send(10)
        for i in range(5, 11):
            answer = gen.send(None)
            self.assertEqual(answer, i)

    def test_check_generator(self):
        counter = 0
        for value in iterations_limit(self.cl.check_values(), 50):
            gen = self.cl.generator()
            gen.send(None)
            for send, awaited in zip(value.send, value.awaited):
                self.assertEqual(gen.send(send), awaited, f"Error on {counter} values iteration")
            counter += 1
