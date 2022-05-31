import math
import random
import sys
import matplotlib.pyplot as plt

with open('nursery.csv', 'r') as f:
    lines = [line.strip().split(',') for line in f.readlines()]
    header = lines[0]
    data = lines[1:]
    nonmissing = [line for line in data if not '?' in line]
    missing = [line for line in data if '?' in line]
    random.shuffle(nonmissing)
    test_set = nonmissing[-50:]
    training_set = nonmissing[:-50]
    possible_classifications = set()
    for row in nonmissing:
        possible_classifications.add(row[-1])
    possible_classifications = list(possible_classifications)


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
        elif calc_entropy(-1, new_rows) > 0 and calc_entropy(-1, rows) == calc_entropy(-1, new_rows):
            tree[best_characteristic][value] = random.choice(possible_classifications)
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

def classify(tree, row):
    for key in tree:
        value = row[header.index(key)]
        if value in tree[key]:
            if type(tree[key][value]) == dict:
                return classify(tree[key][value], row)
            else:
                return tree[key][value]

def learn(size, ts):
    training = random.sample(ts, size)
    tree = build_tree(header[:-1], training)
    success = 0
    for vec in test_set:
        res = classify(tree, vec)
        if res == vec[-1]:
            success += 1
    return success / len(test_set) * 100


def fill_missing(row, data):
    missing = row.index('?')
    classification = row[-1]
    counts = dict()
    for r in data:
        if r[-1] != classification:
            continue
        if r[missing] not in counts.keys():
            counts[r[missing]] = 0
        counts[r[missing]] += 1
    mval = -1
    final = None
    for key in counts.keys():
        if counts[key] > mval:
            mval = counts[key]
            final = key
    row[missing] = final
    return row

def complete_data_set(m, nm):
    final_dataset = nm.copy()
    for r in m:
        final_dataset.append(fill_missing(r, nm))        
    return final_dataset

# comp_data = complete_data_set(missing, nonmissing)

# print(len(comp_data))
# test_set = comp_data[-50:]
# training_set = comp_data[:-50]



sizes = []
accuracies = []
for i in range(5000, 60000, 5000):
    print('Size:', i)
    print('Accuracy:', (a := learn(i, training_set)))
    print()
    sizes.append(i)
    accuracies.append(a)

plt.xlabel('Size')
plt.ylabel('Accuracy')
plt.scatter(sizes, accuracies)
plt.show()