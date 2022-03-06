import sys

empty = ["0","1","2","3","4","5","6","7","8"]

def place(board,index,player):
    return board[:int(index)]+player+board[int(index)+1:]

def getNext(board,player):
    states = []
    for index in range(len(board)):
        if board[index]==".":
            states.append(board[:index]+player+board[index+1:])
    return states

def isOver(board):
    doneList = ["012","345","678","036","147","258","048","246"]
    for x in doneList:
        if board[int(x[0])]==board[int(x[1])]==board[int(x[2])] and board[int(x[0])]!=".":
            return True
    return False

def boardResult(board):
    doneList = ["012","345","678","036","147","258","048","246"]
    for x in doneList:
        if board[int(x[0])]==board[int(x[1])]==board[int(x[2])]:
            if board[int(x[0])]=="X":
                return 1
            if board[int(x[0])]=="O":
                return -1
    return 0

def printBoard(board):
    for x in range(3):
        print(board[x*3:x*3+3] + "   " + str(x*3) + str(x*3+1) + str(x*3+2))

def maxStep(board):
    if isOver(board):
        return boardResult(board)
    if board.count(".")==0:
        return 0
    results = []
    for nextBoard in getNext(board,"X"):
        results.append(minStep(nextBoard))
    return max(results)

def minStep(board):
    if isOver(board):
        return boardResult(board)
    if board.count(".")==0:
        return 0
    results = []
    for nextBoard in getNext(board,"O"):
        results.append(maxStep(nextBoard))
    return min(results)

def maxMove(board):
    results = {}
    maxIndex = 0
    maxValue = -2
    for nextBoard in getNext(board,"X"):
        spot = 0
        for index in range(len(board)):
            if nextBoard[index]!=board[index]:
                spot = index
        results[spot] = minStep(nextBoard)
    for key in results.keys():
        if results[key]>maxValue:
            maxIndex=key
            maxValue = results[key]
    return maxIndex

def minMove(board):
    results = {}
    minIndex = 0
    minValue = 2
    for nextBoard in getNext(board,"O"):
        spot = 0
        for index in range(len(board)):
            if nextBoard[index]!=board[index]:
                spot = index
        results[spot] = maxStep(nextBoard)
    for key in results.keys():
        if results[key]<minValue:
            minIndex=key
            minValue = results[key]
    return minIndex

def bestMove(board,player):
    if player=="O":
        return minMove(board)
    else: return maxMove(board)

def toString(empty):
    s = ""
    for index in empty:
        s+=index+", "
    return s[:len(s)-2]

def printResults(board,player):
    for index in empty:
        s = "Moving at " + str(index) + " results in a "
        if player == "X":
            result = minStep(place(board,index,player))
        else:
            result = maxStep(place(board,index,player))
        x = ""
        if result == 1:
            if player=="X": x = "win."
            else: x = "loss."
        if result == -1:
            if player=="X": x = "loss."
            else: x = "win."
        if result == 0:
            x = "tie."
        print(s+x)

def getTurn(board):
    if board.count("X")>board.count("O"):
        return "O"
    else: return "X"


board = "........."

for index in range(len(board)):
    if board[index] != ".":
        empty.remove(str(index))

player = getTurn(board)
if player == "X":
    me = "O"
else: me = "X"

turn = "2"

if board == ".........":
    player = input("Should I be X or O? ")
    if player == "O":
        turn = "1"
        me = "X"
while not isOver(board) and board.count(".")!=0:
    print("\nCurrent board:")
    printBoard(board)
    print()
    if turn == "1":
        choice = input("You can move to any of these spaces: " + toString(empty) + "." +"\nYour choice? ")
        board = place(board,choice,me)
        empty.remove(choice)
        turn = "2"
    elif turn == "2":
        printResults(board,player)
        best = bestMove(board,player)
        print("\nI choose space " + str(best) + ".")
        empty.remove(str(best))
        board = place(board,str(best),player)
        turn = "1"

print("\nCurrent board:")
printBoard(board)
print()

if boardResult(board) == 1 and player == "X" or boardResult(board) == -1 and player == "O":
    print("I win!")
elif boardResult(board) == 0:
    print("We tied!")
else:
    print("You win!")


            
