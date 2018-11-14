# MTGA Hand Analyzer 
A tool for analyzing winrates of starting hands for Magic the Gathering: Arena.

## Setup
You'll need to clone this repo, as well as install [python-mtga](https://github.com/mtgatracker/python-mtga).
Copy your log files (generally from somewhere like `C:\Program Files (x86)\Wizards of the Coast\MTGA\MTGA_Data\Logs\Logs` on windows) into this repo, under a folder named `Logs`

## Usage
```
python3 mtga-parser.py
```
This will print out the name of the log file, as well as each match type, final hand, which player you were, which player won, and any hands you mulliganed.

## Current Issues/To-Do
- Need to record hand/mulligan actions directly from `Client GRE`, as current logs from MTGA only record a few games from every session, maybe 1 of every 5.
- Need to store data for the user across sessions
- Need to add analytics (winrate with x card, x starting lands, with mulligan to x cards, etc)
- Need to categorize different cards w/ same name together (eg. M19 Island vs GRN Island)
- Need to parse opponent's played cards for winrates vs decktypes
- Need to add more statistics, such as # of draws, maybe extend to analyzing winrates based on what cards you draw and when combined with starting hand
- Create UI (look into using JS for a UI vs python and printing to shell)
- If pulling from `Client GRE` is too difficult, at least pull logs from folder instead of copying them.
