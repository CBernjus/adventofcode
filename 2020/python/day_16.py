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
    return list(map(int, s.split(',')))


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


def create_invalid_filters(rules):
    return list(map(lambda r: lambda x: (x <
                                         r[1] or (r[2] < x and x < r[3]) or r[4] < x), rules))


def create_valid_filters(rules):
    return list(map(lambda r: lambda x: (r[1] <= x <= r[2] or r[3] <= x <= r[4]), rules))


def get_invalid_fields(fields, filters):
    invalid_fields = fields
    for f in filters:
        invalid_fields = list(filter(f, invalid_fields))
        if not invalid_fields:
            break
    return list(invalid_fields)


def map_tickets_to_fields(tickets):
    return [field for ticket in tickets for field in ticket]


def calc_scanning_error(tickets, rules):
    fields = map_tickets_to_fields(tickets)
    filters = create_invalid_filters(rules)
    return functools.reduce(lambda a, b: a+b, get_invalid_fields(fields[3:], filters), 0)


with open(os.path.dirname(__file__) + "/../inputs/input_16.txt") as f:

    (rules, tickets) = read_intput(f)
    print("2020 - Day 16 - Part 1")
    print(calc_scanning_error(tickets, rules))
    # => 26053
    #    =====


# ----------------------------
# Advent of Code 2020 - Day 16
# Part 2: Ticket Translation
# ----------------------------

# Now that you've identified which tickets contain invalid values, discard
# those tickets entirely. Use the remaining valid tickets to determine which
# field is which.

# Using the valid ranges for each field, determine what order the fields
# appear on the tickets. The order is consistent between all tickets: if seat
# is the third field, it is the third field on every ticket, including your
# ticket.

# For example, suppose you have the following notes:

# class: 0-1 or 4-19
# row: 0-5 or 8-19
# seat: 0-13 or 16-19

# your ticket:
# 11,12,13

# nearby tickets:
# 3,9,18
# 15,1,5
# 5,14,9
# Based on the nearby tickets in the above example, the first position must
# be row, the second position must be class, and the third position must be
# seat; you can conclude that in your ticket, class is 12, row is 11, and
# seat is 13.

# Once you work out which field is which, look for the six fields on your
# ticket that start with the word departure. What do you get if you multiply
# those six values together?

def ticket_is_valid(ticket, rules):
    invalid_fields = get_invalid_fields(ticket, create_invalid_filters(rules))
    if invalid_fields:
        return False
    return True


def get_valid_tickets(tickets, rules):
    return list(filter(lambda t: ticket_is_valid(t, rules), tickets))


def find_possible_field_rules(tickets, rules):
    filters = create_valid_filters(rules)
    possible_rules = [range(len(rules))] * len(tickets[0])
    for ticket in tickets:
        for field in range(len(possible_rules)):
            possible_rules[field] = list(
                filter(lambda i: filters[i](ticket[field]), possible_rules[field]))

    return list(map(lambda r: [rules[i] for i in r], possible_rules))


def determine_rule_order(possible_rules, rules):
    order = {}
    sorted_possible_rules = sorted([
        [len(rules), i, rules] for i, rules in enumerate(possible_rules)])

    for field in sorted_possible_rules:
        _, i, rules = field
        filtered = list(filter(lambda r: r[0] not in order.keys(), rules))
        rule = filtered[0]
        order[rule[0]] = i

    return order


def calc_departure_field_product(my_ticket, order):
    departure_keys = filter(lambda f: 'departure' in f, order.keys())
    result = 1
    for key in departure_keys:
        result *= my_ticket[order[key]]
    return result


with open(os.path.dirname(__file__) + "/../inputs/input_16.txt") as f:

    (rules, tickets) = read_intput(f)
    valid_tickets = get_valid_tickets(tickets, rules)
    possible_rules = find_possible_field_rules(valid_tickets, rules)
    order = determine_rule_order(possible_rules, rules)

    print("2020 - Day 16 - Part 2")
    print(calc_departure_field_product(tickets[0], order))
    # => 1515506256421
    #    =============
