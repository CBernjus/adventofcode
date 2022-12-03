# ---------------------------
# Advent of Code 2022 - Day 2
# Part 1: Rock Paper Scissors
# ---------------------------

# The Elves begin to set up camp on the beach. To decide whose tent gets to
# be closest to the snack storage, a giant Rock Paper Scissors tournament is
# already in progress.

# Rock Paper Scissors is a game between two players. Each game contains many
# rounds; in each round, the players each simultaneously choose one of Rock,
# Paper, or Scissors using a hand shape. Then, a winner for that round is
# selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats
# Rock. If both players choose the same shape, the round instead ends in a
# draw.

# Appreciative of your help yesterday, one Elf gives you an encrypted
# strategy guide (your puzzle input) that they say will be sure to help you
# win. "The first column is what your opponent is going to play: A for Rock,
# B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is
# called away to help with someone's tent.

# The second column, you reason, must be what you should play in response: X
# for Rock, Y for Paper, and Z for Scissors. Winning every time would be
# suspicious, so the responses must have been carefully chosen.

# The winner of the whole tournament is the player with the highest score.
# Your total score is the sum of your scores for each round. The score for a
# single round is the score for the shape you selected (1 for Rock, 2 for
# Paper, and 3 for Scissors) plus the score for the outcome of the round (0
# if you lost, 3 if the round was a draw, and 6 if you won).

# Since you can't be sure if the Elf is trying to help you or trick you, you
# should calculate the score you would get if you were to follow the strategy
# guide.

# For example, suppose you were given the following strategy guide:

# A Y
# B X
# C Z

# This strategy guide predicts and recommends the following:

# - In the first round, your opponent will choose Rock (A), and you should
#   choose Paper (Y). This ends in a win for you with a score of 8 (2 because
#   you chose Paper + 6 because you won).
# - In the second round, your opponent will choose Paper (B), and you should
#   choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
# - The third round is a draw with both players choosing Scissors, giving you
#   a score of 3 + 3 = 6.
# - In this example, if you were to follow the strategy guide, you would get
#   a total score of 15 (8 + 1 + 6).

# What would your total score be if everything goes exactly according to your strategy guide?

from __future__ import annotations

import logging as log
import os
from typing import TextIO, List, Tuple, Mapping

# log.basicConfig(level=log.DEBUG, format='[%(levelname)s] %(message)s')
log.basicConfig(level=log.INFO, format='[%(levelname)s] %(message)s')


def get_hand_value(hand: str) -> int:
    match hand:
        case 'A' | 'X':
            return 1
        case 'B' | 'Y':
            return 2
        case 'C' | 'Z':
            return 3


def you_win(opponents_value: int, your_value: int) -> bool:
    # edge cases: rock defeats scissors
    opponents_value += 3 if opponents_value == 1 and your_value == 3 else 0
    your_value += 3 if opponents_value == 3 and your_value == 1 else 0
    return your_value > opponents_value


def is_draw(opponents_value: int, your_value: int) -> bool:
    return your_value == opponents_value


def get_winning_score(opponents_hand: str, your_hand: str) -> int:
    opponents_value = get_hand_value(opponents_hand)
    your_value = get_hand_value(your_hand)
    if is_draw(opponents_value, your_value):
        log.debug(f"opponent: {opponents_value}, you: {your_value} => DRAW (3) => {your_value + 3}")
        return 3
    if you_win(opponents_value, your_value):
        log.debug(f"opponent: {opponents_value}, you: {your_value} => WIN  (6) => {your_value + 6}")
        return 6
    log.debug(f"opponent: {opponents_value}, you: {your_value} => LOST (0) => {your_value}")
    return 0


def calc_score(hands: Tuple[str, str]) -> int:
    opponents_hand, your_hand = hands
    return get_hand_value(your_hand) + get_winning_score(opponents_hand, your_hand)


def list_play_guide(file: TextIO) -> List[Tuple[str, str]]:
    return list(map(lambda line: tuple(line.split()), file.read().split('\n')))


# with open(os.path.dirname(__file__) + "/../examples/example_2.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_2.txt") as f:
    play_guide = list_play_guide(f)
    log.debug(play_guide)
    play_scores = list(map(calc_score, play_guide))
    log.debug(play_scores)

    log.info("2022 - Day X - Part 1")
    log.info("What would your total score be if everything goes exactly according to your strategy guide?")
    log.info(sum(play_scores))
    # => 12794
    #    =====

print()

# ---------------------------
# Advent of Code 2022 - Day 2
# Part 2: Rock Paper Scissors
# ---------------------------

# The Elf finishes helping with the tent and sneaks back over to you.
# "Anyway, the second column says how the round needs to end: X means you
# need to lose, Y means you need to end the round in a draw, and Z means you
# need to win. Good luck!"

# The total score is still calculated in the same way, but now you need to
# figure out what shape to choose so the round ends as indicated. The example
# above now goes like this:

# - In the first round, your opponent will choose Rock (A), and you need the
#   round to end in a draw (Y), so you also choose Rock. This gives you a
#   score of 1 + 3 = 4.
# - In the second round, your opponent will choose Paper (B), and you choose
#   Rock, so you lose (X) with a score of 1 + 0 = 1.
# - In the third round, you will defeat your opponent's Scissors with Rock
#   for a score of 1 + 6 = 7.

# Now that you're correctly decrypting the ultra top secret strategy guide,
# you would get a total score of 12.

# Following the Elf's instructions for the second column, what would your
# total score be if everything goes exactly according to your strategy guide?

NEEDED_HANDS: Mapping[Tuple[str, str], str] = {
    ('A', 'X'): 'Z',
    ('A', 'Y'): 'X',
    ('A', 'Z'): 'Y',
    ('B', 'X'): 'X',
    ('B', 'Y'): 'Y',
    ('B', 'Z'): 'Z',
    ('C', 'X'): 'Y',
    ('C', 'Y'): 'Z',
    ('C', 'Z'): 'X'
}

OUTCOME_STR = {
    'X': 'LOSE',
    'Y': 'DRAW',
    'Z': 'WIN '
}


def deduce_hand(opponents_hand: str, outcome: str) -> str:
    return NEEDED_HANDS[(opponents_hand, outcome)]


def deduce_score(data: Tuple[str, str]) -> int:
    opponents_hand, outcome = data
    your_hand = deduce_hand(opponents_hand, outcome)
    log.debug(f"opponent: {opponents_hand}, you need a {OUTCOME_STR[outcome]} => you: {your_hand}")
    return get_hand_value(your_hand) + get_winning_score(opponents_hand, your_hand)


# with open(os.path.dirname(__file__) + "/../examples/example_2.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_2.txt") as f:
    play_guide = list_play_guide(f)
    hand_values = list(map(deduce_score, play_guide))

    log.info("2022 - Day X - Part 2")
    log.info("What would your total score be if everything goes exactly according to your strategy guide")
    log.info(sum(hand_values))
    # => 14979
    #    =====
