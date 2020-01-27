#!/usr/bin/env python3

#Author: Josh Albertson
#Date: 26-JAN-2020
#Description: Generates 5 passwords with various options

import random
from colorama import Fore, Style, init
init()

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

#Prompts user to select options for their password generation
def userOptions():

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
    print(Fore.WHITE + "Include " + Fore.BLUE + "letters" + Fore.WHITE + " in the password? (Y/N): " , sep = "", end = "")
    if validateInput(input(), "", ["y", "Y", "yes", "YES"]):
        lettersBool = True
    else:
        lettersBool = False
    
    #Include numbers (Y/N)
    print(Fore.WHITE + "Include " + Fore.GREEN + "numbers" + Fore.WHITE + " in the password? (Y/N): " , sep = "", end = "")
    if validateInput(input(), "", ["y", "Y", "yes", "YES"]):
        numbersBool = True
    else:
        numbersBool = False
    
    #Include symbols (Y/N)
    print(Fore.WHITE + "Include " + Fore.RED + "symbols" + Fore.WHITE + " in the password? (Y/N): " , sep = "", end = "")
    if validateInput(input(), "", ["y", "Y", "yes", "YES"]):
        symbolsBool = True
    else:
        symbolsBool = False

    if not any([lettersBool, numbersBool, symbolsBool]):
        print(Fore.RED + "You need to select at least one option.")
        userOptions()
    else:
        generatePassword(int(pwdLength), lettersBool, numbersBool, symbolsBool)

#Generates a list of characters to be used in password generation based on options selected
def generatePassword(pwdLength, lettersBool, numbersBool, symbolsBool):
    
    passwordList = []
    letterList = []

    #Generate lists of characters
    if lettersBool:
        for i in range(65, 91):
            letterList.append(chr(i))
            passwordList.append(chr(i))
        for i in range (97, 123):
            letterList.append(chr(i))
            passwordList.append(chr(i))
    if numbersBool:
        for i in range(10):
            passwordList.append(i)
    if symbolsBool:
        passwordList.extend(["~", "!", "@", "#", "$", "%", "^", "&", "*", "-", "+"])
    
    #Generates and prints 5 passwords
    for i in range(5):
        password = random.choices(passwordList, k = int(pwdLength))
        print(Fore.WHITE + "" , (i + 1), ": ", sep = "", end = "")
        printPassword(password, letterList)
    
    print(Fore.WHITE + "Go again? (Y/N): ", end = "")
    if validateInput(input(), "", ["y", "Y", "yes", "YES"]):
        userOptions()
    else:
        quit

#Prints passwords with color coding based on character type
def printPassword(password, letterList):
    for i in range(len(password)):
        if password[i] in letterList:
            print(Fore.BLUE + "" , password[i], sep = "", end = "")
        elif password[i] in range(10):
            print(Fore.GREEN + "" , password[i], sep = "", end = "")
        elif password[i] in ["~", "!", "@", "#", "$", "%", "^", "&", "*", "-", "+"]:
            print(Fore.RED + "" , password[i], sep = "", end = "")
    print('\n')

def main():
    userOptions()

if __name__ == "__main__":
    main()