import sys


indices = '012345678'

def opposite(token):
    if token == 'X':
        return 'O'
    return 'X'


def possible_next_boards(board, currPlayer):
    boards = set()
    for i in range(len(board)):
        if board[i] == '.':
            temp = list(board)
            temp[i] = currPlayer
            boards.add(''.join(temp))
    
    return boards
    
def print_puzzle(board):
    for x in range(3):
        print(board[x*3 : x*3+3] + "   " + str(x*3) + str(x*3 + 1) + str(x*3 + 2))

def goal_test(board):
    for i in range(3):
        currRow = board[i*3 : (i + 1)*3]
        currCol = board[i] + board[i + 3] + board[i + 6]
        if currRow == 'XXX' or currCol == 'XXX': return 1
        if currRow == 'OOO' or currCol == 'OOO': return -1
    d1 = board[0] + board[4] + board[8]
    d2 = board[2] + board[4] + board[6]
    if d1 == 'XXX' or d2 == 'XXX': return 1
    if d2 == 'OOO' or d2 == 'OOO': return -1
    if board.find('.') == -1:
        return 0
    return None
    
def get_current_player(board):
    if board == '.........':
        return 'X'
    if board.count('X') == board.count('O'):
        return 'X'
    return 'O'


def max_step(board):
    if (x := goal_test(board)) != None:
        return x
    results = list()
    for next_board in possible_next_boards(board, 'X'):
        results.append(min_step(next_board))
    return max(results)

def min_step(board):
    if (x := goal_test(board)) != None:
        return x
    results = list()
    for next_board in possible_next_boards(board, 'O'):
        results.append(max_step(next_board))
    return min(results)

def max_move(board):
    maxValue = -1
    results = dict()
    for nb in possible_next_boards(board, 'X'):
        curr = 0
        for i in range(9):
            if nb[i] != board[i]:
                curr = i
        results[curr] = min_step(nb)
    for key in results.keys():
        if results[key] > maxValue:
            maxIndex, maxValue = key, results[key]
    
    return maxIndex

def min_move(board):
    minValue = 1
    results = dict()
    for nb in possible_next_boards(board, 'O'):
        curr = 0
        for i in range(9):
            if nb[i] != board[i]:
                curr = i
        results[curr] = max_step(nb)
    for key in results.keys():
        if results[key] < minValue:
            minIndex, minValue = key, results[key]
    
    return minIndex

def make_move(board, index, token):
    return board[:index] + token + board[index + 1:]

def make_best_move(board):
    player = get_current_player(board)
    if player == 'X': return max_move(board)
    return min_move(board)


def print_board(board):
    for i in range(3):
        print(board[i  * 3 : (i + 1) * 3] + '\t' + indices[i * 3 : (i + 1) * 3])

def print_results(board, token):
    for move in moves:
        s = 'Moving at ' + str(move) + ' results in a '
        if token == 'X':
            res = min_step(make_move(board, move, token))
        else:
            res = max_step(make_move(board, move, token))
        if (res == 1 and token == 'X') or (res == -1 and token == 'O'):
            temp = 'win.'
        elif (res == -1 and token == 'X') or (res == 1 and token == 'O'):
            temp = 'loss.'
        else:
            temp = 'tie.'
        print(s + temp)

board = sys.argv[1]
moves = []
for i in range(len(board)):
    if board[i] == '.':
        moves.append(i)


if board == '.' * 9:
    computer = input('Should I be X or O? ')
    player = opposite(computer)
else:
    computer = get_current_player(board)
    player = opposite(computer)


while goal_test(board) == None:
    currentPlayer = get_current_player(board)
    print('\nCurrent board:')
    print_board(board)
    print()
    if currentPlayer == computer:
        print_results(board, currentPlayer)
        move = make_best_move(board)
        print('\nI choose space ' + str(move) + '.')
        moves.remove(move)
        board = make_move(board, move, currentPlayer)
    else:
        move = input('You can move to any of these spaces: ' + ', '.join([str(move) for move in moves]) + '.\nYour choice? ')
        board = make_move(board, int(move), currentPlayer)
        moves.remove(int(move))

winner = goal_test(board)
print('\nCurrent board:')
print_board(board)
if (winner == 1 and computer == 'X') or (winner == -1 and computer == 'O'):
    print('\nI win!')
elif (winner == -1 and computer == 'X') or (winner == 1 and computer == 'O'):
    print('\nYou win!')
else:
    print('\nWe tied!')