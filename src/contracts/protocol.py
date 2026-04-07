"""Контракты для источников задач"""

from typing import Protocol, Iterator, runtime_checkable
from ..models.task import Task

@runtime_checkable
class TaskSource(Protocol):
    """
    Контракт для всех источников задач
    Любой источник должен реализовать метод get_tasks()
    """
    def get_tasks(self) -> Iterator[Task]:
        """Вернуть итератор с задачами"""
        ...

def validate_source(source: object) -> bool:
    """Проверяет что источник соблюдает контракт"""
    if not isinstance(source, TaskSource):
        raise TypeError(f"Объект {type(source).__name__} не реализует TaskSource")
    else:
        return True
