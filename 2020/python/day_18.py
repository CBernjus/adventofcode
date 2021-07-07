# ----------------------------
# Advent of Code 2020 - Day 18
# Part 1: Operation Order
# ----------------------------

# As you look out the window and notice a heavily-forested continent slowly
# appear over the horizon, you are interrupted by the child sitting next to
# you. They're curious if you could help them with their math homework.

# Unfortunately, it seems like this "math" follows different rules than you
# remember.

# The homework (your puzzle input) consists of a series of expressions that
# consist of addition (+), multiplication (*), and parentheses ((...)). Just
# like normal math, parentheses indicate that the expression inside must be
# evaluated before it can be used by the surrounding expression. Addition
# still finds the sum of the numbers on both sides of the operator, and
# multiplication still finds the product.

# However, the rules of operator precedence have changed. Rather than
# evaluating multiplication before addition, the operators have the same
# precedence, and are evaluated left-to-right regardless of the order in
# which they appear.

# For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are
# as follows:

# 1 + 2 * 3 + 4 * 5 + 6
#   3   * 3 + 4 * 5 + 6
#       9   + 4 * 5 + 6
#          13   * 5 + 6
#              65   + 6
#                  71

# Parentheses can override this order; for example, here is what happens if
# parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):

# 1 + (2 * 3) + (4 * (5 + 6))
# 1 +    6    + (4 * (5 + 6))
#      7      + (4 * (5 + 6))
#      7      + (4 *   11   )
#      7      +     44
#             51
# Here are a few more examples:

# 2 * 3 + (4 * 5) becomes 26.
# 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
# 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.

# Before you can help with the homework, you need to understand it yourself.
# Evaluate the expression on each line of the homework; what is the sum of
# the resulting values?

import os
from typing import List, Tuple


def read_input(f):
    return f.read().replace('(', '( ').replace(')', ' )').split('\n')


def calculate1(tokens: List[str]) -> str:
    total = tokens.pop(0)
    for operator, number in zip(tokens[0::2], tokens[1::2]):
        total = str(eval(total + operator + number))
    return total


def find_parens(tokens: List[str]) -> List[Tuple[int, int, int]]:
    indices = []
    openParens = 0
    currParens = []
    parens = []

    for i, char in enumerate(tokens):
        if char == '(':
            openParens += 1
            indices.append(i)
        if char == ')':
            end = i - sum(map(lambda p: p[2] - p[1],
                              filter(lambda p: p[0] > openParens, currParens)))
            currParens.append((openParens, indices.pop(), end))
            openParens -= 1
            if openParens == 0:
                parens.extend(sorted(currParens, key=lambda paren: paren[0]))
                currParens = []

    return parens


def evaluate1(line: str) -> int:
    tokens = line.split(' ')
    parens = find_parens(tokens)

    while len(parens) != 0:
        _, start, end = parens.pop()
        total = calculate1(tokens[start + 1:end])
        tokens = tokens[:start] + [total] + tokens[end + 1:]

    return int(calculate1(tokens))


with open(os.path.dirname(__file__) + "/../inputs/input_18.txt") as f:
    lines = read_input(f)
    print("2020 - Day 18 - Part 1")
    print(sum(evaluate1(line) for line in lines))
    # => 30753705453324
    #    ==============
