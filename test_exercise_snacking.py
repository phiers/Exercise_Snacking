import pytest
from pytest import MonkeyPatch
import sqlite3


from exercise_snacking import (
    get_all_data,
    run_process,
    get_exercise_list_for_chosen_category,
    get_category,
    get_exercise_snacking_list,
    get_number_of_exercises,
    output_exercise_list,
    input_exercise_name_to_delete,
    input_new_exercise,
)

from api import seed_db


@pytest.fixture
def test_list():
    return [
        ("foo", "full", 10, "each"),
        ("bar", "upper", 10, "each"),
        ("baz", "full", 10, "each"),
    ]


@pytest.fixture
def connection():
    connection = sqlite3.connect(":memory:")
    yield connection

    connection.close()


def test_fetch_all_data(connection):
    seed_db(connection)
    assert len(get_all_data(connection)) == 12


def test_proper_category_input(connection, monkeypatch):
    seed_db(connection)
    monkeypatch.setattr("builtins.input", lambda _: "core")
    assert get_category(connection, "question") == "Core"


def test_no_category_input(connection, monkeypatch):
    seed_db(connection)
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert get_category(connection, "question") == ""


# def test_improper_category_input(connection, monkeypatch, capsys):
#     seed_db(connection)
#     monkeypatch.setattr("builtins.input", lambda _: "Baz")
#     get_category(connection, "question")
#     captured = capsys.readouterr()
#     assert "valid" in captured.out.strip()


def test_get_category_list_with_category(test_list):
    assert len(get_exercise_list_for_chosen_category("full", test_list)) == 2


def test_get_category_list_with_no_category(test_list):
    assert len(get_exercise_list_for_chosen_category("", test_list)) == 3


def test_valid_number_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3")
    lst = ["foo", "bar", "baz"]
    assert get_number_of_exercises(lst, "question") == 3


def test_get_exercise_snacking_list(test_list):
    assert len(get_exercise_snacking_list(test_list, 2)) == 2


def test_log_exercise_list(test_list, capsys):
    output_exercise_list(test_list)
    captured = capsys.readouterr()
    print(captured.out.strip())
    assert "foo" in captured.out.strip()
