# Imports
#_________________________________________________________________________________________

from utility import *
from classes import *
from rollFunctions import *
#---------------------------
from tkinter import *
from tkinter import ttk

# Actions
#_________________________________________________________________________________________

def performRolls(*args):
    try:
        timesToRoll = int(times.get())
        rollOutput = rollXTimes(timesToRoll, dice, False)
        resultsObject = rollOutput[0]
        resultsString = rollOutput[1]
        winner.set(resultsObject[0].die.owner.name)
        output.set(str(resultsString))
    except ValueError:
        pass

# Setup
#_________________________________________________________________________________________

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

# Interface
#_________________________________________________________________________________________

root = Tk()
root.title("Dice Puzzle")

# Input variables
times = StringVar()

# Output Variables
output = StringVar()
winner = StringVar()

# Main Frame
mainFrame = ttk.Frame(root, padding="10 10 10 10")
mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
mainFrame.columnconfigure(0, weight=1)
mainFrame.rowconfigure(0, weight=1)

# Dice Frame
diceFrame = ttk.Frame(mainFrame, padding="5 5 5 5")
diceFrame.grid(column=0, row=0, sticky=(W, E))

# Add dice to Dice Frame
ttk.Label(diceFrame, text="Available Dice", font='Helvetica 16 bold').grid(column=0, columnspan=3, row=0, sticky=(N, W, E))
for i in range(len(dice)):
    ttk.Label(diceFrame, text=(str(i + 1) + "   ") , font='Helvetica 14 bold').grid(column=0, row=(i + 1), sticky=W)
    ttk.Label(diceFrame, text=(str(dice[i].owner.name) + "'s die with " + str(dice[i].numSides) + " sides (" + buildListString(dice[i].sides) + ")")).grid(column=1, row=(i + 1), sticky=W)
diceFrame.pack()

# Input
ttk.Label(mainFrame, text="How many times would you like to roll?").grid(column=0, row=1, sticky=(W, E))
timesInput = ttk.Entry(mainFrame, width=7, textvariable=times)
timesInput.grid(column=0, row=2, sticky=(W, E))

# Button
rollButton = ttk.Button(mainFrame, text="Roll the Dice", command=performRolls)
rollButton.grid(column=0, row=3, sticky=(W, E))

# Output Label
ttk.Label(mainFrame, text="Results", font='Helvetica 16 bold').grid(column=0, columnspan=2, row=4, sticky=(W, E))
ttk.Label(mainFrame, text="Winner:    ", font='Helvetica 14 bold').grid(column=0, row=5, sticky=W)
winnerLabel = ttk.Label(mainFrame, textvariable=winner)
winnerLabel.grid(column=1, row=5, sticky=W)
outputLabel = ttk.Label(mainFrame, textvariable=output)
outputLabel.grid(column=0, columnspan=2, row=6, sticky=(W, E, S))
outputLabel.pack()

for child in mainFrame.winfo_children(): child.grid_configure(padx=5, pady=5)

timesInput.focus()
root.bind('<Return>', performRolls)

root.mainloop()
