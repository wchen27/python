from collections import deque
from time import perf_counter

s = perf_counter()
spaces = '       '
def print_board(boardList):
    for row in boardList:
        print(spaces[len(row):], end=' ')
        for x in row:
            print(x, end=' ')
        print()
    
def goal_test(boardString):
    c = 0
    for x in boardString:
        if x == '1':
            c += 1
    return c == 1


def list_to_string(boardList):
    s = ''
    for row in boardList:
        for num in row:
            s += str(num)
    return s

def string_to_list(boardString):
    s = []
    for char in boardString:
        s.append(int(char))
    return [[s[0]], s[1:3], s[3:6], s[6:10], s[10:]]

def copy_board(boardList):
  return [x[:] for x in boardList]

def get_children(boardString):
    state = string_to_list(boardString)
    children = []
    # horizontal moves

    for j in range(len(state)):
        row = state[j]
        if len(row) < 3:
            continue
        
        for i in range(len(row)- 2):
            if row[i+1] == 1:
                if row[i] != row[i+2]:
                    temp = copy_board(state)
                    temp[j][i], temp[j][i+2] = temp[j][i+2], temp[j][i]
                    temp[j][i+1] = 0

                    children.append(list_to_string(temp)) 

    # vertical moves

    for r in range(1, len(state) - 1):
        currlen = len(state[r])
        for c in range(currlen):
            if state[r][c] == 1:
                if c == 0:
                    upper = state[r-1][0]
                    lowerleft = state[r+1][c]
                    lowerright = state[r+1][c+1]
                    if upper != lowerleft:
                        temp = copy_board(state)
                        temp[r-1][0], temp[r+1][c] = temp[r+1][c], temp[r-1][0]
                        temp[r][c] = 0
                        children.append(list_to_string(temp))
                    
                elif c == currlen - 1:
                    upper = state[r-1][-1]
                    lowerleft = state[r+1][c]
                    lowerright = state[r+1][c+1]
                    if upper != lowerright:
                        temp = copy_board(state)
                        temp[r-1][-1], temp[r+1][c+1] = temp[r+1][c+1], temp[r-1][-1]
                        temp[r][c] = 0 
                        children.append(list_to_string(temp))
                
                else:
                    upperleft = state[r-1][c-1]
                    upperright = state[r-1][c]
                    lowerleft = state[r+1][c]
                    lowerright = state[r+1][c+1]
                    if upperleft != lowerright:
                        temp = copy_board(state)
                        temp[r-1][c-1], temp[r+1][c+1] = temp[r+1][c+1], temp[r-1][c-1]
                        temp[r][c] = 0
                        children.append(list_to_string(temp))
                    if upperright != lowerleft:
                        temp = copy_board(state)
                        temp[r-1][c], temp[r+1][c] = temp[r+1][c], temp[r-1][c]
                        temp[r][c] = 0
                        children.append(list_to_string(temp))
                    
    return children

board =     [[0],
           [1, 1], 
          [1, 1, 1], 
         [1, 1, 1, 1], 
        [1, 1, 1, 1, 1]]

boardstr = list_to_string(board)

# EXTEND LEVEL 1

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
        for child in get_children(curr):
            if child not in visited:
                npath = path.copy()
                npath.append(curr)
                fringe.append((child, depth + 1, npath))
                visited.add(child)

    return None, -1
x = BFS(boardstr)
e = perf_counter()

for state in x[0]:
    state = string_to_list(state)
    print_board(state)
    print()
print('Path length:', x[1])
print('Total runtime:', e-s)