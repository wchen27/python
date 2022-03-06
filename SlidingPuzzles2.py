
import time, sys
from collections import deque
import heapq

def build_board(puzzleString):
    s = ''
    length, puzzle = int(puzzleString.split()[0]), puzzleString.split()[1]
    for i in range(length):
        for j in range(length):
            s += puzzle[i * length + j] + ' '
        s += '\n'
    return s


def print_puzzle(puzzleString):
    print(build_board(puzzleString))


def find_goal(puzzleString):
    length, puzzle = int(puzzleString.split()[0]), puzzleString.split()[1]
    return str(length) + ' ' + ''.join(sorted(puzzle))[1:] + '.'


def goal_test(puzzleString):
    length, puzzle = int(puzzleString.split()[0]), puzzleString.split()[1]
    return True if puzzleString == find_goal(puzzleString) else False


def get_children(puzzleString):
    length, puzzle = int(puzzleString.split()[0]), puzzleString.split()[1]
    clear = puzzle.find('.')
    legalMoves = []  # indices of legal moves
    abv, blw, nxt, lst = clear - length, clear + length, clear + 1, clear - 1
    if abv >= 0:
        legalMoves.append(abv)
    if blw < length ** 2:
        legalMoves.append(blw)
    if nxt < length ** 2 and nxt % length > clear % length:
        legalMoves.append(nxt)
    if lst >= 0 and lst % length < clear % length:
        legalMoves.append(lst)

    # return list of legal board positions
    legalPositions = []
    for move in legalMoves:
        temp = [c for c in puzzle]
        temp[clear], temp[move] = temp[move], temp[clear]
        legalPositions.append(str(length) + ' ' + ''.join(temp))

    return legalPositions


def parityCheck(puzzleString):
    length, puzzle = puzzleString.split()
    length = int(length)
    parity = 0
    temp = puzzle[:puzzle.find('.')] + puzzle[puzzle.find('.') + 1:]
    for i in range(len(temp) - 1):
        for j in range(i, len(temp)):
            curr = temp[i] + temp[j]
            if curr != ''.join(sorted(curr)):
                parity += 1
    
    if length % 2 == 0:
        clearPos = puzzle.find('.') // length + 1
        if clearPos % 2 == 0:
            return parity % 2 == 0
        return parity % 2 == 1
    
    return parity % 2 == 0

def kDFS(n, k):
    fringe = []
    state = n
    depth = 0
    ancestors = set()
    ancestors.add(state)
    fringe.append((state, depth, ancestors))
    while len(fringe) > 0:
        x = fringe.pop()
        s, d, a = x
        if goal_test(s):
            return True, d
        if d < k:
            for c in get_children(s):
                if c not in a:
                    newa = a.copy()
                    newa.add(c)
                    temp = (c, d + 1, newa)
                    fringe.append(temp)
    
    return None

def IDDFS(start):
    if not parityCheck(start):
        return None
    maxDepth = 0
    res = None
    while res == None:
        res = kDFS(start, maxDepth)
        maxDepth += 1
    
    return res

def BFS(n):
    if goal_test(n):
        return n
    fringe = deque()
    visited = set()
    fringe.append((n, 0, []))
    visited.add(n)
    while len(fringe) > 0:
        curr, depth, path = fringe.popleft()
        if(goal_test(curr)):
            length = depth
            return list(reversed(path)), length
        for child in get_children(curr):
            if child not in visited:
                npath = path.copy()
                npath.append(curr)
                fringe.append((child, depth + 1, npath))
                visited.add(child)

    return None

def taxicab(puzzleString):
    goal = find_goal(puzzleString)
    length = int(puzzleString[0])
    puzzle = puzzleString[2:]
    dist = 0
    for i in range(len(puzzle)):
        if puzzle[i] == '.':
            continue
        coordinates = (i % length, i // length)
        ind = goal.find(puzzle[i]) - 2
        actual = (ind % length, ind // length)
        dist += abs(coordinates[0] - actual[0]) + abs(coordinates[1] - actual[1])

    return dist

def AStar(puzzleString):
    closed = set()
    start = (taxicab(puzzleString), 0, puzzleString)
    fringe = []
    heapq.heappush(fringe, start)
    while fringe:
        curr = heapq.heappop(fringe)
        if goal_test(curr[2]):
            
            return curr[1]
            # return curr[3]
        if curr[2] not in closed:
            closed.add(curr[2])
            for child in get_children(curr[2]):
                if child not in closed:
                    d = curr[1] + 1
                    
                    heapq.heappush(fringe, (d + taxicab(child), d, child))
    
    return None


file = '15_puzzles.txt'
with open(file, 'r') as f:
    lines = [l.strip() for l in f]
f.close()

# for l, x in enumerate(lines):
#     print(l, taxicab(x))


def timeB(puzzle, line):
    start = time.perf_counter()
    x = BFS(puzzle)[1]
    end = time.perf_counter()
    print('Line', line, puzzle[2:], 'BFS -', x, 'moves in', end - start, 'seconds')

def timeD(puzzle, line):
    start = time.perf_counter()
    x = IDDFS(puzzle)[1]
    end = time.perf_counter()
    print('Line', line, puzzle[2:], 'ID-DFS -', x, 'moves in', end - start, 'seconds')

def timeA(puzzle, line):
    start = time.perf_counter()
    x = AStar(puzzle)
    end = time.perf_counter()
    print('Line', line, puzzle[2:], 'A* -', x, 'moves in', end - start, 'seconds')

timeD('3 87436.152', 0)

# for number, line in enumerate(lines):
#     puzzle = '4 ' + line
#     x = line[-1]
#     start = time.perf_counter()
#     if not parityCheck(puzzle):
#         end = time.perf_counter()
#         print('line', number, puzzle, 'no solution determined in', end - start, 'seconds')
#         print()
#         continue
#     timeA(puzzle, number)
    # if x == 'B':
    #     timeB(puzzle, number)
    # if x == 'I':
    #     timeD(puzzle, number)
    # if x == 'A':
    #     timeA(puzzle, number)
    # if x == '!':
    #     timeB(puzzle, number)
    #     timeD(puzzle, number)
    #     timeA(puzzle, number)
    # print()


