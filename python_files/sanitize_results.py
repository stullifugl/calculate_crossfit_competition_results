import python_files.shared as shared
import python_files.setup_workouts as setup_workouts
import os

SETUP_WORKOUTS_PATH = setup_workouts.PATH


def sanitizeResults():
    competitonName = shared.getCompetitionName()

    workoutList = shared.getAllWorkouts()
    for workout in workoutList:
        csvPath = workout + '.csv'
        # Does the workout file exist
        if not os.path.exists(SETUP_WORKOUTS_PATH + '/' + competitonName + '/' + csvPath):
            print("The workout file for " + workout + " has not been setup")
            quit()

        # Check if some score has not been filled out
        sanitized = True
        workoutData = shared.getDataFromFile(csvPath)
        for data in workoutData:
            if data['Skor'] == '' or data['Skor'] == None:
                print("Error found in " + workout)
                print("Skor has not been added for team " +
                      data[shared.getWorkoutFieldToIndexFor()])
                sanitized = False

        if sanitized == True:
            print(workout + " is sanitized")
        else:
            print()
            print(workout + " is not sanitized, please fix")
