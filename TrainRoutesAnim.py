
from time import perf_counter
import heapq
import sys
from math import pi , acos , sin , cos , inf
import tkinter as tk


root = tk.Tk()
canvas = tk.Canvas(root, height=900, width=900, bg='white')
lines = dict()

def calcd(node1, node2):
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees
   y1, x1 = node1
   y2, x2 = node2

   R   = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0

   # approximate great circle distance with law of cosines
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

ids = dict()
with open('rrNodeCity.txt', 'r') as f:
    for curr in f:
        ids[curr[8:].strip()] = curr.split()[0]
f.close()

pos = dict()
with open('rrNodes.txt', 'r') as f:
    for curr in f:
        info = curr.split()
        pos[info[0]] = (float(info[1]), float(info[2]))
f.close()

# for x in list(pos.keys())[0:10]:
#     print(x, pos[x])

start = perf_counter()
dists = dict()
with open('rrEdges.txt', 'r') as f:
    for curr in f:
        line = curr.split()
        s1, s2 = pos[line[0]], pos[line[1]]
        dist = calcd(s1, s2)
        if line[0] not in dists.keys():
            dists[line[0]] = [(line[1], dist)]
        else:
            dists[line[0]].append((line[1], dist))
        if line[1] not in dists.keys():
            dists[line[1]] = [(line[0], dist)]
        else:
            dists[line[1]].append((line[0], dist))
        
        currLine = canvas.create_line([(1400 - s1[1] * (-10), 850 - s1[0] * 10), (1400 - s2[1] * (-10), 850 - s2[0] * 10)], tag='background_line')
        lines[(line[0], line[1])] = currLine
        lines[(line[1], line[0])] = currLine
f.close()
end = perf_counter()



def Djikstra(city1, city2):
    s1, s2 = ids[city1], ids[city2]
    closed = set()
    start = (0, s1, [])
    fringe = []
    i = 0
    heapq.heappush(fringe, start)
    while fringe:
        curr = heapq.heappop(fringe)
        if curr[1] == s2:
            return curr[0], curr[-1]
            # return curr[3]
        if curr[1] not in closed:
            closed.add(curr[1])
            for child, dist in dists[curr[1]]:
                if child not in closed:
                    canvas.itemconfig(lines[(curr[1], child)], fill='red')
                    canvas.pack(expand=True)
                    d = curr[0] + dist
                    i += 1
                    if i % 300 == 0:
                        root.update()
                    tpath = curr[2].copy()
                    tpath.append(lines[(curr[1], child)])
                    heapq.heappush(fringe, (d, child, tpath))
    
    return None


def AStar(city1, city2):
    s1, s2 = ids[city1], ids[city2]
    closed = set()
    start = (0, 0, s1, [])
    fringe = []
    i = 0
    heapq.heappush(fringe, start)
    while fringe:
        curr = heapq.heappop(fringe)
        if curr[2] == s2:
            return curr[1], curr[-1]
            # return curr[3]
        if curr[2] not in closed:
            closed.add(curr[2])
            for child, dist in dists[curr[2]]:
                if child not in closed:
                    canvas.itemconfig(lines[(curr[2], child)], fill='blue')
                    canvas.pack(expand=True)
                    d = curr[1] + dist
                    i += 1
                    if i % 280 == 0:
                        root.update()
                    tpath = curr[3].copy()
                    tpath.append(lines[(curr[2], child)])
                    heapq.heappush(fringe, (d + calcd(pos[child], pos[s2]), d, child, tpath))

    return None

# c1 = sys.argv[1]
# c2 = sys.argv[2]
# s = perf_counter()
# a = Djikstra(c1, c2)
# e = perf_counter()
# s1 = perf_counter()
# b = AStar(c1, c2)
# e1 = perf_counter()

Djikstra(sys.argv[1], sys.argv[2])

for line in AStar(sys.argv[1], sys.argv[2])[1]:
    canvas.itemconfig(line, fill='green')
    root.update()


canvas.pack(expand=True)
root.update()
root.mainloop()

