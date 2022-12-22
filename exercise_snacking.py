import csv
import random

from rich import print


def main():
    # user input questions
    category_question = "If you want exercises from a specific category, type a category here from the list above, or press Return for all categories: "
    number_question = "How many different ones do you want to do today? "

    # read exercises from csv file
    all_exercises = read_file("exercises.csv")
    print("\n[bold]WELCOME TO THE EXERCISE SNACKING LIST GENERATOR!\n")
    # get list by category
    categories = generate_category_list(all_exercises)
    category = get_category(categories, category_question)
    exercises = get_exercise_list_for_chosen_category(category, all_exercises)
    # get number of exercises and generate list
    number = get_number_of_exercises(exercises, number_question)
    exercise_list = get_exercise_list(exercises, number)
    log_exercise_list(exercise_list)


def read_file(file):
    """
    Reads csv file and returns a list of dictionaries containing the following keys:
    --name
    --category
    --reps
    --rep_units
    """
    with open(file, encoding="utf-8-sig") as csvfile:
        exercise_reader = csv.DictReader(
            csvfile,
        )
        exercises = [row for row in exercise_reader]

    return exercises


def generate_category_list(lst_of_dicts):
    """
    Returns a list of values from the category key
    """
    categories = set()
    for item in lst_of_dicts:
        for k, v in item.items():
            if k == "category":
                categories.add(v)

    print(f"Your available categories are: [bold red]{' | '.join(categories)}\n")

    return list(categories)


def get_category(lst, question):
    """Checks user input against list of categories to validate"""
    while True:
        category = input(question).title()
        try:
            if category not in lst and category != "":
                raise ValueError
        except ValueError:
            print(f"\n[bold red]{category} is not a category, please try again.\n")
        else:
            if category == "":
                return None
            else:
                return category


def get_exercise_list_for_chosen_category(category, lst):
    if category:
        return [exercise for exercise in lst if exercise["category"] == category]
    else:
        return lst


def get_number_of_exercises(lst, question):
    parsed = False
    while not parsed:
        print(f"\n[bold]There are {len(lst)} exercises available.\n")
        answer = input(question)
        try:
            number = int(answer)
            if number > len(lst):
                raise ValueError
            parsed = True
        except ValueError:
            print(
                f"\n[bold red]You entered {answer}. Please enter a number less than {len(lst) + 1}"
            )
        else:
            return number


def get_exercise_list(lst, number):
    exercise_list = []
    exercise_name_list = []
    while len(exercise_list) < number:
        exercise = random.choice(lst)
        if exercise["name"] not in exercise_name_list:
            exercise_name_list.append(exercise["name"])
            exercise_list.append(exercise)

    return exercise_list


def log_exercise_list(lst):
    print("\n [bold red]Here is your exercise list:\n")
    for i, exercise in enumerate(lst):
        print(
            f"{i+1}. {exercise['name']}: {exercise['reps']} {exercise['rep_units'] if exercise['rep_units'] != 'each' else 'reps'}"
        )


if __name__ == "__main__":
    main()
