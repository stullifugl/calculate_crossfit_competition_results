import python_files.calculate_workout as calculate_workout
import python_files.shared as shared
import python_files.setup_workouts as setup_workouts
import csv

def getDataFromWorkoutForTeam(team, workoutDictList):
    for dict in workoutDictList:
        if dict['NafnLids'] == team['NafnLids']:
            return dict['Points'], dict['Skor']

    shared.logError("Could not find team in function getDataFromWorkoutForTeam")
    return 0.0

def calculateTeamsScore(workoutDataList):
    totalTeamScoreList = []
    teams = shared.getDataFromFile('lidin.csv')

    for team in teams:
        dict = {}
        totalPoints = 0
        dict['NafnLids'] = team['NafnLids']
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


def generateFiles(teamScoreList):
    folderPath = 'results/general'
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

def displayResults(teamScoreList):
    # shared.debugDictList(teamScoreList)
    generateFiles(teamScoreList)
    

def calculateWorkouts():
    workoutList = setup_workouts.getAllWorkouts()

    workoutDataList = []

    for workout in workoutList:
        workoutDictList = calculate_workout.calculateWorkout(workout + '.csv')
        workoutDataList.append({'workout': workout, 'results': workoutDictList})

    orderedTeamsListScore = calculateTeamsScore(workoutDataList)
    displayResults(orderedTeamsListScore)