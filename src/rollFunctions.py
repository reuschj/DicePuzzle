# Imports
#_________________________________________________________________________________________

import math
import random
import enum
import operator

# Define Functions to Run Program
#_________________________________________________________________________________________

# Returns a roll object given a die
def rollDie(dieToRoll):
    from classes import Roll
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

# Rolls a set of dice a given number of times
def rollXTimes(timesToRoll, listOfDiceToRoll, showAllResults = False):
    from classes import RollGroup
    from classes import ResultCounter
    allResults = []
    for i in range(len(listOfDiceToRoll)):
        allResults.append(ResultCounter(listOfDiceToRoll[i]))
    allRolls = []
    for i in range(timesToRoll):
        currentRollGroup = []
        for j in range(len(listOfDiceToRoll)):
            currentRoll = listOfDiceToRoll[j].roll()
            currentRollGroup.append(currentRoll)
        allRolls.append(RollGroup(sortRolls(currentRollGroup)))
    for i in range(len(allRolls)):
        if showAllResults == True:
            print("\nRoll " + str(i + 1) + "\n-------------")
            print(allRolls[i])
        for j in range(len(allRolls[i].winners)):
            for k in range(len(allResults)):
                if allRolls[i].winners[j].die == allResults[k].die:
                    if len(allRolls[i].winners) > 1:
                        allResults[k].addTie()
                        print("addTie to " + str(allResults[k].die.name))
                    else:
                        allResults[k].addWin()
                        print("addWin to " + str(allResults[k].die.name))
                elif len(allRolls[i].lastPlace) == 1:
                    if allRolls[i].lastPlace[0].die == allResults[k].die:
                        allResults[k].addLoss()
                        print("addTie to " + str(allResults[k].die.name))
                else:
                    allResults[k].addNone()
                    print("addTie to " + str(allResults[k].die.name))
    allResultsSorted = sorted(allResults, key=lambda score: score.totalScore, reverse=True)
    returnStr = "Rolls: %s | Winner: %s" % (str(timesToRoll), str(allResultsSorted[0].die.owner.name)) + "\n"
    returnStr += "-------------\n"
    for i in range(len(allResultsSorted)):
        returnStr += str(allResultsSorted[i]) + "\n"
    print("\n" + returnStr)
    return [allResultsSorted, returnStr]
