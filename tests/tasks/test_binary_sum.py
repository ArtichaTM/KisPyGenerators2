from unittest import TestCase, SkipTest

from kipygen import TaskMeta


class TestTaskBinarySum(TestCase):
    cl: TaskMeta = None

    @classmethod
    def setUpClass(cls):
        cls.cl = TaskMeta.find_task('TaskBinarySum')
        if cls.cl is None:
            raise SkipTest("Can't find task TaskBinarySum")
