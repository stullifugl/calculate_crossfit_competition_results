import csv
import python_files.consts as consts

FILEFOLDER = 'settings'

NONTEAMFIELDS = ['_', 'Nafn']
TEAMFIELDS = ['_', 'Nafn1', 'Nafn2', 'NafnLids']
EXTRATEAMFIELDS = ['KK-KK', 'KVK-KVK', 'KK-KVK']


def getDictKeys(reader):
    headerLine = next(reader)
    return headerLine[1:]


def readFile(fileName: str, fileFolder: str = 'settings') -> list:
    lineList = []

    for line in open(fileFolder + '/' + fileName, 'r', encoding="utf8"):
        lineList.append(line)

    return lineList


def getDataFromFile(fileName: str, folderName: str = "competitions") -> list:
    returnList = []

    with open(folderName + '/' + getCompetitionName() + '/' + fileName, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        dictKeys = getDictKeys(reader)
        for row in reader:
            dict = {}
            for i in range(1, len(row)):
                if dictKeys[i - 1] == 'Skor' and row[i] != '':

                    newStr = row[i].replace(':', '.')
                    dict[dictKeys[i - 1]] = float(newStr)
                else:
                    dict[dictKeys[i - 1]] = row[i]
            returnList.append(dict)

    return returnList


def logError(error: str) -> None:
    print("Error ____ " + error + " _____")


def debugDictList(dictList: list) -> None:
    for item in dictList:
        print(item)


def getSettingInLineList(setting: str, lineList: list = readFile('competition_settings.txt')) -> list:
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


def isTeamCompetition() -> bool:
    competitionSettings = getSettingInLineList('CompetitionSettings')

    return getSettingInLineList('TeamCompetition', competitionSettings)[0] == 'True'


def getCategories() -> list:
    competitionSettings = getSettingInLineList('CompetitionSettings')
    teamCompetition = isTeamCompetition()
    categories = getSettingInLineList(
        'CompetitionCategories', competitionSettings)
    if teamCompetition:
        categories.extend(EXTRATEAMFIELDS)

    return categories


def getCategoriesForFolderCreation() -> tuple:
    competitionSettings = getSettingInLineList('CompetitionSettings')
    categories = getSettingInLineList(
        'CompetitionCategories', competitionSettings)
    teamCompetition = isTeamCompetition()

    if teamCompetition:
        return categories, EXTRATEAMFIELDS

    return categories, []


def getTeamFields() -> list:
    teamCompetition = isTeamCompetition()
    categoryList = getCategories()

    if teamCompetition:
        newList = TEAMFIELDS
        newList.extend(categoryList)

        return newList
    else:
        newList = NONTEAMFIELDS
        newList.extend(categoryList)

        return newList


def getCompetitionName() -> str:
    nameSettings = getSettingInLineList('CompetitionName')

    return nameSettings[0].replace(" ", "_")


def getWorkouts() -> list:
    return getSettingInLineList('Workouts')


def getWorkoutFields() -> list:
    if isTeamCompetition():
        return ['_', getWorkoutFieldToIndexFor(), 'Skor']
    else:
        return ['_', 'Nafn', 'Skor']


def getWorkoutFieldToIndexFor() -> str:
    if isTeamCompetition():
        return 'NafnLids'
    else:
        return 'Nafn'


def getAllWorkouts() -> list:
    fileNameList = getSettingInLineList('Workouts')

    return fileNameList


def getTeamsCategories(teamDict: dict, categories: list) -> str:
    returnString = ""

    for category in categories:
        if teamDict[category].lower() == 'x':
            if returnString == "":
                returnString = category
            else:
                returnString = returnString + '_' + category

    return returnString


def getTeamsInCertainCategory(category: str) -> list:
    if category == "":
        return getDataFromFile('lidin.csv')

    categoryList = getCategories()
    teams = getDataFromFile('lidin.csv')
    returnList = []
    if consts.GENERALGROUPNAME in category:
        updatedCategoryString = category.split('_')[0]

        for team in teams:
            if updatedCategoryString in getTeamsCategories(team, categoryList):
                returnList.append(team)
    else:
        returnList = []

        for team in teams:
            if category == getTeamsCategories(team, categoryList):
                returnList.append(team)

    return returnList


def getAllTeams() -> list:
    return getDataFromFile('lidin.csv')
