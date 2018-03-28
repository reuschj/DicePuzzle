# Imports
#_________________________________________________________________________________________

from utility import *
from rollFunctions import *
#---------------------------
import math
import random
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
        return "Sides: %s | Values: %s | Owner: %s" % (str(self.numSides), buildListString(self.sides), self.owner.name)

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
            runnersUpList = []
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
        if len(self.runnersUp) > 0:
            self.runnersUpResult = self.runnersUp[0].result
            self.runnersUpDies = buildListString(self.runnersUp)
        else:
            self.runnersUpResult = None
            self.runnersUpDies = None
        # Add the last place object properties
        self.lastPlace = lastPlaceList
        self.lastPlaceResult = self.lastPlace[0].result
        self.lastPlaceDies = buildListString(self.lastPlace)

    def __str__(self):
        returnStr = "\n"
        returnStr += "Winning Result: " + str(self.winningResult) + "\n"
        returnStr += "Runner Up Result: " + str(self.runnersUpResult) + "\n"
        returnStr += "Last Place Result: " + str(self.lastPlaceResult) + "\n"
        winnerList = []
        for i in range(len(self.winners)):
            winnerList.append(self.winners[i].die.owner.name)
        if len(self.winners) == 1:
            returnStr += "Winner: "
        else:
            returnStr += "Tied for first: "
        returnStr += buildListString(winnerList) + "\n"
        return returnStr

class ResultCounter(object):
    """represents the counts of wins, ties and losses for a die"""

    def __init__(self, die):
        self.die = die
        self.win = 0
        self.tie = 0
        self.loss = 0
        self.results = []
        self.totalScore = sum(result.value for result in self.results)
        self.winPercent = 0
        self.tiePercent = 0
        self.lossPercent = 0

    def __str__(self):
        return "%s: Total score: %s [ Wins: %s (%s) | Ties: %s (%s) | Losses: %s (%s) ]" % (self.die.name, str(self.totalScore), str(self.win), self.winPercent, str(self.tie), self.tiePercent, str(self.loss), self.lossPercent)

    def reset(self):
        self.win = 0
        self.tie = 0
        self.loss = 0
        self.results = []
        self.totalScore = sum(result.value for result in self.results)
        self.winPercent = Percent(self.win / len(self.results))
        self.tiePercent = Percent(self.tie / len(self.results))
        self.lossPercent = Percent(self.loss / len(self.results))

    def addWin(self):
        self.win += 1
        self.results.append(Result.win)
        self.totalScore = sum(result.value for result in self.results)
        self.winPercent = Percent(self.win / len(self.results))
        self.tiePercent = Percent(self.tie / len(self.results))
        self.lossPercent = Percent(self.loss / len(self.results))

    def addTie(self):
        self.tie += 1
        self.results.append(Result.tie)
        self.totalScore = sum(result.value for result in self.results)
        self.winPercent = Percent(self.win / len(self.results))
        self.tiePercent = Percent(self.tie / len(self.results))
        self.lossPercent = Percent(self.loss / len(self.results))

    def addNone(self):
        self.results.append(Result.none)
        self.winPercent = Percent(self.win / len(self.results))
        self.tiePercent = Percent(self.tie / len(self.results))
        self.lossPercent = Percent(self.loss / len(self.results))

    def addLoss(self):
        self.loss += 1
        self.results.append(Result.loss)
        self.totalScore = sum(result.value for result in self.results)
        self.winPercent = Percent(self.win / len(self.results))
        self.tiePercent = Percent(self.tie / len(self.results))
        self.lossPercent = Percent(self.loss / len(self.results))

class Percent(object):
    """represents the percentage format of a decimal input"""

    def __init__(self, decimalInput):
        self.value = int(round(decimalInput * 100))
        self.inital = self

    def __str__(self):
        return "%s%%" % (str(self.value))


class Result(enum.Enum):
    win = 1
    tie = 0
    none = 0
    loss = -1

    def __str__(self):
        if self == Result.win:
            return "\nWin"
        elif self == Result.loss:
            return "\nLoss"
        elif self == Result.tie:
            return "\nTie"
        else:
            return "\nNone"
