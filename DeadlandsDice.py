import readline
import random
import re

from colorama import Fore
from colorama import Style

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--halfbust", help="going bust merely requires 50% of dice")
args = parser.parse_args()
if args.halfbust:
    useGreaterOrEqual = True
else:
    useGreaterOrEqual = False

from enum import Enum
class ValidDice(Enum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12

class TargetNumbers(Enum):
    Foolproof = 3
    Fair = 5
    Onerous = 7
    Hard = 9
    Incredible = 11



def rollDice(sides):
    result = random.randint(1, sides)
    if(result == sides):
        result += rollDice(sides)
    return result

#main loop
while True:
    userString = input("Enter dice expression: ")
    if(re.fullmatch(r"^quit$", userString)):
        break
    m = re.fullmatch(r"^(\d{,3})[dD](\d{1,2})$", userString)

    try:
        numberOfDice = int(m.group(1))
        sidednessOfDice = int(m.group(2))
    except AttributeError:
        continue

    biggest = 0
    onesCount = 0

    for poolMember in range(numberOfDice):
        result = rollDice(sidednessOfDice)
        if(result > sidednessOfDice):
            print("Roll " + str(poolMember+1) + ": " + Fore.GREEN + str(result) + Style.RESET_ALL)
        else:
            if(result == 1):
                onesCount += 1
            print("Roll " + str(poolMember+1) + ": " + str(result))
        if(result > biggest):
            biggest = result

    if(useGreaterOrEqual):
        evalResult = (onesCount >= (numberOfDice/2))
    else:
        evalResult = (onesCount > (numberOfDice/2))

    if(evalResult):
        print(Fore.RED + "!!!  BUST  !!!" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "Final skill roll result: " + str(biggest) + Style.RESET_ALL)
