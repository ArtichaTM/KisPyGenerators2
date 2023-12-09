from unittest import TestCase, SkipTest

from kipygen import TaskMeta, iterations_limit


class TestTaskCalculator(TestCase):
    cl: TaskMeta = None

    @classmethod
    def setUpClass(cls):
        cls.cl = TaskMeta.find_task('TaskCalculator')
        if cls.cl is None:
            raise SkipTest("Can't find task TaskCalculator")
