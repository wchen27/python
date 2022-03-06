import sys, random, heapq, pickle, re, time


POPULATION_SIZE = 100
NUM_CLONES = 40
TOURNAMENT_SIZE = 10
TOURNAMENT_WIN_PROB = .6
CROSSOVER_LOCATIONS = 1
MUTATION_RATE = 0.2
STRATEGY_LENGTH = 3

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


pieces = {
    'I0' : ([1, 1, 1, 1], [0, 0, 0, 0]),
    'I1' : ([4], [0]),
    'O0' : ([2, 2], [0, 0]),
    'T0' : ([1, 2, 1], [0, 0, 0]),
    'T1' : ([3, 1], [0, -1]),
    'T2' : ([1, 2, 1],[-1, 0, -1]),
    'T3' : ([1, 3], [-1, 0]),
    'S0' : ([1, 2, 1], [0, 0, -1]),
    'S1' : ([2, 2], [-1, 0]),
    'Z0' : ([1, 2, 1], [-1, 0, 0]),
    'Z1' : ([2, 2], [0, -1]),
    'J0' : ([2, 1, 1], [0, 0, 0]),
    'J1' : ([3, 1], [0, -2]),
    'J2' : ([1, 1, 2], [-1, -1, 0]),
    'J3' : ([1, 3], [0, 0]),
    'L0' : ([1, 1, 2], [0, 0, 0]),
    'L1' : ([3, 1], [0, 0]),
    'L2' : ([2, 1, 1], [0, -1, -1]),
    'L3' : ([1, 3], [-2, 0])
}

# piecesIndex = {
#     'I0' : [0, 1, 2, 3],
#     'I1' : [0, 10, 20, 30],
#     'O0' : [0, 1, 10, 11],
#     'T0' : [1, 10, 11, 12],
#     'T1' : [0, 10, 11, 20],
#     'T2' : [0, 1, 2, 11],
#     'T3' : [1, 10, 11, 21],
#     'S0' : [1, 2, 10, 11],
#     'S1' : [0, 10, 11, 21],
#     'Z0' : [0, 1, 11, 12],
#     'Z1' : [1, 10, 11, 20],
#     'J0' : [0, 10, 11, 12],
#     'J1' : [0, 1, 10, 20],
#     'J2' : [0, 1, 2, 12],
#     'J3' : [1, 11, 20, 21],
#     'L0' : [2, 10, 11, 12],
#     'L1' : [0, 10, 20, 21],
#     'L2' : [0, 1, 2, 10],
#     'L3' : [0, 1, 11, 21]
# }

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

def get_depth(boardString):
    depths = []
    for i in range(10):
        curr = 0
        while boardString[curr * 10 + i] != '#':
            curr += 1
        depths.append(20 - curr)

    return depths

# test = sys.argv[1]

def place(board, height, width, depth):
    board = list(board)
    for i in range(height):
        board[190 - 10 * depth - 10 * i + width] = '#'
    
    return ''.join(board)

def place_block(board, block, boardDepths):
    ch, cd = pieces[block]
    boards = []
    
    for i in range(11 - len(ch)):
        currGameOver = False
        currBoard = board
        diff = []
        for d in range(len(cd)):
            diff.append(cd[d] + boardDepths[d + i])
        m = max(diff)

        for d in range(len(cd)):
            if ch[d] + m - cd[d] > 20:
                currGameOver = True
        
        if currGameOver:
            boards.append(('GAME OVER', (-10 ** 9)))
            continue
        
        for h in range(len(ch)):
            currBoard = place(currBoard, ch[h], h + i, m - cd[h])
        
        discardRows = 0
        nbl = ""
        for i in range(20):
            currRow = currBoard[i * 10 : (i + 1) * 10]
            if currRow == '#' * 10:
                discardRows += 1
            else:
                nbl += currRow
        nbl = ' ' * 10 * discardRows + nbl
        boards.append((nbl, scoreDict[discardRows]))
    return boards
    

test = "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"






# hole = re.compile(r"# *(#|$)")
# def heuristic(board, strategy):
#     a, b, c = strategy
#     score = 0
#     rows = to_list(board)
#     cols = to_col_list(board)
#     for i in range(20):
#         if '#' in rows[i]:
#             score += a * i
#     score += max([col.find('#') for col in cols]) * b
#     holes = 0
#     for col in cols:
#         if hole.search(col) != None:
#             holes += 1
#     score += holes * c

#     return score


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
#                 newBoard, scoreAddition = nb
#                 heapq.heappush(boards, ((-1) * heuristic(board, strategy), newBoard, scoreAddition))
#         _, board, scoreAdd = heapq.heappop(boards)
#         if board == 'GAME OVER':
#             break
#         points += scoreAdd
#     return points



# def fitness(strategy):
#     scores = []
#     for _ in range(5):
#         scores.append(play_game(strategy))
#     return sum(scores) / 5

# def generate_starting_pop():
#     pop = dict()
#     while len(list(pop.keys())) < POPULATION_SIZE:
#         strategy = []
#         for _ in range(STRATEGY_LENGTH):
#             strategy.append(random.uniform(-1, 1))
        
#         pop[tuple(strategy)] = fitness(strategy)
#     return pop

# def create_tournament(pop):
#     popList = []
#     for key, val in pop.items():
#         popList.append((val, key))
#     tournamentPop = random.sample(popList, TOURNAMENT_SIZE * 2)
#     random.shuffle(tournamentPop)
#     p1 = tournamentPop[:TOURNAMENT_SIZE]
#     p2 = tournamentPop[TOURNAMENT_SIZE:]
#     p1.sort() ; p2.sort()
#     while p1:
#         if random.random() < TOURNAMENT_WIN_PROB:
#             p1winner = p1.pop()
#             break
#         p1winner = p1.pop()

#     while p2:
#         if random.random() < TOURNAMENT_WIN_PROB:
#             p2winner = p2.pop()
#             break
#         p2winner = p2.pop()
#     return p1winner[1], p2winner[1]

# def breed(p1, p2):
#     child = [''] * len(p1)
#     crossovers = random.sample(list(range(len(p1))), CROSSOVER_LOCATIONS)
#     for i in crossovers:
#         child[i] = p1[i]

#     for letter in p2:
#         if letter in child:
#             continue
#         for i in range(len(child)):
#             if child[i] == '':
#                 child[i] = letter
#                 break


#     if random.random() < MUTATION_RATE:

#         s1 = random.randint(0, len(child) - 1)
#         child[s1] *= random.uniform(-1, 1)


#     return tuple(child)

# def get_next_generation(pop):
#     reversePop = {value : key for (key, value) in pop.items()}
#     reversePop = dict(sorted(reversePop.items(), reverse=True))
#     nextGen = dict()
#     i = 0
#     for key in reversePop.keys():
#         if i >= NUM_CLONES:
#             break
#         nextGen[reversePop[key]] = key
#         i += 1
    
#     while len(list(nextGen.keys())) < POPULATION_SIZE:
#         p1, p2 = create_tournament(pop)
#         child = breed(p1, p2)
#         if child in nextGen.keys():
#             continue
#         nextGen[child] = fitness(child)
    
#     return nextGen

# def get_best(pop):
#     reversePop = {value : key for (key, value) in pop.items()}
#     reversePop = dict(sorted(reversePop.items()))
#     for key in reversed(list(reversePop.keys())):
#         print(reversePop[key], key)
#         return [reversePop[key]], key

# def get_avg(gen):
#     avg = 0
#     for key in gen.keys():
#         avg += gen[key]
#     print('gen', 'pop avg', avg/POPULATION_SIZE)

# currGen = None

# while True:
#     choice = input('(C)reate new, (S)ave, (L)oad, (G)enerate next, or (E)xit: ').lower()
#     if choice == 'c':
#         currGen = generate_starting_pop()

#     elif choice == 's':
#         if currGen == None:
#             print('No generation to store!')
#             sys.exit()
#         f = input('File name: ')
#         pickle.dump(currGen, open(f, 'wb'))

#     elif choice == 'l':
#         f = input('File name: ')
#         currGen = pickle.load(open(f, 'rb'))
    
#     elif choice == 'g':
#         currGen = get_next_generation(currGen)
    
#     elif choice == 'e':
#         sys.exit()
    
#     elif choice == 'get best':
#         get_best(currGen)



s = time.perf_counter()
res = []
depths = get_depth(test)
for p in pieces.keys():
    boards = place_block(test, p, depths)
    for newBoard, s in boards:
        if newBoard != None: res.append(newBoard)

with open('tetrisout.txt', 'w') as f:
    for r in res:
        f.write(r + '\n')

print(time.perf_counter() - s)


# currGen = generate_starting_pop()
# for _ in range(100):
#     currGen = get_next_generation(currGen)

# f = input('File name: ')
# pickle.dump(currGen, open(f, 'wb'))

