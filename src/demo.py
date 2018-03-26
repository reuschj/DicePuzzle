# Imports
#_________________________________________________________________________________________

from utility import *
from classes import *
from rollFunctions import *

# Actions
#_________________________________________________________________________________________


#Load the CSV file to a variable
print("\n")
timesToRoll = int(input("How many times would you like to roll? "))

# ----------------------------------------
print("\n-------------")

# Make the people
Katherine = Person("Katherine")
Zack = Person("Zack")
Justin = Person("Justin")
Hang = Person("Hang")

# Make the dice
dice = []
dice.append( Die([3,3,3,3,3,6], Katherine) ) #0
dice.append( Die([2,2,2,5,5,5], Zack) ) #1
dice.append( Die([3,3,3,3,3,6], Justin) ) #2
dice.append( Die([2,2,2,5,5,5], Hang) ) #3
dice.append( Die([1,2,3,4,5,6], Justin) ) #4
dice.append( Die([1,2,3,4,5,6], Hang) ) #5

# Roll the dice
rolls = []
for i in range(len(dice)):
    rolls.append( dice[i].roll() )

# ----------------------------------------
print("\n-------------")

# Introduce people
print("\nIntroducing...")
print(Katherine)
print(Zack)
print(Justin)
print(Hang)

# ----------------------------------------
print("\n-------------")

# Print a few single rolls
print("\nLet's roll 2 dice...")
print(rolls[0])
print(rolls[1])
# Let's compare them...
print(rolls[0].compareTo(rolls[1]))

print("\n-------------")

# Print a few more single rolls
print("\nLet's roll 2 more...")
print(rolls[4])
print(rolls[5])
# Let's compare them...
print(rolls[4].compareTo(rolls[5]))
print(rolls[5].compareTo(rolls[4]))

# ----------------------------------------
print("\n-------------")

# Roll the first 4 dice 10 times, printing each roll result
print("Rolling 10 times...")
rollXTimes(10,[dice[0], dice[1], dice[2], dice[3]], True)

# ----------------------------------------
print("\n-------------")

# Roll just dice 1 and 2 the inputed amount of times
rollXTimes(timesToRoll,[dice[0], dice[1]], False)

# Roll just dice 1, 2, 5 and 6 the inputed amount of times
rollXTimes(timesToRoll,[dice[0], dice[1], dice[4], dice[5]], False)
print("\n")
