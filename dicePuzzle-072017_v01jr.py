# Imports
#_________________________________________________________________________________________

import math
import random
import sys
import datetime

# Define Objects
#_________________________________________________________________________________________


class dice(object):
    """represents a peice, takes a name and 6 sides"""

    def __init__(self, name, side1, side2, side3, side4, side5, side6):
        self.name = str(name)
        self.side1 = int(side1)
        self.side2 = int(side2)
        self.side3 = int(side3)
        self.side4 = int(side4)
        self.side5 = int(side5)
        self.side6 = int(side6)

    def __str__(self):
        return "I am %s and my sides are %d, %d, %d ,%d, %d and %d." % (self.name, self.side1, self.side2, self.side3, self.side4, self.side5, self.side6)

def makeDie(name, side1, side2, side3, side4, side5, side6):
    die = dice(name, side1, side2, side3, side4, side5, side6)
    return die

# Define Functions to Run Program
#_________________________________________________________________________________________

def rollDice(dieToRoll):
    rolledSide = random.randint(1, 6)
    whichSide = "side" + str(rolledSide)
    return getattr(dieToRoll, whichSide)

def compareDice(firstDie, secondDie):
    valueA = rollDice(firstDie)
    valueB = rollDice(secondDie)
    if valueA > valueB:
        return firstDie
    if valueB > valueA:
        return secondDie
    if valueA == valueB:
        return "Tied"

def rollXTime(timesToRoll, firstDie, secondDie):
    results = []
    firstDieCounter = 0
    secondDieCounter = 0
    tiedCounter = 0
    for i in range(timesToRoll):
        thisTime = compareDice(firstDie, secondDie)
        results.append(thisTime)
    for j in range(len(results)):
        if results[j] == firstDie:
            firstDieCounter += 1
        if results[j] == secondDie:
            secondDieCounter += 1
        if results[j] == "Tied":
            tiedCounter += 1
    output = []
    output.append(firstDieCounter)
    output.append(secondDieCounter)
    output.append(tiedCounter)
    return output


# Actions
#_________________________________________________________________________________________

#Load the CSV file to a variable
timesToRoll = int(raw_input("How many times would you like to roll? "))


#Makes the dice
K = makeDie("Katherine",3,3,3,3,3,6)
Z = makeDie("Zack",2,2,2,5,5,5)
print K
print Z

#Perform the roll
results = rollXTime(timesToRoll, K, Z)
print "%s: %s, %s: %s, Tied: %s" % (K.name, results[0], Z.name, results[1], results[2])
if results[0] > results[1] and results[0] > results[2]:
    print "%s won with %d%%." % (K.name, 100*(float(results[0])/float(timesToRoll)))
if results[1] > results[0] and results[1] > results[2]:
    print "%s won with %d%%." % (Z.name, 100*(float(results[1])/float(timesToRoll)))
if results[2] > results[0] and results[2] > results[1]:
    print "The ties won with %d%%." % 100*(float(results[2])/float(timesToRoll))
