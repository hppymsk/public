#!/usr/bin/env python3

#Author: Josh Albertson
#Date: 26-JAN-2020
#Description: Generates a password

import random
from colorama import Fore, init

#Validates input based on type and range
#inputValue  (any data type): any value
#inputType          (string): either "int" or "str"
#inputRange    (range/array): defines valid range of inputs

def validateInput(inputValue, inputType, inputRange):
    
    if (inputType == "int"):
        try:
            inputValue = int(inputValue)
        except:
            return False
        if (inputValue in inputRange and inputType is not None):
            return True
        else:
            return False
    else:
        if (inputValue in inputRange):
            return True
        else:
            return False

def userOptions():
    #select options
    print(Fore.BLUE + """
    Password Generator
    ------------------
    """)
    
    #Choose length (4-300)
    while True:
        print(Fore.WHITE + "Choose a Password Length (4-300): " , end = "")
        userInput = input()
        if validateInput(userInput, "int", range(4, 301)):
            pwdLength = userInput
            break
        else:
            print(Fore.RED + "Type an integer between 4 and 300.")

    #Include letters (Y/N)
    print(Fore.WHITE + "Include letters in the password? (Y/N): " , end = "")
    userInput = input()
    if validateInput(userInput, "", ["y", "Y", "yes", "YES"]):
        lettersBool = True
    else:
        lettersBool = False
    
    #Include numbers (Y/N)
    print(Fore.WHITE + "Include numbers in the password? (Y/N): " , end = "")
    userInput = input()
    if validateInput(userInput, "", ["y", "Y", "yes", "YES"]):
        numbersBool = True
    else:
        numbersBool = False
    
    #Include symbols (Y/N)
    print(Fore.WHITE + "Include symbols in the password? (Y/N): " , end = "")
    userInput = input()
    if validateInput(userInput, "", ["y", "Y", "yes", "YES"]):
        symbolsBool = True
    else:
        symbolsBool = False

    print(generatePassword(int(pwdLength), lettersBool, numbersBool, symbolsBool))

def generatePassword(pwdLength, lettersBool, numbersBool, symbolsBool):
    
    passwordList = []

    #Generate lists of characters
    if lettersBool:
        for i in range(65, 91):
            passwordList.append(chr(i))
        for i in range (97, 123):
            passwordList.append(chr(i))
    if numbersBool:
        for i in range(10):
            passwordList.append(i)
    if symbolsBool:
        passwordList.extend(["~", "!", "@", "#", "$", "%", "^", "&", "*", "-", "+"])
    
    #return passwordList
    return random.choices(passwordList, k = pwdLength)


def main():
    userOptions()

if __name__ == "__main__":
    random.seed()
    init()
    main()