from collections import deque


name = input("Enter file name: ")
with open(name, 'r') as f:
	lines = [l.strip() for l in f]
f.close()



def build_board(puzzleString):
	s = ''
	length, puzzle = int(puzzleString.split()[0]), puzzleString.split()[1]
	for i in range(length):
		for j in range(length):
			s += puzzle[i * length + j] + ' '
		s += '\n'
	return s


def print_puzzle(puzzleString):
	print(build_board(puzzleString))

def find_goal(puzzleString):
	length, puzzle = int(puzzleString.split()[0]), puzzleString.split()[1]
	return ''.join(sorted(puzzle))[1:] + '.'

def goal_test(puzzleString):
	length, puzzle = int(puzzleString.split()[0]), puzzleString.split()[1]
	return True if puzzle == find_goal(puzzleString) else False

def get_children(puzzleString):
	length, puzzle = int(puzzleString.split()[0]), puzzleString.split()[1]
	clear = puzzle.find('.')
	legalMoves = [] # indices of legal moves
	abv, blw, nxt, lst = clear - length, clear + length, clear + 1, clear - 1
	if abv >= 0:
		legalMoves.append(abv)
	if blw < length ** 2:
		legalMoves.append(blw)
	if nxt < length ** 2 and nxt % length > clear % length:
		legalMoves.append(nxt)
	if lst >= 0 and lst % length < clear % length:
		legalMoves.append(lst)

	# return list of legal board positions
	legalPositions = []
	for move in legalMoves:
		temp = [c for c in puzzle]
		temp[clear], temp[move] = temp[move], temp[clear]
		legalPositions.append(str(length) + ' ' + ''.join(temp))

	return legalPositions

# BFS algorithm

def exhaustiveBFS(puzzleString):
	length, puzzle = int(puzzleString.split()[0]), puzzleString.split()[1]
	visited = set()
	queue = deque()
	visited.add(puzzleString)
	queue.append(puzzleString)
	
	while len(queue) > 0:
		curr = queue.popleft()
		for neighbor in get_children(curr):
			if neighbor not in visited:
			    visited.add(neighbor)
			    queue.append(neighbor)
	
	return visited

def solutionBFS(puzzleString):
    if goal_test(puzzleString):
        return 0
    length, puzzle = int(puzzleString.split()[0]), puzzleString.split()[1]
    visited = set()
    queue = deque()
    paths = {}
    path = [str(length) + ' ' + find_goal(puzzleString)]
    visited.add(puzzleString)
    paths[puzzleString] = (puzzleString, 0)
    queue.append(puzzleString)
	
    while len(queue) > 0:
        curr = queue.popleft()
        if goal_test(curr):
            while paths[curr][1] != 0:
                # print_puzzle(paths[curr][0])
                path.append(paths[curr][0])
                curr = paths[paths[curr][0]][0]
                if curr != puzzleString:
                    # print_puzzle(curr)
                    path.append(curr)
                
            
        for neighbor in get_children(curr):
            if neighbor not in paths:
                paths[neighbor] = (curr, paths[curr][1] + 1)
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    if puzzleString not in path:
        path.append(puzzleString)
    return path[::-1]

for puzzle in lines:
    print(len(solutionBFS(puzzle)) - 1)
    