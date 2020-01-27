from colorama import Fore, Style, init
import random
init()
passwordList = []

letterList = []

for i in range(65, 91):
    letterList.append(chr(i))
    passwordList.append(chr(i))
for i in range (97, 123):
    letterList.append(chr(i))
    passwordList.append(chr(i))
for i in range(10):
    passwordList.append(i)
passwordList.extend(["~", "!", "@", "#", "$", "%", "^", "&", "*", "-", "+"])
password = random.choices(passwordList, k = int(10))

for i in range(len(password)):
    if password[i] in letterList:
        print(Fore.BLUE + "", password[i], sep = "", end = "")
    elif password[i] in range(10):
        print(Fore.GREEN + "", password[i], sep = "", end = "")
    elif password[i] in ["~", "!", "@", "#", "$", "%", "^", "&", "*", "-", "+"]:
        print(Fore.RED + "", password[i], sep = "", end = "")