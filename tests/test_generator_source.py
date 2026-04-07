"""Тесты генератора задач"""
import pytest
from src.sources.generator_source import GeneratorTaskSource, create_generator_source
from src.contracts.protocol import TaskSource

def test_create_with_custom_count():
    source = GeneratorTaskSource(count=5)
    assert source.count == 5

def test_create_with_negative_count():
    with pytest.raises(ValueError):
        GeneratorTaskSource(count=-1)

def test_get_tasks_correct_count():
    source = GeneratorTaskSource(count=5)
    tasks = list(source.get_tasks())
    assert len(tasks) == 5

def test_get_tasks_is_valid_source():
    source = GeneratorTaskSource(count=3)
    assert isinstance(source, TaskSource)

def test_payload_is_string():
    source = GeneratorTaskSource(count=3)
    tasks = list(source.get_tasks())
    assert all(isinstance(task.payload, str) for task in tasks)

def test_priority_in_range():
    source = GeneratorTaskSource(count=10)
    tasks = list(source.get_tasks())
    assert all(1 <= task.priority <= 10 for task in tasks)

def test_create_generator_source():
    source = create_generator_source(count=3)
    assert isinstance(source, GeneratorTaskSource)
    assert source.count == 3
