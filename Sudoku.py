# -*- coding: utf-8 -*-

import sys, time

alphabet = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
N = -1
subblock_height = -1
subblock_width = -1
symbol_set = set()
symbol_string = ''
rows = []
cols = []
blocks = []
neighbors = dict()


def setup(puzzleString):
    global N, subblock_height, subblock_width, symbol_set, neighbors, symbol_string
    
    N = int(len(puzzleString) ** (1/2))
    if int(N ** (1/2)) ** 2 == N:
        subblock_height, subblock_width = int(N ** (1/2)), int(N ** (1/2))
    else:
        for i in range(int(N ** (1/2)) + 1, N):
            if N % i == 0:
                subblock_height = N // i
                subblock_width = i
                break
    symbol_string = alphabet[:N]
    for char in alphabet[:N]:
        symbol_set.add(char)


# setup('13.4..29.5CA98...7C54.31.A2C8.3...977.C..56.19.22513.94.C876.6..1C..5BA.874923.1.ABCA25146BC73.93..69.8.2154B.A5C.96.71..1.278..94656.87.4.3AC..')
# print(N, subblock_height, subblock_width, symbol_set)
    

def print_puzzle(boardString):
    setup(boardString)
    horizLength = -1
    currLine = '| '
    newlines = 0
    for i in range(1, len(boardString) + 1):
        currLine += boardString[i - 1] + ' '
        if i % subblock_width == 0 and i % N != 0:
            currLine += '| '
        if i % N == 0 and i != N ** 2:
            currLine += '|\n'
            newlines += 1
            if horizLength == -1:
                horizLength = len(currLine[:currLine.find('\n')])            
            if newlines % subblock_height == 0:
                currLine += '_' * (horizLength) + '\n| '
            else:
                currLine += '| '
    currLine += '|' + '\n' + '_' * (horizLength) + '\n'
    print('_' * horizLength)
    print(currLine)

def symbol_count(boardString):
    setup(boardString)
    for char in symbol_set:
        print(char, boardString.count(char))

def string_to_list(boardString):
    board = []
    for i in range(N):
        curr = []
        for j in range(i * N, i * N + N):
            curr.append(boardString[j])
        board.append(curr)

    return board

def constraints(boardString):
    global N, rows, cols, blocks, symbol_set, symbol_string

    boardList = []
    index = 0
    rows = []
    cols = []
    blocks = []
    symbol_string = ""
    symbol_set = set()
    setup(boardString)
    for i in range(N):
        curr = []
        for j in range(i * N, i * N + N):
            curr.append(index)
            index += 1
        boardList.append(curr)
    for row in boardList:
        rows.append(set(row))
    for i in range(N):
        currCol = set()
        for j in range(N):
            currCol.add(boardList[j][i])
        cols.append(currCol)
    
    for j in range(N):
        currBlockSet = set()
        for i in range(len(boardString)):
            currRow = i // N
            currCol = i % N
            currBlock = (currRow // subblock_height) * (N // subblock_width) + (currCol // subblock_width)
            if currBlock != j:
                continue
            currBlockSet.add(boardList[currRow][currCol])
        # print(currBlockSet)
        blocks.append(currBlockSet)

blockString = ''
def create_dict(boardString):
    constraints(boardString) 
    fldict = dict()   
    for i in range(len(boardString)):
        global blockString, neighbors
        if boardString[i] == '.':
            fldict[i] = symbol_string
        else:
            fldict[i] = boardString[i]

        currRow = i // N
        currCol = i % N
        currBlock = (currRow // subblock_height) * (N // subblock_width) + (currCol // subblock_width)
        blockString += str(currBlock)
        # print(N, len(boardString), rows, cols, blocks, end=' ')
        # print(i, blocks[currBlock]) 
        neighbors[i] = rows[currRow] | cols[currCol] | blocks[currBlock]
        # print(neighbors[i])
    return fldict 

# def goal_test(state):
#     if state.find('.') == -1:
#         return True
#     return False

def goal_test(state):
    for key in state.keys():
        if len(state[key]) > 1:
            return False
    return True

def get_next_unassigned_var(state):
    return state.find('.')

# def get_sorted_values(state, var):
#     if len(neighbors.keys()) == 0:
#         create_dict(state)
#     temp = symbol_set.copy()
#     for index in neighbors[var]:
#         temp.discard(state[index])
    
#     return sorted(list(temp))

def get_most_constrained_var(state):
    minLen = 100
    for key in state.keys():
        if (x := len(state[key])) < minLen:
            if x == 1:
                continue
            minLen = x
    for key in state.keys():
        if len(state[key]) == minLen:
            return key


def get_sorted_values(state, var):
    if len(neighbors.keys()) == 0:
        create_dict(state)
    return set(state[var])


# def csp_backtracking(state):
#     if goal_test(state):
#         return state
#     var = get_next_unassigned_var(state)
#     for val in (x := get_sorted_values(state, var)):
#         new_state = list(state).copy()
#         new_state[var] = val
#         new_state = ''.join(new_state)
#         # print(new_state, x)
#         result = csp_backtracking(new_state)
#         if result != None:
#             # print_puzzle(result)
#             return result

#     return None

def csp_backtracking_fl(state):
    if goal_test(state):
        return state
    var = get_most_constrained_var(state)
    for val in get_sorted_values(state, var):
        new_state = state.copy()
        new_state[var] = val
        checked_board = check_board(new_state)
        if checked_board != None:
            result = csp_backtracking_fl(checked_board)
            if result != None:
                return result

    return None


def forward_looking(state):
    solved = []
    
    for key in state.keys():
        if len(state[key]) == 1:
            solved.append(key)
        if len(state[key]) == 0:
            return None
    visited = set(solved)
    while solved:
        for key in state.keys():
            if len(state[key]) == 1 and key not in visited:
                solved.append(key)
            if len(state[key]) == 0:
                return None

                
        index = solved.pop()
        visited.add(index)
        for neighbor in neighbors[index]:
            if neighbor == index:
                continue
            temp = set(state[neighbor])
            temp.discard(state[index])
            state[neighbor] = ''.join(temp)
    
    return state
    

def constraint_prop(state):
    global rows, cols, blocks, symbol_set
    for row in rows:
        for sym in symbol_set:
            found = []
            for index in row:
                if state[index].find(sym) != -1:
                    found.append(index)
            if len(found) == 0:
                return None
            if len(found) == 1:
                # print(found[0], sym)
                state[found[0]] = sym
    
    for row in cols:
        for sym in symbol_set:
            found = []
            for index in row:
                if state[index].find(sym) != -1:
                    found.append(index)
            if len(found) == 0:
                return None
            if len(found) == 1:
                # print(found[0], sym)
                state[found[0]] = sym
    for row in blocks:
        for sym in symbol_set:
            found = []
            for index in row:
                if state[index].find(sym) != -1:
                    found.append(index)
            if len(found) == 0:
                return None
            if len(found) == 1:
                # print(found[0], sym)
                state[found[0]] = sym 

    return forward_looking(state)      

def check_board(state):
    state = forward_looking(state)
    if state == None:
        return None
    state = constraint_prop(state)
    if state == None:
        return None
    return state

puzzle = "...49.7...6.721..4.A.7..5.A..33..A86..9...2...3....138..296....7238...9.1.....A7..A..4.87.8.6...5..."
# puzzle = create_dict(puzzle)
# puzzle = forward_looking(puzzle)
# print(constraint_prop(puzzle))


def solve_puzzle(state):
    state = create_dict(state)
    # forward_looking(fldict)
    x = (csp_backtracking_fl(state))
    solution = ''
    for key in x.keys():
        solution += x[key]
    return (solution)

# s = time.perf_counter()
# solve_puzzle(puzzle)
# print(time.perf_counter() - s)

s = time.perf_counter()
solutions = []
with open(sys.argv[1], 'r') as f:
    lines = [line.strip() for line in f]

for line in range(len(lines)):
    solutions.append(solve_puzzle(lines[line]))

e = time.perf_counter()
for solution in solutions:
    print(solution)
print("Total runtime on", sys.argv[1], "was", e - s, "seconds.")
