import sys, random, heapq, pickle, ast


POPULATION_SIZE = 100
NUM_CLONES = 10
TOURNAMENT_SIZE = 10
TOURNAMENT_WIN_PROB = .75
CROSSOVER_LOCATIONS = 2
MUTATION_RATE = 0.8
STRATEGY_LENGTH = 4

def print_board(boardString):
    for i in range(20):
        print(boardString[i * 10 : (i + 1) * 10])

def to_list(boardString):
    boardList = []
    for i in range(20):
        boardList.append(boardString[i * 10 : (i + 1) * 10])
    return boardList

def to_col_list(boardString):
    boardList = to_list(boardString)
    boardList = list(map(list, zip(*boardList)))
    bl = []
    for col in boardList:
        bl.append(''.join(col))
    return bl

def get_depths(boardString):
    depths = []
    for i in range(10):
        currDepth = 0
        for j in range(20):
            if boardString[j * 10 + i] == ' ':
                currDepth += 1
            else:
                break
        depths.append(20 - currDepth)
    return depths

pieces = {
    'I0' : '####',
    'I1' : '#\n#\n#\n#',
    'O0' : '##\n##',
    'T0' : ' # \n###',
    'T1' : '# \n##\n# ',
    'T2' : '###\n # ',
    'T3' : ' #\n##\n #',
    'S0' : ' ##\n## ',
    'S1' : '# \n##\n #',
    'Z0' : '## \n ##',
    'Z1' : ' #\n##\n# ',
    'J0' : '#  \n###',
    'J1' : '##\n# \n#',
    'J2' : '###\n  #',
    'J3' : ' #\n #\n##',
    'L0' : '  #\n###',
    'L1' : '# \n# \n##',
    'L2' : '###\n#  ',
    'L3' : '##\n #\n #'
}

piecesIndex = {
    'I0' : [0, 1, 2, 3],
    'I1' : [0, 10, 20, 30],
    'O0' : [0, 1, 10, 11],
    'T0' : [1, 10, 11, 12],
    'T1' : [0, 10, 11, 20],
    'T2' : [0, 1, 2, 11],
    'T3' : [1, 10, 11, 21],
    'S0' : [1, 2, 10, 11],
    'S1' : [0, 10, 11, 21],
    'Z0' : [0, 1, 11, 12],
    'Z1' : [1, 10, 11, 20],
    'J0' : [0, 10, 11, 12],
    'J1' : [0, 1, 10, 20],
    'J2' : [0, 1, 2, 12],
    'J3' : [1, 11, 20, 21],
    'L0' : [2, 10, 11, 12],
    'L1' : [0, 10, 20, 21],
    'L2' : [0, 1, 2, 10],
    'L3' : [0, 1, 11, 21]
}

pieceNames = {
    'I' : ['I0', 'I1'],
    'O' : ['O0'],
    'T' : ['T0', 'T1', 'T2', 'T3'],
    'S' : ['S0', 'S1'],
    'Z' : ['Z0', 'Z1'],
    'J' : ['J0', 'J1', 'J2', 'J3'],
    'L' : ['L0', 'L1', 'L2', 'L3']
}

scoreDict = {
    0 : 0,
    1 : 40,
    2 : 100,
    3 : 300, 
    4 : 1200
}

# test = sys.argv[1]
test = ' ' * 200
def place_block(board, block, pos):
    length = max([len(line) for line in pieces[block].split('\n')])
    bl = list(board)
    if pos + length > 10:
        return None
    blockInd = piecesIndex[block].copy()
    for i in range(4):
        blockInd[i] += pos
        if bl[blockInd[i]] == '#':
            return 'GAME OVER', -1 * 10 ** 10, 0
    
    for i in blockInd:
        bl[i] = '#'

    while True:
        temp = blockInd.copy()
        for i in range(4):
            bl[blockInd[i]] = ' '
        for i in range(4):
            temp[i] += 10


            if temp[i] >= 200 or (bl[temp[i]] == '#'):
                for j in blockInd:
                    bl[j] = '#'
                discardRows = 0
                bl = ''.join(bl)
                nbl = ''
                for i in range(20):
                    currRow = bl[i * 10 : (i + 1) * 10]
                    if currRow == '#' * 10:
                        discardRows += 1
                    else:
                        nbl += currRow
                nbl = ' ' * 10 * discardRows + nbl
                
                return nbl, scoreDict[discardRows], discardRows
        
        
        for i in range(4):
            bl[temp[i]] = '#'
        blockInd = temp

def get_avg_height(boardString):
    return sum(get_depths(boardString)) / 10

def get_holes(boardString):
    depths = get_depths(boardString)
    holes = 0
    for i in range(10):
        for j in range(depths[i], 0, -1):
            if boardString[190 - j * 10 + i] == ' ':
                holes += 1
    return holes

def get_bumpiness(boardString):
    bumpiness = 0
    depths = get_depths(boardString)
    for i in range(9):
        bumpiness += abs(depths[i] - depths[i + 1])
    return bumpiness



def heuristic(board, strategy, cleared):
    if board == 'GAME OVER':
        return -(10 ** 10)
    a, b, c, d = strategy
    return a * get_avg_height(board) + b * get_holes(board) + c * get_bumpiness(board) + d * cleared


# def play_game(strategy):
#     board = ' ' * 200
#     points = 0
#     while True:
#         boards = []
#         piece = random.choice(list(pieceNames.keys()))
#         orientations = pieceNames[piece]
#         for orientation in orientations:
#             for i in range(10):
#                 nb = place_block(board, orientation, i)
#                 if nb == None:
#                     continue
#                 newBoard, scoreAddition, cleared = nb
#                 heapq.heappush(boards, ((-1) * heuristic(newBoard, strategy, cleared), newBoard, scoreAddition))
#         _, board, scoreAdd = heapq.heappop(boards)
#         if board == 'GAME OVER':
#             break
#         points += scoreAdd
#     return points

def play_game(strategy, printBoard=False):
    board = ' ' * 200
    points = 0
    bestBoard = ''
    bestLinesCleared = 0
    while board != 'GAME OVER':
        currMax = -float('inf')
        piece = random.choice(list(pieceNames.keys()))
        orientations = pieceNames[piece]
        for orientation in orientations:
            for i in range(10):
                nb = place_block(board, orientation, i)
                if nb == None:
                    continue
                newBoard, score, cleared = nb
                if newBoard == 'GAME OVER': continue
                h = heuristic(newBoard, strategy, cleared)
                if h > currMax:
                    currMax = h
                    bestBoard = newBoard
                    bestLinesCleared = cleared
        if board == bestBoard:
            break
        board = bestBoard
        points += scoreDict[bestLinesCleared]
        if printBoard:
            print_board(board)
            print('Points:', points)
    return points


def fitness(strategy):
    scores = []
    for _ in range(5):
        scores.append(play_game(strategy))
    return sum(scores) / 5

def tourneySort(t, popDict):
    tDict = {}
    for i in t:
        tDict[i] = popDict[i]
    return dict(sorted(tDict.items(), key=lambda x: x[1], reverse=True))

def get_next_gen(popDict):
    currGen = list(popDict.keys())
    nextGen = []
    i = 0
    # Clone
    popDict = dict(sorted(popDict.items(), key=lambda x: x[1], reverse=True))
    for temp in popDict.keys():
        nextGen.append(temp)
        i += 1
        if i > NUM_CLONES:
            break
    
    while len(nextGen) < POPULATION_SIZE:
        tournament = random.sample(currGen, TOURNAMENT_SIZE * 2)
        t1, t2 = tournament[:TOURNAMENT_SIZE], tournament[TOURNAMENT_SIZE:]
        st1, st2 = tourneySort(t1, popDict), tourneySort(t2, popDict)

        for i in st1.keys():
            if random.random() < TOURNAMENT_WIN_PROB:
                w1 = i
                break
            w1 = i
        
        for i in st2.keys():
            if random.random() < TOURNAMENT_WIN_PROB:
                w2 = i
                break
            w2 = i
        
        currChild = []
        index = random.randint(1, len(w1) - 1)
        for i in range(index):
            currChild.append(w1[i])
        for i in range(4 - index):
            currChild.append(w2[i + index])
        if random.random() < MUTATION_RATE:
            currChild[random.randint(0, len(currChild) - 1)] += random.uniform(-1, 1)
        
        if currChild not in nextGen:
            nextGen.append(currChild)
    nGenDict = {}
    for i in nextGen:
        nGenDict[tuple(i)] = fitness(i)
        print(i, '-->', nGenDict[tuple(i)])
    return nGenDict


def get_starting_pop():
    popDict = {}
    while len(popDict) < POPULATION_SIZE:
        child = []
        for i in range(4):
            child.append(random.uniform(-1, 1))
        if tuple(child) not in popDict.keys():
            popDict[tuple(child)] = (ft := fitness(tuple(child)) )
            print(child, '-->', ft)
    return popDict

def get_avg(gen):
    avg = 0
    for i in gen:
        avg += gen[i]
    return avg / len(gen)

def get_best(gen):
    best = None
    best_s = 0
    for i in gen.keys():
        if gen[i] > best_s:
            best_s = gen[i]
            best = i
    return best, best_s

best_strategy = (-1.26582441098394, 0.004064980432249232, -0.02265213681715017, -1.2729402391878066)

if __name__ == '__main__':
    s = input("(N)ew game or (L)oad game?")
    if s.lower() == 'n':
        gen = get_starting_pop()
    elif s.lower() == 'l':
        fn = input('filename: ')        
        with open(fn, 'rb') as f:
            gen = pickle.load(f)
        best = get_best(gen)
        print('best strategy: ', best[0])
        print('score: ', best[1])
    c = input('(P)lay, (S)ave, (C)ontinue, or (E)xit?')
    if c.lower() == 'p':
        play_game(best[0], printBoard=True)
    elif c.lower() == 's':
        fn = input('filename: ')
        with open(fn, 'wb') as f:
            pickle.dump((gen), f)
        exit()
    elif c.lower() == 'c':
        gen = get_next_gen(gen)
    elif c.lower() == 'e':
        exit()
    