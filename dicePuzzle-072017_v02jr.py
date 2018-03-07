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
        self.rolls = listOfRolls
        self.rollCount = len(listOfRolls)
        self.winner = sortRolls(listOfRolls)[0].die
        self.runnerUp = sortRolls(listOfRolls)[1].die
        self.lastPlace = sortRolls(listOfRolls)[len(resultList) - 1].die
        self.winningResult = sortRolls(listOfRolls)[0].result
        self.runnerUpResult = sortRolls(listOfRolls)[1].result
        self.lastPlaceResult = sortRolls(listOfRolls)[len(resultList) - 1].result

    def __str__(self):
        return "There were %s rolls. %s was the winner with a roll of %s beating %s with a roll of %s." % (self.rollCount, self.winner, self.winningResult, self.runnerUp, self.runnerUpResult)

class Result(enum.Enum):
    win = 1
    tie = 0
    loss = -1

# Define Functions to Run Program
#_________________________________________________________________________________________

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
    if ssortedRolls.winner == secondRoll:
        return Result.win

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
