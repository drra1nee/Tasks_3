"""Демонстрация платформы обработки задач"""
from src.contracts.protocol import validate_source
from src.sources.generator_source import create_generator_source
from src.sources.api_source import create_api_source
from src.models.task import Task
from src.exceptions.task_exceptions import TransitionError, InvalidPriorityError
from src.queue.task_queue import TaskQueue

def demo_task_model() -> None:
    """Демонстрация модели Task с дескрипторами"""
    print("Модель задачи:")
    print("-" * 40)
    # Создание задачи с валидацией
    task = Task(payload="Process order", priority=7, status="Pending")
    print(f"Создана: {task}")
    print(f"  ID: {task.id}")
    print(f"  Приоритет: {task.priority}")
    print(f"  Статус: {task.status}")
    print(f"  Время создания: {task.created_at}")
    print(f"  Готовность: {task.is_ready}")
    # Смена статуса
    task.change_status("InProgress")
    print(f"\nСтатус изменён: {task.status}")
    print(f"  Готовность: {task.is_ready}")
    print(f"  Завершена: {task.is_completed}")
    # Попытка недопустимого перехода
    print("\nПопытка недопустимого перехода:")
    try:
        task.change_status("Pending")
    except TransitionError as e:
        print(f"  ✗ Ошибка: {e}")
    # Попытка невалидного приоритета
    print("\nПопытка невалидного приоритета:")
    try:
        task.priority = 15
    except InvalidPriorityError as e:
        print(f"  ✗ Ошибка: {e}")
    print()

def demo_generator_source() -> None:
    """Демонстрация источника-генератора"""
    print("Источник: Генератор задач:")
    print("-" * 40)
    source = create_generator_source(count=3)
    if validate_source(source):
        print("Контракт соблюден: GeneratorTaskSource")
    for task in source.get_tasks():
        print(f"  {task.id}: {task.payload} (priority={task.priority}, status={task.status})")
    print()

def demo_api_source() -> None:
    """Демонстрация API-заглушки"""
    print("Источник: API-заглушка:")
    print("-" * 40)
    source = create_api_source(tasks_count=3)
    if validate_source(source):
        print("Контракт соблюден: APITaskSource")
    for task in source.get_tasks():
        print(f"  {task.id}: {task.payload} (priority={task.priority}, status={task.status})")
    print()

def demo_task_queue() -> None:
    """Демонстрация очереди задач с итерацией, фильтрацией и потоковой обработкой"""
    print("Очередь задач (TaskQueue):")
    print("-" * 40)

    # Создание и заполнение очереди
    queue = TaskQueue()
    queue.add_task(Task(payload="Process order", priority=7, status="Pending"))
    queue.add_task(Task(payload="Send notification", priority=3, status="InProgress"))
    queue.add_task(Task(payload="Check status", priority=10, status="Pending"))
    queue.add_task(Task(payload="Sync data", priority=5, status="Done"))
    queue.add_task(Task(payload="Generate report", priority=8, status="Cancelled"))
    print(f"Добавлено задач: {len(queue)}")

    # Итерация (for)
    print("\nВсе задачи (for):")
    for task in queue:
        print(f"  {task.id}: {task.payload} (priority={task.priority}, status={task.status})")

    # Повторный обход
    print("\nПовторный обход (второй for):")
    count = sum(1 for _ in queue)
    print(f"  Найдено задач: {count}")

    # Ленивая фильтрация по статусу
    print("\nФильтр по статусу 'Pending':")
    for task in queue.filter_by_status("Pending"):
        print(f"  {task.id}: {task.payload}")

    # Ленивая фильтрация по приоритету
    print("\nФильтр по приоритету 1-5:")
    for task in queue.filter_by_priority(1, 5):
        print(f"  {task.id}: {task.payload} (priority={task.priority})")

    # Фильтр готовых задач
    print("\nГотовые задачи (filter_ready):")
    for task in queue.filter_ready():
        print(f"  {task.id}: {task.payload}")

    # Фильтр завершённых задач
    print("\nЗавершённые задачи (filter_completed):")
    for task in queue.filter_completed():
        print(f"  {task.id}: {task.payload} (status={task.status})")

    # Пакетная обработка
    print("\nПакеты по 2 (batch):")
    for i, batch in enumerate(queue.batch(2), 1):
        print(f"  Пакет {i}: {[t.payload for t in batch]}")

    # take / skip
    print("\nПервые 3 задачи (take):")
    for task in queue.take(3):
        print(f"  {task.id}: {task.payload}")

    print("\nПропуск первых 3 (skip):")
    for task in queue.skip(3):
        print(f"  {task.id}: {task.payload}")

    # Агрегатные методы
    print(f"\nСумма приоритетов: {queue.total_priority()}")
    print(f"Максимальный приоритет: {queue.max_priority()}")
    print(f"Минимальный приоритет: {queue.min_priority()}")

    # Проверка наличия
    first_task = list(queue)[0]
    print(f"\nПроверка наличия (first_task in queue): {first_task in queue}")

    # Удаление задачи
    print(f"\nУдаление задачи {first_task.id}: {queue.remove_task(first_task.id)}")
    print(f"Осталось задач: {len(queue)}")
    print()

def main() -> None:
    """Точка входа платформы"""
    print("ПЛАТФОРМА ОБРАБОТКИ ЗАДАЧ")
    demo_task_model()
    demo_generator_source()
    demo_api_source()
    demo_task_queue()

if __name__ == "__main__":
    main()
