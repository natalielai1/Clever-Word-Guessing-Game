'''
Description:
        A guess the word game that allows the user to play and guess a secret word.
        See the assignment description for details.
    
@author: Natalie Lai
'''
import random



def handleUserInputDifficulty():
    '''
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the 
    corresponding number of misses allowed for the game. 
    '''

    print("How many misses do you want? Hard has 8 and Easy has 12.")
    level = input("(h)ard or (e)asy> ")
    num = 0
    if level=="h":
        num = 8
    else:
        num = 12
    return num  # assume easy




def getWord(words, length):
    '''
    Selects the secret word that the user must guess. 
    This is done by randomly selecting a word from words that is of length length.
    '''
    

    wordsOfLen = [w for w in words if len(w)==length]
    numwords = len(wordsOfLen)
    pos = random.randint(0,numwords-1)
    word = wordsOfLen[pos]
    return word




def createDisplayString(lettersGuessed, missesLeft, guessedWordAsList):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''

    retString = "letters you've guessed: "
    listletters = sorted(lettersGuessed)
    retString += " ".join(listletters) + "\n"
    retString += "misses remaining = " + str(missesLeft) + "\n"
    retString += " ".join(guessedWordAsList) + "\n"
    return retString




def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''

    print(displayString)
    let = input("letter to guess? > ")
    while let in lettersGuessed:
        print("you already guessed letter "+ let)
        let = input("try again. letter to guess? > ")
    return let


def updateGuessedWordAsList(guessedLetter, secretWord, guessedWordAsList):
    '''
    Updates guessedWordAsList according to whether guessedLetter is in secretWord and where in secretWord guessedLetter is in.
    '''

    for index in range(len(secretWord)):
        if secretWord[index] == guessedLetter:
            guessedWordAsList[index] = guessedLetter
    return guessedWordAsList




def processUserGuess(guessedLetter, secretWord, guessedWordAsList, missesLeft):
    '''
    Uses the information in the parameters to update the user's progress in the word game.
    '''

    guessed = True
    oldGuessedWordAsList = guessedWordAsList[:]
    guessedWordAsList = updateGuessedWordAsList(guessedLetter, secretWord, guessedWordAsList)
    if "".join(oldGuessedWordAsList) == "".join(guessedWordAsList):  # didn't guess letter
        missesLeft -= 1
        guessed = False
    return [guessedWordAsList, missesLeft, guessed]






def runGame(filename ):
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    '''

    f  = open(filename,encoding="utf-8")
    allwords = []
    for line in f:
        for word in line.strip().split():
            allwords.append(word)
    wordLength = random.randint(5, 10)
    missesAllowed = handleUserInputDifficulty()
    print("you have " + str(missesAllowed) + " guesses to guess the word\n")
    secretWord = getWord(allwords, wordLength)

    wordToGuess = ['_'] * wordLength
    lettersGuessed = ""
    missesLeft = missesAllowed
    playGame = True
    gameStatus = "lost"
    while (playGame):
        displayString = createDisplayString(lettersGuessed, missesLeft, wordToGuess)
        guessedLetter = handleUserInputLetterGuess(lettersGuessed, displayString )
        [wordToGuess, missesLeft, didGuessLetter] = processUserGuess(guessedLetter, secretWord, wordToGuess, missesLeft)
        lettersGuessed += guessedLetter

        if didGuessLetter == False:
            print("you missed: " + guessedLetter + " is not in word\n")
        if '_' not in wordToGuess:
            gameStatus = "won"
            playGame = False
        elif missesLeft <= 0:
            gameStatus = 'lost'
            playGame = False
            handleUserInputDifficulty()
    if gameStatus == 'won':
        print("You guessed the word " + secretWord)
    else:
        print("Sorry you ran out of guesses. The word was " + secretWord)
    print("you made " + str(len(lettersGuessed)) + " guesses with "+ str(missesAllowed-missesLeft) + " misses")
    return gameStatus








if __name__ == "__main__":
    '''
    Running GuessWord.py starts the game, which is done by calling runGame
    '''
    playAgain = True
    wontotal = 0
    losstotal = 0
    while(playAgain):
        result = runGame('lowerwords.txt')
        if result == 'won':
            wontotal += 1
        else:
            losstotal += 1
        answer = input("Would you like to play again? (y or n): ")
        if (answer == 'n'):
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
