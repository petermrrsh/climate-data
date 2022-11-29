import numpy as np
import matplotlib.pyplot as plt
import math
import random

RANGE = [1991, 2014]
ALLCODES = ['AG.LND.AGRI.K2', 'AG.LND.AGRI.ZS', 'AG.LND.ARBL.ZS', 'AG.LND.FRST.K2', 'AG.LND.FRST.ZS',
                  'AG.YLD.CREL.KG', 'EG.FEC.RNEW.ZS', 'EN.ATM.CO2E.EG.ZS', 'EN.ATM.CO2E.GF.KT', 'EN.ATM.CO2E.GF.ZS',
                  'EN.ATM.CO2E.KD.GD', 'EN.ATM.CO2E.KT', 'EN.ATM.CO2E.LF.KT', 'EN.ATM.CO2E.LF.ZS', 'EN.ATM.CO2E.PC',
                  'EN.ATM.CO2E.PP.GD', 'EN.ATM.CO2E.PP.GD.KD', 'EN.ATM.CO2E.SF.KT', 'EN.ATM.CO2E.SF.ZS',
                  'EN.ATM.GHGT.KT.CE', 'EN.ATM.METH.KT.CE', 'EN.ATM.NOXE.KT.CE', 'EN.URB.MCTY.TL.ZS', 'SP.POP.GROW',
                  'SP.URB.GROW', 'SP.URB.TOTL', 'SP.URB.TOTL.IN.ZS']
NUM_CENTERS = 3

# Removes commas that are inside quotes in a given string
# Example -> "China,CHN,2019,\"Foreign direct investment, net inflows (% of GDP)\""
# Should return -> "China,CHN,2019,\"Foreign direct investment net inflows (% of GDP)\"" (removed commas in quotes)
# We split our data on commas so when commas exist in the field name parsing the csv parses incorrectly
# param string data: a line of a given csv file
# return string: param with no commas in between quotes
def removeCommas(data):
    insideQuotes = False  # false if not inside quotes, true otherwise
    output = ''
    for char in data:
        if char == '\"':
            insideQuotes = True
        if not insideQuotes:
            output += char
        if char != ',' and insideQuotes == True:
            output += char
    return output

# returns the euclidean distance between two points and their values
# param list[float] point1: a list of len(ALLCODES) with values
# param list[float] point2: a list of len(ALLCODES) with values
# return float: euclidean distance between two given points
def distance(point1, point2): # assume size are the same
    total = 0
    for a in range(len(point1)):
        total += (point1[a]-point2[a]) ** 2
    return math.sqrt(total)

# returns the new centers given clusters if points
# param list[dictionary(key=string, value=list[float])] clusters: a list of dictionaries, each dictionary describing a cluster
# return list[list[floats]]: list of len(NUM_CENTERS), each list being of len(ALLCODES). each entry of the list is the
#   new center based on given data
def getNewCenters(clusters):
    newCenters = [None]*len(clusters)
    for a in range(len(newCenters)): # need to do this b/c weird doubly linked list things in python
        newCenters[a] = []
    for center in range(len(clusters)):
        for i in range(len(ALLCODES)):
            total = 0
            for field in clusters[center]:
                total += clusters[center][field][i]
            newCenters[center].append(total / max(len(clusters[center].keys()), 1))
    return newCenters

# parses the csv file and organizes data into a dictionary
# param string filename: the name of the file we are getting the data from
# param dictionary dictionary: dictionary defined with all possible years in range with a value of empty list
# param list[string] possibleFields: the fields we are adding to the dictionary
# returns nothing: dynamically changes the dictionary passed in since it is defined outside this function
def getData(filename: str, dictionary: dict, possibleFields: list):
    file = open(filename, 'r')
    lines = file.readlines()
    lines = lines[2:] # first two lines of files describe how the data is organized

    YEAR = 2; CODE = 4; VALUE = 5
    x = []; y = []

    for line in lines:
        newLine = removeCommas(line)
        cells = newLine.split(",")
        year = ""; code = ""; value = ""

        for i in range(len(cells)):
            if i == YEAR:
                year = cells[i]
            elif i == CODE:
                code = cells[i]
            elif i == VALUE:
                value = cells[i]
                value = value[:len(value)-1] # remove extra new line character

        if RANGE[0] <= int(year) <= RANGE[1] and code in possibleFields:
            dictionary[year][possibleFields.index(code)] = float(value)

    file.close()

# normalizes given dictionary's data
# param dictionary dict
# returns nothing, dynamically changes given dictionary to be normalized as dictionary is defined outside of this function
def normalize(dict):
    for x in range(0, len(ALLCODES)):
        max = -math.inf
        min = math.inf
        for y in dict.keys():
            if dict[y][x] < min:
                min = dict[y][x] # find min for specific field
            if dict[y][x] > max:
                max = dict[y][x] # find max for specific field
        for y in dict.keys():
            dict[y][x] = (dict[y][x] - min) / (max - min) # normalize all data in specific field

# generates random centers to start k means clustering
# returns a list of lists of centers
def getRandomCenters():
    centers = []
    for i in range(NUM_CENTERS):
        centers.append([])
    for field in range(len(ALLCODES)):
        for j in range(NUM_CENTERS):
            centers[j].append(random.random())
    return centers

# perform k means clustering on given dictionary containing data
# param dictionary dict: dictionary containing years as keys and values parsed from csv as values
def KMeansClustering(dict):
    centers = getRandomCenters()
    while True:
        centerObjs = [None]*len(centers)
        for i in range(len(centerObjs)):
            centerObjs[i] = {}
        for key in dict.keys():
            distances = []*len(centers)
            min = (math.inf, None)
            for center in range(len(centers)):
                if distance(centers[center], dict[key]) < min[0]:
                    min = (distance(centers[center], dict[key]), center)
            centerObjs[min[1]][key] = dict[key]
        newCenters = getNewCenters(centerObjs)
        if newCenters == centers:
            return centerObjs
        else:
            centers = newCenters


def main():
    chinaDict = {}
    pakistanDict = {}
    for i in range(RANGE[0], RANGE[1]+1):
        chinaDict[str(i)] = [None]*len(ALLCODES)
        pakistanDict[str(i)] = [None]*len(ALLCODES)
    getData("china.csv", chinaDict, ALLCODES)
    getData("pakistan.csv", pakistanDict, ALLCODES)
    normalize(chinaDict)
    normalize(pakistanDict)
    total = {}
    # following code is used to gather results of running code many times
    for a in range(1000):
        for x in KMeansClustering(pakistanDict):
            a2 = list({int(k):[float(i) for i in v] for k,v in x.items()}.keys())
            if (a2 != []):
                if str(min(a2))+"-"+str(max(a2)) in total.keys():
                    total[str(min(a2))+"-"+str(max(a2))] += 1
                else:
                    total[str(min(a2))+"-"+str(max(a2))] = 1
            else:
                if "empty" in total.keys():
                    total["empty"] += 1
                else:
                    total["empty"] = 1
    print(total)


if __name__ == '__main__':
    main()
