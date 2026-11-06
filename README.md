# texas-holdem-pygame

A "Diamond Casino" version of Ultimate Texas Hold'em made with pygame, for 1 to 3 players on the same computer. Made in March 2026 as a personal project while learning Python, after the course exercises.

## What it does
- Setup screens for number of players, names and starting chips
- Ante / blind, optional Trips side bet, then pre-flop (raise x3 or x4), flop (raise x2) and river (call x1 or fold)
- Dealer must have at least a pair to qualify
- Hand evaluation of the best 5 cards out of 7 (royal flush down to high card)
- Payout table and leaderboard screens, players are eliminated under $20

## Stack
Python 3 and pygame. It is a single file, `pygame_main.py` (window 1400x800).

## How to run
```
pip install -r requirements.txt
python3 pygame_main.py
```
The card suits use a system font with symbols (Apple Symbols, Segoe UI Symbol, DejaVu Sans...), on some systems they can look a bit different.

## What it shows about learning
Classes and enums, dictionaries for the players, a state machine (GameState) for the game flow, drawing with pygame, and a simple hand evaluator with `itertools.combinations`.

## Known issues
- Everything is in one file and the window is created when the file is imported.
- The rules are simplified compared to the real casino game.
