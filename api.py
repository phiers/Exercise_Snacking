import sqlite3
from dataclasses import dataclass


@dataclass
class Exercise:
    name: str
    category: str
    reps: int
    rep_units: str


def seed_db(db_conn):
    with db_conn:
        cur = db_conn.cursor()
        cur.execute(
            """CREATE TABLE exercises
                    (name TEXT,
                    category TEXT, 
                    reps INTEGER,
                    rep_units TEXT)"""
        )

        data = [
            Exercise("Push-ups", "Upper body", "12", "each"),
            Exercise("Squats", "Lower body", "25", "each"),
            Exercise("Lunges", "Lower body", "15", "each side"),
            Exercise("Lunges - side", "Lower body", "15", "each side"),
            Exercise("Lunges - reverse", "Lower body", "15", "each side"),
            Exercise("Plank", "Core", "1", "minute"),
            Exercise("Plank - arm under", "Core", "10", "reps per side"),
            Exercise("Sprint-in-place", "Aerobic", "30", "seconds"),
            Exercise("Deadlift", "Full body", "12", "each"),
            Exercise("Windmills", "Mobility", "10", "each"),
            Exercise("Sun salutation A", "Mobility", "3", "each"),
            Exercise("Sun salutation B", "Mobility", "2", "each"),
        ]
        for item in data:
            data_dict = {
                "name": item.name.title(),
                "category": item.category.title(),
                "reps": item.reps,
                "rep_units": item.rep_units.title(),
            }
            cur.execute(
                "INSERT INTO exercises VALUES(:name, :category, :reps, :rep_units)",
                data_dict,
            )


def fetch_all(db_conn):
    with db_conn:
        cur = db_conn.cursor()
        results = cur.execute("SELECT * FROM exercises ORDER BY category")
        return results.fetchall()


def fetch_categories(db_conn):
    """Returns a set of categories from the database"""
    cur = db_conn.cursor()
    cur.execute("SELECT category FROM exercises")
    category_list = [cat for (cat,) in cur.fetchall()]
    categories = set(category_list)

    return sorted(categories)


def fetch_exercise_names(db_conn):
    cur = db_conn.cursor()
    cur.execute("SELECT name FROM exercises")
    exercise_names_list = [name for (name,) in cur.fetchall()]

    return sorted(exercise_names_list)


def create_exercise(db_conn, exercise):
    """
    ::param exercise:: a dictionary with keys name, category, reps, and rep_units
    adds exercise to the database
    returns None
    """
    with db_conn:
        cur = db_conn.cursor()
        cur.execute(
            "INSERT INTO exercises VALUES(:name, :category, :reps, :rep_units)",
            exercise,
        )


def delete_exercise(db_conn, exercise_name):
    with db_conn:
        cur = db_conn.cursor()
        cur.execute(
            "DELETE from exercises WHERE name = :name", {"name": exercise_name.title()}
        )
