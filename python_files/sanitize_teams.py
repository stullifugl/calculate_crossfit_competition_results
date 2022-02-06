import python_files.shared as shared


def getTeamNames():
    teams = shared.getAllTeams()

    teamNames = []
    for team in teams:
        teamNames.append(team['NafnLids'])

    return teamNames


def createDictCountList(teamNames):
    dict = {}

    for name in teamNames:
        if name in dict.keys():
            dict[name] = dict[name] + 1
        else:
            dict[name] = 1

    return dict


def checkCount(teamDict):
    keys = teamDict.keys()

    valid = True
    for key in keys:
        if teamDict[key] > 1:
            print(key + " name is used " + str(teamDict[key]))
            valid = False

    if valid == True:
        print("Teams are sanitized")

    if valid == False:
        print("Teams are not sanitized, please fix")


def sanitizeTeams():
    teamNames = getTeamNames()
    teamDict = createDictCountList(teamNames)

    checkCount(teamDict)
