import csv

FILEFOLDER = 'workouts/'

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

    with open(FILEFOLDER + fileName, newline='', encoding='utf-8') as csvfile:
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