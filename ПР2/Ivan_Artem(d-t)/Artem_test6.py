import pytest
from Artem_mutant5 import display_tasks, add_task, mark_task_done, delete_task, get_task_count

@pytest.fixture
def sample_tasks():
    return [
        {"desc": "Задача 1", "done": 0},
        {"desc": "Задача 2", "done": 1}
    ]

def test_display_tasks(sample_tasks):
    result = display_tasks(sample_tasks)
    assert "Задача 1" in result
    assert "не выполнено" in result
    assert "выполнено" in result

def test_add_task(sample_tasks):
    add_task(sample_tasks, "Новая задача")
    assert sample_tasks[-1]["desc"] == "Новая задача"
    assert sample_tasks[-1]["done"] == 0

def test_add_task_with_comma(sample_tasks, capsys):
    add_task(sample_tasks, "Задача, с запятой")
    captured = capsys.readouterr()
    assert "описание задачи не может содержать разделители" in captured.out

def test_add_task_empty_description(sample_tasks, capsys):
    add_task(sample_tasks, "")
    captured = capsys.readouterr()
    assert "описание задачи не должно быть пустым" in captured.out

def test_mark_task_done(sample_tasks):
    mark_task_done(sample_tasks, 0)
    assert sample_tasks[0]["done"] == 1

def test_mark_task_done_invalid_index(sample_tasks, capsys):
    mark_task_done(sample_tasks, 10)
    captured = capsys.readouterr()
    assert "такого индекса не существует! В данный момент индексы находятся в диапазоне от 0 до 1 включительно" in captured.out

def test_mark_task_done_invalid_type(sample_tasks, capsys):
    mark_task_done(sample_tasks, "abc")
    captured = capsys.readouterr()
    assert "неправильный формат ввода. Индекс должен быть целым неотрицательным числом" in captured.out

def test_delete_task(sample_tasks):
    delete_task(sample_tasks, 0)
    assert len(sample_tasks) == 1
    assert sample_tasks[0]["desc"] == "Задача 2"

def test_delete_task_invalid_index(sample_tasks, capsys):
    mark_task_done(sample_tasks, 10)
    captured = capsys.readouterr()
    assert "такого индекса не существует! В данный момент индексы находятся в диапазоне от 0 до 1 включительно" in captured.out

def test_delete_task_invalid_type(sample_tasks, capsys):
    delete_task(sample_tasks, "abc")
    captured = capsys.readouterr()
    assert "неправильный формат ввода. Индекс должен быть целым неотрицательным числом" in captured.out

def test_get_task_count(sample_tasks):
    assert get_task_count(sample_tasks) == "2"