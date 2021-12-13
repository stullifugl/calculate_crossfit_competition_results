import python_files.calculate_workout as calculate_workout
import python_files.shared as shared
import python_files.consts as consts
import csv
import os
import shutil

PATH = 'results'

def getDataFromWorkoutForTeam(team, workoutDictList):
    for dict in workoutDictList:
        if dict[shared.getWorkoutFieldToIndexFor()] == team[shared.getWorkoutFieldToIndexFor()]:
            return dict['Points'], dict['Skor']

    shared.logError("Could not find team in function getDataFromWorkoutForTeam")
    return 0.0

def calculateTeamsScore(workoutDataList, categoryString):
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

def generateWorkoutDataListDict(teamScoreList, file):
    returnList = []
    orderedList = calculate_workout.orderDictList(teamScoreList, False, file + '_points')

    for team in orderedList:
        dict = {}
        dict['NafnLids'] = team['NafnLids']
        dict['Skor'] = team[file + '_score']
        dict['Stig'] = team[file + '_points']

        returnList.append(dict)

    return returnList

def generateTotalDataListDict(teamScoreList):
    returnList = []
    orderedList = calculate_workout.orderDictList(teamScoreList, False, 'total_points')
    keyList = teamScoreList[0].keys()

    for team in orderedList:
        dict = {}
        for key in keyList:
            dict[key] = team[key]

        returnList.append(dict)

    return returnList

def populateWorkoutResults(folderPath, teamScoreList, file):
    with open(folderPath + '/' + file + '.csv', 'w', encoding='UTF8', newline='') as f:
        fieldList = ['NafnLids', 'Skor', 'Stig']

        writer = csv.DictWriter(f, fieldnames=fieldList)
        writer.writeheader()
        for dict in generateWorkoutDataListDict(teamScoreList, file):
            writer.writerow(dict)

def populateGeneralResults(folderPath, teamScoreList):
    with open(folderPath + '/total.csv', 'w', encoding='UTF8', newline='') as f:
        keyList = teamScoreList[0].keys()
        writer = csv.DictWriter(f, fieldnames=keyList)
        writer.writeheader()
        for dict in generateTotalDataListDict(teamScoreList):
            writer.writerow(dict)


def generateFiles(teamScoreList, categoryString):
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
    else:
        print("No competitors signed for the following category: " + categoryString)
    
def generateCategoryFolders():
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


def calculateWorkoutsHelper(workoutList, categoryString):
    workoutDataList = []

    for workout in workoutList:
        workoutDictList = calculate_workout.calculateWorkout(workout + '.csv', categoryString)
        workoutDataList.append({'workout': workout, 'results': workoutDictList, 'category': categoryString})

    orderedTeamsListScore = calculateTeamsScore(workoutDataList, categoryString)
    generateFiles(orderedTeamsListScore, categoryString)

def resetCompetitionFolder():
    competitionName = shared.getCompetitionName()
    competitionPath = PATH + '/' + competitionName

    try:
        if os.path.exists(competitionPath):
            shutil.rmtree(competitionPath)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    if not os.path.exists(competitionPath):
        os.mkdir(competitionPath)

def calculateWorkouts():
    resetCompetitionFolder()
    workoutList = shared.getAllWorkouts()
    generateCategoryFolders()
    firstCategoryList, secondCategoryList = shared.getCategoriesForFolderCreation()

    for firstCategory in firstCategoryList:
        if len(secondCategoryList) > 0:
            for secondCategory in secondCategoryList:
                categoryString = firstCategory + '_' + secondCategory
                calculateWorkoutsHelper(workoutList, categoryString)
            calculateWorkoutsHelper(workoutList, firstCategory + '_' + consts.GENERALGROUPNAME)
        else:
            calculateWorkoutsHelper(workoutList, firstCategory)