#  EXERCISE SNACK LIST GENERATOR
#### Video Demo: URL https://youtu.be/q3zPHxHDu54

#### Description:
The Exercise Snack List Generator is a command line interface tool that does all of the following:
1. Provides a database (sqlite3) of 12 exercises with categories on initial startup.
2. Allows the user to add exercises to their database
3. Allows the user to delete exercises from their database
4. Updating exercises is planned for a future release. In the meantime, if you want to update an exercise, you must delete and then add it with your changes.
5. Creates a randomly-generated list of exercises to perform. In creating the list, the user can select a particular exercise category (i.e., "Core") or all categories.

### Usage:
To run the program, clone and then enter "python project.py" on the command line. You will be walked thru a series of command line prompts to perform your desired action.
### Files:
1. *project.py*: The main file for running the program. It prompts the user to enter a number related to what s/he would like to do - add an exercise to the db, delete an exercise, generate a list of exercises, or quit.
2. *api.py*: Contains all functions related to interacting with the sqlite3 database, including intially seeding the database if it doesn't exist; fetching all exercises; creating new exercises; deleting exercises; fetching all exercise names; and fetching exercise categories. 
3. *exercise_snacking.py*: Contains all functions to operate the program based on user interaction on the command line. 
4. *test_api.py*: Tests forapi.py.
5. *test_exercise_snacking.py*: Tests for exercise_snacking.py.

### Future Enhancements
The plan is to convert this project to a web-based application using Django and a more robust database. This will allow for enhancements such as:
1. A robust GUI
2. A community database of exercises
3. Additional user-defined data fields for routines, frequencies, etc.