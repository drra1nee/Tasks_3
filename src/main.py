"""Демонстрация платформы обработки задач"""
from src.contracts.protocol import validate_source
from src.sources.generator_source import create_generator_source
from src.sources.api_source import create_api_source
from src.models.task import Task
from src.exceptions.task_exceptions import TransitionError, InvalidPriorityError

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

def main() -> None:
    """Точка входа платформы"""
    print("ПЛАТФОРМА ОБРАБОТКИ ЗАДАЧ")
    demo_task_model()
    demo_generator_source()
    demo_api_source()

if __name__ == "__main__":
    main()
