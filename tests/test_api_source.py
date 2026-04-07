"""Тесты API-заглушки источника задач"""
import pytest
from src.sources.api_source import APITaskSource, create_api_source
from src.contracts.protocol import TaskSource, validate_source

def test_create_api_source_default():
    source = APITaskSource()
    tasks = list(source.get_tasks())
    assert len(tasks) == 3

def test_create_api_source_custom_data():
    custom_data = [{"action": "test52"}, {"action": "test67"}]
    source = APITaskSource(tasks_data=custom_data)
    tasks = list(source.get_tasks())
    assert len(tasks) == 2

def test_api_source_implements_contract():
    source = APITaskSource()
    assert isinstance(source, TaskSource)
    assert validate_source(source) is True

def test_create_api_source():
    source = create_api_source(tasks_count=5)
    tasks = list(source.get_tasks())
    assert len(tasks) == 5

def test_api_source_refresh():
    custom_data = [{"action": "temp"}]
    source = APITaskSource(tasks_data=custom_data)
    assert len(list(source.get_tasks())) == 1
    source.refresh()
    assert len(list(source.get_tasks())) == 3

def test_payload_is_string():
    source = APITaskSource()
    tasks = list(source.get_tasks())
    assert all(isinstance(task.payload, str) for task in tasks)
