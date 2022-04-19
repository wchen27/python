from cmath import inf
import random
import time
import sys
import pickle

population = 10
clones = 2
tourneySize = 4
winProb = .75
mutation = .8

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

def printBoard(board,points):
    total = "-----------------------"
    for i in range(20):
        s = "| "
        for n in range(10):
            s+= board[i*10+n] + " "
        s+= "|"
        total += "\n" + s
    total += "\n-----------------------\nPoints: " + str(points)
    print(total)

def getDepth(board):
    allD = []
    for i in range(10):
        d = 0
        for x in range(20):
            if board[x*10+i] == " ":
                d+=1
            else:
                break
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
                over = True
        if over:
            allBoards.append(("over",0))
            continue
        for h in range(len(colH)):
            currBoard = place(currBoard,colH[h],i+h,maxDiff-colD[h])
        count = 0
        for x in range(20):
            if currBoard[x*10:(x+1)*10] == "##########":
                currBoard = "          " + currBoard[:x*10] + currBoard[(x+1)*10:]
                count+=1
        allBoards.append((currBoard,count))
    return allBoards

def swap(s):
    i1 = int(random.random()*len(s))
    i2 = int(random.random()*len(s))
    while i1 == i2:
        i2 = int(random.random()*len(s))
    temp = s[i1]
    s[i1] = s[i2]
    s[i2] = temp
    return s

def totalHeight(board):
    return sum(getDepth(board))

def numHoles(board):
    depth = getDepth(board)
    num = 0
    for i in range(10):
        for x in range(depth[i],0,-1):
            if board[190-x*10+i] == " ": 
                num += 1
    return num

def bumpiness(board):
    score = 0
    depths = getDepth(board)
    for i in range(9):
        score += abs(depths[i] - depths[i+1])
    return score

def heuristic(board, strategy, lines):
    a,b,c,d = strategy
    score = 0
    score += a*totalHeight(board)
    score += b*numHoles(board)
    score += c*bumpiness(board)
    score += d*lines
    return score

def playGame(strategy):
    board = " "*200
    points = 0
    best = ""
    bestLines = 0
    while board != "over":
        maxScore = -inf
        piece = random.choice(list(pieces.keys()))
        depths = getDepth(board)
        for orientation in pieces[piece].keys():
            for curr in addPiece(board,pieces[piece][orientation],depths):
                (currBoard, lines) = curr
                if currBoard == "over":
                    continue
                currH = heuristic(currBoard,strategy,lines)
                if currH>maxScore:
                    maxScore = currH
                    best = currBoard
                    bestLines = lines
        if board == best:
            board = "over"
        else:
            board = best
        if bestLines == 1: points += 40
        if bestLines == 2: points += 100
        if bestLines == 3: points += 300
        if bestLines == 4: points += 1200
    return points

def getPopulation(size):
    pop = []
    for i in range(size):
        a = random.random()*2-1
        b = random.random()*2-1
        c = random.random()*2-1
        d = random.random()*2-1
        pop.append((a,b,c,d))
    return pop

def fitness(strategy):
    scores = []
    for i in range(5):
        scores.append(playGame(strategy))  
    return sum(scores)/5

def getNextGen(genDict):
    nextGen = []
    i = 0
    for gi in genDict.keys():
        nextGen.append(gi)
        i+=1
        if i>clones:
            break

    while len(nextGen)<population:
        #Making tournament
        t1 = random.sample(gen,tourneySize)
        t2 = []
        while len(t2) < tourneySize:
            temp = random.choice(gen)    
            if temp not in t1: t2.append(temp)
        curr1 = {}
        for t in t1:
            curr1[t] = genDict[t]
        curr1 = dict(sorted(curr1.items(), key=lambda x: x[1],reverse=True))

        curr2 = {}
        for t in t2:
            curr2[t] = genDict[t]
        curr2 = dict(sorted(curr2.items(), key=lambda x: x[1],reverse=True))

        winner1 = []
        winner2 = []

        for t in curr1.keys():
            if random.random()<winProb:
                winner1 = t
                break
            winner1 = t

        for t in curr2.keys():
            if random.random()<winProb:
                winner2 = t
                break
            winner2 = t

        child = []

        index = int(random.random()*3)+1
        
        for x in range(index):
            child.append(winner1[x])
        
        for x in range(4-index):
            child.append(winner2[x+index])

        if random.random()<mutation:
            child[int(random.random()*3)+1] += random.random()*2

        if child not in nextGen:
            nextGen.append(tuple(child))
    return nextGen

def printGen(gen,g):
    genDict = {}
    n = 1
    total = 0
    for i in range(population):
        score = fitness(gen[i])
        print("Gen. " + str(g) + ": " + str(n) + " --> " + str(score))
        n+=1
        genDict[gen[i]] = score
        total += score
    genDict = dict(sorted(genDict.items(), key=lambda x: x[1],reverse=True))
    first = list(genDict.keys())[0]
    print("Best stretegy: " + str(first))
    print("Best score: " + str(genDict[first]))
    print("Avg. score: " + str(total/population))
    return genDict

def printGame(strategy):
    board = " "*200
    points = 0
    best = ""
    bestLines = 0
    while board != "over":
        printBoard(board,points)
        maxScore = -inf
        piece = random.choice(list(pieces.keys()))
        depths = getDepth(board)
        for orientation in pieces[piece].keys():
            for curr in addPiece(board,pieces[piece][orientation],depths):
                (currBoard, lines) = curr
                if currBoard == "over":
                    continue
                currH = heuristic(currBoard,strategy,lines)
                if currH>maxScore:
                    maxScore = currH
                    best = currBoard
                    bestLines = lines
        if board == best:
            board = "over"
        else:
            board = best
        if bestLines == 1: points += 40
        if bestLines == 2: points += 100
        if bestLines == 3: points += 300
        if bestLines == 4: points += 1200

end = False
#Getting a random population and ranking them
gen = []
g = 1
play = True
start = input("(N)ew process, or (L)oad saved process?")
if start.lower() == "n":
    gen = getPopulation(population)
    genDict = {}
if start.lower() == "l":
    filename = input("What filename?")
    infile = open(filename,"rb")
    genInfo = pickle.load(infile)
    infile.close()
    gen = genInfo[0]
    genDict = genInfo[1]
    g = genInfo[2]
    print("Generation: " + str(g))
    print("Best strategy so far: " + str(list(genDict.keys())[0]))
    g+=1
    play = False
while not end:
    if play:
        genDict = printGen(gen,g)
        gen = getNextGen(genDict) 
        g+=1
    m = input("(P)lay a game with current best strategy, (S)ave current progress, or (C)ontinue?")
    if m.lower() == "c":
        play = True
        continue
    if m.lower() == "p":
        printGame(list(genDict.keys())[0])
        play = False
    if m.lower() == "s":
        filename = input("What filename?")
        outfile = open(filename,"wb")
        pickle.dump([gen,genDict,g],outfile)
        end = True
