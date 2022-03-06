
from collections import deque
import time, sys

# dictionary = sys.argv[1]
# puzzles = sys.argv[2]
dictionary = 'words_06_letters.txt'
puzzles = 'puzzles_normal.txt'
s = time.perf_counter()
with open(puzzles, 'r') as f:
    testCases = [line.strip().split() for line in f]
f.close()

info = dict()
vowels = 'aeiou'
alphabet = 'aeioubcdfghjklmnpqrstvwxyz'
def get_children(s):
    children = set()
    for i in range(len(s)):
        for char in alphabet:
            temp = s[:i] + char + s[i+1:]
            if temp in words and temp != s:
                children.add(temp)
    return children


start = time.perf_counter()
with open(dictionary, 'r') as f:
    words = {line.strip() for line in f}
f.close()
end = time.perf_counter()


def BFS2(start, end):
    if start == end:
        return [start], 0
    fringe = deque()
    visited = set()
    fringe.append((start, 0, []))
    visited.add(start)
    while len(fringe) > 0:
        curr, depth, path = fringe.popleft()
        if(curr == end):
            length = depth
            path.append(end)
            return path, length + 1
        
        if curr not in info.keys():
            info[curr] = get_children(curr)

        for child in info[curr]:
            if child not in visited:
                npath = path.copy()
                npath.append(curr)
                fringe.append((child, depth + 1, npath))
                visited.add(child)

        

    return None, 0

l = []
for i, case in enumerate(testCases):
    l.append((BFS2(case[0], case[1])))
e = time.perf_counter()
print('time to generate data structure:', end-start)
print(len(words), 'in this dict')
for line, res in enumerate(l):
    print('line:', line)
    if res[0] == None:
        print('no solution')
        continue

    print('length', res[1])
    print('path')
    for x in res[0]:
        print(x)
print('total runtime:', e-s)
print(get_children('abased'))
# for x in l: print(x)
