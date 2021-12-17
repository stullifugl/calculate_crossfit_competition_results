import python_files.shared as shared
import python_files.setup_workouts as setup_workouts
import python_files.consts as consts

def orderDictList(dictList: list, scoredByTime: bool, fieldToOrderBy: str) -> list:
    return sorted(dictList, key=lambda x: x[fieldToOrderBy], reverse = not scoredByTime)

def appendCategoriesToWorkoutDict(workoutDictList: list) -> list:
    returnList = []

    teamsData = shared.getDataFromFile('lidin.csv')
    categories = shared.getCategories()

    for workoutDict in workoutDictList:
        for team in teamsData:
            if team[shared.getWorkoutFieldToIndexFor()] == workoutDict[shared.getWorkoutFieldToIndexFor()]:
                workoutDict['Categories'] = shared.getTeamsCategories(team, categories)
                break
        returnList.append(workoutDict)

    return returnList

def calculateScoreCount(dictList: list, sortedScoreSet: list):
    returnList = []

    for score in sortedScoreSet:
        count = 0
        for item in dictList:
            if item['Skor'] == score:
                count += 1
        
        dict = {}
        dict['Skor'] = score
        dict['Count'] = count
        returnList.append(dict)

    return returnList

def calculateScorePointsHelper(score: float, calculatedScoreCounts: list):
    count = 0
    for calculatedScore in calculatedScoreCounts:
        if calculatedScore['Skor'] == score:
            calculatedScore =  consts.POINTSFORFIRSTPLACE - consts.DECREMENT * count
            if calculatedScore < 0:
                return 0.0
            else:
                return calculatedScore
        else:
            count += calculatedScore['Count']

    return 0.0

def calculateScorePoints(dictList: list, scoredByTime: bool) -> None:
    returnList = []
    scoreSet = set()

    for item in dictList:
        scoreSet.add(item['Skor'])

    sortedScoreSet = sorted(scoreSet, reverse = not scoredByTime)
    calculatedScoreCounts = calculateScoreCount(dictList, sortedScoreSet)

    for i in range (0, len(sortedScoreSet)):
        dict = {}
        dict['Skor'] = sortedScoreSet[i]
        dict['Points'] = calculateScorePointsHelper(sortedScoreSet[i], calculatedScoreCounts)

        returnList.append(dict)

    return returnList

def findPointsForScore(score: float, pointForScore: list) -> float:
    for point in pointForScore:
        if (point['Skor'] == score):
            return point['Points']

    shared.logError("Could not find findPointsForScore")
    return 0.0

def addScoreToDict(dictList: list, pointsForScore: list) -> list:
    for dict in dictList:
        dict['Points'] = findPointsForScore(dict['Skor'], pointsForScore)

    return dictList

def createWorkoutDictBasedOnCategory(workoutDictList: list, categoryString: str) -> list:
    if categoryString == "":
        return workoutDictList

    returnList = []
    
    if consts.GENERALGROUPNAME in categoryString.lower():
        for workoutDict in workoutDictList:
            updatedCategoryString = categoryString.split('_')[0]
            if updatedCategoryString in workoutDict['Categories']:
                returnList.append(workoutDict)

    for workoutDict in workoutDictList:
        if workoutDict['Categories'] == categoryString:
            returnList.append(workoutDict)

    return returnList
    

def calculateWorkout(fileName: str, categoryString: str) -> list:
    scoredByTime = setup_workouts.getWorkoutSetting(fileName.replace('.csv', ''), 'ScoredByTime') == 'True'

    workoutData = shared.getDataFromFile(fileName)
    workoutDictList = orderDictList(workoutData, scoredByTime, 'Skor')
    workoutDictList = appendCategoriesToWorkoutDict(workoutDictList)
    workoutDictList = createWorkoutDictBasedOnCategory(workoutDictList, categoryString)

    pointsForScore = calculateScorePoints(workoutDictList, scoredByTime)
    workoutDictList = addScoreToDict(workoutDictList, pointsForScore)

    return workoutDictList