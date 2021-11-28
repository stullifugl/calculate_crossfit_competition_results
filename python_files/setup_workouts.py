import csv
import python_files.shared as shared
import python_files.consts as consts
import random

fieldnames = ['_', 'NafnLids', 'Skor']

def getSettingInLineList(setting, lineList):
    returnList = []

    foundSettingInitializer = False
    for line in lineList:
        if '###' + setting in line and foundSettingInitializer == True:
            foundSettingInitializer = False
            break

        if foundSettingInitializer == True:
            returnList.append(line.strip())

        if '###' + setting in line:
            foundSettingInitializer = True

    return returnList

def appendZeroIfNeededToTime(number):
    if number < 10:
        return '0' + str(number)

    return str(number)

def generateRandomScore(scoredByTime):
    if scoredByTime == False:
        return str(random.randint(70, 150))
    else:
        randomNumberOne = appendZeroIfNeededToTime(random.randint(5, 20))
        randomNumberTwo = appendZeroIfNeededToTime(random.randint(0, 60))

        return randomNumberOne + ':' + randomNumberTwo

def getWorkoutSetting(fileName, workoutSetting):
    fileLines = shared.readFile('workout_settings.txt')
    workoutSettingsLines = getSettingInLineList(fileName, fileLines)
    
    return getSettingInLineList(workoutSetting, workoutSettingsLines)[0]

def fillWorkoutsWithData(writer, fileName):
    scoredByTime = False
    if consts.ADDRANDOMSCORES:
        scoredByTime = getWorkoutSetting(fileName, 'ScoredByTime') == 'True'

    teams = shared.getDataFromFile('lidin.csv')
    for team in teams:
        dict = {}
        if consts.ADDRANDOMSCORES:
            dict={'_': '_', 'NafnLids': team['NafnLids'], 'Skor': generateRandomScore(scoredByTime)}
        else:
            dict={'_': '_', 'NafnLids': team['NafnLids'], 'Skor': ''}
        writer.writerow(dict)


def createCsvFiles(fileNames):
    for name in fileNames:
        with open('workouts/' + name + '.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            # Add all the teams to the workout files as well
            fillWorkoutsWithData(writer, name)

def getAllWorkouts():
    fileLines = shared.readFile('workout_settings.txt')
    fileNameList = getSettingInLineList('Workouts', fileLines)

    return fileNameList

def createWorkoutFiles():
    fileNameList = getAllWorkouts()
    createCsvFiles(fileNameList)

def setupWorkouts():
    createWorkoutFiles()

    