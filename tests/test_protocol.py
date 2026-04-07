"""Тесты контракта TaskSource"""

import pytest
from typing import Iterator
from src.models.task import Task
from src.contracts.protocol import TaskSource, validate_source
from src.sources.generator_source import GeneratorTaskSource

class ValidSource:
    def get_tasks(self) -> Iterator[Task]:
        yield Task()

class InvalidSource:
    def fetch_tasks(self) -> Iterator[Task]:
        yield Task()

def test_generator_source_is_task_source():
    source = GeneratorTaskSource(count=3)
    assert isinstance(source, TaskSource)

def test_valid_source_is_task_source():
    assert isinstance(ValidSource(), TaskSource)

def test_invalid_source_not_task_source():
    assert not isinstance(InvalidSource(), TaskSource)

def test_validate_valid_source():
    source = GeneratorTaskSource(count=2)
    result = validate_source(source)
    assert result is True

def test_validate_invalid_source():
    with pytest.raises(TypeError) as ex_info:
        validate_source(InvalidSource())
    assert "не реализует TaskSource" in str(ex_info.value)
