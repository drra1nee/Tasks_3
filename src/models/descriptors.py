"""Модуль дескрипторов для валидации атрибутов задачи"""

from typing import Any, Optional
from ..exceptions.task_exceptions import (
    InvalidDescriptionError,
    InvalidPriorityError,
    InvalidStatusError,
    TransitionError,
)

class NonEmptyString:
    """Data descriptor для валидации строк"""
    def __init__(self, name: str, max_length: int = 500) -> None:
        """Инициализирует дескриптор"""
        self.name = name
        self.max_length = max_length

    def __get__(self, instance: Optional[object], owner: type) -> Any:
        """Получает значение атрибута"""
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance: object, value: Any) -> None:
        """Устанавливает значение атрибута с валидацией"""
        if not isinstance(value, str):
            raise InvalidDescriptionError(f"{self.name} должен быть строкой, не {type(value).__name__}")
        if not value.strip():
            raise InvalidDescriptionError(f"{self.name} не может быть пустым!")
        if len(value) > self.max_length:
            raise InvalidDescriptionError(f"{self.name} не может быть длиннее {self.max_length} символов")
        instance.__dict__[self.name] = value

    def __delete__(self, instance: object) -> None:
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]

class PriorityDescriptor:
    """
    Data descriptor для валидации приоритета задачи
    Приоритет должен быть целым числом от 1 до 10
    """
    def __init__(self, name: str = "priority", min_value: int = 1, max_value: int = 10) -> None:
        """Инициализирует дескриптор"""
        self.name = name
        self.min_value = min_value
        self.max_value = max_value

    def __get__(self, instance: Optional[object], owner: type) -> Any:
        """Получает значение приоритета или значение 5 если не установлено"""
        if instance is None:
            return self
        return instance.__dict__.get(self.name, 5)

    def __set__(self, instance: object, value: Any) -> None:
        """Устанавливает значение приоритета с валидацией"""
        if not isinstance(value, int):
            raise InvalidPriorityError(f"{self.name} должно быть целым числом, не {type(value).__name__}")
        if not (self.min_value <= value <= self.max_value):
            raise InvalidPriorityError(
                f"{self.name} должен быть от {self.min_value} до {self.max_value}, получено {value}"
            )
        instance.__dict__[self.name] = value

    def __delete__(self, instance: object) -> None:
        """Удаляет значение из хранилища"""
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]


class StatusDescriptor:
    """
    Data descriptor для валидации статуса задачи
    Допустимые статусы: Pending, InProgress, Done, Cancelled
    """
    VALID_STATUSES = ("Pending", "InProgress", "Done", "Cancelled")
    VALID_TRANSITIONS = {
        "Pending": ["Pending", "InProgress", "Cancelled"],
        "InProgress": ["InProgress", "Done", "Cancelled"],
        "Done": ["Done"],
        "Cancelled": ["Cancelled"],
    }

    def __init__(self, name: str = "status") -> None:
        """Инициализирует дескриптор"""
        self.name = name

    def __get__(self, instance: Optional[object], owner: type) -> Any:
        """Получает значение статуса"""
        if instance is None:
            return self
        return instance.__dict__.get(self.name, "Pending")

    def __set__(self, instance: object, value: Any) -> None:
        """Устанавливает значение статуса с валидацией"""
        if not isinstance(value, str):
            raise InvalidStatusError(
                f"{self.name} должен быть строкой, не {type(value).__name__}"
            )
        if value not in self.VALID_STATUSES:
            raise InvalidStatusError(
                f"Недопустимый статус: {value}. "
                f"Разрешены: {', '.join(self.VALID_STATUSES)}"
            )
        # Проверка изменения статусов
        if self.name in instance.__dict__:
            current_status = instance.__dict__[self.name]
            if value not in self.VALID_TRANSITIONS.get(current_status, []):
                raise TransitionError(f"Недопустимый переход: {current_status} -> {value}")
        instance.__dict__[self.name] = value

    def __delete__(self, instance) -> None:
        key = self.name
        if key in instance.__dict__:
            del instance.__dict__[self.name]


class ReadOnlyDescriptor:
    """Data descriptor для защищённых атрибутов (только чтение)"""
    def __init__(self, name: str) -> None:
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value) -> None:
        """Разрешает первую установку, запрещает повторную"""
        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = value
            return
        # Повторная установка запрещена
        raise AttributeError(f"Атрибут '{self.name}' только для чтения")

    def __delete__(self, instance) -> None:
        raise AttributeError(f"Атрибут '{self.name}' нельзя удалить")
