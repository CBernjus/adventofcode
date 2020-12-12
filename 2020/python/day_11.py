# ----------------------------
# Advent of Code 2020 - Day 11
# Part 1: Seating System
# ----------------------------
 
# Your plane lands with plenty of time to spare. The final leg of your
# journey is a ferry that goes directly to the tropical island where you can
# finally start your vacation. As you reach the waiting area to board the
# ferry, you realize you're so early, nobody else has even arrived yet!

# By modeling the process people use to choose (or abandon) their seat in the
# waiting area, you're pretty sure you can predict the best place to sit. You
# make a quick map of the seat layout (your puzzle input).

# The seat layout fits neatly on a grid. Each position is either floor (.),
# an empty seat (L), or an occupied seat (#). For example, the initial seat
# layout might look like this:

# L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL

# Now, you just need to model the people who will be arriving shortly.
# Fortunately, people are entirely predictable and always follow a simple set
# of rules. All decisions are based on the number of occupied seats adjacent
# to a given seat (one of the eight positions immediately up, down, left,
# right, or diagonal from the seat). The following rules are applied to every
# seat simultaneously:

# - If a seat is empty (L) and there are no occupied seats adjacent to it,
#   the seat becomes occupied.
# - If a seat is occupied (#) and four or more seats adjacent to it are
#   also occupied, the seat becomes empty.
# - Otherwise, the seat's state does not change.

# Floor (.) never changes; seats don't move, and nobody sits on the floor.

# After one round of these rules, every seat in the example layout becomes
# occupied:

# #.##.##.##
# #######.##
# #.#.#..#..
# ####.##.##
# #.##.##.##
# #.#####.##
# ..#.#.....
# ##########
# #.######.#
# #.#####.##

# After a second round, the seats with four or more occupied adjacent seats
# become empty again:

# #.LL.L#.##
# #LLLLLL.L#
# L.L.L..L..
# #LLL.LL.L#
# #.LL.LL.LL
# #.LLLL#.##
# ..L.L.....
# #LLLLLLLL#
# #.LLLLLL.L
# #.#LLLL.##

# This process continues for three more rounds:

# #.##.L#.##
# #L###LL.L#
# L.#.#..#..
# #L##.##.L#
# #.##.LL.LL
# #.###L#.##
# ..#.#.....
# #L######L#
# #.LL###L.L
# #.#L###.##
# #.#L.L#.##
# #LLL#LL.L#
# L.L.L..#..
# #LLL.##.L#
# #.LL.LL.LL
# #.LL#L#.##
# ..L.L.....
# #L#LLLL#L#
# #.LLLLLL.L
# #.#L#L#.##
# #.#L.L#.##
# #LLL#LL.L#
# L.#.L..#..
# #L##.##.L#
# #.#L.LL.LL
# #.#L#L#.##
# ..L.L.....
# #L#L##L#L#
# #.LLLLLL.L
# #.#L#L#.##

# At this point, something interesting happens: the chaos stabilizes and
# further applications of these rules cause no seats to change state! Once
# people stop moving around, you count 37 occupied seats.

#Simulate your seating area by applying the seating rules repeatedly until
# no seats change state. How many seats end up occupied?

import os

f = open(os.path.dirname(__file__) + "/../inputs/input_11.txt")

layout = f.read().split('\n')
height = len(layout)
width = len(layout[0])

def get_seats(layout):
    seats = {}

    for y in range(len(layout)):
        for x in range(len(layout[y])):
            seat = layout[y][x]
            if seat == "L":
                seats[(x, y)] = False

    return seats

def print_layout(seats):
    for y in range(height):
        for x in range(width):
            seat = seats.get((x, y))
            if seat == None:
                print('.', end='')
            elif seat:
                print('#', end='')
            else:
                print('L', end='')
        print()
    print()

def simulate_1_step(seats):
    new_seats = {}
    for (x, y) in seats:
        neighbor_indices = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        neighbors = 0
        for (nx, ny) in neighbor_indices:
            if seats.get((nx, ny)):
                neighbors += 1
        seat = seats.get((x, y))
        if seat and neighbors >= 4:
            new_seats[(x, y)] = False
        elif not seat and neighbors == 0:
            new_seats[(x, y)] = True
        else:
            new_seats[(x, y)] = seat
    #print_layout(new_seats)
    return new_seats

def simulate_1(layout):
    seats = get_seats(layout)
    step = simulate_1_step(seats)
    while(seats != step):
        seats = step
        step = simulate_1_step(seats)

    return seats

def count_occupied(seats):
    count = 0
    for (x, y) in seats:
        if seats.get((x, y)):
            count += 1
    return count

print("2020 - Day 11 - Part 1")
print(count_occupied(simulate_1(layout)))
# => 2334
#    ====

# ----------------------------
# Advent of Code 2020 - Day 11
# Part 2: Seating System
# ----------------------------

# As soon as people start to arrive, you realize your mistake. People don't
# just care about adjacent seats - they care about the first seat they can
# see in each of those eight directions!

# Now, instead of considering just the eight immediately adjacent seats,
# consider the first seat in each of those eight directions. For example,
# the empty seat below would see eight occupied seats:

# .......#.
# ...#.....
# .#.......
# .........
# ..#L....#
# ....#....
# .........
# #........
# ...#.....

# The leftmost empty seat below would only see one empty seat, but cannot see
# any of the occupied ones:

# .............
# .L.L.#.#.#.#.
# .............

# The empty seat below would see no occupied seats:

# .##.##.
# #.#.#.#
# ##...##
# ...L...
# ##...##
# #.#.#.#
# .##.##.

# Also, people seem to be more tolerant than you expected: it now takes five
# or more visible occupied seats for an occupied seat to become empty (rather
# than four or more from the previous rules). The other rules still apply:
# empty seats that see no occupied seats become occupied, seats matching no
# rule don't change, and floor never changes.

# Given the same starting layout as above, these new rules cause the seating
# area to shift around as follows:

# L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL

# #.##.##.##
# #######.##
# #.#.#..#..
# ####.##.##
# #.##.##.##
# #.#####.##
# ..#.#.....
# ##########
# #.######.#
# #.#####.##

# #.LL.LL.L#
# #LLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLL#
# #.LLLLLL.L
# #.LLLLL.L#

# #.L#.##.L#
# #L#####.LL
# L.#.#..#..
# ##L#.##.##
# #.##.#L.##
# #.#####.#L
# ..#.#.....
# LLL####LL#
# #.L#####.L
# #.L####.L#

# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##LL.LL.L#
# L.LL.LL.L#
# #.LLLLL.LL
# ..L.L.....
# LLLLLLLLL#
# #.LLLLL#.L
# #.L#LL#.L#

# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##L#.#L.L#
# L.L#.#L.L#
# #.L####.LL
# ..#.#.....
# LLL###LLL#
# #.LLLLL#.L
# #.L#LL#.L#

# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##L#.#L.L#
# L.L#.LL.L#
# #.LLLL#.LL
# ..#.L.....
# LLL###LLL#
# #.LLLLL#.L
# #.L#LL#.L#

# Again, at this point, people stop shifting around and the seating area
# reaches equilibrium. Once this occurs, you count 26 occupied seats.

# Given the new visibility method and the rule change for occupied seats
# becoming empty, once equilibrium is reached, how many seats end up
# occupied?

dirs = 8
dx = [-1, 0, 1, -1, 1, -1, 0, 1]
dy = [-1, -1, -1, 0, 0, 1, 1, 1]
        

def in_bounds(x, y):
    return -1 < x < width and -1 < y < height

def simulate_2_step(seats):
    new_seats = {}
    for (x, y) in seats:
        neighbors = 0
        for d in range(dirs):
            nx = x + dx[d]
            ny = y + dy[d]

            while(in_bounds(nx, ny) and seats.get((nx, ny)) == None):
                nx += dx[d]
                ny += dy[d]
            
            if seats.get((nx, ny)):
                neighbors += 1
        seat = seats.get((x, y))
        if seat and neighbors >= 5:
            new_seats[(x, y)] = False
        elif not seat and neighbors == 0:
            new_seats[(x, y)] = True
        else:
            new_seats[(x, y)] = seat
    #print_layout(new_seats)
    return new_seats

def simulate_2(layout):
    seats = get_seats(layout)
    step = simulate_2_step(seats)
    while(seats != step):
        seats = step
        step = simulate_2_step(seats)

    return seats

print("\n2020 - Day 11 - Part 2")
print(count_occupied(simulate_2(layout)))
# => 2334
#    ====