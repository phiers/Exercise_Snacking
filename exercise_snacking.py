import random
import sqlite3
import sys

from api import (
    fetch_all,
    fetch_categories,
    fetch_exercise_names,
    seed_db,
    create_exercise,
    delete_exercise,
)


def get_all_data(conn):
    """
    Fetches all data in the exercise table of the db. If the exercise table doesn't exist, the fetch_all
    function will fail, and seed_db is called to setup the exercise table with the initial data.
    Returns all data in database as a list of tuples
    """
    try:
        data = fetch_all(conn)
    except sqlite3.OperationalError:
        seed_db(conn)
        data = fetch_all(conn)
    else:
        return data


def run_process(conn, user_choice):
    data = get_all_data(conn)
    if user_choice == "1":
        exercise = input_new_exercise(conn)
        create_exercise(conn, exercise)
        sys.exit(f"{exercise['name']} added to the database")
    elif user_choice == "2":
        exercise_name = input_exercise_name_to_delete(conn)
        delete_exercise(conn, exercise_name)
        sys.exit(f"{exercise_name} was deleted from the database.")
    elif user_choice == "3":
        category_question = "If you want exercises from a specific category, type a category from the list above, or press Return for all categories: "
        number_question = "How many different ones do you want to do today? "
        category = get_category(conn, category_question)
        exercise_list = get_exercise_list_for_chosen_category(category, data)
        number_of_exercises = get_number_of_exercises(exercise_list, number_question)
        snacking_list = get_exercise_snacking_list(exercise_list, number_of_exercises)
        output_exercise_list(snacking_list)
    elif user_choice == "4":
        sys.exit()
    else:
        print("Please choose a valid option.")
        run_process(conn)


def input_new_exercise(conn):
    existing_exercises = fetch_exercise_names(conn)
    print(
        f"You have the following exercises in your database:\n {' | '.join(existing_exercises)}"
    )
    name = ""
    while not name:
        input_name = input("Enter a name for the exercise: ")
        if input_name not in existing_exercises:
            name = input_name
        else:
            print("That exercise already exists")
            name = ""
    print(f"Your existing categories are:\n {' | '.join(fetch_categories(conn))}")
    category = input("Enter a category from above or create a new one: ")
    rep_units = input(
        "What are the rep units for this exercise (e.g., 'each', 'minute', etc.): "
    )
    reps = None
    while not reps:
        try:
            input_reps = input("How many reps will you perform? ")
            reps = int(input_reps)
        except ValueError:
            print("You must enter an integer for this field")
            reps = None

    return {
        "name": name.title(),
        "category": category.title(),
        "reps": reps,
        "rep_units": rep_units.title(),
    }


def input_exercise_name_to_delete(conn):
    existing_exercises = fetch_exercise_names(conn)
    print(
        f"You have the following exercises in your database:\n {' | '.join(existing_exercises)}\n"
    )
    exercise_name = ""
    while not exercise_name:
        input_name = input("What exercise would you like to delete? ").title()
        if input_name in existing_exercises:
            exercise_name = input_name
        else:
            print(f"There is no exercise named {input_name} in the database")
            try_again = input("Would you like to try again? (y/n) ").lower()
            if try_again != "y":
                sys.exit()

    return exercise_name


def get_category(conn, question):
    """Checks user input against list of categories to validate"""
    category = ""
    category_list = fetch_categories(conn)
    while not category:
        print(
            f"Please enter a category from the following list:\n {' | '.join(category_list)}"
        )
        input_category = input(question).title()
        if input_category == "":
            return category
        if input_category in category_list:
            category = input_category
            return category
        else:
            print("Please enter a valid category or press return for all categories")


def get_exercise_list_for_chosen_category(category, lst):
    if category:
        return [exercise for exercise in lst if exercise[1] == category]
    else:
        return lst


def get_number_of_exercises(lst, question):
    parsed = False
    while not parsed:
        print(f"\nThere are {len(lst)} exercises available.\n")
        answer = input(question)
        try:
            number = int(answer)
            if number > len(lst):
                raise ValueError
            parsed = True
        except ValueError:
            print(
                f"\nYou entered {answer}. Please enter a number less than {len(lst) + 1}"
            )
        else:
            return number


def get_exercise_snacking_list(lst, number):
    exercise_list = []
    exercise_name_list = []
    while len(exercise_list) < number:
        exercise = random.choice(lst)
        if exercise[0] not in exercise_name_list:
            exercise_name_list.append(exercise[0])
            exercise_list.append(exercise)

    return exercise_list


def output_exercise_list(lst):
    print("\n Here is your exercise list:\n")
    for i, exercise in enumerate(lst):
        (name, _, reps, rep_units) = exercise
        print(f"{i+1}. {name}: {reps} {rep_units if rep_units != 'Each' else 'Reps'}")
