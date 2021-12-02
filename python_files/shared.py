import csv

FILEFOLDER = 'workouts/'

NONTEAMFIELDS = ['_', 'Nafn']
TEAMFIELDS = ['_', 'Nafn1', 'Nafn2', 'NafnLids']
EXTRATEAMFIELDS = ['KK-KK', 'KVK-KVK', 'KK-KVK']

def getDictKeys(reader):
    headerLine = next(reader)
    return headerLine[1:]

def readFile(fileName):
    lineList = []

    for line in open(FILEFOLDER + fileName, 'r', encoding="utf8"):
        lineList.append(line)

    return lineList

def getDataFromFile(fileName):
    returnList = []

    with open('results/' + getCompetitionName() + '/' + fileName, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        dictKeys = getDictKeys(reader)
        for row in reader:
            dict = {}
            for i in range(1, len(row)):
                if dictKeys[i - 1] == 'Skor':
                    newStr = row[i].replace(':', '.')
                    dict[dictKeys[i - 1]] = float(newStr)
                else:
                    dict[dictKeys[i - 1]] = row[i]
            returnList.append(dict)

    return returnList

def logError(error):
    print("Error ____ " + error + " _____")

def debugDictList(dictList):
    for item in dictList:
        print(item)

def getSettingInLineList(setting, lineList = readFile('competition_settings.txt')):
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

def isTeamCompetition():
    competitionSettings = getSettingInLineList('CompetitionSettings')

    return getSettingInLineList('TeamCompetition', competitionSettings)[0] == 'True'

def getCategories():
    competitionSettings = getSettingInLineList('CompetitionSettings')
    teamCompetition = isTeamCompetition()
    categories = getSettingInLineList('CompetitionCategories', competitionSettings)
    if teamCompetition:
        categories.extend(EXTRATEAMFIELDS)
    
    return categories

def getTeamFields():
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

def getCompetitionName():
    nameSettings = getSettingInLineList('CompetitionName')

    return nameSettings[0].replace(" ", "_")

def getWorkouts():
    return getSettingInLineList('Workouts')

def getWorkoutDetail(workout, setting):
    return getSettingInLineList(workout, setting)[0] == 'True'

def getWorkoutFields():
    if isTeamCompetition():
        return ['_', 'NafnLids', 'Skor']
    else:
        return ['_', 'Nafn', 'Skor']

def getWorkoutFieldToIndexFor():
    if isTeamCompetition():
        return 'NafnLids'
    else:
        return 'Nafn'