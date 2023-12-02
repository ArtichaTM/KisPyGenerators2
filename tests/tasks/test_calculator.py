from unittest import TestCase, SkipTest

from kipygen import TaskMeta, iterations_limit


class TestTaskCalculator(TestCase):
    cl: TaskMeta = None

    @classmethod
    def setUpClass(cls):
        cls.cl = TaskMeta.find_task('TaskCalculator')
        if cls.cl is None:
            raise SkipTest("Can't find task TaskCalculator")

    def test_check_generator(self):
        iteration = 0
        for value in iterations_limit(self.cl.check_values(), 50):
            gen = self.cl.generator()
            gen.send(None)
            for send, awaited in zip(value.send, value.awaited):
                self.assertEqual(
                    gen.send(send),
                    awaited,
                    f"Error on {iteration} values iteration"
                )
            iteration += 1
