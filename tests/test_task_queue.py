"""Тесты очереди задач TaskQueue"""
import pytest
from itertools import islice
from src.queue.task_queue import TaskQueue
from src.models.task import Task

def test_create_empty_queue():
    queue = TaskQueue()
    assert len(queue) == 0

def test_add_and_remove_task():
    queue = TaskQueue()
    task = Task(payload="Test")
    queue.add_task(task)
    assert len(queue) == 1
    assert queue.remove_task(task.id) is True
    assert len(queue) == 0

def test_remove_task_not_exists():
    queue = TaskQueue()
    assert queue.remove_task("nonexistent_id") is False

def test_get_task_by_id():
    queue = TaskQueue()
    task = Task(payload="Test")
    queue.add_task(task)
    found = queue.get_task_by_id(task.id)
    assert found is not None and found.id == task.id

def test_iter_for_loop_and_to_list():
    queue = TaskQueue()
    queue.add_task(Task(payload="A"))
    queue.add_task(Task(payload="B"))
    assert sum(1 for _ in queue) == 2
    assert len(list(queue)) == 2

def test_iter_reusable():
    queue = TaskQueue()
    queue.add_task(Task(payload="A"))
    first_pass = list(queue)
    second_pass = list(queue)
    assert first_pass == second_pass

def test_iter_empty_queue():
    queue = TaskQueue()
    assert list(queue) == []

def test_contains_task():
    queue = TaskQueue()
    task = Task(payload="Test")
    queue.add_task(task)
    assert task in queue

def test_filter_by_status():
    queue = TaskQueue()
    queue.add_task(Task(payload="A", status="Pending"))
    queue.add_task(Task(payload="B", status="InProgress"))
    queue.add_task(Task(payload="C", status="Pending"))
    filtered = list(queue.filter_by_status("Pending"))
    assert len(filtered) == 2
    assert all(t.status == "Pending" for t in filtered)

def test_filter_by_priority_range():
    queue = TaskQueue()
    queue.add_task(Task(payload="A", priority=3))
    queue.add_task(Task(payload="B", priority=7))
    queue.add_task(Task(payload="C", priority=5))
    queue.add_task(Task(payload="D", priority=10))
    filtered = list(queue.filter_by_priority(4, 7))
    assert len(filtered) == 2

def test_filter_ready():
    queue = TaskQueue()
    queue.add_task(Task(payload="A", status="Pending"))
    queue.add_task(Task(payload="B", status="Done"))
    ready = list(queue.filter_ready())
    assert len(ready) == 1
    assert ready[0].is_ready

def test_filter_completed():
    queue = TaskQueue()
    queue.add_task(Task(payload="A", status="Done"))
    queue.add_task(Task(payload="B", status="Pending"))
    queue.add_task(Task(payload="C", status="Cancelled"))
    completed = list(queue.filter_completed())
    assert len(completed) == 2

def test_batch_split():
    queue = TaskQueue()
    for _ in range(7):
        queue.add_task(Task(payload="T"))
    batches = list(queue.batch(3))
    assert len(batches) == 3
    assert len(batches[0]) == 3
    assert len(batches[2]) == 1

def test_batch_invalid_size():
    queue = TaskQueue()
    with pytest.raises(ValueError):
        list(queue.batch(0))

def test_take():
    queue = TaskQueue()
    for i in range(10):
        queue.add_task(Task(payload=f"T{i}"))
    taken = list(queue.take(3))
    assert len(taken) == 3 and taken[0].payload == "T0"

def test_skip():
    queue = TaskQueue()
    for i in range(10):
        queue.add_task(Task(payload=f"T{i}"))
    skipped = list(queue.skip(8))
    assert len(skipped) == 2 and skipped[0].payload == "T8"

def test_skip_take_pagination():
    queue = TaskQueue()
    for i in range(10):
        queue.add_task(Task(payload=f"T{i}"))
    page = list(islice(queue.skip(5), 3))
    assert len(page) == 3
    assert page[0].payload == "T5"

def test_total_priority():
    queue = TaskQueue()
    queue.add_task(Task(payload="A", priority=3))
    queue.add_task(Task(payload="B", priority=7))
    assert queue.total_priority() == 10

def test_max_min_priority():
    queue = TaskQueue()
    queue.add_task(Task(payload="A", priority=3))
    queue.add_task(Task(payload="B", priority=10))
    queue.add_task(Task(payload="C", priority=5))
    assert queue.max_priority() == 10
    assert queue.min_priority() == 3

def test_aggregates_on_empty_queue():
    queue = TaskQueue()
    assert queue.total_priority() == 0
    assert queue.max_priority() is None
    assert queue.min_priority() is None

def test_large_queue_iteration():
    queue = TaskQueue()
    for i in range(10000):
        queue.add_task(Task(payload=f"Task_{i}", priority=(i % 10) + 1))
    assert sum(1 for _ in queue) == 10000

def test_sorted_by_priority():
    queue = TaskQueue()
    queue.add_task(Task(payload="A", priority=7))
    queue.add_task(Task(payload="B", priority=3))
    queue.add_task(Task(payload="C", priority=5))
    sorted_tasks = sorted(queue, key=lambda t: t.priority)
    assert [t.priority for t in sorted_tasks] == [3, 5, 7]
