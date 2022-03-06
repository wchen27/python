
from collections import deque

def board_to_list(boardString):
    board = []
    for i in range(6):
        curr = []
        for j in range(i * 6, i * 6 + 6):
            curr.append(boardString[j])
        board.append(curr)

    return board

def list_to_board(boardList):
    board = ''
    for l in boardList:
        board += ''.join(l)
    return board

def solved(boardString):
    boardList = board_to_list(boardString)
    row = boardList[2]
    ind = row.index('A') + 2
    for i in range(ind, 6):
        if row[i] != '.':
            return False, None
    boardList[2][ind - 2], boardList[2][ind - 1] = '.', '.'
    boardList[2][-1], boardList[2][-2] = 'A', 'A'
    return True, list_to_board(boardList)

def copy_board(boardList):
  return [x[:] for x in boardList]

def print_board(boardString):
    for i in range(6):
        j = i * 6
        print(boardString[j:j+6])


start = dict()

def get_info(boardString):
    boardList = board_to_list(boardString)
    done = set()
    
    done.add('.')
    for r in range(6):
        for c in range(6):
            curr = boardList[r][c]
            if curr not in done:
                done.add(curr)
                
                isVertical = False
                if c + 1 > 5 or boardList[r][c+1] != curr:
                    isVertical = True
                length = 0
                if isVertical:
                    x = r
                    while x < 6 and boardList[x][c] == curr:
                        length += 1
                        x += 1
                else:
                    x = c
                    while x < 6 and boardList[r][x] == curr:
                        length += 1
                        x += 1
                start[curr] = (r, c, length, isVertical)

    return start

def make_move(boardString, char, dist):
    boardList = board_to_list(boardString)
    r, c, length, isVertical = start[char]
    if isVertical:
        er = r + length - 1
        nr = r + dist
        ner = er + dist
        if dist < 0:
            legal = True
            if nr < 0:
                legal = False
            for i in range(nr, r):
                if boardList[i][c] != '.':
                    legal = False
                    break
            
            if legal:
                for i in range(r, er + 1):
                    boardList[i][c] = '.'
                for i in range(nr, ner + 1):
                    boardList[i][c] = char
                
                return list_to_board(boardList)
        if dist > 0:
            legal = True
            if ner > 5:
                legal = False
            for i in range(er + 1, ner + 1):
                if boardList[i][c] != '.':
                    legal = False
                    break
            
            if legal:
                for i in range(r, er + 1):
                    boardList[i][c] = '.'
                for i in range(nr, ner + 1):
                    boardList[i][c] = char
                
                return list_to_board(boardList)

    else:
        ec = c + length - 1
        nc = c + dist
        nec = ec + dist
        if dist < 0:
            legal = True
            if nc < 0:
                legal = False
            for i in range(nc, c):
                if boardList[r][i] != '.':
                    legal = False
                    break
            
            if legal:
                for i in range(c, ec + 1):
                    boardList[r][i] = '.'
                for i in range(nc, nec + 1):
                    boardList[r][i] = char
                
                return list_to_board(boardList)
        if dist > 0:
            legal = True
            if nec > 5:
                legal = False
            for i in range(ec + 1, nec + 1):
                if boardList[r][i] != '.':
                    legal = False
                    break
            
            if legal:
                for i in range(c, ec + 1):
                    boardList[r][i] = '.'
                for i in range(nc, nec + 1):
                    boardList[r][i] = char
                
                return list_to_board(boardList)


    return None


def get_children(boardString):
    info = get_info(boardString)
    children = set()
    for car in info.keys():
        possible = [0, 1, 2, 3, 4, 5]
        dists = set()
        r, c, length, isVertical = info[car]
        if isVertical:
            er = r + length - 1
            for i in possible[:r]:
                dists.add(i - r)
            for i in possible[er + 1:]:
                dists.add(i - er)
            for i in dists:
                if (x := make_move(boardString, car, i)) != None:
                    children.add(x)

        else:
            
            ec = c + length - 1
            for i in possible[:c]:
                dists.add(i - c)
            for i in possible[ec + 1:]:
                dists.add(i - ec)
            for i in dists:
                if (x := make_move(boardString, car, i)) != None:
                    children.add(x)

        
    return children



test = [['B', 'C', 'D', 'D', 'D', 'F'], 
        ['B', 'C', '.', '.', 'E', 'F'], 
        ['H', 'A', 'A', '.', 'E', 'G'], 
        ['H', 'I', 'I', '.', 'E', 'G'], 
        ['.', '.', 'J', '.', '.', '.'], 
        ['K', 'K', 'J', 'L', 'L', '.']]


teststr = list_to_board(test)


def BFS(n):
    if solved(n)[0]:
        return n
    fringe = deque()
    visited = set()
    fringe.append((n, 0, []))
    visited.add(n)
    while len(fringe) > 0:
        curr, depth, path = fringe.popleft()
        if(solved(curr)[0]):
            length = depth
            path.append(curr)
            path.append(solved(curr)[1])
            return path, length + 1
        for child in get_children(curr):
            if child not in visited:
                npath = path.copy()
                npath.append(curr)
                fringe.append((child, depth + 1, npath))
                visited.add(child)

    return None


print(BFS(teststr)[1], '\n')
for state in BFS(teststr)[0]:
    print_board(state)
    print()


# get_info(teststr)
# print_board(make_move(teststr, 'B', 1))


# for child in (get_children(list_to_board(test))):
#     print_board(child)
#     print()
