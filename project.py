import sqlite3


from exercise_snacking import run_process


def main():
    conn = sqlite3.connect("exercise.db")
    print("\nWELCOME TO THE EXERCISE SNACKING LIST GENERATOR!\n")
    user_choice = input(
        """What would you like to do?
                         1) Add an exercise to the database
                         2) Delete an exercise from the database
                         3) Generate an exercise list
                         4) Quit the program 
                         
                         Enter your your choice number: """
    )
    run_process(conn, user_choice)


if __name__ == "__main__":
    main()
