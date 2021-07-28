# ----------------------------
# Advent of Code 2020 - Day 21
# Part 1: Allergen Assessment
# ----------------------------

# You reach the train's last stop and the closest you can get to your
# vacation island without getting wet. There aren't even any boats here, but
# nothing can stop you now: you build a raft. You just need a few days' worth
# of food for your journey.

# You don't speak the local language, so you can't read any ingredients
# lists. However, sometimes, allergens are listed in a language you do
# understand. You should be able to use this information to determine which
# ingredient contains which allergen and work out which foods are safe to
# take with you on your trip.

# You start by compiling a list of foods (your puzzle input), one food per
# line. Each line includes that food's ingredients list followed by some or
# all of the allergens the food contains.

# Each allergen is found in exactly one ingredient. Each ingredient contains
# zero or one allergen. Allergens aren't always marked; when they're listed
# (as in (contains nuts, shellfish) after an ingredients list), the
# ingredient that contains each listed allergen will be somewhere in the
# corresponding ingredients list. However, even if an allergen isn't listed,
# the ingredient that contains that allergen could still be present: maybe
# they forgot to label it, or maybe it was labeled in a language you don't
# know.

# For example, consider the following list of foods:

# mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
# trh fvjkl sbzzf mxmxvkd (contains dairy)
# sqjhc fvjkl (contains soy)
# sqjhc mxmxvkd sbzzf (contains fish)

# The first food in the list has four ingredients (written in a language you
# don't understand): mxmxvkd, kfcds, sqjhc, and nhms. While the food might
# contain other allergens, a few allergens the food definitely contains are
# listed afterward: dairy and fish.

# The first step is to determine which ingredients can't possibly contain any
#  of the allergens in any food in your list. In the above example, none of
# the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen.
# Counting the number of times any of these ingredients appear in any
# ingredients list produces 5: they all appear once each except sbzzf, which
# appears twice.

# Determine which ingredients cannot possibly contain any of the allergens in
# your list. How many times do any of those ingredients appear?

import os
from collections import defaultdict
from typing import Dict, List, Set, Tuple


def read_foods(f) -> List[Tuple[List[str], List[str]]]:
    lines = f.read().split('\n')
    foods = []
    for line in lines:
        tokens = line.split(' (contains ')
        ingredients = set(tokens[0].split())
        allergens = set(tokens[1][:-1].split(', '))
        foods.append((ingredients, allergens))
    return foods


def count_ingredients(foods: List[Tuple[List[str], List[str]]]) -> Dict[str, int]:
    foodCount = defaultdict(lambda: 0)
    for ingredients, _ in foods:
        for ingredient in ingredients:
            foodCount[ingredient] += 1
    return foodCount


def find_possible_allergic_ingredients(foods: List[Tuple[List[str], List[str]]]) -> Dict[str, Set[str]]:
    possible = {}

    # Find possible allergic ingredients
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen not in possible:
                possible[allergen] = ingredients.copy()
            else:
                # Narrow down ingredient list
                possible[allergen] &= ingredients
    return possible


def find_allergic_ingredients(foods: List[Tuple[List[str], List[str]]]) -> Set[str]:
    possible = find_possible_allergic_ingredients(foods)
    return set().union(*possible.values())


# with open(os.path.dirname(__file__) + "/../examples/example_21.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_21.txt") as f:
    foods = read_foods(f)
    foodCount = count_ingredients(foods)
    allergic = find_allergic_ingredients(foods)
    print("2020 - Day 21 - Part 1")
    print(sum(foodCount[ingredient]
          for ingredient in (foodCount.keys() - allergic)))
    # => 2826
    #    ====

# ----------------------------
# Advent of Code 2020 - Day 21
# Part 2: Allergen Assessment
# ----------------------------

# Now that you've isolated the inert ingredients, you should have enough
# information to figure out which ingredient contains which allergen.

# In the above example:

# mxmxvkd contains dairy.
# sqjhc contains fish.
# fvjkl contains soy.

# Arrange the ingredients alphabetically by their allergen and separate them
# by commas to produce your canonical dangerous ingredient list. (There
# should not be any spaces in your canonical dangerous ingredient list.) In
# the above example, this would be mxmxvkd,sqjhc,fvjkl.

# Time to stock your raft with supplies. What is your canonical dangerous
# ingredient list?


def map_allergens_to_ingredients(foods: List[Tuple[List[str], List[str]]]) -> Dict[str, str]:
    possible = find_possible_allergic_ingredients(foods)
    found = set()
    allergenMap = []
    while len(allergenMap) < len(possible):
        for allergen, ingredients in possible.items():
            options = list(ingredients - found)
            if len(options) == 1:
                allergenMap.append((allergen, options[0]))
                found.add(options[0])
                break
    return allergenMap


# with open(os.path.dirname(__file__) + "/../examples/example_21.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_21.txt") as f:
    foods = read_foods(f)
    allergenMap = map_allergens_to_ingredients(foods)
    print("2020 - Day 21 - Part 2")
    print(repr(','.join(allergen[1] for allergen in sorted(allergenMap))))
    # => 'pbhthx,sqdsxhb,dgvqv,csnfnl,dnlsjr,xzb,lkdg,rsvlb'
    #    ===================================================
