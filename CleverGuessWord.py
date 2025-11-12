"""
Created on 11/12/25

@author: natalielai
"""
import random


def handleUserInputDifficulty():
    """
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the
    corresponding number of misses allowed for the game.
    """
    print("How many misses do you want? Hard has 8 and Easy has 12.")
    level = input("(h)ard or (e)asy> ")
    if level == "h":
        value = 8
    else:
        value = 12
    return value


def handleUserInputLetterGuess(lettersGuessed, displayString):
    """
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    """
    print(displayString)
    let = input("letter> ")
    while let in lettersGuessed:
        print("you already guessed that")
        let = input("letter> ")
    return let


def createDisplayString(lettersGuessed, missesLeft, guessedWordAsList):
    """
    Creates the string that will be displayed to the user, using the information in the parameters.
    Shows letters NOT yet guessed.
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    retString = "letters not yet guessed: "
    unguessedWord = ""

    for let in alphabet:
        if let in lettersGuessed:
            unguessedWord += " "
        else:
            unguessedWord += let

    retString += unguessedWord + "\n"
    retString += "misses remaining = " + str(missesLeft) + "\n"
    retString += " ".join(guessedWordAsList)

    return retString

def handleUserInputDebugMode():
    """
    Asks user if they want to play in debug mode.
    Returns True for debug mode, False otherwise.
    """
    mode = input("Which mode do you want: (d)ebug or (p)lay: ")
    if mode == "d":
        return True
    else:
        return False


def handleUserInputWordLength():
    """
    Asks user how long the secret word should be.
    Returns the length as an integer.
    """
    answer = input("How many letters in the word you'll guess: ")
    secretWordlength = int(answer)
    return secretWordlength


def createTemplate(currTemplate, letterGuess, word):
    """
    Creates a new template based on current template, letter guessed, and the word.
    """
    output = ""
    for i in range(len(word)):
        if currTemplate[i] != "_":
            output += currTemplate[i]
        elif word[i] == letterGuess:
            output += letterGuess
        else:
            output += "_"
    return output


def getNewWordList(currTemplate, letterGuess, wordList, debug):
    """
    Creates a dictionary mapping templates to words that fit them based on letterGuess,
    and returns the template with the largest word list. If tied, pick template with most underscores.
    """
    templateDict = {}

    # Build the dictionary
    for word in wordList:
        newTemplate = createTemplate(currTemplate, letterGuess, word)
        if newTemplate not in templateDict:
            templateDict[newTemplate] = []
        templateDict[newTemplate].append(word)

    # Print debug info if needed
    if debug:
        sortedTemplates = sorted(templateDict.keys())
        for template in sortedTemplates:
            print(f"{template} : {len(templateDict[template])}")
        print(f"# keys = {len(templateDict)}")

    # Find the template with largest list (break ties with most underscores)
    bestTemplate = None
    largestList = []
    maxUnderscores = -1

    for template, words in templateDict.items():
        if len(words) > len(largestList):
            bestTemplate = template
            largestList = words
            maxUnderscores = template.count('_')
        elif len(words) == len(largestList):
            underscores = template.count('_')
            if underscores > maxUnderscores:
                bestTemplate = template
                largestList = words
                maxUnderscores = underscores

    return (bestTemplate, largestList)


def processUserGuessClever(guessedLetter, guessedWordAsList, missesLeft):
    """
    Updates missesLeft based on whether guessedLetter appears in guessedWordAsList.
    Returns [updatedMissesLeft, correctGuessBool]
    """
    if guessedLetter in guessedWordAsList:
        correct = True
    else:
        correct = False
        missesLeft -= 1
    return [missesLeft, correct]


def runGame(filename):
    """
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    """
    # Get user input for game settings
    debug = handleUserInputDebugMode()
    wordLength = handleUserInputWordLength()
    missesAllowed = handleUserInputDifficulty()

    # Read words from file
    f = open(filename, encoding="utf-8")
    allwords = []
    for line in f:
        for word in line.strip().split():
            allwords.append(word)
    f.close()

    # Filter words by length
    wordList = [w for w in allwords if len(w) == wordLength]

    # Initialize game state
    wordToGuess = ['_'] * wordLength
    lettersGuessed = ""
    missesLeft = missesAllowed
    playGame = True
    gameStatus = "lost"

    # Game loop
    while playGame:
        displayString = createDisplayString(lettersGuessed, missesLeft,
                                            wordToGuess)

        # Debug info
        if debug:
            if wordList:
                secretWord = random.choice(wordList)
                print(f"(word is {secretWord})")
            print(f"# possible words: {len(wordList)}")

        guessedLetter = handleUserInputLetterGuess(lettersGuessed,
                                                   displayString)

        # Get new word list and template using clever algorithm
        (newTemplate, wordList) = getNewWordList("".join(wordToGuess),
                                                 guessedLetter, wordList, debug)
        wordToGuess = list(newTemplate)

        # Process the guess
        [missesLeft, didGuessLetter] = processUserGuessClever(guessedLetter,
                                                              wordToGuess,
                                                              missesLeft)
        lettersGuessed += guessedLetter

        # Inform user of guess result
        if not didGuessLetter:
            print(f"you missed: {guessedLetter} not in word\n")
        else:
            print()

        # Check if game is won or lost
        if '_' not in wordToGuess:
            gameStatus = "won"
            playGame = False
        elif missesLeft <= 0:
            gameStatus = "lost"
            playGame = False

    # Final game result
    if gameStatus == 'won':
        secretWord = wordList[0] if wordList else "".join(wordToGuess)
        print(f"You won! The word was {''.join(wordToGuess)}")
        print(
            f"you made {len(lettersGuessed)} guesses with {missesAllowed - missesLeft} misses\n")
        return True
    else:
        secretWord = wordList[0] if wordList else "".join(wordToGuess)
        print(f"you're hung!!")
        print(f"word was {secretWord}")
        print(
            f"you made {len(lettersGuessed)} guesses with {missesAllowed - missesLeft} misses\n")
        return False

if __name__ == "__main__":
    """
    Running CleverGuessWord.py starts the game, which is done by calling runGame
    """
    playAgain = True
    wontotal = 0
    losstotal = 0

    while playAgain:
        result = runGame('lowerwords.txt')
        if result == 'won':
            wontotal += 1
        else:
            losstotal += 1
        answer = input("Do you want to play again? y or n> ")
        if answer == 'n':
            playAgain = False

    # Print stats
    print(f"You won {wontotal} game(s) and lost {losstotal}")

if __name__ == '__main__':
    """
       Running GuessWord.py starts the game, which is done by calling runGame
   """

    playAgain = True
    wontotal = 0
    losstotal = 0
    while (playAgain):
        result = runGame('lowerwords.txt')
        if result == 'won':
            wontotal += 1
        else:
            losstotal += 1
        answer = input("Would you like to play again? (y or n): ")
        if answer == 'n':
            playAgain = False
    # print stats
    if wontotal == 1:
        print("you won " + str(wontotal) + " game")
    else:
        print("you won " + str(wontotal) + " games")
    if losstotal == 1:
        print("you lost " + str(losstotal) + " game")
    else:
        print("you lost " + str(losstotal) + " games")

