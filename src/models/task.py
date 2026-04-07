"""Модель задачи"""

from datetime import datetime
from .descriptors import (
    NonEmptyString,
    PriorityDescriptor,
    StatusDescriptor,
    ReadOnlyDescriptor,
)

class Task:
    """Задача платформы обработки"""
    # Дескрипторы
    payload = NonEmptyString("payload", max_length=500)
    priority = PriorityDescriptor("priority", min_value=1, max_value=10)
    status = StatusDescriptor("status")
    id = ReadOnlyDescriptor("_id")
    created_at = ReadOnlyDescriptor("_created_at")
    _task_counter = 0

    def __init__(self, payload: str = "No description", priority: int = 5, status: str = "Pending") -> None:
        """
        Инициализирует задачу
        Атрибуты:
            payload: Описание задачи
            priority: Приоритет задачи
            status: Статус задачи
            id: Уникальный идентификатор (только чтение)
            created_at: Время создания (только чтение)
        """
        self.id = self._generate_id()
        self.created_at = datetime.now()
        self.payload = payload
        self.priority = priority
        self.status = status

    @property
    def is_ready(self) -> bool:
        """Задача готова к выполнению"""
        return self.status == "Pending"

    @property
    def is_completed(self) -> bool:
        """Задача завершена"""
        return self.status in ("Done", "Cancelled")

    @property
    def age(self):
        """Время с момента создания"""
        return datetime.now() - self.created_at

    def change_status(self, new_status: str) -> None:
        """Смена статуса"""
        self.status = new_status

    def change_priority(self, new_priority: int) -> None:
        """Смена приоритета"""
        self.priority = new_priority

    def to_dict(self) -> dict:
        """Сериализация в словарь"""
        return {
            "id": self.id,
            "payload": self.payload,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def _generate_id(cls) -> str:
        """Генерирует уникальный код задачи"""
        cls._task_counter += 1
        return f"task_{cls._task_counter}"

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Десериализация из словаря"""
        if "payload" not in data:
            raise ValueError("Словарь должен содержать поле 'payload'")
        return cls(
            payload=data["payload"],
            priority=data.get("priority", 5),
            status=data.get("status", "Pending"),
        )

    def __str__(self) -> str:
        return f"Task(id={self.id}, status={self.status}, payload={self.payload!r})"

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id!r}, payload={self.payload!r}, "
            f"priority={self.priority}, status={self.status})"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
