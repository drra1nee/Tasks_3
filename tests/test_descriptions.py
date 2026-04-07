"""Тесты дескрипторов"""
import pytest
from src.models.task import Task
from src.models.descriptors import (
    PriorityDescriptor,
    ReadOnlyDescriptor,
    StatusDescriptor,
    NonEmptyString,
)

def test_nonempty_string_descriptor_get():
    desc = NonEmptyString("payload")
    result = desc.__get__(None, Task)
    assert result is desc

def test_nonempty_string_delete():
    task = Task(payload="Test")
    del task.payload
    assert task.payload is None

def test_priority_descriptor_get():
    pd = PriorityDescriptor("priority")
    result = pd.__get__(None, Task)
    assert result is pd

def test_priority_descriptor_delete():
    task = Task(payload="Test", priority=5)
    del task.priority

def test_status_descriptor_get():
    sd = StatusDescriptor("status")
    result = sd.__get__(None, Task)
    assert result is sd

def test_status_descriptor_delete():
    task = Task(payload="Test", status="Pending")
    del task.status

def test_readonly_descriptor_get():
    rd = ReadOnlyDescriptor("_id")
    result = rd.__get__(None, Task)
    assert result is rd

def test_readonly_descriptor_delete():
    task = Task(payload="Test")
    with pytest.raises(AttributeError):
        del task.id