import numpy as np
import matplotlib.pyplot as plt

class DataPoint:
  def __init__(self, year : int, code : str, value : int):
    self.year = year
    self.code = code
    self.value = value

def getData(filename:str, code_to_get:str):

    file = open(filename, 'r')
    lines = file.readlines()
    lines = lines[2:]

    #Country Name,Country ISO3,Year,Indicator Name,Indicator Code,Value
    YEAR = 2
    CODE = 4
    VALUE = 5

    x = []
    y = []

    # Strips the newline character
    for line in lines:
        cells = line.split(",")

        year = ""
        code = ""
        value = ""

        for i in range(len(cells)):
            if i == YEAR:
                year = cells[i]
            elif i == CODE:
                code = cells[i]
            elif i == VALUE:
                value = cells[i]

        if code == code_to_get:
            x.append(int(year))
            y.append(float(value))

    file.close()
    return x, y




def main():
    
    x, y = getData("pakistan.csv", "AG.LND.ARBL.ZS")
    plt.scatter(x, y, c='#0000FF')
    plt.show()

if __name__ == '__main__':
    main()
