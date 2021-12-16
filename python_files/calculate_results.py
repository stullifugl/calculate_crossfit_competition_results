import python_files.calculate_workout as calculate_workout
import python_files.shared as shared
import python_files.consts as consts
import python_files.setup_workouts as setup_workouts
import csv
import os
import shutil

PATH = 'results'
SETUP_WORKOUTS_PATH = setup_workouts.PATH

def getDataFromWorkoutForTeam(team: dict, workoutDictList: list) -> tuple:
    for dict in workoutDictList:
        if dict[shared.getWorkoutFieldToIndexFor()] == team[shared.getWorkoutFieldToIndexFor()]:
            return dict['Points'], dict['Skor']

    shared.logError("Could not find team in function getDataFromWorkoutForTeam")
    return 0.0, 0.0

def calculateTeamsScore(workoutDataList: list, categoryString: str) -> list:
    totalTeamScoreList = []
    teams = shared.getTeamsInCertainCategory(categoryString)

    for team in teams:
        dict = {}
        totalPoints = 0
        dict[shared.getWorkoutFieldToIndexFor()] = team[shared.getWorkoutFieldToIndexFor()]
        for workoutDict in workoutDataList:
            pointsForWorkout, workoutScore = getDataFromWorkoutForTeam(team, workoutDict['results'])
            dict[workoutDict['workout'] + '_points'] = pointsForWorkout
            dict[workoutDict['workout'] + '_score'] = workoutScore
            totalPoints += pointsForWorkout
        dict['total_points'] = totalPoints

        totalTeamScoreList.append(dict)
    
    return calculate_workout.orderDictList(totalTeamScoreList, False, 'total_points')

def generateWorkoutDataListDict(teamScoreList: list, file: str) -> list:
    returnList = []
    orderedList = calculate_workout.orderDictList(teamScoreList, False, file + '_points')

    for team in orderedList:
        dict = {}
        dict[shared.getWorkoutFieldToIndexFor()] = team[shared.getWorkoutFieldToIndexFor()]
        dict['Skor'] = team[file + '_score']
        dict['Stig'] = team[file + '_points']

        returnList.append(dict)

    return returnList

def generateTotalDataListDict(teamScoreList: list) -> list:
    returnList = []
    orderedList = calculate_workout.orderDictList(teamScoreList, False, 'total_points')
    keyList = teamScoreList[0].keys()

    for team in orderedList:
        dict = {}
        for key in keyList:
            dict[key] = team[key]

        returnList.append(dict)

    return returnList

def populateWorkoutResults(folderPath: str, teamScoreList: list, file: str) -> None:
    with open(folderPath + '/' + file + '.csv', 'w', encoding='UTF8', newline='') as f:
        fieldList = [shared.getWorkoutFieldToIndexFor(), 'Skor', 'Stig']

        writer = csv.DictWriter(f, fieldnames=fieldList)
        writer.writeheader()
        for dict in generateWorkoutDataListDict(teamScoreList, file):
            writer.writerow(dict)

def populateGeneralResults(folderPath: str, teamScoreList: list) -> None:
    with open(folderPath + '/total.csv', 'w', encoding='UTF8', newline='') as f:
        keyList = teamScoreList[0].keys()
        writer = csv.DictWriter(f, fieldnames=keyList)
        writer.writeheader()
        for dict in generateTotalDataListDict(teamScoreList):
            writer.writerow(dict)

def getTopThreeTeams(teamScoreList: list) -> list:
    returnList = []

    for i in range(0, 3):
        if len(teamScoreList) > i:
            data = teamScoreList[i]
            dataStr = '\t' + str(i + 1) + ':  ' + data[shared.getWorkoutFieldToIndexFor()] + ' - ' + str(data['total_points'])
            returnList.append(dataStr)

    return returnList

def addTopTeamsToOverallFile(teamScoreList: list, categoryString: str) -> None:
    competitionName = shared.getCompetitionName()
    competitionPath = PATH + '/' + competitionName

    topTeams = getTopThreeTeams(teamScoreList)
    with open(competitionPath + '/' + consts.OVERALLFILENAME, "a+") as file:
        file.write(categoryString.replace('_', ' -> ') + '   (' + str(len(teamScoreList)) + ' lið)')
        file.write('\n')
        for teamStr in topTeams:
            file.write(teamStr)
            file.write('\n')
        
        file.write('\n')
        file.write('\n')
        

def generateFiles(teamScoreList: list, categoryString: str) -> None:
    folderPath = ""
    folderPath = PATH + '/' + shared.getCompetitionName() + '/' + '/'.join(categoryString.split('_'))
    
    if teamScoreList:
        keyList = teamScoreList[0].keys()
        keySet = set()
        fileNameList = []

        for key in keyList:
            if 'workout' in key:
                str = key.replace('_points', '')
                str = str.replace('_score', '')
                keySet.add(str)

        fileNameList = list(keySet)
        for file in fileNameList:
            populateWorkoutResults(folderPath, teamScoreList, file)
        populateGeneralResults(folderPath, teamScoreList)
        addTopTeamsToOverallFile(teamScoreList, categoryString)
    else:
        print("No competitors assigned for the following category: " + categoryString)
    
def generateCategoryFolders() -> None:
    categoryList, secondCategoryList = shared.getCategoriesForFolderCreation()
    competitionName = shared.getCompetitionName()

    for category in categoryList:
        categoryPath = PATH + '/' + competitionName + '/' + category
        if not os.path.exists(categoryPath):
            os.mkdir(categoryPath)

        if len(secondCategoryList) > 0:
            for secondCategory in secondCategoryList:
                if not os.path.exists(categoryPath + '/' + secondCategory):
                    os.mkdir(categoryPath + '/' + secondCategory)
            if not os.path.exists(categoryPath + '/general'):
                os.mkdir(categoryPath + '/general')

def calculateWorkoutsHelper(workoutList: list, categoryString: str) -> None:
    workoutDataList = []

    for workout in workoutList:
        workoutDictList = calculate_workout.calculateWorkout(workout + '.csv', categoryString)
        workoutDataList.append({'workout': workout, 'results': workoutDictList, 'category': categoryString})

    orderedTeamsListScore = calculateTeamsScore(workoutDataList, categoryString)
    generateFiles(orderedTeamsListScore, categoryString)

def resetCompetitionFolder() -> None:
    competitionName = shared.getCompetitionName()
    competitionPath = PATH + '/' + competitionName

    try:
        if os.path.exists(competitionPath):
            shutil.rmtree(competitionPath)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    if not os.path.exists(competitionPath):
        os.mkdir(competitionPath)

def createOverallFile() -> None:
    competitionName = shared.getCompetitionName()
    competitionPath = PATH + '/' + competitionName

    open(competitionPath + '/' + consts.OVERALLFILENAME, "w")

def checkIfWorkoutsCanBeCalculated() -> None:
    competitonName = shared.getCompetitionName()

    # Do the competitions file exist
    if not os.path.exists(SETUP_WORKOUTS_PATH + '/' + competitonName):
        print("The competition for " + competitonName + " has not been setup")
        quit()

    workoutList = shared.getAllWorkouts()
    for workout in workoutList:
        csvPath = workout + '.csv'
        # Does the workout file exist
        if not os.path.exists(SETUP_WORKOUTS_PATH + '/' + competitonName + '/' + csvPath):
            print("The workout file for " + workout + " has not been setup")
            quit()
    
        # Check if some score has not been filled out
        workoutData = shared.getDataFromFile(csvPath)
        for data in workoutData:
            if data['Skor'] == '' or data['Skor'] == None:
                print("Error found in " + workout)
                print("Skor has not been added for team " + data[shared.getWorkoutFieldToIndexFor()])
                quit()

def calculateWorkouts() -> None:
    checkIfWorkoutsCanBeCalculated()

    resetCompetitionFolder()
    createOverallFile()
    workoutList = shared.getAllWorkouts()
    generateCategoryFolders()
    firstCategoryList, secondCategoryList = shared.getCategoriesForFolderCreation()

    for firstCategory in firstCategoryList:
        if len(secondCategoryList) > 0:
            calculateWorkoutsHelper(workoutList, firstCategory + '_' + consts.GENERALGROUPNAME)
            for secondCategory in secondCategoryList:
                categoryString = firstCategory + '_' + secondCategory
                calculateWorkoutsHelper(workoutList, categoryString)
        else:
            calculateWorkoutsHelper(workoutList, firstCategory)