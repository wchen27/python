import math
import sys

with open('mushroom.csv', 'r') as f:
    lines = [line.strip().split(',') for line in f.readlines()]
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

def calc_expected_entropy(characteristic, rows):
    characteristic = header.index(characteristic)
    counts = {}
    newRows = {}
    for row in rows:
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

def calc_information_gain(characteristic, rows):
    return calc_entropy(header[-1], rows) - calc_expected_entropy(characteristic, rows)

def build_tree(characteristics, rows):
    best_characteristic = max(characteristics, key=lambda x: calc_information_gain(x, rows))
    tree = {best_characteristic:{}}
    remaining_characteristics = [c for c in characteristics if c != best_characteristic]
    values = sorted(list(set([row[header.index(best_characteristic)] for row in rows])))
    for value in values:
        new_rows = [row for row in rows if row[header.index(best_characteristic)] == value]
        if calc_entropy(-1, new_rows) == 0:
            tree[best_characteristic][value] = new_rows[0][-1]
        else:
            subtree = build_tree(remaining_characteristics, new_rows)
            tree[best_characteristic][value] = subtree
    return tree

def display_tree(tree, indent):
    for key in tree:
        print('  ' * indent + '*', key, end=' ')
        if type(tree[key]) == dict:
            print()
            display_tree(tree[key], indent + 1)
        else:
            print('-->', tree[key])

print_stream = sys.stdout
with open('treeout.txt', 'w') as f:
    sys.stdout = f
    display_tree(build_tree(header[:-1], data), 0)
    sys.stdout = print_stream