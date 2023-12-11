[![Unittest 3.7-3.12](https://github.com/ArtichaTM/KisPyGenerators2/actions/workflows/unittest.yml/badge.svg)](https://github.com/ArtichaTM/KisPyGenerators2/actions/workflows/unittest.yml)
[![Flake8](https://github.com/ArtichaTM/KisPyGenerators2/actions/workflows/flake8.yml/badge.svg)](https://github.com/ArtichaTM/KisPyGenerators2/actions/workflows/flake8.yml)

# Задания на генераторы
Данный репозиторий предоставляет разного типа задачи для проверки знаний на [генераторы](https://docs.python.org/3/howto/functional.html#generators) на языке Python
## Зависимости
* Python: 3.10+
* Релиз: никакие
* Разработка: flake8
## Требуемые знания
* Общие знания об генераторах Python
* Понимание метода Generator.send()
* Понимание концепции передачи данных из и в генератор
## Примеры
#### Создание описания задач
```python
# Импортируем класс Exercise
from kipygen import Exercise

# Проходим циклом по всем задачам со сложностью от 10 до 20
for exercise in Exercise.random_range(10, 20):

  # Выведем описание упражнения
  print(exercise.description(), end='\n\n')
```
#### Сериализация и десериализация упражнений
```python
# Импортируем класс Exercise
from kipygen import Exercise, TaskMeta

# Создаём упражнение, состоящие из первых двух существующих задач
e1 = Exercise([TaskMeta.all_tasks[0], TaskMeta.all_tasks[1]])

# Сериализация
values: tuple[str, ...] = e1.save()

# Проверка
assert isinstance(values, tuple)
assert all((isinstance(i, str) for i in values))

# Десериализация
e2 = Exercise.load(values)

# Проверяем сходство
for left, right in zip(e1.tasks, e2.tasks):
    assert left.__qualname__ == right.__qualname__
```
#### Проверка существующего генератора
```python
# Импортируем класс Exercise
from kipygen import Exercise

# Загружаем задачи
e = Exercise.load(('TaskRange', 'TaskPassword'))

# Создаём генератор, решающий задачу
def gen():
    start = yield
    end = yield
    password = None
    yield
    while start <= end:
        password = yield start
        start += 1
    new_password = yield
    while True:
        if new_password == password:
            break
        new_password = yield False
    yield True

# Проверяем, отсутствуют ли ошибки
assert '' == e.validate(gen)
```

## Описание методов и переменных
В данном разделе описываются классы, их методы и переменные, рекомендуемые для взаимодействия с библиотекой.

Каждой отдельной задачей стоит класс Task из файла [tasks.py](src/tasks.py). Задачи составляют упражнение, его класс определён в [exercise.py](src/exercise.py).

### Структура
* **[src/kipygen](/src/kipygen)** - исходный код библиотеки
  * **[meta.py](src/kipygen/meta.py)** - Метакласс всех задач
  * **[tasks.py](src/kipygen/tasks.py)** - Задачи. Независимые классы, которые собираются в Exercise
  * **[exercise.py](src/kipygen/exercise.py)** - содержит класс Exercise, который является контейнером для задач, описанных в tasks.py
  * **[checkers.py](src/kipygen/checkers.py)** - содержит класс Checker и все основные проверяющие классы
  * **[checkhooks.py](src/kipygen/checkhooks.py)** - содержит класс CheckHook и все основные отправляющие классы
* **[tests](/tests)** - разные тесты для исходного кода
  * **[exercise](tests/exercise)** - Тесты относящиеся к классу Exercise
    * **[test_exercise.py](tests/exercise/test_exercise.py)** - Тесты методов Exercise
    * **[test_exercise_samples.py](tests/exercise/test_exercise_samples.py)** - Тесты синергии разных задач
  * **[tasks](tests/tasks)** - Индивидуальные тесты каждой задачи
### Классы
#### Exercise
```python
from typing import *

class Exercise:
  """ Класс, через который рекомендуется производить всё взаимодействие с библиотекой
  Русское название: упражнение
  """
  def check_values(self):
    """
    Возвращает генератор с ValuesTuple, который содержат последовательные значения из каждой задачи.
    Длины списков ValuesTuple.send и ValuesTuple.awaited гарантированно равны
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
    Задачи в каждом упражнении не повторяются.
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
    "Упражнение с 2 заданиями и 4 уровнем сложности"
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
Пример ввода и вывода (списки выровнены по элементам):
Входящие в генератор данные:    [ 1   , 3   , None, None, None, 'Password', 2    , ''   , 'Password', 0, ('+', 5) ]
Выходящие из генератора данные: [ None, None, 1   , 2   , 3   , None      , False, False, True      , 0, 5        ]
Входящие в генератор данные:    [ 1   , 4   , None, None, None, None, 1   , 2    , ''   , 1   , 70, ('*', 2) ]
Выходящие из генератора данные: [ None, None, 1   , 2   , 3   , 4   , None, False, False, True, 70, 140      ]
    """

```
#### TaskMeta
```python
from typing import *

class TaskMeta(type):
  """
  Метакласс для всех задач. Указывайте в качестве метакласса
  при создании разных задач
  """

  # Содержит задачи из всех источников
  # Предполагается, что переменная read-only
  all_tasks: List['TaskMeta'] = []

  @classmethod
  def find_task(cls, name: str) -> Union['TaskMeta', None]:
    """Возвращает задачу с указанным названием"""
```
#### Checker
```python
from typing import *

class Checker:
  """
  Данный класс предоставляет возможность кастомизировать проверку ввода и вывода
  данных из/в генератор
  Обязателен хотя бы один из методов send_value/output_value
  """
  def send_value(self) -> Any:
    """ Вызывается, когда нужно получить значение для отправки в генератор"""

  def output_value(self, generator_output: Any) -> str:
    """ Вызывается, когда получено значение из генератора и его нужно проверить
    :param generator_output: Вывод из генератора
    :return: Строка, содержащая ошибку.
        Пустая строка признаётся отсутствием ошибки
        Строка 'FINISH' сигнализирует об завершении проверки генератора.
            Зачастую это нужно для того, чтобы досрочно выйти из проверки
            при получении ожидаемого исключения

    """
    raise NotImplementedError()

  def name(self) -> str:
    """
    Вызывается при заполнении описаний ввода/вывода для пользователя.
    Краткое описание сути
    """
    raise NotImplementedError()

  def description(self) -> str:
    """
    Вызывается при составлении детального описания проверки.
    Обычно содержится внизу после списков ввода/вывода
    """
    raise NotImplementedError()
```
#### Checker
```python
from typing import *
from queue import Queue

class CheckHook:
  """
  Позволяет вручную вызывать методы у генератора и отправлять в него данные
  """
  __slots__ = ()

  def __call__(
      self,
      q_in: Queue,
      q_out: Queue,
      gen: Generator
  ) -> Any:
    """ Вызывается при требовании от генератора нового значения
    :param q_in: Очередь, в которую передаются значения для генератора.
    :param q_out: Очередь, в которую передаются значения полученные из генератора.
    :param gen: Проверяемый генератор
    :return: Значение, полученное от генератора
    """

  def name(self) -> str:
    """
    Вызывается при заполнении описаний ввода/вывода для пользователя.
    Краткое описание сути
    """

  def description(self) -> str:
    """
    Вызывается при составлении детального описания проверки.
    Обычно содержится внизу после списков ввода/вывода
    """

```
## Использование
Для начала нужно установить проект в качестве библиотеки
```commandline
python -m pip install .
```
В результате можно воспользоваться классами Exercise и TaskMeta из библиотеки KiPyGen:
```python
# Импортируем класс Exercise и TaskMeta
from kipygen import Exercise, TaskMeta

# Выведем список всех доступных задач
print(TaskMeta.all_tasks)

# Выведем количество возможных комбинаций задач
print(Exercise.combinations_amount())

# Пройдёмся по всевозможным комбинациям задач
for exercise in Exercise.random():
  # И выведем её краткой название
  print(exercise.name())
```
Список всех методов и их описание можно найти [выше](./readme.md#описание-методов-и-переменных)

