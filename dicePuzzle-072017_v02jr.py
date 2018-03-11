# Imports
#_________________________________________________________________________________________

import math
import random
import sys
import datetime
import enum

# Define Objects
#_________________________________________________________________________________________


class Die(object):
    """represents a single die, takes a name and an array of sides"""

    def __init__(self, name, sides):
        self.name = str(name)
        self.sides = sides
        self.numSides = len(sides)

    def __str__(self):
        sideStringList = ""
        before = ""
        for side in range(len(self.sides)):
            if side == 0:
                before = ""
            elif side == len(self.sides) - 1:
                before = " and "
            else:
                before = ", "
            sideStringList += before + str(self.sides[side])
        return "I am %s and I have a %s-sided die with values %s." % (self.name, self.numSides, sideStringList)

    def roll(self):
        rolledSide = random.randint(0, len(self.sides) - 1)
        theRoll = Roll(self.name, self.sides[rolledSide])
        return theRoll

class Roll(object):
    """represents the results of a die roll, takes a name and an array of sides"""

    def __init__(self, die, result):
        self.die = die
        self.result = result

    def __str__(self):
        return "The roll result of the %s's die is %s." % (self.die, str(self.result))

    def compareTo(self, anotherRoll):
        if self.result > anotherRoll.result:
            return Result.win
        elif self.result < anotherRoll.result:
            return Result.loss
        elif self.result == anotherRoll.result:
            return Result.tie

class RollGroup(object):
    """represents a group of rolls"""

    def __init__(self, listOfRolls):
        self.rolls = sortRolls(listOfRolls)
        self.rollCount = len(listOfRolls)
        # Determine if there are mulitple winners
        # Make a list of winners
        winnerIndex = 0 # Intialize winnerIndex
        winnerList = [self.rolls[winnerIndex]] # Add the first value to winner list
        while winnerIndex < self.rollCount - 1 and self.rolls[winnerIndex].result == self.rolls[winnerIndex + 1].result:
            winnerIndex += 1
            winnerList.append(self.rolls[winnerIndex]) # Adds the next value to the winner list if equal to the first
        if winnerIndex < self.rollCount - 1:
            # Make list of runners up
            runnerUpIndex = winnerIndex + 1 # Initializes runner-up index as
            runnersUpList = [sortRolls(listOfRolls)[runnerUpIndex]]
            while runnerUpIndex < self.rollCount - 1 and self.rolls[runnerUpIndex].result == self.rolls[runnerUpIndex + 1].result:
                runnerUpIndex += 1
                runnersUpList.append(self.rolls[runnerUpIndex]);
        else:
            # There are no runners up if all are tied for first
            self.runnersUp = nil
        # Make list of last place finishers
        lastPlaceIndex = len(resultList) - 1
        lastPlaceList = [sortRolls(listOfRolls)[lastPlaceIndex]]
        while lastPlaceIndex > 0 and self.rolls[lastPlaceIndex].result == self.rolls[lastPlaceIndex - 1].result:
            lastPlaceIndex -= 1
            lastPlaceList.append(self.rolls[lastPlaceIndex])
        # Add the winner object properties
        self.winners = winnerList
        self.winningResult = self.winners[0].result
        self.winningDies = buildListSting(self.winners)
        # Add the runner up object properties
        self.runnersUp = runnersUpList
        self.runnersUpResult = self.runnersUp[0].result
        self.runnersUpDies = buildListSting(self.runnersUp)
        # Add the last place object properties
        self.lastPlace = lastPlaceList
        self.lastPlaceResult = self.lastPlace[0].result
        self.lastPlaceDies = buildListSting(self.lastPlace)

    def __str__(self):
        return "There were %s rolls. %s was the winner with a roll of %s beating %s with a roll of %s. %s was last with a roll of %s." % (self.rollCount, self.winningDies, self.winningResult, self.runnersUpDies, self.runnersUpResult, self.lastPlaceDies, self.lastPlaceResult)

class Result(enum.Enum):
    win = 1
    tie = 0
    loss = -1

# Define Functions to Run Program
#_________________________________________________________________________________________

# Build a string describing a list
def buildListSting(inputList):
    outputString = ""
    for i in range(len(inputList)):
        if i == len(inputList) - 1 and i != 0:
            outputString.append("and ")
        elif i != len(inputList) - 1 and i != 0:
            outputString.append(", ")
        outputString.append(inputList[i])
    return outputString

# Returns a roll object given a die
def rollDie(dieToRoll):
    rolledSide = random.randint(0, len(dieToRoll.sides) - 1)
    return Roll(dieToRoll, dieToRoll.sides[rolledSide])

# Returns a sorted roll group, given a list of rolls
def sortRolls(listOfRolls):
    sortedList = sorted(listOfRolls, key=lambda roll: roll.result)
    return RollGroup(sortedList)

# Returns a win result if first die roll is greater, loss if first die roll is less and tie if rolls are even
def compareRolls(firstRoll, secondRoll):
    sortedRolls = sortRolls([firstRoll, secondRoll])
    if sortedRolls.winner == sortedRolls.lastPlace:
        return Result.tie
    if sortedRolls.winner == firstRoll:
        return Result.win
    if sortedRolls.winner == secondRoll:
        return Result.win

def rollXTime(timesToRoll, firstDie, secondDie):
    results = []
    firstDieCounter = 0
    secondDieCounter = 0
    tiedCounter = 0
    for i in range(timesToRoll):
        thisTime = compareRolls(firstDie, secondDie)
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
timesToRoll = int(input("How many times would you like to roll? "))

#Makes the dice
Katherine = Die("Katherine",[3,3,3,3,3,6])
Zack = Die("Zack",[2,2,2,5,5,5])
print(Katherine)
print(Zack)

#Perform the roll
results = rollXTime(timesToRoll, Katherine, Zack)
print("%s: %s, %s: %s, Tied: %s" % (Katherine.name, results[0], Zack.name, results[1], results[2]))
if results[0] > results[1] and results[0] > results[2]:
    print("%s won with %d%%." % (Katherine.name, 100*(float(results[0])/float(timesToRoll))))
if results[1] > results[0] and results[1] > results[2]:
    print("%s won with %d%%." % (Zack.name, 100*(float(results[1])/float(timesToRoll))))
if results[2] > results[0] and results[2] > results[1]:
    print("The ties won with %d%%." % 100*(float(results[2])/float(timesToRoll)))
