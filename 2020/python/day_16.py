# ----------------------------
# Advent of Code 2020 - Day 16
# Part 1: Ticket Translation
# ----------------------------

# As you're walking to yet another connecting flight, you realize that one of
# the legs of your re-routed trip coming up is on a high-speed train.
# However, the train ticket you were given is in a language you don't
# understand. You should probably figure out what it says before you get to
# the train station after the next flight.

# Unfortunately, you can't actually read the words on the ticket. You can,
# however, read the numbers, and so you figure out the fields these tickets
# must have and the valid ranges for values in those fields.

# You collect the rules for ticket fields, the numbers on your ticket, and
# the numbers on other nearby tickets for the same train service (via the
# airport security cameras) together into a single document you can reference
# (your puzzle input).

# The rules for ticket fields specify a list of fields that exist somewhere
# on the ticket and the valid ranges of values for each field. For example, a
# rule like class: 1-3 or 5-7 means that one of the fields in every ticket is
# named class and can be any value in the ranges 1-3 or 5-7 (inclusive, such
# that 3 and 5 are both valid in this field, but 4 is not).

# Each ticket is represented by a single line of comma-separated values. The
# values are the numbers on the ticket in the order they appear; every ticket
# has the same format. For example, consider this ticket:

# .--------------------------------------------------------.
# | ????: 101    ?????: 102   ??????????: 103     ???: 104 |
# |                                                        |
# | ??: 301  ??: 302             ???????: 303      ??????? |
# | ??: 401  ??: 402           ???? ????: 403    ????????? |
# '--------------------------------------------------------'

# Here, ? represents text in a language you don't understand. This ticket
# might be represented as 101,102,103,104,301,302,303,401,402,403; of course,
# the actual train tickets you're looking at are much more complicated. In
# any case, you've extracted just the numbers in such a way that the first
# number is always the same specific field, the second number is always a
# different specific field, and so on - you just don't know what each
# position actually means!

# Start by determining which tickets are completely invalid; these are
# tickets that contain values which aren't valid for any field. Ignore your
# ticket for now.

# For example, suppose you have the following notes:

# class: 1-3 or 5-7
# row: 6-11 or 33-44
# seat: 13-40 or 45-50

# your ticket:
# 7,1,14

# nearby tickets:
# 7,3,47
# 40,4,50
# 55,2,20
# 38,6,12

# It doesn't matter which position corresponds to which field; you can
# identify invalid nearby tickets by considering only whether tickets contain
# values that are not valid for any field. In this example, the values on the
# first nearby ticket are all valid for at least one field. This is not true
# of the other three nearby tickets: the values 4, 55, and 12 are are not
# valid for any field. Adding together all of the invalid values produces
# your ticket scanning error rate: 4 + 55 + 12 = 71.

# Consider the validity of the nearby tickets you scanned. What is your
# ticket scanning error rate?

import os
import re
import functools

rule_pattern = re.compile(r'(.+): (\d+)\-(\d+) or (\d+)\-(\d+)')


def parse_rule(s):
    (name, minmin, minmax, maxmin, maxmax) = rule_pattern.match(s).groups()
    return (name, int(minmin), int(minmax), int(maxmin), int(maxmax))


def parse_ticket(s):
    return s.split(',')


def read_intput(f):
    lines = f.read().split('\n')

    rules = []
    tickets = []

    atTickets = False
    for line in lines:
        if not line or 'ticket' in line.lower():
            atTickets = True
            continue
        elif atTickets:
            tickets.append(parse_ticket(line))
        else:
            rules.append(parse_rule(line))

    return (rules, tickets)


def check_fields(fields, rules):
    filters = list(map(lambda r: lambda x: (x <
                                            r[1] or (r[2] < x and x < r[3]) or r[4] < x), rules))
    invalid_fields = fields
    for f in filters:
        invalid_fields = list(filter(f, invalid_fields))
    return list(invalid_fields)


def map_tickets_to_fields(tickets):
    return [int(field) for ticket in tickets for field in ticket]


def calc_scanning_error(tickets, rules):
    fields = map_tickets_to_fields(tickets)
    return functools.reduce(lambda a, b: a+b, check_fields(fields[3:], rules), 0)


with open(os.path.dirname(__file__) + "/../inputs/input_16.txt") as f:

    (rules, tickets) = read_intput(f)
    print(calc_scanning_error(tickets, rules))
