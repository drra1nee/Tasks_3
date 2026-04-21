"""Специализированные исключения для очереди задач"""


class QueueError(Exception):
    """Базовое исключение для очереди задач"""
    pass


class EmptyQueueError(QueueError):
    """Попытка получения задачи из пустой очереди"""
    pass


class TaskNotFoundError(QueueError):
    """Задача с указанным ID не найдена в очереди"""
    pass


class InvalidBatchSizeError(QueueError):
    """Некорректный размер пакета для потоковой обработки"""
    pass


class InvalidSkipCountError(QueueError):
    """Отрицательное количество пропускаемых задач"""
    pass