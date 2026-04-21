"""Очередь задач с поддержкой итерации, фильтрации и потоковой обработки"""

from typing import Iterator, Optional, Callable, Iterable
from itertools import islice
from ..models.task import Task
from ..exceptions.queue_exceptions import (
    EmptyQueueError,
    TaskNotFoundError,
    InvalidBatchSizeError,
    InvalidSkipCountError,
)


class TaskQueue:
    """Коллекция задач с ленивой фильтрацией и потоковой обработкой"""

    def __init__(self, tasks_iter: Optional[Iterable[Task]] = None) -> None:
        """
        Инициализирует очередь задач
        tasks_iter: Итерируемый источник задач, если не указан, создаётся пустая очередь
        """
        self._source: Optional[Iterable[Task]] = tasks_iter
        self._pending: list[Task] = []  # Задачи, добавленные до первого обхода
        self._cache: Optional[list[Task]] = None  # Кэш для повторного обхода

    def _materialize(self) -> list[Task]:
        """Материализует все задачи в кэш"""
        if self._cache is not None:
            return self._cache

        self._cache = []
        # Сначала добавляем задачи из источника
        if self._source is not None:
            for task in self._source:
                self._cache.append(task)
            self._source = None

        # Затем добавляем отложенные задачи
        if self._pending:
            self._cache.extend(self._pending)
            self._pending = []

        return self._cache

    def _get_tasks(self) -> Iterator[Task]:
        """Возвращает итератор по задачам"""
        if self._cache is not None:
            yield from self._cache
            return
        self._cache = []
        if self._source is not None:
            for task in self._source:
                self._cache.append(task)
                yield task
            self._source = None
        if self._pending:
            for task in self._pending:
                self._cache.append(task)
                yield task
            self._pending = []

    def add_task(self, task: Task) -> None:
        """Добавляет задачу в очередь"""
        if self._cache is not None:
            self._cache.append(task)
        else:
            self._pending.append(task)

    def remove_task(self, task_id: str) -> bool:
        """Удаляет задачу по ID"""
        if self._cache is not None:
            for i, task in enumerate(self._cache):
                if task.id == task_id:
                    self._cache.pop(i)
                    return True
            raise TaskNotFoundError(f"Задача с ID '{task_id}' не найдена в очереди")
        elif self._source is not None:
            self._materialize()
            for i, task in enumerate(self._cache):
                if task.id == task_id:
                    self._cache.pop(i)
                    return True
            raise TaskNotFoundError(f"Задача с ID '{task_id}' не найдена в очереди")
        else:
            for i, task in enumerate(self._pending):
                if task.id == task_id:
                    self._pending.pop(i)
                    return True
            raise TaskNotFoundError(f"Задача с ID '{task_id}' не найдена в очереди")

    def __iter__(self) -> Iterator[Task]:
        """Возвращает новый итератор по задачам, поддерживает многократный обход очереди"""
        if len(self) == 0:
            raise EmptyQueueError("Невозможно создать итератор по пустой очереди")
        return self._get_tasks()

    def __len__(self) -> int:
        """Количество задач в очереди"""
        return len(self._materialize())

    def __contains__(self, task: Task) -> bool:
        """Проверка наличия задачи в очереди"""
        for t in self:
            if t == task:
                return True
        return False

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Возвращает задачу по ID или None если не найдена"""
        for task in self:
            if task.id == task_id:
                return task
        return None

    # Ленивые фильтры (генераторы)

    def filter_by_status(self, status: str) -> Iterator[Task]:
        """Генератор задач с указанным статусом"""
        for task in self:
            if task.status == status:
                yield task

    def filter_by_priority(self, min_priority: int, max_priority: int) -> Iterator[Task]:
        """Генератор задач в диапазоне приоритетов"""
        for task in self:
            if min_priority <= task.priority <= max_priority:
                yield task

    def filter_ready(self) -> Iterator[Task]:
        """Генератор готовых к выполнению задач"""
        for task in self:
            if task.is_ready:
                yield task

    def filter_completed(self) -> Iterator[Task]:
        """Генератор завершённых задач"""
        for task in self:
            if task.is_completed:
                yield task

    def filter(self, predicate: Callable[[Task], bool]) -> Iterator[Task]:
        """Универсальный ленивый фильтр по предикату"""
        for task in self:
            if predicate(task):
                yield task

    def map(self, func: Callable[[Task], any]) -> Iterator[any]:
        """Ленивое преобразование задач"""
        for task in self:
            yield func(task)

    # Потоковая обработка

    def batch(self, size: int) -> Iterator[list[Task]]:
        """Генератор пакетов задач указанного размера"""
        if size <= 0:
            raise InvalidBatchSizeError(f"Размер пакета должен быть положительным: {size}")
        batch = []
        for task in self:
            batch.append(task)
            if len(batch) >= size:
                yield batch
                batch = []
        if batch:
            yield batch

    def take(self, n: int) -> Iterator[Task]:
        """Генератор первых n задач"""
        if n <= 0:
            return
        count = 0
        for task in self:
            if count >= n:
                break
            yield task
            count += 1

    def skip(self, n: int) -> Iterator[Task]:
        """Генератор задач, пропуская первые n"""
        if n < 0:
            raise InvalidSkipCountError(f"Количество пропускаемых задач не может быть отрицательным: {n}")
        count = 0
        for task in self:
            if count < n:
                count += 1
                continue
            yield task

    # Удобные агрегатные методы

    def total_priority(self) -> int:
        """Сумма приоритетов всех задач"""
        return sum(t.priority for t in self)

    def max_priority(self) -> Optional[int]:
        """Максимальный приоритет в очереди"""
        priorities = [t.priority for t in self]
        return max(priorities) if priorities else None

    def min_priority(self) -> Optional[int]:
        """Минимальный приоритет в очереди"""
        priorities = [t.priority for t in self]
        return min(priorities) if priorities else None