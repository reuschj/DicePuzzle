# Imports
#_________________________________________________________________________________________

import math
import random
import sys
import datetime
import enum
import operator

# Define Objects
#_________________________________________________________________________________________

class Person(object):
    """represents a person who can posess one or more dice"""

    def __init__(self, name, die = None):
        self.name = name
        if die == None:
            self.dice = []
        else:
            self.dice = [die]
            die.owner = self

    def __str__(self):
        diceStatement = ""
        numDice = len(self.dice)
        dieStr = "die" if numDice == 1 else "dice"
        if numDice == 0:
            diceStatement = "I don't have any dice yet."
        else:
            diceStatement += "I have %s %s with values:\n" % (str(numDice), dieStr)
            for i in range(numDice):
                diceStatement += "Die %s (%s sides): %s" % (str(i + 1), str(self.dice[i].numSides), buildListString(self.dice[i].sides))
                if i < numDice - 1:
                    diceStatement += "\n"
        return "\nI'm %s. %s" % (self.name, diceStatement)

    def getDie(self, die):
        self.dice.append(die)
        print("\n%s now owns a new die with %s sides." % (self.name, str(die.numSides)))
        die.owner = self

class Die(object):
    """represents a single die, takes a name and an array of sides"""

    def __init__(self, sides, owner = None):
        self.sides = sides
        self.numSides = len(sides)
        if owner == None:
            self.owner = None
            self.name = "Unnamed Die with %s Sides" % (str(self.numSides))
        else:
            self.owner = owner
            self.name = "%s's Die with %s Sides" % (owner.name.capitalize(), str(self.numSides))
            owner.getDie(self)

    def __str__(self):
        return "Sides: %s | Values %s | Owner: %s" % (str(self.numSides), buildListString(self.sides), self.owner.name)

    def assignOwner(self, owner):
        self.owner = owner
        print("\n%s now owns a new die with %s sides." % (owner.name, str(self.numSides)))
        owner.getDie(self)

    def roll(self):
        rolledSide = random.randint(0, len(self.sides) - 1)
        return Roll(self, self.sides[rolledSide])

class Roll(object):
    """represents the results of a die roll, takes a name and an array of sides"""

    def __init__(self, die, result):
        self.die = die
        self.result = result

    def __str__(self):
        ownerTag = self.die.owner.name + ": " if self.die.owner != None else ""
        return "\n%sThe roll result is %s." % (ownerTag, str(self.result))

    def compareTo(self, anotherRoll):
        ownerTag = self.die.owner.name + ": " if self.die.owner != None else ""
        printResult = "\n" + ownerTag
        if self.result > anotherRoll.result:
            print(printResult + "I win! :)")
            return Result.win
        elif self.result < anotherRoll.result:
            print(printResult + "I lose. :(")
            return Result.loss
        elif self.result == anotherRoll.result:
            print(printResult + "We tied.")
            return Result.tie

class RollGroup(object):
    """represents a group of rolls"""

    def __init__(self, listOfRolls):
        self.rolls = sortRolls(listOfRolls, True)
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
            runnersUpList = [sortRolls(listOfRolls, True)[runnerUpIndex]]
            while runnerUpIndex < self.rollCount - 1 and self.rolls[runnerUpIndex].result == self.rolls[runnerUpIndex + 1].result:
                runnerUpIndex += 1
                runnersUpList.append(self.rolls[runnerUpIndex]);
        else:
            # There are no runners up if all are tied for first
            self.runnersUp = nil
        # Make list of last place finishers
        lastPlaceIndex = len(listOfRolls) - 1
        lastPlaceList = [sortRolls(listOfRolls, True)[lastPlaceIndex]]
        while lastPlaceIndex > 0 and self.rolls[lastPlaceIndex].result == self.rolls[lastPlaceIndex - 1].result:
            lastPlaceIndex -= 1
            lastPlaceList.append(self.rolls[lastPlaceIndex])
        # Add the winner object properties
        self.winners = winnerList
        self.winningResult = self.winners[0].result
        self.winningDies = buildListString(self.winners)
        # Add the runner up object properties
        self.runnersUp = runnersUpList
        self.runnersUpResult = self.runnersUp[0].result
        self.runnersUpDies = buildListString(self.runnersUp)
        # Add the last place object properties
        self.lastPlace = lastPlaceList
        self.lastPlaceResult = self.lastPlace[0].result
        self.lastPlaceDies = buildListString(self.lastPlace)

    def __str__(self):
        return "There were %s rolls. %s was the winner with a roll of %s beating %s with a roll of %s. %s was last with a roll of %s." % (self.rollCount, self.winningDies, self.winningResult, self.runnersUpDies, self.runnersUpResult, self.lastPlaceDies, self.lastPlaceResult)

class Result(enum.Enum):
    win = 1
    tie = 0
    loss = -1

    def __str__(self):
        if self == Result.win:
            return "\nWin"
        elif self == Result.loss:
            return "\nLoss"
        else:
            return "\nTie"

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

# Returns a roll object given a die
def rollDie(dieToRoll):
    rolledSide = random.randint(0, len(dieToRoll.sides) - 1)
    return Roll(dieToRoll, dieToRoll.sides[rolledSide])

# Returns a sorted roll group, given a list of rolls
def sortRolls(listOfRolls, reversed = False):
    sortedList = sorted(listOfRolls, key=lambda roll: roll.result, reverse=reversed)
    return sortedList

# Returns a win result if first die roll is greater, loss if first die roll is less and tie if rolls are even
def compareRolls(firstRoll, secondRoll):
    sortedRolls = sortRolls([firstRoll, secondRoll])
    if sortedRolls.winner == sortedRolls.lastPlace:
        return Result.tie
    if sortedRolls.winner == firstRoll:
        return Result.win
    if sortedRolls.winner == secondRoll:
        return Result.win

# Rough working pass
def rollXTimes(timesToRoll, listOfDiceToRoll):
    winCounter = []
    for i in range(len(listOfDiceToRoll)):
        currentDie = {"name": listOfDiceToRoll[i].name, "wins": 0}
        winCounter.append(currentDie)
    print(winCounter)
    allRolls = []
    for i in range(timesToRoll):
        currentRollGroup = []
        for j in range(len(listOfDiceToRoll)):
            currentRoll = listOfDiceToRoll[j].roll()
            currentRollGroup.append(currentRoll)
        allRolls.append(RollGroup(sortRolls(currentRollGroup)))
    for i in range(len(allRolls)):
        print("\nRoll " + str(i + 1) + "\n-------------")
        print("Winning Result: " + str(allRolls[i].winningResult))
        print("Runner Up Result: " + str(allRolls[i].runnersUpResult))
        print("Last Place Result: " + str(allRolls[i].lastPlaceResult))
        print("Winners:")
        for j in range(len(allRolls[i].winners)):
            for k in range(len(winCounter)):
                if allRolls[i].winners[j].die.name == winCounter[k]['name']:
                    winCounter[k]['wins'] += 1
            print(allRolls[i].winners[j].die.owner.name)
    winCounter.sort(key=operator.itemgetter('wins'), reverse=True)
    print("\n")
    for i in range(len(winCounter)):
        print("%s: %s wins" % (str(winCounter[i]['name']), str(winCounter[i]['wins'])))


# Actions
#_________________________________________________________________________________________

#Load the CSV file to a variable
# timesToRoll = int(input("How many times would you like to roll? "))``
timesToRoll = 100

# Makes the people
Katherine = Person("Katherine")
Zack = Person("Zack")
Justin = Person("Justin")
Hang = Person("Hang")

# Makes the dice
die01 = Die([3,3,3,3,3,6], Katherine)
die02 = Die([2,2,2,5,5,5], Zack)
die03 = Die([3,3,3,3,3,6], Justin)
die04 = Die([2,2,2,5,5,5], Hang)
die05 = Die([1,2,3,4,5,6], Justin)
die06 = Die([1,2,3,4,5,6], Hang)
print(Katherine)
print(Zack)
print(Justin)
print(Hang)

roll01 = die01.roll()
roll02 = die02.roll()
roll03 = die05.roll()
roll04 = die06.roll()
print(roll01)
print(roll02)
print(roll01.compareTo(roll02))
print(roll03)
print(roll04)
print(roll03.compareTo(roll04))
print(roll04.compareTo(roll03))

rollXTimes(10,[die01, die02, die03, die04])
print("\n")

#Perform the roll
# results = rollXTime(timesToRoll, Katherine, Zack)
# print("%s: %s, %s: %s, Tied: %s" % (Katherine.name, results[0], Zack.name, results[1], results[2]))
# if results[0] > results[1] and results[0] > results[2]:
#     print("%s won with %d%%." % (Katherine.name, 100*(float(results[0])/float(timesToRoll))))
# if results[1] > results[0] and results[1] > results[2]:
#     print("%s won with %d%%." % (Zack.name, 100*(float(results[1])/float(timesToRoll))))
# if results[2] > results[0] and results[2] > results[1]:
#     print("The ties won with %d%%." % 100*(float(results[2])/float(timesToRoll)))
