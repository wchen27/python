import time
from random import choice

def test_solution(state):
    for var in range(len(state)):
        left, middle, right = state[var], state[var], state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, 'middle', compare)
                return False
            if left >= 0 and state[compare] == left:
                print(var, 'left', compare)
                return False
            if right < len(state) and state[compare] == right:
                print(var, 'right', compare)
                return False
    
    return True

def is_legal(r1, c1, r2, c2):
    
    if r1 == None or r2 == None or c1 == None or c2 == None:
        return False
    if c1 == c2:
        return False
    
    if abs(r1 - r2) == abs(c1 - c2):
        return False
    
    return True

# def get_next_unassigned_var(state):
#     for x in range(1, len(state)):
#         if state[x] == 0:
#             return x

def get_next_unassigned_var(state):
    poss = []
    for x in range(len(state)):
        if state[x] == None:
            poss.append(x)
    return choice(poss)
            

def get_sorted_values(state, r):
    values = []
    for i in range(len(state)):
        valid = True
        for j in range(len(state)):
            if state[j] == None:
                continue
            if not is_legal(r, i, j, state[j]):
                valid = False
        if valid:
            values.append(i)
    return values
        
    
def goal_test(state):
    for i in range(len(state) - 1):
        for j in range(i + 1, len(state)):
            if not is_legal(i, state[i], j, state[j]):
                return False
    
    return True


def csp_backtracking(state, start):
    if goal_test(state):
        return state
    if time.perf_counter() - start > 1:
        return ""
    var = get_next_unassigned_var(state)
    for val in get_sorted_values(state, var):
        new_state = state.copy()
        new_state[var] = val
        result = csp_backtracking(new_state, start)
        if result != None:
            return result

    return None


# solfound = 0
# s1 = time.perf_counter()
# for i in range(31, 100):
#     state = [None]*i
#     s = time.perf_counter()
#     if solfound >= 2:
#         break
#     x=((csp_backtracking(state, s)))
#     if x == "":
#         continue
#     print(str(i) + 'x' + str(i), 'solution', x, 'found in:', time.perf_counter() - s, 'seconds \nsolution test:', test_solution(x))
#     solfound += 1
# print('total time', time.perf_counter() - s1, 'seconds')



# Incremental repair

board = [0] * 31

for i in range(len(board)):
    board[i] = (3 * i + 1) % len(board)

def get_conflicts(board):
    conflicts = [0] * len(board)
    cfrows = []
    for i in range(len(board)):
        for j in range(len(board)):
            if i == j:
                continue
            if not is_legal(i, board[i], j, board[j]):
                conflicts[i] += 1
    m = max(conflicts)
    if m == 0:
        return 0
    for i in range(len(conflicts)):
        if conflicts[i] == m:
            cfrows.append(i)

    return cfrows, sum(conflicts)

def get_row_conflicts(board, row):
    conflicts = 0
    for i in range(len(board)):
        if i == row:
            continue
        if not is_legal(i, board[i], row, board[row]):
            conflicts += 1
    
    return conflicts

def inc_repair(board):
    while not goal_test(board):
        print(board, get_conflicts(board)[1])
        board = least_conflict(board)
        
    return board
        

def least_conflict(board):
    r = choice(get_conflicts(board)[0])
    conf = [0] * len(board)
    conflicts = []
    for i in range(len(board)):
        nb = board.copy()
        nb[r] = i
        conf[i] = get_row_conflicts(nb, r)
    
    m = min(conf)
    for i in range(len(conf)):
        if conf[i] == m:
            conflicts.append(i)
    
    nb[r] = choice(conflicts)
    return nb
        
for i in range(31, 33):
    board = [0] * 31
    s = time.perf_counter()
    x = (test_solution(inc_repair(board)))
    print(x, time.perf_counter() - s)


        
        




