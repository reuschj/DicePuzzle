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
    allResults = [] # To hold result counters
    for i in range(len(listOfDiceToRoll)):
        # Initialize a result counter for each die to roll in allResults
        allResults.append(ResultCounter(listOfDiceToRoll[i]))
    allRolls = [] # To hold the rolls
    for i in range(timesToRoll):
        currentRollGroup = [] # Holds each "turn" of rolling
        for j in range(len(listOfDiceToRoll)):
            currentRoll = listOfDiceToRoll[j].roll()
            currentRollGroup.append(currentRoll)
        allRolls.append(RollGroup(sortRolls(currentRollGroup)))
    # Goes through all rolls and adds the counters
    for i in range(len(allRolls)):
        # Prints the outcome of each roll (optional)
        if showAllResults == True:
            print("\nRoll " + str(i + 1) + "\n-------------")
            print(allRolls[i])
        # Goes through each die and adds to the appropriate counter
        for j in range(len(allResults)):
            noResults = True # Resets... will change to false when result is found
            # If there is a single winner (no tie for first)
            if len(allRolls[i].winners) == 1:
                # If the current die is the single winner
                if allResults[j].die == allRolls[i].winners[0].die:
                    allResults[j].addWin()
                    noResults = False # Found a result
            # If there are multiple winners (tie for first)
            else:
                # For each winner (tie)
                for k in range(len(allRolls[i].winners)):
                    # If the current die is in the winner (tie) list
                    if allResults[j].die == allRolls[i].winners[k].die:
                        allResults[j].addTie()
                        noResults = False # Found a result
            # If no winning or tie result was found
            if noResults:
                # If there is a single last place result (loss) and the current die is the single loser
                if len(allRolls[i].lastPlace) == 1 and allResults[j].die == allRolls[i].lastPlace[0].die:
                    allResults[j].addLoss()
                    noResults = False # Found a result
                # If the die has not matched a win, tie or loss, then count it as "no result"
                else:
                    allResults[j].addNone()
    # Sort results by total score
    allResultsSorted = sorted(allResults, key=lambda score: score.totalScore, reverse=True)
    returnStr = "Rolls: %s | Winner: %s" % (str(timesToRoll), str(allResultsSorted[0].die.owner.name)) + "\n"
    returnStr += "-------------\n"
    for i in range(len(allResultsSorted)):
        returnStr += str(allResultsSorted[i]) + "\n"
    print("\n" + returnStr)
    return [allResultsSorted, returnStr]
