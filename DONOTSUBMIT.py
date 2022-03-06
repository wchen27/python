from collections import deque
import time
import sys



# "4 7 7x4"
# "2 3 1x2 2x2"
# "18 9 3x11 5x7 4x8 6x10 1x2"
# "4 8 4x1 1x6 1x3 3x1 1x3 1x3 6x1 1x4"
# "11 12 3x6 2x5 4x10 7x9 1x1"
# "9 18 3x8 5x10 4x11 6x7 1x2"
# "13 14 4x5 3x8 6x11 7x10 2x1"
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
puzzle = sys.argv[1].split()
puzzleHeight = int(puzzle[0])
puzzleWidth = int(puzzle[1])
rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]
board = ""
pairDict = {}

def printBoard(board,height,width):
    for h in range(height):
        s = ""
        for w in range(width):
            s+=board[h*width+w]+" "
        print(s) 

def getNext(state):
    return state.index(".")

def getRemaining(state,y):
    used = set()
    for i in state:
        if i != ".":
            used.add(i)
    for x in used:
        (height,width) = pairDict[x]
        y.remove((x,height,width))
    return y

def getChildren(state,var):
    values = []
    temp = rectangles.copy()
    remaining = getRemaining(state,temp)
    for pair in remaining:
        (code,height,width) = pair
        if width+int(var%puzzleWidth)>puzzleWidth or height+int(var/puzzleWidth)>puzzleHeight:
            continue
        else:
            newState = list(state)
            for x in range(height):
                for y in range(width):
                    if state[var+x*puzzleWidth+y] ==".":
                        newState[var+x*puzzleWidth+y] = code
                    else:
                        continue
            values.append("".join(newState))
    for pair in remaining:
        (code,width,height) = pair
        if width+int(var%puzzleWidth)>puzzleWidth or height+int(var/puzzleWidth)>puzzleHeight:
            continue
        else:
            newState = list(state)
            for x in range(height):
                for y in range(width):
                    if state[var+x*puzzleWidth+y] ==".":
                        newState[var+x*puzzleWidth+y] = code
                    else:
                        continue
            values.append("".join(newState))
    return values

def printSolution(state):
    for key in pairDict.keys():
        index = state.index(key)
        temp = index
        (height,width) = pairDict[key]
        width1 = 0
        while temp<len(state) and state[temp] == key:
            width1+=1
            temp+=1
        if width1 != width:
            height = width
            width = width1
        s = str(int(index/puzzleWidth)) + " " + str(int(index%puzzleWidth)) + " " + str(height) + " " + str(width)
        print(s)

def BFS(board):
    visited = set()
    fringe = deque()
    fringe.append(board)
    visited.add(board)
    while len(fringe) != 0:
        currBoard = fringe.pop()
        if currBoard.count(".") == 0:
            return currBoard
        children = getChildren(currBoard,currBoard.index("."))
        for child in children:
            if child not in visited:
                fringe.append(child)
                visited.add(child)
    return None

area = 0
for i in rectangles:
    (height,width) = i
    area += height*width
if area != puzzleHeight*puzzleWidth:
    print("Containing rectangle incorrectly sized.")
else:
    
    for i in range(puzzleWidth*puzzleHeight):
        board += "."
    for i in range(len(rectangles)):
        (height,width) = rectangles[i]
        rectangles[i] = (letters[i],height,width)
        pairDict[letters[i]] = (height,width)
    solution = BFS(board)
    printBoard(solution, puzzleHeight, puzzleWidth)
    if solution == None:
        print("No solution.")
    else:
        printSolution(solution)