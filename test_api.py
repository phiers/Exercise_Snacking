import pytest
import sqlite3

from api import (
    seed_db,
    fetch_all,
    fetch_categories,
    fetch_exercise_names,
    create_exercise,
    delete_exercise,
)


@pytest.fixture
def connection():
    connection = sqlite3.connect(":memory:")
    yield connection

    connection.close()


def test_fetch_all(connection):
    seed_db(connection)
    assert len(fetch_all(connection)) == 12
    assert type(fetch_all(connection)) == list
    assert type(fetch_all(connection)[0]) == tuple


def test_fetch_categories(connection):
    seed_db(connection)
    assert len(fetch_categories(connection)) == 6
    assert type(fetch_categories(connection)) == list
    assert len(set(fetch_categories(connection))) == len(fetch_categories(connection))


def test_fetch_exercise_names(connection):
    seed_db(connection)
    assert len(fetch_exercise_names(connection)) == 12
    assert type(fetch_exercise_names(connection)) == list
    assert type(fetch_exercise_names(connection)[0]) == str
    assert len(fetch_exercise_names(connection)) == len(
        set(fetch_exercise_names(connection))
    )


def test_create_exercise(connection):
    seed_db(connection)
    exercise = {"name": "test", "category": "test", "reps": 10, "rep_units": "test"}
    create_exercise(connection, exercise)
    assert len(fetch_all(connection)) == 13
    assert "test" in fetch_exercise_names(connection)
    assert "test" in fetch_categories(connection)


def test_delete_exercise(connection):
    seed_db(connection)
    delete_exercise(connection, "squats")
    assert len(fetch_all(connection)) == 11
    assert "squats" not in fetch_exercise_names(connection)
