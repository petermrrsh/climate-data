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

def noCommas(string):
    quotes = False
    output = ''
    for char in string:
        if char == '\"':
            quotes = True
        if not quotes:
            output += char
        if char != ',' and quotes == True:
            output += char
    return output


def distance(point1, point2): # assume size are the same
    total = 0
    for a in range(len(point1)):
        total += (point1[a]-point2[a]) ** 2
    return math.sqrt(total)

def getNewCenter(objs):
    newCenters = [None]*len(objs)
    for a in range(len(newCenters)): # need to do this b/c weird doubly linked list things in python
        newCenters[a] = []
    for center in range(len(objs)):
        for i in range(len(ALLCODES)):
            total = 0
            for field in objs[center]:
                total += objs[center][field][i]
            newCenters[center].append(total / max(len(objs[center].keys()), 1))
    return newCenters

def getData(filename: str, dictionary: dict, possibleFields: list):
    file = open(filename, 'r')
    lines = file.readlines()
    lines = lines[2:]

    # Country Name,Country ISO3,Year,Indicator Name,Indicator Code,Value
    YEAR = 2; CODE = 4; VALUE = 5
    x = []; y = []

    for line in lines:
        newLine = noCommas(line)
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
    return dictionary

def normalize(dict):
    for x in range(0, len(ALLCODES)):
        max = -math.inf
        min = math.inf
        for y in dict.keys():
            if dict[y][x] < min:
                min = dict[y][x]
            if dict[y][x] > max:
                max = dict[y][x]
        for y in dict.keys():
            dict[y][x] = (dict[y][x] - min) / (max - min)

def getRandomCenters(val):
    centers = []
    for i in range(val):
        centers.append([])
    for i in range(len(ALLCODES)):
        for a in range(0, val):
            centers[a].append(random.random())
    return centers


def KMeansClustering(dict):
    centers = getRandomCenters(NUM_CENTERS)
    end = False
    while end == False:
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
        newCenters = getNewCenter(centerObjs)
        if newCenters == centers:
            for center in range(NUM_CENTERS):
                # print("Center "+str(center+1)+": " + str(newCenters[center]))
                print("Years in center "+str(center+1)+": " + str(centerObjs[center].keys()))
            end = True
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
    KMeansClustering(chinaDict)
    KMeansClustering(pakistanDict)

if __name__ == '__main__':
    main()
