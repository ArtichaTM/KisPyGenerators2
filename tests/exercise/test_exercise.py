from unittest import TestCase
from random import choices, randint, shuffle
from functools import partialmethod

from kipygen import Exercise, TaskMeta, iterations_limit


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

    def random_range(self, _min: int, _max: int):
        for exercise in Exercise.random_range(_min, _max):
            text = ', '.join((i.__qualname__ for i in exercise.tasks))
            text = (
                f"Exercise {exercise} with {text} complexity not in range "
                f"{_min} <= {exercise.complexity} <= {_max}"
            )
            self.assertGreaterEqual(exercise.complexity, _min, text)
            self.assertLessEqual(exercise.complexity, _max, text)

    def test_random_range(self):
        assert len(TaskMeta.all_tasks) >= 2
        self.random_range(1, 5)
        self.random_range(5, 10)

    def test_description_all_tasks(self):
        values = [*Exercise.random_range(8, 15)]
        shuffle(values)
        for exercise in values:
            exercise_description = exercise.description()
            for task in exercise.tasks:
                for line in task.short_description():
                    self.assertIn(
                        line,
                        exercise_description,
                        f"Awaited line:\n> {line}\nText:\n>{exercise_description}"
                    )

    def test_all_tasks_send_awaited_length(self):
        for exercise in Exercise.random():
            if len(exercise.tasks) > 1:
                continue
            for check_values in iterations_limit(exercise.check_values(), 100):
                self.assertEqual(
                    len(check_values.send),
                    len(check_values.awaited),
                    f'Task {exercise.tasks[0].__qualname__} send and awaited lists length'
                    ' are not equal:'
                    f'\nSend:    {len(check_values)} - {check_values.send}'
                    f'\nAwaited: {len(check_values)} - {check_values.awaited}'
                )

    def test_save_load(self):
        task1, task2 = choices(TaskMeta.all_tasks, k=2)
        e1 = Exercise([task1, task2])
        values = e1.save()
        e2 = Exercise.load(values)
        self.assertEqual(len(e1.tasks), len(e2.tasks))
        for left, right in zip(e1.tasks, e2.tasks):
            left: TaskMeta
            right: TaskMeta
            self.assertEqual(left.__qualname__, right.__qualname__)


def fill_with_tests(cl):
    for task in TaskMeta.all_tasks:
        def function(self, _task):
            e = Exercise([_task])
            self.assertEqual('', e.validate(_task.generator))
        function = partialmethod(function, _task=task)
        setattr(cl, f"test_{task.__qualname__}", function)
    return cl


@fill_with_tests
class TestEveryTask(TestCase):
    pass
