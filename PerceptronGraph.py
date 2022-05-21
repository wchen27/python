import matplotlib.pyplot as plt
import random
import sys
import math
import ast

NUM_EPOCHS = 100

def truth_table(bits, n):
    table = {}
    bn = str(bin(n))[2:]
    bn = '0' * (2 ** bits - len(bn)) + bn
    currInd = 0
    for i in range(2 ** (bits) - 1, -1, -1):
        currTup = [k for k in bin(i)[2:]]
        currTup = ''.join(currTup)
        currTup = '0' * (bits - len(currTup)) + currTup
        table[tuple(int(k) for k in currTup)] = int(bn[currInd])
        currInd += 1
    return table

def dot(a, b):
    dot = 0
    for i in range(len(a)):
        dot += a[i] * b[i]
    return dot

def step(num):
    if num > 0:
        return 1
    return 0

def sigmoid(num):
    return 1 / (1 + math.exp(-num))

def sigmoidderiv(x):
    return sigmoid(x) * (1 - sigmoid(x))

def perceptron(A, w, b, x):
    return A(dot(w, x) + b)

def check(table, w, b):
    ncorrect = 0
    for x in table.keys():
        correct = table[x]
        if perceptron(step, w, b, x) == correct:
            ncorrect += 1
    return ncorrect / len(table)

def pprint(table):
    for i in range(1, len(list(table.keys())[0]) + 1):
        print('In' + str(i) + '\t', end='')
    print('|\tOut')
    print ('-' * (len(table) + 1) * 6)
    for key in table.keys():
        for i in range(len(key)):
            print(key[i], end='\t')
        print('|\t' + str(table[key]))

def add(t1, t2):
    return tuple([t1[i] + t2[i] for i in range(len(t1))])

def mult(t1, c):
    return tuple([t1[i] * c for i in range(len(t1))])

def calc_curr_output(w, b, x):
    return perceptron(step, w, b, x)

def update(w, b, x, l, table):
    correct = table[x]
    diff = correct - calc_curr_output(w, b, x)
    nw = add(w, mult(x, l * diff))
    nb = b + l * diff
    return nw, nb

def generate_all_tables(n):
    tables = []
    for i in range(2 ** 2 ** n):
        tables.append(truth_table(n, i))
    return tables

def train(table):
    w = [0] * len(list(table.keys())[0])
    b = 0
    old = (w, b)
    for _ in range(NUM_EPOCHS):
        for x in table.keys():
            w, b = update(w, b, x, 1, table)
        if old == (w, b):
            break
        old = (w, b)
    return w, b, check(table, w, b)


def color_p(w, b, point):
    if perceptron(step, w, b, point) == 1:
        return 'red'
    return 'green'

def color_t(table, point):
    point = (int(point[0]), int(point[1]))
    if table[point] == 1:
        return 'red'
    return 'green'

if __name__ == '__main__':
    d = [i / 10 for i in range(-20, 20)]
    r = [i / 10 for i in range(-20, 20)]
    tables = generate_all_tables(2)
    figure, axis = plt.subplots(4, 4)
    for i in range(4):
        for j in range(4):
            w, b, acc = train(tables[i * 4 + j])
            for x in d:
                for y in r:
                    axis[i][j].plot([x], [y], markersize=0.1, marker='.', color=color_p(w, b, (x, y)))
            for point in tables[i * 4 + j].keys():
                axis[i][j].plot(point[0], point[1], color=color_t(tables[i * 4 + j], (point[0], point[1])), marker='o', markersize=1)
    plt.show()
