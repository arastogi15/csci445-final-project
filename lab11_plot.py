"""
Tool to plot a given vector graphics file (YAML).

Run "python3 lab11_plot.py lab11_img1.yaml" to plot the
bezier curves and lines defined in lab11_img1.yaml.
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import math

import lab11_image

class myLine:
    
    def __init__(self, xStartParam, yStartParam, xEndParam, yEndParam, colorParam, typeParam):
        self.xStart = float(xStartParam)
        self.xEnd = float(xEndParam)
        self.yStart = float(yStartParam)
        self.yEnd = float(yEndParam)
        self.color = colorParam
        self.type = typeParam
        self.isCompleted = False
        
def formatDirections(startPos):
    currentPos = startPos
    
    myLines = []
    finalSolution = []
    iFile = open("lineOutput.txt", "r")
    for line in iFile:
        words = line.split()
        myTempLine = myLine(words[0], words[1], words[2], words[3], words[4], words[5])
        myLines.append(myTempLine)
    for i in myLines:
        print(i.xStart, i.yStart, i.xEnd, i.yEnd, i.color, i.type)
    
    currentLine = myLines[currentPos]
    currentLine.isCompleted = True
    finalSolution.append(currentLine)
    pathFound = False
    while(pathFound == False):
        possibleMoves, isOnline = getPossibleMoves(myLines, currentLine)
        
        lowestCost = 999
        currentNextMove = None
        for i in possibleMoves:
            currentCost = 0
            if(currentLine.color != i.color):
                currentCost += 5
            currentCost += distance((currentLine.xEnd, currentLine.yEnd), (i.xEnd, i.yEnd))
            if(currentCost < lowestCost):
                lowestCost = currentCost
                currentNextMove = i
        
        if(isOnline == False):
            currentNextMove.isCompleted = True
        else:
            currentNextMove.isCompleted = False
            
        
        finalSolution.append(currentNextMove)
        currentLine = currentNextMove
        
        if(len(finalSolution) == len(myLines)):
            pathFound = True
        
        
    print("Made it past pathfinding algorithm, here are results:")
    for i in finalSolution:
        print(i.xStart, i.yStart, i.xEnd, i.yEnd, i.color, i.type, i.isCompleted)
        
            
        
        

def getPossibleMoves(lines, currentLine):
    
    ## Handles case where line starts where old line ends
    possibleLines = []
    isOnLine = False
    for i in range(0, len(lines)):
        if (float(lines[i].xStart) - float(currentLine.xEnd) < .02 and float(lines[i].yStart) - float(currentLine.yEnd) < .02 and lines[i] is not currentLine and lines[i].isCompleted == False):
            possibleLines.append(lines[i])
    ##Handles case where old line finishses along another line - only works when line is horizontal (that is only case in current picture - yes I know this is terrible code)
            
    if(len(possibleLines) < 1):
        for i in range(0, len(lines)):
            if(float(lines[i].yStart) - float(currentLine.yEnd) < .02):
                possibleLines.append(lines[i])
                isOnLine = True
                
    return possibleLines, isOnLine
    
def distance(sPoint, ePoint):
    return math.sqrt((float(sPoint[0]) - float(ePoint[0]))**2 + (float(sPoint[1]) - float(ePoint[1]))**2)
    
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="vector image file to plot (YAML)")
    args = parser.parse_args()

    # read file
    img = lab11_image.VectorImage(args.image)

    # setup figure
    fig = plt.figure()
    ax = fig.add_subplot(111,aspect='equal')
    plotOutput = []
    # draw all bezier curves
    for path in img.paths:
        ts = np.linspace(0, 1.0, 100)
        result = np.empty((0,3))
        for i in range(0, path.num_segments()):
            for t in ts[:-2]:
                s = path.eval(i, t)
                result = np.vstack([result, s])
        sizeOfResults=len(result) -1
        print("Size of results: " , sizeOfResults)

        tempLine = myLine(result[0,0], result[0,1], result[sizeOfResults,0], result[sizeOfResults,1], path.color, "bezier")
        plotOutput.append(tempLine)
        ax.plot(result[:,0], result[:,1], path.color)
    
    # draw lines
    for line in img.lines:
        print([line.u[0], line.v[0]], [line.u[1], line.v[1]], line.color)
        plotOutput.append(myLine(line.u[0], line.u[1], line.v[0], line.v[1], line.color, "line"))
        plt.plot([line.u[0], line.v[0]], [line.u[1], line.v[1]], line.color)

    print("white space placeholder")
    outputFile = open("lineOutput.txt", "w+")
    for i in plotOutput:
        print(i.xStart, i.yStart, i.xEnd, i.yEnd, i.color, i.type)
        
    print("Second white space placeholder")
    for i in plotOutput:
        outputFile.write(str(i.xStart))
        outputFile.write(" ")
        outputFile.write(str(i.yStart))
        outputFile.write(" ")
        outputFile.write(str(i.xEnd))
        outputFile.write(" ")
        outputFile.write(str(i.yEnd))
        outputFile.write(" ")
        outputFile.write(str(i.color))
        outputFile.write(" ")
        outputFile.write(str(i.type))
        outputFile.write("\n")
    outputFile.close()
    
    print("Finished Writing to File, now attempting to parse")
    
    input = []
    
    iFile = open("lineOutput.txt", "r")
    for line in iFile:
        words = line.split()
        myTempLine = myLine(words[0], words[1], words[2], words[3], words[4], words[5])
        input.append(myTempLine)
    for i in input:
        print(i.xStart, i.yStart, i.xEnd, i.yEnd, i.color, i.type)
    
    ##formatDirections(6)
    
    hardList = []
    tempHard = myLine(0, 0, .366, .099, "blue", "line")
    hardList.append(tempHard)
    tempHard = myLine(.366, .099, .366, .455, "blue", "line")
    hardList.append(tempHard)
    tempHard = myLine(.366, .455, .578, .455, "blue", "line")
    hardList.append(tempHard)
    tempHard = myLine(.578, .455, .578, .099, "blue", "line")
    hardList.append(tempHard)
    
    tempHard = myLine(.578, .099, .044, .097, "green", "line")
    hardList.append(tempHard)
    tempHard = myLine(.044, .097, 1.09, .097, "green", "line")
    hardList.append(tempHard)
    
    tempHard = myLine(1.09, .097, 1.09, .78, "black", "line")
    hardList.append(tempHard)
    
    tempHard = myLine(1.09, .78, .8, .85, "red", "bezier")
    hardList.append(tempHard)
    tempHard = myLine(.8, .85, .55, .9, "red", "bezier")
    hardList.append(tempHard)
    tempHard = myLine(.55, .9, .35, .85, "red", "bezier")
    hardList.append(tempHard)
    tempHard = myLine(.35, .85, .05, .78, "red", "bezier")
    hardList.append(tempHard)
    
    tempHard = myLine(.05, .78, .56, 1.3, "red", "line")
    hardList.append(tempHard)
    tempHard = myLine(.56, 1.3, 1.09, .78, "red", "line")
    hardList.append(tempHard)
    
    tempHard = myLine(1.09, .78, .8, .85, "red", "bezier")
    hardList.append(tempHard)
    tempHard = myLine(.8, .85, .55, .9, "red", "bezier")
    hardList.append(tempHard)
    tempHard = myLine(.55, .9, .35, .85, "red", "bezier")
    hardList.append(tempHard)
    tempHard = myLine(.35, .85, .05, .78, "red", "bezier")
    hardList.append(tempHard)
    
    tempHard = myLine(.05, .78, .05, .09, "black", "line")
    hardList.append(tempHard)
    
    outputFile = open("hardOutput.txt", "w+")

    print("Second white space placeholder")
    for i in hardList:
        outputFile.write(str(i.xStart))
        outputFile.write(" ")
        outputFile.write(str(i.yStart))
        outputFile.write(" ")
        outputFile.write(str(i.xEnd))
        outputFile.write(" ")
        outputFile.write(str(i.yEnd))
        outputFile.write(" ")
        outputFile.write(str(i.color))
        outputFile.write(" ")
        outputFile.write(str(i.type))
        outputFile.write("\n")
    outputFile.close()
    
    print("Finished Writing to File, now attempting to parse")
    
    
    # show the output
    plt.show()



