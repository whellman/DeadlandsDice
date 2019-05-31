# Initial thoughts:
# Deadlands dice are not well-served by existing dice apps.
# High level description of deadlands style dice:
#   Skill rolls are done with a pool of dice; this pool contains a certain
#      number of member dice, and each member is a certain sidedness.
#   When you roll a skill roll, you roll the entire pool of dice.
#   Your skill roll result is the single highest dice roll within this pool.
#   Since you only take one result, the purpose of rolling many dice rather
#       than one die is to increase the chances of rolling the number you need.
#   There are two additional mechanics that need to be taken into account:
#       Exploding Dice
#           If a die rolls its highest possible value, that's an "ace" and the
#               die "explodes" (generic dice term, not deadlands term). This
#               means that you roll one additional dice, and in the final tally
#               its value will be added to the dice that originated it with an
#               ace.
#               This process is recursive. E.g.: I roll 2d6. In this pool of two
#                   dice, say one rolls a 2 and the other rolls a 6. That is an
#                   "ace" so we roll another d6 into the existing roll-pool (or,
#                   in real-world game terms, into the dice tray) and, when it
#                   comes time to tally the dice and find the so-called "single
#                   highest die roll" we add the result of the new dice we roll
#                   into the value of the original ace that exploded. So say the
#                   new dice also rolls a 6, and therefore it also explodes. One
#                   more additional dice is rolled, and say it results in a 3.
#                   For the final result, then, we have to evaluate "each" dice
#                   in the original pool, which means tracking their explosions
#                   as well.
#                   So the choices to pick from for "highest single result" of
#                       our roll, nominally, of 2d6, are the following two
#                       options:
#                       (1)  2. This was what one of the original dice rolled.
#                       (2)  6+6+3, or 15.  We take the value of the die rolled,
#                           plus the value of its explosion roll. Its explosion
#                           roll's value is the value of the die roll, plus the
#                           value of its explosion roll. 6+(6+(3))
#       Going Bust
#           Somewhat controversial, sort of, in that there are at least two
#               interpretations of how this works floating around out there,
#               both supported, in some degree, by even the most recent reprints
#               of this notoriously typo-filled game.
#           Going Bust is the equivalent of a critical failure in a game like
#               D&D or Call of Cthulhu etc, where you are only rolling one die
#               (a d20 or d100 [virtualized via 2d10] respectively). In that
#               other style of system, a critical failure would be a result of
#               1 or 001: the absolute worst possible result of the roll.
#           Because Deadlands Classic uses a pool of dice from which a "single"
#               result is selected, it wouldn't make sense to allow one bad die
#               to overpower several good dice. Therefore, the critical failure state
#               is obtained when--depending on the interpretation being used--
#               50% or >50% of the dice come up as 1.
#
#               FIXME: Cite pages from most recent version to support each
#                   interpretation. Also probably compare the Savage Worlds
#                   mechanic, if it exists.
#
#           We want to somehow allow for the user to pick from both
#               interpretations.  Either way, we'll have to keep track of how
#               many dice roll a 1 and compare that to the total number of dice
#               rolled.
#
#   Implementation ideas.
#   Good idea would be to implement this as a class that evaluates results of
#   abstract rolls, so that we can pass in different roll systems--such as pure
#   RNG for an initial text-based version, or some kind of elaborate Unity engine
#   physics-derived pseudoreal roll of a dice model.

import readline
import random
import re

from colorama import Fore
from colorama import Style

from enum import Enum
class ValidDice(Enum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12

def rollDice(sides):
    result = random.randint(1, sides)
    if(result == sides):
        result += rollDice(sides)
    return result

#main loop
while True:
    userString = input("Enter dice expression: ")

    m = re.fullmatch(r"^(\d{,3})[dD](\d{1,2})$", userString)

    numberOfDice = int(m.group(1))
    sidednessOfDice = int(m.group(2))

    biggest = 0

    for poolMember in range(numberOfDice):
        result = rollDice(sidednessOfDice)
        if(result > sidednessOfDice):
            print("Roll " + str(poolMember+1) + ": " + Fore.GREEN + str(result) + Style.RESET_ALL)
        else:
            print("Roll " + str(poolMember+1) + ": " + str(result))
        if(result > biggest):
            biggest = result

    print(Fore.RED + "Final skill roll result: " + str(biggest) + Style.RESET_ALL)
