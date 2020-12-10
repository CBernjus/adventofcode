# ---------------------------
# Advent of Code 2020 - Day 1
# Part 1: Report Repair
# ---------------------------

# After saving Christmas five years in a row, you've decided to take a
# vacation at a nice resort on a tropical island. Surely, Christmas will go
# on without you.

# The tropical island has its own currency and is entirely cash-only. The
# gold coins used there have a little picture of a starfish; the locals just
# call them stars. None of the currency exchanges seem to have heard of them,
# but somehow, you'll need to find fifty of these coins by the time you
# arrive so you can pay the deposit on your room.

# To save your vacation, you need to get all fifty stars by December 25th.

# Collect stars by solving puzzles. Two puzzles will be made available on
# each day in the Advent calendar; the second puzzle is unlocked when you
# complete the first. Each puzzle grants one star. Good luck!

# Before you leave, the Elves in accounting just need you to fix your expense
# report (your puzzle input); apparently, something isn't quite adding up.

# Specifically, they need you to find the two entries that sum to 2020 and
# then multiply those two numbers together.

# For example, suppose your expense report contained the following:

# 1721 979 366 299 675 1456

# In this list, the two entries that sum to 2020 are 1721 and 299.
# Multiplying them together produces 1721 * 299 = 514579, so the correct
# answer is 514579.

# Of course, your expense report is much larger. Find the two entries that
# sum to 2020; what do you get if you multiply them together?

import os

f = open(os.path.dirname(__file__) + "/../inputs/input_1.txt")

inputArr = sorted(map(int, f.read().split()))

def get_two_summands(arr, target):
    for i in range(len(inputArr)):
        for j in range(len(inputArr) - 1, i, -1):
            sum = inputArr[i] + inputArr[j]
            if(sum > target):
                continue
            elif(sum < target):
                break
            else:
                return [inputArr[i], inputArr[j]]
    raise Exception("There are no two numbers which add up to " + str(target))

def get_two_summands_efficiently(arr, target):
    arrSet = set(arr)
    
    for i in arr:
        if target - i in arrSet:
            return [i, target - i]

    raise Exception("There are no two numbers which add up to " + str(target))

print("2020 - Day 1 - Part 1")
try:
    #[a, b] = get_two_summands(inputArr, 2020)
    [a, b] = get_two_summands_efficiently(inputArr, 2020)
    print(a, "*", b, "=", a * b)
except Exception as e:
    print(str(e))

# => 647 * 1373 = 888331
#                 ======


# ---------------------------
# Advent of Code 2020 - Day 1
# Part 2: Report Repair
# ---------------------------

# The Elves in accounting are thankful for your help; one of them even offers
# you a starfish coin they had left over from a past vacation. They offer you
# a second one if you can find three numbers in your expense report that meet
# the same criteria.

# Using the above example again, the three entries that sum to 2020 are 979,
# 366, and 675. Multiplying them together produces the answer, 241861950.

# In your expense report, what is the product of the three entries that sum
# to 2020?

def get_three_summands(arr, target):
    # don't allow 0, x, y as a solution
    for i in range(len(arr) - 1, 0, -1):
        try:
            c = arr[i]
            #[a, b] = get_two_summands(arr, target - c)
            [a, b] = get_two_summands_efficiently(arr, target - c)
            if(a + b + c == 2020):
                return [a, b, c]
            else:
                raise Exception("There are no three numbers which add up to " + str(target))
        except:
            continue

print("\n2020 - Day 1 - Part 2")
try:
    [a, b, c] = get_three_summands(inputArr, 2020)
    print(a, "*", b, "*", c, "=", a * b * c)
except Exception as e:
    print(str(e))

# => 195 * 511 * 1314 = 130933530
#                       =========