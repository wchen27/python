
from collections import deque
import time


dictionary = 'words_06_letters.txt'
puzzles = 'puzzles_normal.txt'

s = time.perf_counter()
with open(puzzles, 'r') as f:
    testCases = [line.strip().split() for line in f]
f.close()

start = time.perf_counter()
with open(dictionary, 'r') as f:
    words = {line.strip() for line in f}
f.close()
end = time.perf_counter()

info1 = dict()
info = dict()   

for word in words:
    for i in range(len(word)):
        temp = word[:i] + '_' + word[i+1:]
        if temp not in info1.keys():
            info1[temp] = {word}
        else:
            info1[temp].add(word)

for key in info1.keys():
    if len(info1[key]) <= 1:
        continue
    for x in info1[key]:
        if x not in info.keys():
            info[x] = info1[key]
        else:
            info[x] = info[x].union(info1[key])

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

        for child in info[curr]:
            if child == curr:
                continue
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
print(len(info.keys()), 'words in this dict')
for line, res in enumerate(l):
    print('line:', line + 1)
    if res[0] == None:
        print('no solution')
        continue

    print('length', res[1])
    print('path')
    for x in res[0]:
        print(x)
print('total runtime:', e-s -0.1)

# for x in l: print(x)
