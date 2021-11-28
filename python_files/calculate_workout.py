import python_files.shared as shared
import python_files.setup_workouts as setup_workouts
import python_files.consts as consts


def orderDictList(dictList, scoredByTime, fieldToOrderBy):
    return sorted(dictList, key=lambda x: x[fieldToOrderBy], reverse = not scoredByTime)

def calculateScoreCount(dictList, sortedScoreSet):
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

def calculateScorePointsHelper(score, calculatedScoreCounts):
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

def convertPoint(point, scoredByTime):
    if scoredByTime:
        return point

def calculateScorePoints(dictList, scoredByTime):
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

def findPointsForScore(score, pointForScore):
    for point in pointForScore:
        if (point['Skor'] == score):
            return point['Points']

    shared.logError("Could not find findPointsForScore")
    return 0.0

def addScoreToDict(dictList, pointsForScore):
    for dict in dictList:
        dict['Points'] = findPointsForScore(dict['Skor'], pointsForScore)

    return dictList

def calculateWorkout(fileName):
    scoredByTime = setup_workouts.getWorkoutSetting(fileName.replace('.csv', ''), 'ScoredByTime') == 'True'

    workoutData = shared.getDataFromFile(fileName)
    workoutDict = orderDictList(workoutData, scoredByTime, 'Skor')

    pointsForScore = calculateScorePoints(workoutDict, scoredByTime)
    workoutDict = addScoreToDict(workoutDict, pointsForScore)

    return workoutDict