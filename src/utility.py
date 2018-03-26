# Imports
#_________________________________________________________________________________________

import math
import random
import enum
import operator


# Define Functions to Run Program
#_________________________________________________________________________________________

# Build a string describing a list
def buildListString(inputList):
    outputString = ""
    for i in range(len(inputList)):
        if i == len(inputList) - 1 and i != 0:
            outputString += " and "
        elif i != len(inputList) - 1 and i != 0:
            outputString += ", "
        outputString += str(inputList[i])
    return outputString
