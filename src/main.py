# Imports
#_________________________________________________________________________________________

from utility import *
from tkinter import *

# Actions
#_________________________________________________________________________________________

#Load the CSV file to a variable
timesToRoll = int(input("How many times would you like to roll? "))

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

rollXTimes(10,[die01, die02, die03, die04], True)
rollXTimes(timesToRoll,[die01, die02], False)
rollXTimes(timesToRoll,[die01, die02, die05, die06], False)
print("\n")
