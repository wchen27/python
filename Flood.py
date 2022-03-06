from collections import deque
import random, heapq
from time import perf_counter

colors = 'ROYGBV'

choice = input('1 - Manual input\n2 - Random board\nEnter choice: ')
choice = int(choice)
if choice == 1:
    print('COLORS:\nR-RED, O-ORANGE, Y-YELLOW\nG-GREEN, B-BLUE, V-VIOLET\n')
    print('INPUT FORMAT: 3 ROYGBVROY')
    i = input('Enter board: ')
    size, board = int(i.split()[0]), i.split()[1]
elif choice == 2:
    size = int(input('Enter Size: '))
    board = '.' * (size ** 2)
    for r in range(len(board)):
        board = board[:r] + colors[random.randint(0, 5)] + board[r+1:]

else:
    exit()


def board_to_list(boardString):
    board = []
    for i in range(size):
        curr = []
        for j in range(i * size, i * size + size):
            curr.append(boardString[j])
        board.append(curr)

    return board

def list_to_board(boardList):
    board = ''
    for l in boardList:
        board += ''.join(l)
    return board

def copy_board(boardList):
  return [x[:] for x in boardList]

def print_board(boardString):
    for i in range(size):
        j = i * size
        print(boardString[j:j+size])

def get_upper(boardString, r, c):
    board = board_to_list(boardString)
    if r - 1 < 0:
        return None, 0, 0
    return board[r-1][c], r-1, c

def get_lower(boardString, r, c):
    board = board_to_list(boardString)
    if r + 1 >= size:
        return None, 0, 0
    return board[r+1][c], r+1, c

def get_right(boardString, r, c):
    board = board_to_list(boardString)
    if c + 1 >= size:
        return None, 0, 0
    return board[r][c+1], r, c+1

def get_left(boardString, r, c):
    board = board_to_list(boardString)
    if c - 1 < 0:
        return None, 0, 0
    return board[r][c-1], r, c-1

def get_connecting(boardString, currColor):
    visited = {(0, 0)}
    start = {(0, 0)}
    fringe = deque()
    fringe.append((0, 0))
    while fringe:
        curr = fringe.popleft()
        pc = (get_left(boardString, *curr), get_right(boardString, *curr), get_upper(boardString, *curr), get_lower(boardString, *curr))
        for child, r, c in pc:
            if (r, c) not in visited:
                if child == None:
                    continue
                if child == currColor:
                    start.add((r, c))
                    fringe.append((r, c))
                visited.add((r, c))

    return start


def change_color(boardString, color):
    board = board_to_list(boardString)
    x = get_connecting(boardString, board[0][0])
    for r, c in x:
        board[r][c] = color
    return get_connecting(boardString, color), list_to_board(board)

# cc = change_color(board, 'G')

# print(cc)
# print_board(change_color(board, 'B')[1])
# print(change_color(board, 'B')[0])

def get_neighbors(boardString, r, c):
    pc = [get_left(boardString, r, c), get_right(boardString, r, c), get_lower(boardString, r, c), get_upper(boardString, r, c)]
    c = []
    for child in pc:
        if not child == None:
            c.append(child)
    return c

def get_borders(boardString):
    currColor = boardString[0]
    borderColors = []
    for r, c in get_connecting(boardString, currColor):
        n = get_neighbors(boardString, r, c)
        for color in n:
            if color[0] not in borderColors and not color[0] == None:
                borderColors.append(color[0])

    return borderColors


def goal_test(boardString):
    initialChar = boardString[0]
    for char in boardString:
        if char != initialChar:
            return False
    return True

# def get_children(boardString):
#     children = set()
#     curr = len(get_connecting(boardString, boardString[0]))
#     for color in colors:
#         x = change_color(boardString, color)
#         if len(x[0]) >= curr:
#             print(curr, len(x[0]), color, x[0])
#             children.add(x[1])
#     return children

def get_children(boardString):
    children = set()
    for color in get_borders(boardString):
        x = change_color(boardString, color)
        children.add((x[1], len(x[0])))
    return children

def BFS(n):
    if goal_test(n):
        return n, 0
    fringe = deque()
    visited = set()
    fringe.append((n, 0, []))
    visited.add(n)
    while len(fringe) > 0:
        curr, depth, path = fringe.popleft()
        if(goal_test(curr)):
            length = depth
            path.append(curr)
            return path, length
        for child, h in get_children(curr):
            if child not in visited:
                npath = path.copy()
                npath.append(curr)
                fringe.append((child, depth + 1, npath))
                visited.add(child)

    return None, -1

def HeapDFS(puzzleString):
    closed = set()
    start = (len(get_connecting(puzzleString, puzzleString[0])), 0, puzzleString, [])
    fringe = []
    heapq.heappush(fringe, start)
    while fringe:
        curr = heapq.heappop(fringe)
        if goal_test(curr[2]):
            curr[-1].append(curr[2])
            return (curr[1], curr[-1])
            # return curr[3]
        if curr[2] not in closed:
            closed.add(curr[2])
            for child, h in get_children(curr[2]):
                if child not in closed:
                    d = curr[1] + 1
                    tpath = curr[3].copy()
                    tpath.append(curr[2])
                    heapq.heappush(fringe, (-(d-h), d, child, tpath))
    
    return None, -1

# def AStar(puzzleString):
#     closed = set()
#     start = (taxicab(puzzleString), 0, puzzleString, [])
#     fringe = []
#     heapq.heappush(fringe, start)
#     while fringe:
#         curr = heapq.heappop(fringe)
#         if goal_test(curr[2]):
#             return curr[-1], len(curr[-1]) - 1
#             # return curr[3]
#         if curr[2] not in closed:
#             closed.add(curr[2])
#             for child in get_children(curr[2]):
#                 if child not in closed:
#                     d = curr[1] + 1
#                     tpath = curr[3].copy()
#                     tpath.append(curr[2])
#                     heapq.heappush(fringe, (d + taxicab(child), d, child, tpath))
    
#     return None, -1

s = perf_counter()
x = BFS(board)
e = perf_counter()
print('Time to find solution',e-s)

# s1 = perf_counter()
# y = HeapDFS(board) 
# e1 = perf_counter()
# print(e1-s1)
# path = []
# curr = len(get_connecting(y[1][0], y[1][0][0]))
# for i in range(len(y[1])):
#     n = len(get_connecting(y[1][i], y[1][i][0]))
#     if n < curr:
#         continue
#     curr = n
#     path.append(y[1][i])
        
# print(len(path))

print('Path length:', x[1])
if x[0] == None:
    print('Error solving puzzle.')
else:
    for child in x[0]:
        print_board(child)
        print()
    
    print('COLOR FILL ORDER:')
    for child in x[0][1:]:
        print(child[0], end=' ')
    print()