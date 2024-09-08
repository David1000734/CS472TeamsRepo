import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import random

inputFile = []

# get input data
with open("data/author_touches.csv", mode = 'r') as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        inputFile.append(lines)

# get all unique files
uniqueFiles = []
for i in range(1, len(inputFile)):
    isIn = False
    for j in uniqueFiles:
        if(inputFile[i][2] == j):
            isIn = True
    if not isIn:
       uniqueFiles.append(inputFile[i][2])

# change filenames to numerical values
for i in range(1, len(inputFile)):
    for j in range(len(uniqueFiles)):
        if(inputFile[i][2] == uniqueFiles[j]):
            inputFile[i][2] = j;

# convert time     
baselineWeek = datetime.date(int(inputFile[len(inputFile)-1][1][:4]), int(inputFile[len(inputFile)-1][1][5:7]), int(inputFile[len(inputFile)-1][1][8:10])).isocalendar().week
baseYear = int(inputFile[len(inputFile)-1][1][:4])
for i in range(1, len(inputFile)):
    year = inputFile[i][1][:4]
    month = inputFile[i][1][5:7]
    day = inputFile[i][1][8:10]
    # get what week of the year it is
    week = datetime.date(int(year), int(month), int(day)).isocalendar().week
    # subtract base amount
    week = week - baselineWeek
    # add more if worked on in a later year
    week = week + ((int(year) - baseYear) * 53)
    inputFile[i][1] = week

# change names to unique colors
names = []
colors = []
count = 1
for i in range(1, len(inputFile)):
    name = inputFile[i][0]
    if(name[0] != '#'):
        names.append(name)
        randColor = "#" + "%06x" % random.randint(0, 0xFFFFFF)
        colors.append(randColor)
        # print("name2: ", randColor)
        for j in range(1, len(inputFile)):
            if(name == inputFile[j][0]):
                inputFile[j][0] = randColor
        inputFile[count], inputFile[i] = inputFile[i], inputFile[count]
        count = count + 1
            

# get x and y values
x = []
y = []
c = []
for i in range(1, len(inputFile)):
    plt.scatter(inputFile[i][2], inputFile[i][1], s=20, c = inputFile[i][0])

plt.xlabel("File")
plt.ylabel("Weeks")
plt.legend(names, prop={'size': 6})

plt.savefig('foo.png');

for i in inputFile:
    print(i)
print("count: ", len(uniqueFiles)) 