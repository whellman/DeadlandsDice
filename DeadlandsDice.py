import readline
import random
import re

from colorama import init
init()

from colorama import Fore, Style

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--halfbust", help="going bust merely requires 50%% of dice", action='store_true')
parser.add_argument("--verbose", help="display full roll series for aces", action='store_true')

args = parser.parse_args()

if args.halfbust:
    useGreaterOrEqual = True
else:
    useGreaterOrEqual = False
if args.verbose:
    verbose = True
else:
    verbose = False

# These aren't used yet because nonstandard dice are useful for testing.
from enum import Enum
class ValidDice(Enum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

# This should be used in the future to automatically describe the success of
# the roll and the number of raises, if any, for different TN difficulties.
class TargetNumbers(Enum):
    FOOLPROOF = 3
    FAIR = 5
    ONEROUS = 7
    HARD = 9
    INCREDIBLE = 11
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

# FIXME: This isn't ideal. The most important part of this line for configuring
# is the word wedged between the periods in the middle of the expression.
# Previously, the value was tacked on whenever it was needed to grab the tn as int,
# but the ability to input an arbitrary tn required a change...
tn = TargetNumbers.FAIR.value

def rollDice(sides):
    result = random.randint(1, sides)
    if(result == sides):
        result += rollDice(sides)
    return result

print("Enter 'quit' in dice expression prompt to stop")
#main loop
while True:
    userString = input("Enter dice expression: ")
    if(re.fullmatch(r"^quit$", userString)):
        break
    # The following is extremely clunky.
    # FIXME: don't do this in a way that doubles up on the match testing.
    if(re.fullmatch(r"^tn\s*(\d{1,2})$", userString)):
        m = re.fullmatch(r"^tn\s*(\d{1,2})$", userString)
        tn = int(m.group(1))
        print("Target number set to " + str(tn))
        continue
    m = re.fullmatch(r"^(\d{,3})[dD](\d{1,2})$", userString)

    try:
        numberOfDice = int(m.group(1))
    except AttributeError as ae:
        # print("Bad input: " + str(ae))
        continue
    except ValueError:
        numberOfDice = 1
        pass

    try:
        sidednessOfDice = int(m.group(2))
        if not ValidDice.has_value(sidednessOfDice):
            raise AttributeError('Not a valid sidedness of dice!')
    except AttributeError as ae:
        print("Bad input: " + str(ae))
        continue

    biggest = 0
    onesCount = 0

    for poolMember in range(numberOfDice):
        result = rollDice(sidednessOfDice)
        if(result > sidednessOfDice):
            expandedRoll = ""
            if verbose:
                acesAndRemainder = divmod(result, sidednessOfDice)
                for i in range(acesAndRemainder[0]):
                    expandedRoll += (str(sidednessOfDice) + " + ")
                expandedRoll += (str(acesAndRemainder[1]) + " = ")
            print("Roll " + str(poolMember+1) + ": " + expandedRoll + Fore.GREEN + str(result) + Style.RESET_ALL)
        else:
            if(result == 1):
                onesCount += 1
                print("Roll " + str(poolMember+1) + ": " + Fore.RED + str(result) + Style.RESET_ALL)
            else:
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
        successAndRaise = biggest // tn
        if(successAndRaise > 2):
            print(Fore.GREEN + "A success with " + Fore.BLUE +
                  str(successAndRaise - 1) + " raises " + Fore.GREEN +
                  "for TN of " + str(tn) + Style.RESET_ALL)
        elif (successAndRaise > 1):
            print(Fore.GREEN + "A success with " + Fore.BLUE +
                  str(successAndRaise - 1) + " raise " + Fore.GREEN +
                  "for TN of " + str(tn) + Style.RESET_ALL)
        elif (successAndRaise == 1):
            print(Fore.GREEN + "A success for TN of " + str(tn) + Style.RESET_ALL)
        else:
            print(Fore.RED + "A failure for TN of " + str(tn) + Style.RESET_ALL)
