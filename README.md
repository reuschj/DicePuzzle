# DicePuzzle
A Python app to simulate multiple dice rolls given dice with various side values.

## The Purpose of This App
The genesis of this app was a simulation for a math puzzle. In the puzzle, there were two people each rolling a six-sided die with different values. Katherine had a die with sides 3, 3, 3, 3, 3 and 6. Zack had a die with sides 2, 2, 2, 5, 5 and 5. The puzzle asked which die was more likely to win.

The solution to this puzzle concludes that Katherine's die wins about 60% of the time. The initial version of this app simply ran a simulation of these two dice against each other a variable amount of times. With this app, this probability could be shown by rolling a high number of times.

I recently revisited this simple app and made it a bit more flexible. Why? In part, to allow the app to simulate other similar dice puzzles (and rolling more than two dice). However, the primary reason to build this app was just as a simple, fun way to practice coding in Python.

I've added a couple pre-made dice (in addition to Katherine and Zack from the initial puzzle). Hang and Justin (named after my wife and I) both roll standard six-side dice. John rolls a die with sides 1, 1, 1, 6, 6 and 6. Bob rolls a die with a 3 on all sides. You can add, remove or modify these dice in the setup section of `main.py`.

If you've found this app and find it useful, please feel free to use it and customize it however you wish. Enjoy!

## Usage

Run the app by navigating to the /src directory in a terminal and entering: `python3 main.py` This will launch the tkinter GUI.

On the top section of the window, you will see a list of all the pre-made dice to roll. By default, all dice are checked. You can deselect any you don't want to roll.

To change the pre-made dice, you can add, remove or modify these dice in the setup section of `main.py`. Dice are made by appending them to the dice array. A Die object takes an array of side values and a person to own the die. You can also add, remove or modify people in the setup section.

You an enter a number of times to roll the dice in the input field. The default is set to 100 rolls. Press *Roll the Dice* to perform the rolls.

The results will show below the button, followed by a key and reset button. You can either press *Roll the Dice* to immediately re-roll, or *Reset* to return to the initial view.

The results section shows the winner and a table of results. Each contestant is listed by row, ranked by performance. The rank is based on the total score, which is calculated by awarding a point for each "win" and subtracting a point for each "loss." No points are awarded or subtracted for a tie or no result.

Per the key, a "win" is defined as being the *only* die with a winning (high) result. A "tie" is defined as being one of several dice with the winning result (a.k.a. tied for first). A "loss" is defined as being the *only* die with a losing (low) result. All other dice count as "no result."

Consider these two examples with four dice per roll. In the first table, there is a winner and loser. In the second table, there is no clear winner or loser, only a tie for first.

Die Roll | Result
--- | ---
5 | Win
3 | No Result
3 | No Result
2 | Loss

or

Die Roll | Result
--- | ---
6 | Tie
6 | Tie
3 | No Result
3 | No Result

## Structure

The app is divided into multiple files in the `src` folder.

### main.py

This is the main file to run for the tkinter GUI. This file also contains a setup section to define the dice available to the GUI.

### demo.py

This file runs a demo script (to the terminal only) with multiple rolls that demonstrate some of the capabilities of the app.

### classes.py

This file contains all the classes to define the primary Python objects, including:

* Person - Represents a person who can posess one or more dice
* Die - Represents a single die, takes a name and an array of sides
* Roll - Represents the results of a die roll, takes a name and an array of sides
* RollGroup - Represents a group of rolls
* ResultCounter - Represents the counts of wins, ties and losses for a die
* Percent - Represents the percentage format of a decimal input
* Result (enumerator) - Assigns numerical values for wins, losses and ties

### rollFunctions.py

This file contains all the functions used for dice rolls, including:

* rollDie - Returns a roll object given a die
* sortRolls - Returns a sorted roll group, given a list of rolls
* compareRolls - Returns a win result if first die roll is greater, loss if first die roll is less and tie if rolls are even
* rollXTimes - Rolls a set of dice a given number of times

### utility.py

This file contains any general-purpose functions used by the app. It currently only contains one:

* buildListString - Builds a string describing a list

## Current Version
The current version is 1.0.0 and requires Python 3 and `tkinter` (for the GUI).

## Python Versions

DicePuzzle Version | Python Version
--- | ---
1.0.0 | 3.6.4
v02jr | 3.6.4
v01jr | 2.7.10
