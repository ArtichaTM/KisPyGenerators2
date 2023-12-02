[![Unittest 3.7-3.12](https://github.com/ArtichaTM/KisPyGenerators2/actions/workflows/unittest.yml/badge.svg)](https://github.com/ArtichaTM/KisPyGenerators2/actions/workflows/unittest.yml)
[![Flake8](https://github.com/ArtichaTM/KisPyGenerators2/actions/workflows/flake8.yml/badge.svg)](https://github.com/ArtichaTM/KisPyGenerators2/actions/workflows/flake8.yml)

# Задания на генераторы
Данный репозиторий предоставляет разного типа задачи для проверки знаний на [генераторы](https://docs.python.org/3/howto/functional.html#generators) на языке Python
### Зависимости
* Релиз: никакие
* Разработка: flake8
### Требуемые знания
* Общие знания об генераторах Python
* Понимание метода Generator.send()
* Понимание концепции передачи данных из и в генератор
## Примеры
TODO
## Описание методов и переменных
В данном разделе описываются классы, их методы и переменные, рекомендуемые для взаимодействия с библиотекой.

Каждой отдельной задачей стоит класс Task из файла [tasks.py](src/tasks.py). Задачи составляют упражнение, его класс определён в [exercise.py](src/exercise.py).

### Структура
* **[src](/src)** - исходный код библиотеки
  * **[meta.py](src/meta.py)** - Метакласс всех задач
  * **[tasks.py](src/tasks.py)** - Задачи. Независимые классы, которые собираются в Exercise
  * **[exercise.py](src/exercise.py)** - содержит класс Exercise, который является контейнером для задач, описанных в tasks.py
* **[tests](/tests)** - разные тесты для исходного кода
  * **[exercise](tests/exercise)** - Tests corresponding to Exercise class
    * **[test_exercise.py](tests/exercise/test_exercise.py)** - Tasks to Exercise class methods
    * **[test_exercise_samples.py](tests/exercise/test_exercise_samples.py)** - Tests to some Exercise examples
  * **[tasks](tests/tasks)** - Individual task tests
### Методы
#### Exercise
```python
from typing import *

class Exercise:
    def check_values(self):
        """
        Возвращает генератор с ValuesTuple, который содержат последовательные значения из каждой задачи
        """
    def validate(self, factory: Callable[[], Generator], max_iterations: int = 50) -> str:
        """
        Проверяет фабрику генераторов на корректность в данном упражнение.
        В случае каких-либо ошибок возвращаемая строка содержит информацию об ошибке
        """
    @staticmethod
    def combinations_amount() -> int:
        """Возвращает число всевозможных комбинаций задач"""


    @classmethod
    def random(cls) -> Generator['Exercise', None, None]:
        """
        Возвращает генератор из всевозможных комбинаций задач без повторения.
        Задачи не повторяются.
        """

    @classmethod
    def random_range(
            cls,
            complexity_min: int = None,
            complexity_max: int = None
    ) -> Generator['Exercise', None, None]:
        """
        Возвращает генератор из всевозможных комбинаций задач без повторения со сложностью в отрезке complexity_min <= task.complexity <= complexity_min
        """

    def name(self) -> str:
      """
      Возвращает краткое название задачи. Пример:
      Упражнение с 2 заданиями и 4 уровнем сложности
      """

    def description(self) -> str:
      """
      Возвращает полное описание задачи, требуемое для её решения
      Пример:

Перед вами стоит задача построить генератор, который выполняет несколько последовательных задач:
1. Нужно вернуть все целые числа в диапазоне [start, end]
2. В генератор передаётся пароль. Возвращать False до тех пор, пока генератору не будет передан тот же пароль. В этом случае вернуть True и закончить работу
3. В первую очередь в генератор передаётся изначальное число, над которым будут производится операции, возвращая его обратно. Дальше в генератор будут передаваться пары (операция, число), где:
   > число: любое число типа float или int
   > операция: символ +, -, *, / для выполнения соответствующих операций
4. В первую очередь в генератор передаётся изначальное число, над которым будут производится операции, возвращая его обратно. Дальше в генератор будут передаваться пары (операция, число), где:
   > число: любое число типа float или int
   > операция: символ +, -, *, / для выполнения соответствующих операций
Пример ввода и вывода:
Входящие в генератор данные:    [1, 3, None, None, None, 'Password', 2, '', 'Password', 0, ('+', 5), None, 0, ('+', 5), None] 15
Выходящие из генератора данные: [None, 0, 1, 2, 3, None, False, False, True, 0, 5, 0, 5] 13
Входящие в генератор данные:    [1, 4, None, None, None, None, 1, 2, '', 1, 70, ('*', 2), None, 70, ('*', 2), None] 16
Выходящие из генератора данные: [None, 0, 1, 2, 3, 4, None, False, False, True, 70, 140, 70, 140] 14
      """

```
