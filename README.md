# Clever Word Guessing Game

## Overview
A Python "Guess the Word" game where the user tries to reveal a secret word one letter at a time before running out of misses.

## Files
- **GuessWord.py** – Main game file  
- **lowerwords.txt** – Word list  
- **CheckMyFunctions.py** – Function tester  

## Setup
1. Download and unzip the project.  
2. In PyCharm, select **File > Open…** and choose the unzipped folder.  
3. Run **GuessWord.py** to start the game.  

## Gameplay
- Choose difficulty: **Easy (e)** = 12 misses, **Hard (h)** = 8 misses.  
- A random 5–10 letter word is selected from *lowerwords.txt*.  
- Guessed letters (correct and missed) are shown in sorted order.  
- Correct guesses don’t reduce misses; repeated guesses are ignored.  
- The game ends when the word is guessed or misses run out.  

After each game, statistics are shown for guesses and misses. The player can choose to play again. When the player quits, overall win/loss totals for the session are displayed.

