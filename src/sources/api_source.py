"""Модуль API-заглушки"""

from typing import Iterator
from ..models.task import Task


class APITaskSource:
    """API-заглушка для имитации внешнего источника задач"""

    def __init__(self, tasks_data: list[dict] | None = None) -> None:
        """Инициализирует API-заглушку"""
        self._tasks_data = tasks_data or self._get_default_tasks()

    def _get_default_tasks(self) -> list[dict]:
        """Возвращает данные задач по умолчанию"""
        return [
            {"action": "notify", "user_id": 1, "priority": 7},
            {"action": "process", "order_id": 67, "priority": 5},
            {"action": "check", "resource": "db", "priority": 3},
        ]

    def get_tasks(self) -> Iterator[Task]:
        """Генерирует итератор задач из API-заглушки"""
        for task_data in self._tasks_data:
            action = task_data.get("action", "unknown")
            payload = f"API Task: {action}"
            priority = task_data.get("priority", 5)
            status = task_data.get("status", "Pending")
            yield Task(
                payload=payload,
                priority=priority,
                status=status
            )

    def refresh(self) -> None:
        """Имитирует обновление данных из API"""
        self._tasks_data = self._get_default_tasks()

def create_api_source(tasks_count: int = 3) -> APITaskSource:
    """Функция для создания API-заглушки"""
    tasks_data = [
        {"action": "job", "index": i, "priority": (i % 10) + 1}
        for i in range(tasks_count)
    ]
    return APITaskSource(tasks_data=tasks_data)
