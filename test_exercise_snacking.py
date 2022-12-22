import pytest
from pytest import MonkeyPatch

from exercise_snacking import (
    get_category,
    get_number_of_exercises,
    get_exercise_list,
    generate_category_list,
    get_exercise_list_for_chosen_category,
    log_exercise_list,
)


@pytest.fixture
def test_list():
    return [
        {"name": "foo", "category": "full", "reps": 10, "rep_units": "each"},
        {"name": "bar", "category": "upper", "reps": 10, "rep_units": "each"},
        {"name": "baz", "category": "full", "reps": 10, "rep_units": "each"},
    ]


def test_generate_category_list(test_list):
    assert "upper" in generate_category_list(test_list)  
    assert "full" in generate_category_list(test_list)  


def test_proper_category_input(monkeypatch):
    lst = ["Foo", "Bar", "Baz"]
    monkeypatch.setattr("builtins.input", lambda _: "baz")
    assert get_category(lst, "question") == "Baz"


def test_no_category_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert get_category([], "question") == None


def test_get_category_list_with_category(test_list):
    category = "full"
    assert len(get_exercise_list_for_chosen_category(category, test_list)) == 2


def test_get_category_list_with_no_category(test_list):
    category = ""
    assert len(get_exercise_list_for_chosen_category(category, test_list)) == 3


def test_valid_number_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3")
    lst = ["foo", "bar", "baz"]
    assert get_number_of_exercises(lst, "question") == 3


def test_get_exercise_list(test_list):
    assert len(get_exercise_list(test_list, 2)) == 2


def test_log_exercise_list(capsys):
    lst = [{"name": "foo", "category": "full", "reps": 10, "rep_units": "each"}]
    log_exercise_list(lst)
    captured = capsys.readouterr()
    assert "foo" in captured.out.strip()
