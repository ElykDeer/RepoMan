#!/usr/bin/env python3

"""

Make groups

"""

from random import choices, shuffle
from math import ceil
from petname import generate
from string import ascii_lowercase, digits

# Example with a bunch of random people
def randomPeople(names = 150):
    people = [
        (uid, name) for uid, name in zip(
            [''.join(choices(ascii_lowercase, k=3)) + ''.join(choices(digits, k=3)) for i in range(names)],
            [generate(words=3, separator=' ').title() for i in range(names)])]
    assert(len(set(people)) == names) # No duplicates, pls
    return people

# Can pre-populate if groups have already been made..
# Format: A list of the lists of groupings...ie:
#  [
#   [  # Project One
#    [person1, person2, person3], # Group One
#    [person4, person5, person6], # Group Two
#    [person7, person8, person9], # Group Three
#   ],
#   [  # Project Two
#    [person1, person4, person7], # Group One
#    [person2, person5, person8], # Group Two
#    [person3, person6, person9], # Group Three
#   ],
#   [  # Project Three
#    [person1, person5, person9], # Group One
#    [person2, person6, person7], # Group Two
#    [person3, person4, person8], # Group Three
#   ],
#  ]
savedGroupings = []

# Tells you how many people each person has worked with before in the current grouping
# Ex:
#   calculateUniqueness([['a', 'k', 'c'], ['d', 'e', 'f'], ['k', 'h', 'i'], ['j', 'k', 'l']], [['k', 'j', 'a', 'd', 'i']])
#                       [       ^                            ^                     ^       ]  [  ^                      ]
def calculateUniqueness(savedGroups, currentGroups, debug = True):

    savedGroups = [i for j in savedGroups for i in j]

    for newGroup in currentGroups: # compare the new
        for person in newGroup:
            totals = 0
            for oldGroup in savedGroups: # to the old
                if person in oldGroup:
                    totals += 1
            if debug:
                print(person, "worked with", totals, "other people that they're currently working with now")

# Make groups
def group(people, groupSize = 5, savedGroups = [], debug = True):
    unique = False
    tries = 0
    difference = 1
    difficulty = 100000 # Increase this number to try harder to get unique groups
    while not unique:

        # If it's too hard to make entirely unique groups, reduce the criterion
        tries += 1
        if tries > difficulty:
            difference += 1

        # Randomize Groups
        shuffle(people) # Yes I know this is a bad way to do this, but it works
        groups = [people[i:i+groupSize] for i in range(0, len(people), groupSize)]

        # Fix groupings such that all groups are == groupSize or groupSize-1
        if len(groups[-1]) < groupSize-1:
            for i in range(1, (groupSize-1) - len(groups[-1]) + 1):
                groups[-1].append(groups[-i - 1][groupSize-1])
                groups[-i - 1].pop()

        # Make sure no two people work with eachother ever (almost)
        unique = True # Assume unique until proven otherwise
        for groupingSet in range(len(savedGroups)):
            for old in range(len(savedGroups[groupingSet])): # Compare the old
                for new in range(len(groups)):               # to the new
                    if len(set(savedGroups[groupingSet][old] + groups[new])) < len(savedGroups[groupingSet][old]) + len(groups[new]) - difference:
                        unique = False
                        break
                if not unique:
                    break
    if debug:
        print("No more than", difference, "people are the same in any two groups.")
    return groups

# Break people into categories however you want
group1, group2, group3, group4 = [randomPeople()[i::4] for i in range(4)]
grouped1 = group(group1) # Smart
print(grouped1, '\n')
savedGroupings.append(grouped1)
grouped2 = group(group2) # Silly
print(grouped2, '\n')
savedGroupings.append(grouped2)
grouped3 = group(group3) # Stinky
print(grouped3, '\n')
savedGroupings.append(grouped3)
grouped4 = group(group4) # Sad
print(grouped4, '\n')
savedGroupings.append(grouped4)

for project, name in zip(savedGroupings, ['Smart', 'Silly', 'Stinky', 'Sad']):
    print('\n', name, ' :')
    for groupp in project:
        print(groupp)

# Or group everyone together!
print('\nAll grouped together:\n', group(group1 + group2 + group3 + group4), '\n')

# Also make new unique groups for future projects... Maybe even re-organize who's in which group between pairings - just save the previous groups!
grouped1 = group(group1, savedGroups = savedGroupings) # Smart
print(grouped1, '\n')
savedGroupings.append(grouped1)
grouped2 = group(group2, savedGroups = savedGroupings) # Silly
print(grouped2, '\n')
savedGroupings.append(grouped2)
grouped3 = group(group3, savedGroups = savedGroupings) # Stinky
print(grouped3, '\n')
savedGroupings.append(grouped3)
grouped4 = group(group4, savedGroups = savedGroupings) # Sad
print(grouped4, '\n')
savedGroupings.append(grouped4)

# Etc...
grouped1 = group(group1, savedGroups = savedGroupings) # Smart
print(grouped1, '\n')
savedGroupings.append(grouped1)
grouped2 = group(group2, savedGroups = savedGroupings) # Silly
print(grouped2, '\n')
savedGroupings.append(grouped2)
grouped3 = group(group3, savedGroups = savedGroupings) # Stinky
print(grouped3, '\n')
savedGroupings.append(grouped3)
grouped4 = group(group4, savedGroups = savedGroupings) # Sad
print(grouped4, '\n')
savedGroupings.append(grouped4)

for project, name in zip(savedGroupings, ['Project1:\nSmart', 'Silly', 'Stinky', 'Sad', 'Project2:\nSmart', 'Silly', 'Stinky', 'Sad', 'Project3:\nSmart', 'Silly', 'Stinky', 'Sad']):
    print('\n' + name + ':')
    for groupp in project:
        print(groupp)
