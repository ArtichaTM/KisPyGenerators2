from unittest import TestCase
from random import choices, randint

from src.meta import TaskMeta
from src.tasks import iterations_limit
from src.exercise import Exercise


class TestExercise(TestCase):
    __slots__ = ()

    def setUp(self):
        if len(TaskMeta.all_tasks) < 2:
            self.skipTest('Not enough tasks to check Exercise')

    def test_complexity_calculator(self):
        for _ in range(8):
            tasks = choices(TaskMeta.all_tasks, k=randint(1, len(TaskMeta.all_tasks)))
            e = Exercise(tasks)
            self.assertEqual(sum((i.complexity for i in tasks)), e.complexity)
