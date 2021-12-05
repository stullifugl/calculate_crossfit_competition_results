import csv
import python_files.shared as shared
import python_files.consts as consts
import random
import os

PATH = 'competitions'

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
    workoutSettingsLines = shared.getSettingInLineList(fileName)
    
    return shared.getSettingInLineList(workoutSetting, workoutSettingsLines)[0]

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


def createWorkoutFiles(fileNames):
    path = PATH + '/' + shared.getCompetitionName() + '/'

    for name in fileNames:
        with open(path + name + '.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=shared.getWorkoutFields())
            writer.writeheader()

            # Add all the teams to the workout files as well
            fillWorkoutsWithData(writer, name)

def addRandomDataToTeamFile(writer, fields):
    nrOfTeams = random.randint(30, 50)
    categories = shared.getCategories()
    firstCategoryList, secondCategorylist = shared.getCategoriesForFolderCreation()

    dict = {}
    for i in range(0, nrOfTeams):
        dict = {}
        firstRandomCategory = random.randint(len(fields) - len(categories), len(fields) - 1)
        secondRandomCategory = -1
        if len(secondCategorylist) > 0:
            secondRandomCategory = random.randint(len(fields) - len(secondCategorylist), len(fields) - 1)
            firstRandomCategory = random.randint(len(fields) - len(secondCategorylist) - len(firstCategoryList), len(fields) - len(secondCategorylist) - 1)
        for x in range(0, len(fields)):
            if '_' in fields[x]:
                dict[fields[x]] = '_'
            elif 'Nafn' in fields[x]:
                if fields[x] == 'NafnLids':
                    dict[fields[x]] = 'Lid' + str(i)
                else:
                    dict[fields[x]] = fields[x] + str(i)
            else:
                if x == firstRandomCategory or x == secondRandomCategory:
                    dict[fields[x]] = 'x'
                else:
                    dict[fields[x]] = ''
        writer.writerow(dict)

def createTeamFile(path):
    fields = shared.getTeamFields()

    with open(path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        if consts.ADDRANDOMSCORES:
            addRandomDataToTeamFile(writer, fields)

def createCompetitionFolder():
    competitionName = shared.getCompetitionName()
    
    if not os.path.exists(PATH + '/' + competitionName):
        os.mkdir(PATH + '/' + competitionName)
    
    createTeamFile(PATH + '/' + competitionName + '/lidin.csv')

def setupWorkouts():
    fileNameList = shared.getAllWorkouts()
    createCompetitionFolder()
    createWorkoutFiles(fileNameList)

    