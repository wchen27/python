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



board = "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"
pieces = {
            "I":{
                "0":([1,1,1,1],[0,0,0,0]),
                "1":([4],[0])
            },
            "O":{
                "0":([2,2],[0,0])
            },
            "T":{
                "0":([1,2,1],[0,0,0]),
                "1":([3,1],[0,-1]),
                "2":([1,2,1],[-1,0,-1]),
                "3":([1,3],[-1,0])
            },
            "S":{
                "0":([1,2,1],[0,0,-1]),
                "1":([2,2],[-1,0])
            },
            "Z":{
                "0":([1,2,1],[-1,0,0]),
                "1":([2,2],[0,-1])
            },
            "J":{
                "0":([2,1,1],[0,0,0]),
                "1":([3,1],[0,-2]),
                "2":([1,1,2],[-1,-1,0]),
                "3":([1,3],[0,0])
            },
            "L":{
                "0":([1,1,2],[0,0,0]),
                "1":([3,1],[0,0]),
                "2":([2,1,1],[0,-1,-1]),
                "3":([1,3],[-2,0])
            }
        }

def printBoard(board):
    for i in range(20):
        print(board[i*10:(i+1)*10])

def getDepth(board):
    allD = []
    for i in range(10):
        d = 0
        while board[d*10+i] == " ":
            d+=1
        allD.append(20-d)
    return allD

def place(b,h,w,d):
    b = list(b)
    for i in range(h):
        b[190-10*d-10*i+w] = "#"
    return "".join(b)

def addPiece(board,piece,depths):
    allBoards = []
    (colH,colD) = piece
    for i in range(11-len(colH)):
        currBoard = board
        diff = []
        over = False
        for d in range(len(colD)):
            diff.append(colD[d]+depths[d+i])
        maxDiff = max(diff)
        for d in range(len(colD)):
            if colH[d]+maxDiff-colD[d]>20:
                
                allBoards.append("over")
                continue
        for h in range(len(colH)):
            currBoard = place(currBoard,colH[h],i+h,maxDiff-colD[h])
        for x in range(20):
            if currBoard[x*10:(x+1)*10] == "##########":
                currBoard = "          " + currBoard[:x*10] + currBoard[(x+1)*10:]
        allBoards.append(currBoard)
    return allBoards

start = time.perf_counter()
depths = getDepth(board)
with open("tetrisout.txt","w") as f:
    for key1 in pieces.keys():
        for key2 in pieces[key1].keys():
            for b in addPiece(board,pieces[key1][key2],depths):
                if b != "over":
                    f.write(b+ "\n") 
                else:
                    f.write("GAME OVER\n")            
end = time.perf_counter()
print(end-start)


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
