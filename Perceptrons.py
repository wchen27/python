import sys
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

def perceptron(A, w, b, x):
    return A(dot(w, x) + b)

def check(n, w, b):
    table = truth_table(len(w), n)
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
    diff = calc_curr_output(w, b, x) - correct
    nw = add(w, mult(x, l * diff))
    nb = l
    nb += l * diff
    return nw, nb

def generate_all_tables(n):
    tables = []
    for i in range(2 ** 2 ** n):
        tables.append(truth_table(n, i))
    return tables

def train(table):
    w = [0] * len(list(tbl[0].keys())[0])
    b = 0
    for i in range(NUM_EPOCHS):
        pw, pb = w, b
        for x in table.keys():
            w, b = update(w, b, x, 1, table)
        if (w, b) == (pw, pb):
            break
        pw, pb = w, b
    print(w, b)
    print(check(2 ** len(w) - 1, w, b))

if __name__ == '__main__':
    tbl = generate_all_tables(2)
    for table in tbl:
        train(table)