# Imports
#_________________________________________________________________________________________

from utility import *
from classes import *
from rollFunctions import *
#---------------------------
from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont


# Setup
#_________________________________________________________________________________________

# Make the people
Katherine = Person("Katherine")
Zack = Person("Zack")
Justin = Person("Justin")
Hang = Person("Hang")
John = Person("John")
Bob = Person("Bob")


# Make the dice
dice = []
dice.append( Die([3,3,3,3,3,6], Katherine) )
dice.append( Die([2,2,2,5,5,5], Zack) )
dice.append( Die([3,3,3,3,3,6], Justin) )
dice.append( Die([2,2,2,5,5,5], Hang) )
dice.append( Die([1,2,3,4,5,6], Justin) )
dice.append( Die([1,2,3,4,5,6], Hang) )
dice.append( Die([1,1,1,6,6,6], John) )
dice.append( Die([3,3,3,3,3,3], Bob) )

# Interface
#_________________________________________________________________________________________

class App:

    def __init__(self, master):
        # Define fonts
        self.normalFont = tkFont.Font(family="Helvetica", size=14, weight="normal")
        self.boldFont = tkFont.Font(family="Helvetica", size=14, weight="bold")
        self.headerFont = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.gray = "#999999"
        self.lightGray = "#cccccc"
        self.darkGray = "#555555"
        self.blue = "#0071ce"

        # Main Frame
        mainFrame = ttk.Frame(master, padding="10 10 10 10")
        mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.rowconfigure(0, weight=1)

        # Dice Frame
        diceFrame = ttk.Frame(mainFrame, padding="5 5 5 5")
        diceFrame.grid(column=0, sticky=(W, E))

        # Add dice to Dice Frame
        ttk.Label(diceFrame, text="Dice to Roll", font=self.headerFont, foreground=self.blue).grid(column=0, columnspan=3, row=0, sticky=(N, W, E))
        diceChecks = []
        # For each die, add a checkbox
        for i in range(len(dice)):
            checkBoxes[i].set(1) # Check all by default
            descriptions[i].set(str(dice[i].owner.name) + "'s die with " + str(dice[i].numSides) + " sides (" + buildListString(dice[i].sides) + ")")
            thisCheck = ttk.Checkbutton(diceFrame, text=descriptions[i].get(), variable=checkBoxes[i])
            thisCheck.grid(row=(i + 1), sticky=W)
            diceChecks.append(thisCheck)
        diceFrame.pack()

        # Main input
        ttk.Label(mainFrame, text="How many times would you like to roll?", justify='center').grid(column=0, row=1, sticky=(W, E))
        times.set(str(100)) # Set default value to 100
        timesInput = ttk.Entry(mainFrame, width=7, textvariable=times, justify='center')
        timesInput.grid(column=0, row=2, sticky=(W, E))

        # Buttons
        ttk.Label(mainFrame, text="").grid(column=0, row=3, sticky=(W, E)) # Spacer
        rollButton = ttk.Button(mainFrame, text="Roll the Dice", command=self.performRolls)
        rollButton.grid(column=0, row=4, sticky=(W, E))
        # resetButton = ttk.Button(mainFrame, text="Reset", command=self.reset)
        # resetButton.grid(column=0, row=5, sticky=(W, E))
        ttk.Label(mainFrame, text="").grid(column=0, row=6, sticky=(W, E)) # Spacer

        # Results Frame
        resultsFrame = ttk.Frame(mainFrame, padding="5 5 5 5")
        resultsFrame.grid(column=0, row=7, sticky=(W, E))
        self.output = resultsFrame

        for child in mainFrame.winfo_children(): child.grid_configure(padx=5, pady=5)

        timesInput.focus()
        master.bind('<Return>', self.performRolls)
        master.title("Dice Puzzle")

    def performRolls(self, *args):
        try:
            # Get the checked dice
            diceList = []
            # Look through checked items. If checked, add it to the list of dice to roll.
            for i in range(len(dice)):
                if checkBoxes[i].get() == 1:
                    diceList.append(dice[i])
                # Failsafe: If no dice are checked, then roll all
                if i + 1 == len(dice) and len(diceList) == 0:
                    diceList: dice
            # Gets the input
            timesToRoll = int(times.get())
            # Runs rollXTimes
            rollOutput = rollXTimes(timesToRoll, diceList, True)
            # Makes variable for the array output and string output
            resultsArray = rollOutput[0]
            resultsString = rollOutput[1]
            # Used for the string output (matches terminal output)
            output.set(str(resultsString))
            # Sets the winner
            winner.set(str(resultsArray[0].die.owner.name))
            # Loads result values for each die rolled
            for i in range(len(diceList)):
                names[i].set(resultsArray[i].die.owner.name)
                totalScores[i].set(resultsArray[i].totalScore)
                wins[i].set(resultsArray[i].win)
                ties[i].set(resultsArray[i].tie)
                noResults[i].set(resultsArray[i].none)
                losses[i].set(resultsArray[i].loss)
                winPercents[i].set("(" + str(resultsArray[i].winPercent) + ")")
                tiePercents[i].set("(" + str(resultsArray[i].tiePercent) + ")")
                noResultPercents[i].set("(" + str(resultsArray[i].nonePercent) + ")")
                lossPercents[i].set("(" + str(resultsArray[i].lossPercent) + ")")
                dieDescriptions[i].set(str(resultsArray[i].die.numSides) + " sides (" + buildListString(resultsArray[i].die.sides) + ")")
            # Count the number of dice roled and build the results output
            resultsCount = len(resultsArray)
            self.buildResult(resultsCount)
        except ValueError:
            pass

    def buildResult(self, resultsCount, *args):
        try:
            # Clear any previous results from the frame
            for item in self.output.winfo_children():
                item.destroy()
            # Builds the output label with winner
            ttk.Label(self.output, text="Results", font=self.headerFont, foreground=self.blue).grid(column=0, row=0, columnspan=2, sticky=(W, E))
            ttk.Label(self.output, text="").grid(column=0, row=1, sticky=(W, E)) # Spacer
            ttk.Label(self.output, text="Winner:    ", font=self.boldFont).grid(column=0, row=2, sticky=W)
            ttk.Label(self.output, textvariable=winner).grid(column=1, row=2, sticky=W)
            ttk.Label(self.output, text="").grid(column=0, row=3, sticky=(W, E)) # Spacer
            # Build the header
            ttk.Label(self.output, text="Name    ", font=self.boldFont).grid(column=0, row=4, sticky=W)
            ttk.Label(self.output, text="Total Score    ", font=self.boldFont).grid(column=1, row=4, sticky=W)
            ttk.Label(self.output, text="Wins            ", font=self.boldFont).grid(column=2, columnspan=2, row=4, sticky=W)
            ttk.Label(self.output, text="Ties            ", font=self.boldFont).grid(column=4, columnspan=2, row=4, sticky=W)
            ttk.Label(self.output, text="Losses            ", font=self.boldFont).grid(column=6, columnspan=2, row=4, sticky=W)
            ttk.Label(self.output, text="No Result            ", font=self.boldFont).grid(column=8, columnspan=2, row=4, sticky=W)
            ttk.Label(self.output, text="Die Description", font=self.boldFont).grid(column=10, columnspan=2, row=4, sticky=W)
            # Build result rows
            for i in range(resultsCount):
                ttk.Label(self.output, textvariable=names[i]).grid(column=0, row= 5 + i, sticky=W)
                ttk.Label(self.output, textvariable=totalScores[i], font=self.boldFont).grid(column=1, row= 5 + i, sticky=W)
                ttk.Label(self.output, textvariable=wins[i]).grid(column=2, row= 5 + i, sticky=W)
                ttk.Label(self.output, textvariable=winPercents[i], foreground=self.gray).grid(column=3, row= 5 + i, sticky=W)
                ttk.Label(self.output, textvariable=ties[i]).grid(column=4, row= 5 + i, sticky=W)
                ttk.Label(self.output, textvariable=tiePercents[i], foreground=self.gray).grid(column=5, row= 5 + i, sticky=W)
                ttk.Label(self.output, textvariable=losses[i]).grid(column=6, row= 5 + i, sticky=W)
                ttk.Label(self.output, textvariable=lossPercents[i], foreground=self.gray).grid(column=7, row= 5 + i, sticky=W)
                ttk.Label(self.output, textvariable=noResults[i]).grid(column=8, row= 5 + i, sticky=W)
                ttk.Label(self.output, textvariable=noResultPercents[i], foreground=self.gray).grid(column=9, row= 5 + i, sticky=W)
                ttk.Label(self.output, textvariable=dieDescriptions[i]).grid(column=10, row= 5 + i, sticky=W)
            # Builds the key
            ttk.Label(self.output, text="").grid(column=0, row=5 + resultsCount + 1, sticky=(W, E)) # Spacer
            ttk.Label(self.output, text="Key", font=self.headerFont, foreground=self.blue).grid(column=0, columnspan=10, row=5 + resultsCount + 2, sticky=(W, E))
            ttk.Label(self.output, text="Win: Only die with the winning result").grid(column=0, columnspan=10, row=5 + resultsCount + 3, sticky=(W, E))
            ttk.Label(self.output, text="Tie: Tied with other dice for the winning result").grid(column=0, columnspan=10, row=5 + resultsCount + 4, sticky=(W, E))
            ttk.Label(self.output, text="Loss: Only die with the last place result").grid(column=0, columnspan=10, row=5 + resultsCount + 5, sticky=(W, E))
            ttk.Label(self.output, text="No Result: Anything else than above").grid(column=0, columnspan=10, row=5 + resultsCount + 6, sticky=(W, E))
            ttk.Label(self.output, text="").grid(column=0, row=5 + resultsCount + 7, sticky=(W, E)) # Spacer
            resetButton = ttk.Button(self.output, text="Reset", command=self.reset)
            resetButton.grid(column=0, columnspan=15, row=5 + resultsCount + 8, sticky=(W, E))
        except ValueError:
            pass

    def reset(self, *args):
        try:
            # Clear any previous results from the frame
            for item in self.output.winfo_children():
                item.destroy()
            ttk.Label(self.output, text="").grid(column=0, row=0, sticky=(W, E)) # Blank
        except ValueError:
            pass

root = Tk()

# Input variables --------------------------------------------------------------
dicelist = StringVar()
times = StringVar()

# Output Variables -------------------------------------------------------------
output = StringVar()
winner = StringVar()
# These Python arrays will hold results for each die
checkBoxes = []
descriptions = []
names = []
totalScores = []
wins = []
ties = []
noResults = []
losses = []
winPercents = []
tiePercents = []
noResultPercents = []
lossPercents = []
dieDescriptions = []
# For each die created, create a tk variable and load it to the Python array
for i in range(len(dice)):
    checkbox = IntVar()
    description = StringVar()
    name = StringVar()
    totalscore = IntVar()
    win = StringVar()
    tie = StringVar()
    noresult = StringVar()
    loss = StringVar()
    winPercent = StringVar()
    tiePercent = StringVar()
    noresultPercent = StringVar()
    lossPercent = StringVar()
    dieDescription = StringVar()
    # Add to Python arrays
    checkBoxes.append(checkbox)
    descriptions.append(description)
    names.append(name)
    totalScores.append(totalscore)
    wins.append(win)
    ties.append(tie)
    noResults.append(noresult)
    losses.append(loss)
    winPercents.append(winPercent)
    tiePercents.append(tiePercent)
    noResultPercents.append(noresultPercent)
    lossPercents.append(lossPercent)
    dieDescriptions.append(dieDescription)

# Call app
app = App(root)

root.mainloop()
