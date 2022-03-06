import sys
from collections import deque
import time

# You are given code to read in a puzzle from the command line.  The puzzle should be a single input argument IN QUOTES.
# A puzzle looks like this: "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4"
# The code below breaks it down:
puzzle = sys.argv[1].split()
puzzle_height = int(puzzle[0])
puzzle_width = int(puzzle[1])
rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]
# puzzle_height is the height (number of rows) of the puzzle
# puzzle_width is the width (number of columns) of the puzzle
# rectangles is a list of tuples of rectangle dimensions



# INSTRUCTIONS:
#
# First check to see if the sum of the areas of the little rectangles equals the big area.
# If not, output precisely this - "Containing rectangle incorrectly sized."
#
currSize = 0
for rectangle in rectangles:
    currSize += rectangle[0] * rectangle[1]

namedRectangles = dict()
pieces = dict()
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

if currSize != (puzzle_height * puzzle_width):
    print("Containing rectangle incorrectly sized.")
    sys.exit()
board = '.' * (puzzle_height  * puzzle_width)

for i in range(len(rectangles)):
    namedRectangles[i] = (alphabet[i], rectangles[i][0], rectangles[i][1])
    pieces[alphabet[i]] = (rectangles[i][0], rectangles[i][1])

# Then try to solve the puzzle.
# If the puzzle is unsolvable, output precisely this - "No solution."
#


def print_board(board, h, w):
    for i in range(h):
        curr = ''
        for j in range(w):
            curr += board[i * w + j] + ' '
        print(curr)

def get_next_unassigned_var(board):
    return board.find('.')

def get_possible_next_boards(board, space):
    children = []
    rect = namedRectangles.copy()
    visited = set()
    for char in board:
        if not char == '.':
            visited.add(char)
    
    for s in visited:
        (h, w) = pieces[s]
        del rect[alphabet.find(s)]
    
    for rectangle in rect.keys():
        letter, h, w = rect[rectangle]
        if int(w + space % puzzle_width) > puzzle_width or int(h + space // puzzle_width) > puzzle_height:
            continue
        newBoard = list(board)
        for x in range(h):
            for y in range(w):
                if board[space + x * puzzle_width + y] == '.':
                    newBoard[space + x * puzzle_width + y] = letter

        children.append(''.join(newBoard))    
    
    for rectangle in rect.keys():
        letter, w, h = rect[rectangle]
        if int(w + space % puzzle_width) > puzzle_width or int(h + space // puzzle_width) > puzzle_height:
            continue
        newBoard = list(board)
        for x in range(h):
            for y in range(w):
                if board[space + x * puzzle_width + y] == '.':
                    newBoard[space + x * puzzle_width + y] = letter

        children.append(''.join(newBoard)) 

    return children

def BFS(start):
    visited = set()
    fringe = deque()
    fringe.append(start)
    visited.add(start)
    while fringe:
        currBoard = fringe.pop()
        if currBoard.count('.') == 0:
            return currBoard
        for child in get_possible_next_boards(currBoard, currBoard.find('.')):
            if child not in visited:
                fringe.append(child)
                visited.add(child)
    
    return None


def csp_backtracking(state):
    if state.find('.') == -1:
        return state
    var = state.find('.')
    for board in get_possible_next_boards(state, var):
        result = csp_backtracking(board)
        if result != None:
            return result
    return None


# If the puzzle is solved, output ONE line for EACH rectangle in the following format:
# row column height width
# where "row" and "column" refer to the rectangle's top left corner.
#
# For example, a line that says:
# 3 4 2 1
# would be a rectangle whose top left corner is in row 3, column 4, with a height of 2 and a width of 1.
# Note that this is NOT the same as 3 4 1 2 would be.  The orientation of the rectangle is important.
#
# Your code should output exactly one line (one print statement) per rectangle and NOTHING ELSE.
# If you don't follow this convention exactly, my grader will fail.

solution = csp_backtracking(board)
start = time.perf_counter()
if solution == None:
    print('No solution.')

else:
    # print_board(solution, puzzle_height, puzzle_width)
    if len(rectangles) == 1:
        print('0 0', puzzle_height, puzzle_width)
        sys.exit()
    
    for key in pieces.keys():
        i = solution.index(key)
        h, w = pieces[key]
        temp = 0
        s = str(i // puzzle_width) + ' ' + str(i % puzzle_width)
        while i < len(solution) and solution[i] == key:
            temp += 1
            i += 1
        if temp != w:
            h = w
            w = temp
        s += ' ' + str(h) + ' ' + str(w)
        print(s)
print('Total runtime:', time.perf_counter() - start)