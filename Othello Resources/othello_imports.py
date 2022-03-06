import heapq

directions = [-11, -10, -9, -1, 1, 9, 10, 11]
import time
import sys

inf = float('inf')
neginf = float('-inf')
scoreHeap = []
board = "...........................ox......xo..........................."

def convert8(x):
    i = x - 11
    i -= ((x//10)-1)*2
    return int(i)

def convert10(x):
    i = x + 11
    i += ((x//8))*2
    return int(i)

def opposite(token):
    if token == 'x':
        return 'o'
    return 'x'

def possible_moves(board, token):
    board = create_border(board)
    if token == 'x':
        other = 'o'
    else:
        other = 'x'
    moves = []
    for i in range(len(board)):
        if board[i] == token:
            for d in directions:
                temp = i + d
                if board[temp] != other:
                    continue
                while board[temp] == other:
                    temp += d
                if board[temp] == '.':
                    moves.append(convert8(temp))
    
    return moves


def game_over(board):
    if possible_moves(board, 'x') == [] and possible_moves(board, 'o') == []:
        return True
    return False


def make_move(board, token, index):
    index = convert10(index)
    board = create_border(board)
    if token == 'x':
        other = 'o'
    else:
        other = 'x'
    board = board[:index] + token + board[index + 1:]
    for d in directions:
        possflip = []
        temp = index + d
        if board[temp] != other:
            continue
        while board[temp] == other:
            possflip.append(temp)
            temp += d
        if board[temp] == token:
            for flip in possflip:
                board = board[:flip] + token + board[flip + 1:]

    return remove_border(board)

def possible_next_boards(board, token):
    spaces = possible_moves(board, token)
    boards = set()
    for space in spaces:
        boards.add((space, make_move(board, token, space)))
    return boards

def create_border(board):
    border = '?' * 10
    for i in range(8):
        border += '?' + board[i * 8 : (i + 1) * 8] + '?'
    border += '??????????'
    return border

def remove_border(board):
    boardList = board_to_list(board)
    b = ''
    for line in boardList:
        if line == '?' * 10:
            continue
        b += line[1 : -1]
    return b


 

def score(board):
    if len(possible_moves(board, 'x')) == 0 or len(possible_moves(board, 'o')) == 0:
        score = board.count('x') - board.count('o')
        return score * 100000
    if board in scoreDict.keys():
        return scoreDict[board]
    score = 0
    if "." not in board:
        score = board.count('x') - board.count('o')
        return score * 10 ** (10)

    corners_dict = {
    0: [[1, 8, 9], [1, 8], [2, 9, 16]],
    7: [[6, 14, 15], [6, 15], [5, 14, 23]],
    56: [[57, 48, 49], [48, 57], [40, 49, 58]],
    63: [[62, 54, 55], [62, 55], [61, 54, 47]]
    }
    
    edges = [16, 24, 32, 40, 58, 59, 60, 61, 47, 39, 31, 23, 2, 3, 4, 5]
    for edge in edges:
        if board[edge] == 'x':
            score += 100
        elif board[edge] == 'o':
            score -= 100

    stable_count = 0
    for corner in corners_dict.keys():
        if board[corner] == "x":
            score += 1000
            for adj in corners_dict[corner][0]:
                if board[adj] == "x":
                    stable_count += 1
                if board[adj] == 'o':
                    stable_count -= 1

        elif board[corner] == "o":
            score -= 1000
            for adj in corners_dict[corner][0]:
                if board[adj] == "o":
                    stable_count -= 1
                if board[adj] == 'x':
                    stable_count += 1

        else:
            for adj in corners_dict[corner][0]:
                if board[adj] == "x":
                    score -= 1000
                if board[adj] == "o":
                    score += 1000
            for space in corners_dict[corner][2]:
                if board[space] == 'x':
                    score += 500
                if board[space] == 'o':
                    score -= 500

    score += (len(possible_moves(board, "x")) - len(possible_moves(board, "o"))) * (64 - board.count('.')) * 2
    score += stable_count * 500
    scoreDict[board] = score
    return score

def board_to_list(board):
    nb = []
    length = int(len(board) ** (1/2))
    for i in range(length):
        nb.append(board[i * length : (i + 1) * length])
    return nb

def print_board(board):
    for i in range(10):
        print(board[i * 10 : (i + 1) * 10])

# def find_next_move(board, player, depth):
#     if player == 'x': return max_move(board, depth)
#     return min_move(board, depth)

# def max_step(board, depth):
#     if depth == 0:
#         return score(board)
#     results = list()
#     for next_board in possible_next_boards(board, 'x'):
#         results.append(min_step(next_board, depth - 1))
#     return max(results)

# def min_step(board, depth):
#     if depth == 0:
#         return score(board)
#     results = list()
#     for next_board in possible_next_boards(board, 'o'):
#         results.append(max_step(next_board, depth - 1))
#     return min(results)


scoreDict = dict()

def alphabeta(board, depth, alpha, beta, token):
    best_move = None
    if depth == 0 or game_over(board):
        s = score(board)
        # heapq.heappush(scoreHeap, (s, board, ))
        return s, None
    if token == 'x':
        val = float('-inf')
        currscore = neginf
        for index, nb in possible_next_boards(board, 'x'):
            temp_max, _ = alphabeta(nb, depth - 1, alpha, beta, opposite(token))
            if temp_max > currscore:
                currscore = temp_max
                best_move = index
            val = max(val, alphabeta(nb, depth - 1, alpha, beta, 'o')[0])
            if val >= beta:
                break
            alpha = max(alpha, val)
        return val, best_move
    else:
        val = float('inf')
        currscore = inf
        for index, nb in possible_next_boards(board, 'o'):
            temp_max, _ = alphabeta(nb, depth - 1, alpha, beta, opposite(token))
            if temp_max < currscore:
                currscore = temp_max
                best_move = index
            val = min(val, alphabeta(nb, depth - 1, alpha, beta, 'x')[0])
            if val <= alpha:
                break
            beta = min(beta, val)
        return val, best_move

# def find_next_move(board, token, depth):
#     global bestMove
#     best, bestMove = alphabeta(board, depth, neginf, inf, token, 0)
#     newBoard = ''
#     for key in scoreDict.keys():
#         if key in possible_next_boards(board, token) and key != board and scoreDict[key] == best:
#             newBoard = key
#     print(newBoard)
#     #if depth == 0:
#     return int(bestMove)
#     # return find_next_move(newBoard, opposite(token), depth - 1)
    
def find_next_move(board, token, depth):
    # possMoves = possible_moves(board, token)
    # for move in possMoves:
    #     nb = make_move(board, token, move)
    #     score = alphabeta(nb, depth, neginf, inf, opposite(token))
    #     if token == 'o':
    #         heapq.heappush(scoreHeap, (-(score), move, nb))
    #     else:
    #         heapq.heappush(scoreHeap, (score, move, nb))
    # return heapq.heappop(scoreHeap)[1]
    return alphabeta(board, depth, neginf, inf, token)[1]



class Strategy():

   logging = False  # Optional

   def best_strategy(self, board, player, best_move, still_running):

       depth = 1

       for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all

           best_move.value = find_next_move(board, player, depth)

           depth += 1


if __name__ == '__main__':
    board = sys.argv[1]
    player = sys.argv[2]
    depth = 1
    for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
        print(find_next_move(board, player, depth))
        depth += 1

# results = []
# with open("boards_timing.txt") as f:
#     for line in f:
#         board, token = line.strip().split()
#         temp_list = [board, token]
#         print(temp_list)
#         for count in range(1, 7):
#             print("depth", count)
#             start = time.perf_counter()
#             find_next_move(board, token, count)
#             end = time.perf_counter()
#             temp_list.append(str(end - start))
#         print(temp_list)
#         print()
#         results.append(temp_list)
# with open("boards_timing_my_results.csv", "w") as g:
#     for l in results:
#         g.write(", ".join(l) + "\n")