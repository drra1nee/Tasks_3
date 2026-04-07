"""Тесты для main"""
from src.main import main

def test_run_without_error(capsys):
    main()
    captured = capsys.readouterr()
    assert "ПЛАТФОРМА ОБРАБОТКИ ЗАДАЧ" in captured.out

def test_print_generator_source(capsys):
    main()
    captured = capsys.readouterr()
    assert "Источник: Генератор задач:" in captured.out
    assert "Контракт соблюден: GeneratorTaskSource" in captured.out


def test_print_api_source(capsys):
    main()
    captured = capsys.readouterr()
    assert "Источник: API-заглушка:" in captured.out
    assert "Контракт соблюден: APITaskSource" in captured.out
