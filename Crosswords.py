import sys; args = sys.argv[1:]
import time, math, random, re



alphabet = 'ETAOINSRHDLUCMFYWGPBVKXQJZ'
dictionary = args[0]
height, length = args[1].split('x')
height, length = int(height), int(length)
blocks = args[2]
puzzleDict = dict()
try:
    temp = args[3:]
    seedstrings = []   
    for seedstring in temp:
        data = seedstring.split('x')
        isVertical = data[0][0] == 'V'
        row = int(data[0][1:])
        string = ""
        for i in range(1, len(data[1])):
            if data[1].isnumeric():
                string = '#'
                col = int(data[1])
                break
            if not data[1][:i].isnumeric():
                break
            col = int(data[1][:i])
            string = data[1][i:]
        seedstrings.append((string, row, col, isVertical))

except IndexError:
    seeedstrings = None

def print_puzzle(puzzleDict):
    index = 0
    for key in puzzleDict.keys():
        if index % length == 0:
            print()
        if puzzleDict[key] == alphabet:
            print('-', end=' ')
        else:
            print(puzzleDict[key], end=' ')
        index += 1


def get_implied_blocks_dir_helper_row(puzzleDict, index, direction):
    if len(puzzleDict[index]) == 1 and puzzleDict[index] != '#':
        return None
    puzzleDict[index] = '#'
    wordLength = 0
    possBlocks = []
    currRow = index // length
    rowList = set(range(currRow * length, (currRow + 1) * (length)))
    while index in rowList:
        index += direction
        if not index in puzzleDict.keys() or index not in rowList:
            break
        if puzzleDict[index] == '#':
            break
        possBlocks.append(index)
        wordLength += 1
        
    if wordLength <= 2:
        for block in possBlocks:
            if len(puzzleDict[block]) == 1:
                return None
            puzzleDict[block] = '#'
        return puzzleDict, possBlocks
    return puzzleDict, []

def get_implied_blocks_dir_helper_col(puzzleDict, index, direction):
    if len(puzzleDict[index]) == 1 and puzzleDict[index] != '#':
        return None
    puzzleDict[index] = '#'
    wordLength = 0
    possBlocks = []
    currCol = index % length
    colList = {currCol}
    while currCol in puzzleDict.keys():
        colList.add(currCol)
        currCol += length
    
    while index in colList:
        index += direction * length
        if not index in puzzleDict.keys() or index not in colList:
            break
        if puzzleDict[index] == '#':
            break
        
        possBlocks.append(index)
        wordLength += 1
        
    if wordLength <= 2:
        for block in possBlocks:
            if len(puzzleDict[block]) == 1:
                return None
            puzzleDict[block] = '#'
        return puzzleDict, possBlocks
    return puzzleDict, []

def place_block_helper(puzzleDictArg, index):
    #checks all 4 directions and returns blocked squares
    #cleaner code
    puzzleDict = puzzleDictArg.copy()
    blocked = []
    try:
        puzzleDict, newBlocked = get_implied_blocks_dir_helper_row(puzzleDict, index, 1)
        blocked += newBlocked
        puzzleDict, newBlocked = get_implied_blocks_dir_helper_row(puzzleDict, index, -1)
        blocked += newBlocked
        puzzleDict, newBlocked = get_implied_blocks_dir_helper_col(puzzleDict, index, 1)
        blocked += newBlocked
        puzzleDict, newBlocked = get_implied_blocks_dir_helper_col(puzzleDict, index, -1)
        blocked += newBlocked
        return puzzleDict, blocked
    except:
        return None

def place_block(puzzleDictArg, index):
    placed = [index, length * height - index - 1]
    puzzleDict = puzzleDictArg.copy()
    while placed:
        curr = placed.pop()
        try:
            puzzleDict, blocked = place_block_helper(puzzleDict, curr)
        except:
            return None
        placed += blocked
    return puzzleDict

def check_failure(puzzleDict):
    if check_disconnect(puzzleDict):
        return True
    

def check_disconnect(puzzleDict):
    key = 0
    while puzzleDict[key] != '#':
        key += 1
    
# def area_fill(puzzleDictArg, index):
#     directions = [1, -1, length, (-1) * length]
#     puzzleDict = puzzleDictArg.copy()
    

def place_seedstrings(puzzleArg, seedstringList):
    puzzle = puzzleArg.copy()
    for seedstring in seedstringList:
        string, row, col, isVertical = seedstring
        for i in range(len(string)):
            puzzle[row * length + col] = string[i]
            if isVertical:
                row += 1
            else:
                col += 1
    
    for key in puzzle.keys():
        if puzzle[key] == '#':
            print(key)
            puzzle = place_block(puzzle, key)
    return puzzle


def create_puzzle(seedstringList):
    for i in range(length * height):
        puzzleDict[i] = alphabet
    return place_seedstrings(puzzleDict, seedstringList)

puzzleDict = create_puzzle(seedstrings)

print_puzzle(puzzleDict)