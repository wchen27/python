
class Troll:
    global height, length, iq, n

    def __init__(self, n):
        self.height = calch(n)
        self.length = calcl(n)
        self.iq = calcq(n)
        self.n = n
    
    def getHeight(self):
        return self.height
    
    def getLength(self):
        return self.length
    
    def getIQ(self):
        return self.iq
    
    def getRatio(self):
        return self.iq/self.height
    

    
def calcr(n):
    return (((5**n) % (10**9 + 7)) % 101) + 50

def calch(n):
    return calcr(3*n)

def calcl(n):
    return calcr(3*n + 1)

def calcq(n):
    return calcr(3*n + 2)

def getRatio(n):
    return calcq(n)/calch(n)
# test = Troll(0)
# print(test.getHeight(), test.getLength(), test.getIQ())

N = 5
DN = (1/2)**(1/2) + sum(calch(n) for n in range(N))
print(DN)
trolls = {}
totalHeight = 0
totalIQ = 0


for i in range(N):
    totalHeight += Troll(i).getHeight()
    totalIQ += Troll(i).getIQ()
    trolls[Troll(i).getIQ()/Troll(i).getHeight()] = Troll(i)
    # trolls[i] = [calch[i], calcl[i], calcq[i]]

trolls = sorted(trolls.items()) # Sorted Dictionary (returns list of tuples)
print(totalHeight, totalIQ)




# Attempted start of brute-force solution
# possible = []
# for troll in trolls:
#     hsum = troll.getHeight() + troll.getLength()
#     for i in range(len(trolls) - 1):
#         pass
        
#         #for j in possible:
#           #  if .contains(troll):
#          #       possible.remove(j)
        
#         #print(t.getIQ() for t in possible)
        

# print(' '.join([str(troll.getHeight()) for troll in trolls]))
# print([troll.getIQ() for troll in trolls].index(max()))
# print(sum(troll.getIQ() for troll in trolls))


# Code that doesn't work
# # Greedy 
# This algorithm attempts to get out the highest IQ trolls first. Only works for small values of N. 

def greedy(ls):
    greedyIQ = 0
    currHeight = sum(troll.getHeight() for troll in ls)
    maxLength = (max(troll.getLength() for troll in ls))
    # print("Height: ", currHeight + maxLength, "length:", maxLength, "depth: ", DN)
    highestIQ = [troll.getIQ() for troll in ls].index(max(troll.getIQ() for troll in ls))
    # print("IQ: ", finalIQ)
    return highestIQ
# Shortest First

finalIQ = 0
while True:
    currHeight = sum(troll.getHeight() for troll in trolls)
    maxLength = (max(troll.getLength() for troll in trolls))
    bestRemove = greedy(trolls)
    finalIQ += (trolls.pop(bestRemove).getIQ())
    if currHeight + maxLength < DN:
        break

print(finalIQ)
        
'''
def shortest(ls):
    shortestIQ = 0
    currHeight = sum(troll.getHeight() for troll in ls)
    maxLength = (max(troll.getLength() for troll in ls))
    minHeight = [troll.getHeight() for troll in ls].index(min(troll.getHeight() for troll in ls))
    return minHeight

# Largest IQ/Height Ratio First


def ratio(ls):
    ratioIQ = 0
    currHeight = sum(troll.getHeight() for troll in ls)
    maxLength = (max(troll.getLength() for troll in ls))
    maxRatio = [troll.getRatio() for troll in ls].index(max(troll.getRatio() for troll in ls))
    return maxRatio




# while sum(troll[2] for troll in trolls.keys()) + max(troll[1] for troll in trolls.keys()) >= DN:
'''