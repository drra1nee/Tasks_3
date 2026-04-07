"""Тесты класса Task"""
import pytest
from src.models.task import Task
from datetime import timedelta
from src.exceptions.task_exceptions import (
    InvalidDescriptionError,
    InvalidPriorityError,
    InvalidStatusError,
    TransitionError,
)

def test_create_task_default():
    task = Task()
    assert task.id.startswith("task_")
    assert task.payload == "No description"
    assert task.priority == 5
    assert task.status == "Pending"

def test_create_task_custom():
    task = Task(payload="Test", priority=7, status="InProgress")
    assert task.payload == "Test"
    assert task.priority == 7
    assert task.status == "InProgress"

def test_task_id_unique():
    task1 = Task()
    task2 = Task()
    assert task1.id != task2.id

def test_id_readonly():
    task = Task()
    with pytest.raises(AttributeError):
        task.id = "hacked"

def test_created_at_readonly():
    task = Task()
    with pytest.raises(AttributeError):
        task.created_at = None

def test_empty_payload_error():
    with pytest.raises(InvalidDescriptionError):
        Task(payload="")

def test_invalid_priority_low():
    with pytest.raises(InvalidPriorityError):
        Task(payload="Test", priority=0)

def test_invalid_priority_high():
    with pytest.raises(InvalidPriorityError):
        Task(payload="Test", priority=11)

def test_invalid_status():
    with pytest.raises(InvalidStatusError):
        Task(payload="Test", status="Unknown")

def test_valid_transition():
    task = Task(payload="Test")
    task.change_status("InProgress")
    assert task.status == "InProgress"

def test_invalid_transition():
    task = Task(payload="Test", status="InProgress")
    with pytest.raises(TransitionError):
        task.change_status("Pending")

def test_is_ready():
    task = Task(payload="Test", status="Pending")
    assert task.is_ready is True

def test_is_completed():
    task = Task(payload="Test", status="Done")
    assert task.is_completed is True

def test_to_dict():
    task = Task(payload="Test", priority=7)
    data = task.to_dict()
    assert data["payload"] == "Test"
    assert data["priority"] == 7
    assert "id" in data
    assert "created_at" in data

def test_from_dict():
    task = Task.from_dict({"payload": "Test", "priority": 5})
    assert task.payload == "Test"
    assert task.priority == 5

def test_from_dict_missing_payload():
    with pytest.raises(ValueError):
        Task.from_dict({"priority": 5})

def test_task_eq():
    task1 = Task(payload="Test")
    task2 = Task(payload="Test")
    assert (task1 == task2) is False

def test_task_hash_exists():
    task = Task(payload="Test")
    assert isinstance(hash(task), int)

def test_task_age():
    task = Task(payload="Test")
    assert task.age is not None
    assert isinstance(task.age, timedelta)

def test_change_priority():
    task = Task(payload="Test", priority=5)
    task.change_priority(8)
    assert task.priority == 8

def test_task_eq_with_non_task():
    task = Task(payload="Test")
    result = task.__eq__("not_a_task")
    assert result is NotImplemented
