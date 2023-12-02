from unittest import TestCase
from random import choices, randint, shuffle

from src import TaskMeta, Exercise


class TestExercise(TestCase):
    __slots__ = ()

    def setUp(self):
        if len(TaskMeta.all_tasks) < 2:
            self.skipTest('Not enough tasks to check Exercise')

    def test_complexity_calculator(self):
        assert len(TaskMeta.all_tasks) >= 2
        for _ in range(8):
            tasks = choices(TaskMeta.all_tasks, k=randint(1, len(TaskMeta.all_tasks)))
            e = Exercise(tasks)
            self.assertEqual(sum((i.complexity for i in tasks)), e.complexity)

    def test_random(self):
        assert len(TaskMeta.all_tasks) >= 2
        counter = None
        for counter, _ in enumerate(Exercise.random()):
            pass
        if counter is None:
            self.fail("No tasks returned from Exercise.random()")
        self.assertEqual(
            counter+1,
            Exercise.combinations_amount(),
            'Wrong algorithm for random combinations calculate'
        )

    def random_range(self, min: int, max: int):
        for exercise in Exercise.random_range(min, max):
            text = ', '.join((i.__qualname__ for i in exercise.tasks))
            text = (
                f"Exercise {exercise} with {text} complexity not in range "
                f"{min} <= {exercise.complexity} <= {max}"
            )
            self.assertGreaterEqual(exercise.complexity, min, text)
            self.assertLessEqual(exercise.complexity, max, text)

    def test_random_range(self):
        assert len(TaskMeta.all_tasks) >= 2
        self.random_range(1, 5)
        self.random_range(5, 10)

    def test_description(self):
        values = [*Exercise.random_range(3, 6)]
        shuffle(values)
        print('Tasks amount:', len(values))
        for i in values:
            print(i.description(), '\n\n')
