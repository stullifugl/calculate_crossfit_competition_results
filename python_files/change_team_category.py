import python_files.shared as shared
import python_files.setup_workouts as setup_workouts

def findTeams() -> list:
    returnList = []

    print()
    teamName = input("Name of the team: ")
    teamsData = shared.getDataFromFile('lidin.csv')

    indexNumber = 1
    for i in range(0, len(teamsData)):
        name: str = teamsData[i][shared.getWorkoutFieldToIndexFor()]
        if teamName.lower() in name.lower():
            returnList.append({
                'num': indexNumber,
                'index': i,
                'name': name
            })
            indexNumber += 1

    return returnList

def checkIfIndexExists(teams: list, number: int) -> None:
    for team in teams:
        if team['num'] == number:
            return

    print("Number inputted does not exist")
    quit()        

def pickTeam(teams: list) -> dict:
    print()
    print("Which team are you looking for")
    for team in teams:
        print(str(team['num']) + ': ' + team['name'])

    teamIndex = int(input("Pick number: "))
    checkIfIndexExists(teams, teamIndex)

    return teams[teamIndex - 1]


def pickCategory() -> str:
    print("Which category do you wish to change to?")
    categories, _ = shared.getCategoriesForFolderCreation()
    for i in range(0, len(categories)):
        print(str(i + 1) + ': ' + categories[i])

    categoryIndex = int(input("Pick number: "))

    if categoryIndex <= 0 or categoryIndex > len(categories):
        print("Number inputted does not exist")
        quit()  

    return categories[categoryIndex - 1]

def overrideLineList(list: list, keys: list, category: str) -> list:
    categories, _ = shared.getCategoriesForFolderCreation()
    indexes = []
    categoryIndex = -1

    for i in range(0, len(keys)):
        for cat in categories:
            if cat == keys[i]:
                indexes.append(i)
            if category == keys[i]:
                categoryIndex = i

    if categoryIndex != -1:
        for index in indexes:
            list[index + 1] = ''
        list[categoryIndex + 1] = 'x'

    return list


def overrideTeamDocument(team: dict, category: str) -> None:
    fileLines = shared.readFile('lidin.csv', fileFolder='competitions/' + shared.getCompetitionName())
    teamsData = shared.getDataFromFile('lidin.csv')
    keyList = [*teamsData[0].keys()]

    for x in range(0, len(fileLines)):
        list = fileLines[x].split(',')
        for item in list:
            if team['name'].lower() == item.lower():
                newList = overrideLineList(list, keyList, category)
                listStr = ','.join(newList)
                # Override line in list with the new line
                fileLines[x] = listStr

    # Update the team file
    setup_workouts.updateTeamFile(fileLines)


def changeTeams() -> None:
    teams = findTeams()

    team = pickTeam(teams)
    category = pickCategory()

    overrideTeamDocument(team, category)

    print()
    print("Managed to change teams category")
