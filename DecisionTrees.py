import math

with open('play_tennis.csv', 'r') as f:
    lines = [line.strip().split(',') for line in f.readlines()]
    # make a dictionary with key as first row and value as column
    header = lines[0]
    data = lines[1:]

def calc_starting_entropy(characteristic):
    if type(characteristic) != int:
        characteristic = header.index(characteristic)
    counts = {}
    for row in data:
        value = row[characteristic]
        if value not in counts:
            counts[value] = 0
        counts[value] += 1    
    entropy = 0
    for value in counts:
        p = counts[value] / len(data)
        entropy -= p * math.log2(p)
    return entropy

def calc_entropy(characteristic, cl):
    if type(characteristic) != int:
        characteristic = header.index(characteristic)
    counts = {}
    for row in cl:
        value = row[characteristic]
        if value not in counts:
            counts[value] = 0
        counts[value] += 1    
    entropy = 0
    for value in counts:
        p = counts[value] / len(cl)
        entropy -= p * math.log2(p)
    return entropy

def calc_expected_entropy(characteristic):
    characteristic = header.index(characteristic)
    counts = {}
    newRows = {}
    for row in data:
        value = row[characteristic]
        if value not in counts:
            counts[value] = 0
            newRows[value] = []
        counts[value] += 1
        newRows[value].append(row)
    expected_entropy = 0
    for value in counts:
        p = counts[value] / len(data)
        expected_entropy += p * calc_entropy(-1, newRows[value])
    return expected_entropy

def calc_information_gain(characteristic):
    return calc_starting_entropy(-1) - calc_expected_entropy(characteristic)
