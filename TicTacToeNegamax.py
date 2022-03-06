import sys

indices = '012345678'

def possible_next_boards(board, currPlayer):
    boards = set()
    for i in range(len(board)):
        if board[i] == '.':
            temp = list(board)
            temp[i] = currPlayer
            boards.add(''.join(temp))
    
    return boards
    
def make_move(board, index, token):
    return board[:index] + token + board[index + 1:]

def goal_test(board):
    for i in range(3):
        currRow = board[i*3 : (i + 1)*3]
        currCol = board[i] + board[i + 3] + board[i + 6]
        if currRow == 'XXX' or currCol == 'XXX': return 'X'
        if currRow == 'OOO' or currCol == 'OOO': return 'O'
    d1 = board[0] + board[4] + board[8]
    d2 = board[2] + board[4] + board[6]
    if d1 == 'XXX' or d2 == 'XXX': return 'X'
    if d2 == 'OOO' or d2 == 'OOO': return 'O'
    if board.find('.') == -1:
        return 0
    return None
    
def get_current_player(board):
    if board == '.........':
        return 'X'
    if board.count('X') == board.count('O'):
        return 'X'
    return 'O'

def opposite(token):
    if token == 'X':
        return 'O'
    return 'X'


# NegaMax function

def NegaMax(board, token):
    # goal testing
    if (x := goal_test(board)) != None:
        if x == token:
            return 1
        if x == 0:
            return 0
        return -1
    
    results = list()
    for next_board in possible_next_boards(board, token):
        # negating the opposite token's results gives current token's results
        results.append(-NegaMax(next_board, opposite(token)))
    # return (Nega)max value
    return max(results)

def NegaMaxMove(board, token):
    maxValue = -1
    results = dict()
    for nb in possible_next_boards(board, token):
        curr = 0
        for i in range(9):
            if nb[i] != board[i]:
                curr = i
        results[curr] = -NegaMax(nb, opposite(token))
    for key in results.keys():
        if results[key] > maxValue:
            maxIndex, maxValue = key, results[key]
    
    return maxIndex

def print_board(board):
    for i in range(3):
        print(board[i  * 3 : (i + 1) * 3] + '\t' + indices[i * 3 : (i + 1) * 3])

def print_results(board, token):
    for move in moves:
        s = 'Moving at ' + str(move) + ' results in a '
        res = NegaMax(make_move(board, move, token), opposite(token))
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
        move = NegaMaxMove(board, currentPlayer)
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
if winner == computer:
    print('\nI win!')
elif winner == player:
    print('\nYou win!')
else:
    print('\nWe tied!')



    
        




