board = "...........................ox......xo..........................."
directions = [-11, -10, -9, -1, 1, 9, 10, 11]

def convert8(x):
    i = x - 11
    i -= ((x//10)-1)*2
    return int(i)

def convert10(x):
    i = x + 11
    i += ((x//8))*2
    return int(i)


def possible_moves(board, token):
    board = create_border(board)
    if token == 'x':
        other = 'o'
    else:
        other = 'x'
    moves = set()
    for i in range(len(board)):
        if board[i] == token:
            for d in directions:
                temp = i + d
                if board[temp] != other:
                    continue
                while board[temp] == other:
                    temp += d
                if board[temp] == '.':
                    moves.add(convert8(temp))
    
    return moves
                

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


def board_to_list(board):
    nb = []
    length = int(len(board) ** (1/2))
    for i in range(length):
        nb.append(board[i * length : (i + 1) * length])
    return nb

def print_board(board):
    for i in range(10):
        print(board[i * 10 : (i + 1) * 10])




