"""Модуль генератора задач"""

from typing import Iterator
import random
from ..models.task import Task

class GeneratorTaskSource:
    """Генератор задач для тестирования и демонстрации"""

    # Список описаний для случайного выбора
    TASK_DESCRIPTIONS = [
        "Process order",
        "Send notification",
        "Check status",
        "Sync data",
        "Generate report",
        "Clear cache",
        "Verify database",
        "Backup data",
        "Process payment",
        "Update inventory",
    ]

    def __init__(self, count: int = 10) -> None:
        """Инициализирует генератор задач"""
        if count < 0:
            raise ValueError(f"count должен быть неотрицательным: {count}")
        self.count = count

    def get_tasks(self) -> Iterator[Task]:
        """Генерирует итератор задач"""
        for _ in range(self.count):
            # Случайный выбор описания из списка (могут повторяться)
            payload = random.choice(self.TASK_DESCRIPTIONS)
            yield Task(
                payload=payload,
                priority=random.randint(1, 10),
                status=random.choice(["Pending", "InProgress"])
            )

def create_generator_source(count: int = 10) -> GeneratorTaskSource:
    """Функция для создания генератора"""
    return GeneratorTaskSource(count=count)