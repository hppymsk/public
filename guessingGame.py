#!/usr/bin/env python3

#Author: Josh Albertson
#This program is a guessing game that prompts the user to guess a number in a range with increasing levels of difficulty

import random
from colorama import Fore, init

#Global variable to save the players highest level in a session
highestLevel = 1

#game initilization function, this function takes the level argument and then initializes
#the upper range of numbers, max guesses and a new winning number based on the current level
#then sends these values to the gameLoop function as arguments.
def playGame(level):
    
    currentLevel = level
    global highestLevel

    if highestLevel < currentLevel: 
        highestLevel = currentLevel
    
    upperRange = (currentLevel + 1) * 5
    maxGuesses = (11 - currentLevel)
    print(Fore.BLUE + "Level " , currentLevel , ": Guess between 1 and " , upperRange , ". You have " , maxGuesses , " Guesses.", sep = "")
    while True:
        winningNum = random.randrange(1, upperRange)
        
        result = gameLoop(winningNum, maxGuesses, upperRange)
        
        if result == True:
            currentLevel += 1
            playGame(currentLevel)
        else:
            print(Fore.RED + "Game over. Your highest level is " , highestLevel , ". Try Again? (Y/N): " , sep = "" , end = "")
            tryAgain = input()
            if tryAgain.upper() in ('Y', 'YES', 'OK', 'SURE'):
                playGame(1)
            else:
                print(Fore.GREEN + "Thanks for playing!")
                break
        break

#main game loop, takes arguments for the winning number, max guesses and upper range for the level
def gameLoop(winningNum, maxGuesses, upperRange):  
    guesses = 0
    while True:
        guesses += 1
        
        #checks if the player has any guesses remaining then returns the False value if they don't
        if guesses > maxGuesses:
            print (Fore.BLUE + "You have run out of guesses. Unlucky!")
            return False
        
        #Input validation
        while True:            
            
            print(Fore.WHITE + "Enter your guess: " , end = "")
            playerGuess = input()
            
            try:
                playerGuess = int(playerGuess)
            except:
                print(Fore.RED + "Invalid input.")
                continue
            if playerGuess not in range(upperRange + 1) or playerGuess == 0:
                print(Fore.RED + "Input an integer between 1 and", upperRange)
            else:
                break

        #loops through guesses until the player either guesses the correct number or runs out of guesses, then returns
        #the True value if the player wins the game.           
        if playerGuess > winningNum:
            print(Fore.RED + "Your guess is too high.", (maxGuesses - guesses), "guesses left.")
        elif playerGuess < winningNum:
            print (Fore.RED + "Your guess is too low.", (maxGuesses - guesses), "guesses left.")
        else:
            if guesses == 1:
                print(Fore.GREEN + "Hole in one! You guessed right on the first try.")
            else:
                print(Fore.GREEN + "You guessed correctly! The right number was" , winningNum, "and it took", guesses , "guesses.")
            return True

#Main function
def main():

    playGame(1)

if __name__ == "__main__":
    init()
    main()
