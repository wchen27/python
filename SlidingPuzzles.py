from collections import deque
import time
import sys


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

# BFS algorithm

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


# Bidirectional BFS algorithm

def BiBFS2(n):
    if goal_test(n):
        return [n], 0
    ffringe = deque()
    fvisited = set()
    bfringe = deque()
    bvisited = set()
    ffringe.append((n, 0))
    bfringe.append((find_goal(n), 0))
    fvisited.add(n)
    bvisited.add(find_goal(n))
    while len(ffringe) > 0 and len(bfringe) > 0:
        curr = ffringe.popleft()
        bcurr = bfringe.popleft()  
        for child in get_children(curr[0]):
            if goal_test(child):
                return curr[1] + 1
            for x in bfringe:
                if x[0] == child:
                    return x[1] + curr[1] + 1
            if child not in fvisited:
                ffringe.append((child, curr[1] + 1))
                fvisited.add(child)

        
        for bchild in get_children(bcurr[0]):
            for x in ffringe:
                if x[0] == bchild:
                    return x[1] + bcurr[1] + 1

            if bchild not in bvisited:
                bfringe.append((bchild, bcurr[1] + 1))
                bvisited.add(bchild)


    return None

# print(BFS('3 863.54217'))


# length, solutions, solutionPaths = longest_solution('3 12345678.')
# print('Longest path length:', length)
# for number, solution in enumerate(solutions):
#     print('Complex state:')
#     print_puzzle(solution)
#     print('Path:')
#     for state in solutionPaths[number]:
#         print_puzzle(state)




name = sys.argv[1]
with open(name, 'r') as f:
    lines = [l.strip() for l in f]
f.close()


for number, line in enumerate(lines):
    # print("Line", number, "Start:")
    # print_puzzle(line)
    # print("Goal:\n" + build_board(find_goal(line)))
    # print("Children:", get_children(line))
    start = time.perf_counter()
    length = BFS(line)[1]
    end = time.perf_counter()
    start2 = time.perf_counter()
    length2 = BiBFS2(line)
    end2 = time.perf_counter()
    print("Line %s: %s, %s moves found in %s seconds." %
          (str(number), line[2:], str(length), (end - start)))
    print("Line %s: %s, %s moves found in %s seconds." %
          (str(number), line[2:], (length2), (end2 - start2)))
    print('Line %s: BiBFS faster by %s' %(str(number), (end - start) - (end2 - start2)))
