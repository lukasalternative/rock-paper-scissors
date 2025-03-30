# Rock, Paper, Scissors

Python implementation of Rock, Paper, Scissors.

## Overview:
- Game supports a human player and an AI player
- Two rules versions: classic, rock, paper, scissors, lizard, spock
- Extensible, data-driven implementation to enable easy implementation of new game variants, rules, movesets, AI strategies, or two-player mode.

## Requirements and Setup

- Python 3.10+
- Recommended: Create new virtual environment
- The only third-party dependency is pydantic. Install in your environment with  `pip install pydantic` or using `pip install -r requirements.txt`

Code was tested under Linux and Windows, but should also support MacOS


## Run the Game

Just run `python main.py` and enjoy a nice round of classic Rock, Paper, Scissors or its nerdy variant including Lizard and Spock!

## Configuring and exending the Game
The basic game config can be found in `data/gameconf.json` select the supported game variants and AI algorithm here.

The game's variants, movesets, and rulesets are implemented in a data-driven manner. You can change the rules or add new moves, rules, or game variants in `data/moves.json` or `data/rules.json`, respectively. 

