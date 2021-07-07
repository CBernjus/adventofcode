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


# ----------------------------
# Advent of Code 2020 - Day 18
# Part 2: Operation Order
# ----------------------------

# You manage to answer the child's questions and they finish part 1 of their
# homework, but get stuck when they reach the next section: advanced math.

# Now, addition and multiplication have different precedence levels, but
# they're not the ones you're familiar with. Instead, addition is evaluated
# before multiplication.

# For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are
# now as follows:

# 1 + 2 * 3 + 4 * 5 + 6
#   3   * 3 + 4 * 5 + 6
#   3   *   7   * 5 + 6
#   3   *   7   *  11
#      21       *  11
#          231
# Here are the other examples from above:

# 1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
# 2 * 3 + (4 * 5) becomes 46.
# 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
# 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.

# What do you get if you add up the results of evaluating the homework
# problems using these new rules?

def calculate2(tokens: List[str]) -> str:
    # print(tokens)
    equation = ""
    num1 = tokens.pop(0)
    operators = list(zip(tokens[0::2], tokens[1::2]))
    for i, (operator, num2) in enumerate(operators):
        # print('bef', i, len(operators), repr(equation), num1, operator, num2)
        if operator == '+':
            num1 = str(eval(num1 + operator + num2))
        if operator == '*':
            equation += num1 + '*'
            num1 = num2
        if i == len(operators) - 1:
            equation += num1
        # print('aft', i, len(operators), repr(equation), num1, operator, num2, '\n')

    return str(eval(equation))


def evaluate2(line: str) -> int:
    # print(line)
    tokens = line.split(' ')
    parens = find_parens(tokens)

    while len(parens) != 0:
        _, start, end = parens.pop()
        total = calculate2(tokens[start + 1:end])
        tokens = tokens[:start] + [total] + tokens[end + 1:]

    return int(calculate2(tokens))


with open(os.path.dirname(__file__) + "/../inputs/input_18.txt") as f:
    lines = read_input(f)
    print("2020 - Day 18 - Part 2")
    print(sum(evaluate2(line) for line in lines))
    # => 244817530095503
    #    ===============
