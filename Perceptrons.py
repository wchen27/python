import numpy as np
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


# XOR HAPPENS HERE
def xor(inp):
    p1 = train(truth_table(2, 7))
    p2 = train(truth_table(2, 14))
    p3 = train(truth_table(2, 8))
    w1, b1, _ = p1
    w2, b2, _ = p2
    w3, b3, _ = p3
    v1 = perceptron(step, w1, b1, inp)
    v2 = perceptron(step, w2, b2, inp)
    out = perceptron(step, w3, b3, (v1, v2))
    return out

def p_net(A, x, w_list, b_list, round=False):
    vA = np.vectorize(A)
    a = [x]
    for i in range(len(w_list)):
        if round:
            res = np.around(vA(a[i]@w_list[i] + b_list[i]), 0)
            a.append(res)
        else:
            a.append(vA(a[i]@w_list[i] + b_list[i]))
    return a

# XOR HAPPENS HERE (matrix)
def xor_matrix(inp):
    w1 = np.array([[-1, 1], [-2, 1]])
    b1 = np.array([[3, 0]])
    w2 = np.array([[1], [2]])
    b2 = np.array([[-2]])
    return p_net(step, inp, [None, w1, w2], [None, b1, b2])

def diamond(inp):
    w1 = np.array([[-1, 1, 1, -1], [-1, 1, -1, 1]])
    b1 = np.array([[1, 1, 1, 1]])
    w2 = np.array([[1], [1], [1], [1]])
    b2 = np.array([[-3]])
    return p_net(step, inp, [None, w1, w2], [None, b1, b2])

def circle(inp):
    w1 = np.array([[-1, 1, 1, -1], [-1, 1, -1, 1]])
    b1 = np.array([[1.57079] * 4])
    w2 = np.array([[1], [1], [1], [1]])
    b2 = np.array([[-3.14159]])
    vecRound = np.vectorize(round)
    return vecRound(p_net(sigmoid, inp, [None, w1, w2], [None, b1, b2]))

def inside(x, y):
    if ((x) ** 2 + (y) ** 2) ** (1/2) < 1:
        return 1
    return 0

def calc_error(x, y, wList, bList):
    a = p_net(sigmoid, x, wList, bList)[-1][0]
    error = 0
    for i in range(len(y[0])):
        error += (y[0][i] - a[i]) ** 2
    return error / 2 

def back_prop_epoch(x, y, wList, bList, lr):
    network = p_net(sigmoid, x, wList, bList)
    final = network[-1]
    deltas = [final * (1 - final) * (y - final)]
    for i in range(len(wList) - 1, -1, -1):
        L = network[i] * (1 - network[i]) * (deltas[0] @ (wList[i].transpose()))
        deltas = [L] + deltas
    for i in range(len(deltas) - 1):
        bList[i] = bList[i] + lr * deltas[i + 1]
        wList[i] = wList[i] + lr * ((network[i].transpose()) @ deltas[i + 1])
    return (wList, bList)

def back_prop(training_set, wList, bList, lr, num_epochs):
    for i in range(num_epochs):
        for x, y in training_set:
            wList, bList = back_prop_epoch(x, y, wList, bList, lr)
            print(p_net(sigmoid, x, wList, bList)[-1][0])
    return wList, bList

def train_sum():
    w1 = np.array([[random.uniform(-1, 1), random.uniform(-1, 1)], [random.uniform(-1, 1), random.uniform(-1, 1)]])
    w2 = np.array([[random.uniform(-1, 1), random.uniform(-1, 1)], [random.uniform(-1, 1), random.uniform(-1, 1)]])
    b1 = np.array([[random.uniform(-1, 1), random.uniform(-1, 1)]])
    b2 = np.array([[random.uniform(-1, 1), random.uniform(-1, 1)]])
    wList = [w1, w2]
    bList = [b1, b2]
    inputs = [(0, 0), (0, 1), (1, 0), (1,1)]
    outputs = [(0, 0), (0, 1), (0, 1), (1, 0)]
    training_set = []
    for i in range(len(inputs)):
        training_set.append((np.array([inputs[i]]), np.array([outputs[i]]))) 
    wList, bList = back_prop(training_set, wList, bList, 0.2, 2000)
    print()
    for x, y in training_set:
        print(p_net(sigmoid, x, wList, bList, round=True)[-1][0])
    


if __name__ == '__main__':
    # Perceptrons 1
    # args = sys.argv[1:]
    # n = int(args[0])
    # w = ast.literal_eval(args[1])
    # b = float(args[2])
    # print(check(truth_table(len(w), n), w, b))

    # Perceptrons 2
    # bits, n = sys.argv[1:]
    # w, b, acc = train(truth_table(int(bits), int(n)))
    # print('Weights:', w)
    # print('Bias:', b)
    # print('Accuracy:', acc)


    # XOR
    # inp = sys.argv[1]
    # inp = ast.literal_eval(inp)
    # print(xor(inp)) 

    # Perceptrons 4
    # args = len(sys.argv)
    # if args == 2:
    #     # XOR Matrix
    #     inp = sys.argv[1]
    #     inp = ast.literal_eval(inp)
    #     print(xor_matrix(inp)[0])
    # if args == 3:
    #     # Diamond
    #     x = float(sys.argv[1])
    #     y = float(sys.argv[2])
    #     print('outside') if inside(x, y) == 0 else print('inside')
    
    # if args == 1:
    #     # Circle
    #     points = []
    #     for i in range(500):
    #         x = random.uniform(-1, 1)
    #         y = random.uniform(-1, 1)
    #         points.append((x, y))
    #     correct = 0
    #     for point in points:
    #         if inside(point[0], point[1]) == circle(point):
    #             correct += 1
    #     print(correct / 500)
    if sys.argv[1] == 'S':
        train_sum()
    