"""Очередь задач с поддержкой итерации, фильтрации и потоковой обработки"""

from typing import Iterator, Optional
from itertools import islice
from ..models.task import Task


class TaskQueue:
    """Коллекция задач с ленивой фильтрацией и потоковой обработкой"""

    def __init__(self) -> None:
        """Инициализирует пустую очередь задач"""
        self._tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Добавляет задачу в очередь"""
        self._tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        """Удаляет задачу по ID"""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                self._tasks.pop(i)
                return True
        return False

    def __iter__(self) -> Iterator[Task]:
        """Возвращает новый итератор по задачам"""
        return iter(self._tasks)

    def __len__(self) -> int:
        """Количество задач в очереди"""
        return len(self._tasks)

    def __contains__(self, task: Task) -> bool:
        """Проверка наличия задачи в очереди"""
        return task in self._tasks

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Возвращает задачу по ID или None если не найдена"""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    # Ленивые фильтры (генераторы)

    def filter_by_status(self, status: str) -> Iterator[Task]:
        """Генератор задач с указанным статусом"""
        for task in self._tasks:
            if task.status == status:
                yield task

    def filter_by_priority(self, min_priority: int, max_priority: int) -> Iterator[Task]:
        """Генератор задач в диапазоне приоритетов (включительно)"""
        for task in self._tasks:
            if min_priority <= task.priority <= max_priority:
                yield task

    def filter_ready(self) -> Iterator[Task]:
        """Генератор готовых к выполнению задач"""
        for task in self._tasks:
            if task.is_ready:
                yield task

    def filter_completed(self) -> Iterator[Task]:
        """Генератор завершённых задач"""
        for task in self._tasks:
            if task.is_completed:
                yield task

    # Потоковая обработка

    def batch(self, size: int) -> Iterator[list[Task]]:
        """Генератор пакетов задач указанного размера"""
        if size <= 0:
            raise ValueError(f"Размер пакета должен быть положительным: {size}")
        for i in range(0, len(self._tasks), size):
            yield self._tasks[i:i + size]

    def take(self, n: int) -> Iterator[Task]:
        """Генератор первых n задач"""
        if n <= 0:
            return
        yield from islice(self._tasks, n)

    def skip(self, n: int) -> Iterator[Task]:
        """Генератор задач, пропуская первые n"""
        if n < 0:
            raise ValueError(f"Количество пропускаемых задач не может быть отрицательным: {n}")
        yield from islice(self._tasks, n, None)
