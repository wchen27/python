
from time import perf_counter


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

# def solve_board(N):
#     board = [-1] * N 
#     diagonals1 = [True] * (2 * N - 1)
#     diagonals2 = [True] * (2 * N - 1)
#     def clear_space(row, col):
#         board[row] = -1
#         diagonals1[row + col] = True
#         diagonals2[row - col + N - 1] = True
    
#     def place_queen(row, col):
#         board[row] = col
#         diagonals1[row + col] = False
#         diagonals2[row - col + N - 1] = False
    
#     def test_space(col):
#         for row in range(N):
#             if board[row] == -1 and diagonals1[row + col] and diagonals2[row - col + N - 1]:
#                 place_queen(row, col)
#                 if col < N - 1 and not test_space(col + 1):
#                     clear_space(row, col)
#                 else:
#                     return True
#         return False
    
#     test_space(0)
#     return board

# Staircase solution finder that exists for N > 4

def solve_board(N):
    if not (N % 6 == 2) and not (N % 6 == 3):
        return list(range(1, N, 2)) + list(range(0, N, 2))
        
    else:
        l1 = list(range(0, N, 2))
        l2 = list(range(1, N, 2))
        if N % 6 == 2:
            l1[0], l1[1] = l1[1], l1[0]
            temp = l1.pop(2)
            l1.append(temp)
            return l2 + l1
        l2 = l2[1:] + [1]
        l1 = l1[2:] + [0, 2]
        return l2 + l1


i = 8
s = perf_counter()
solutions = []

while perf_counter() - s < 30:
    solutions.append(solve_board(i))
    i += 1

for solution in solutions:
    print(len(solution), solution, test_solution(solution))

