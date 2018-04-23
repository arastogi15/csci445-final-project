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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="vector image file to plot (YAML)")
    args = parser.parse_args()

    # read file
    img = lab11_image.VectorImage(args.image)

    # setup figure
    fig = plt.figure()
    ax = fig.add_subplot(111,aspect='equal')

    # draw all bezier curves
    for path in img.paths:
        ts = np.linspace(0, 1.0, 100)
        result = np.empty((0,3))
        for i in range(0, path.num_segments()):
            for t in ts[:-2]:
                s = path.eval(i, t)
                result = np.vstack([result, s])

        ax.plot(result[:,0], result[:,1], path.color)
    plotOutput = []
    # draw lines
    for line in img.lines:
        print([line.u[0], line.v[0]], [line.u[1], line.v[1]], line.color)
        plotOutput.append(line)
        plt.plot([line.u[0], line.v[0]], [line.u[1], line.v[1]], line.color)

    print("white space placeholder")
    outputFile = open("lineOutput.txt", "w+")
    for i in plotOutput:
        print([i.u[0], i.v[0]], [i.u[1], i.v[1]], i.color)
        
    print("Second white space placeholder")
    for i in plotOutput:
        print(i.u[0], i.v[0], i.u[1], i.v[1], i.color)
        outputFile.write(str(i.u[0]))
        outputFile.write(" ")
        outputFile.write(str(i.v[0]))
        outputFile.write(" ")
        outputFile.write(str(i.u[1]))
        outputFile.write(" ")
        outputFile.write(str(i.v[1]))
        outputFile.write(" ")
        outputFile.write(str(i.color))
        outputFile.write("\n")
    outputFile.close()
    
    print("Finished Writing to File, now attempting to parse")
    
    input = []
    
    iFile = open("lineOutput.txt", "r")
    for line in iFile:
        words = line.split()
        input.append(((words[0], words[1]), (words[2], words[3]), words[4]))
    for i in input:
        print(i)
    
    numberForm = []
    for i in input:
        numberForm.append(i)
    print("Attempting number form output")
    counter =0
    for i in numberForm:
        print(numberForm[counter][0][0], numberForm[counter][0][1], numberForm[counter][1][0], numberForm[counter][1][1], numberForm[counter][2])
        counter+=1
    
    
    
    # show the output
    plt.show()
