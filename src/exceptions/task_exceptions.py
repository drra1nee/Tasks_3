"""Специализированные исключения для задач"""

class TaskError(Exception):
    """Базовое исключение для задач"""
    pass

class InvalidPriorityError(TaskError):
    """Приоритет вне допустимого диапазона"""
    pass

class InvalidStatusError(TaskError):
    """Недопустимый статус задачи"""
    pass

class InvalidDescriptionError(TaskError):
    """Некорректное описание задачи"""
    pass

class TransitionError(TaskError):
    """Недопустимый переход между статусами"""
    pass