
import time
start = time.time()

# Global Variables
N = 1000
trolls = []
totalTrollHeight = 0
reach = 300 # reach is at most 300 because of the first troll to escape

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
    
# Functions to calculate r, height, length, and IQ
    
def calcr(n):
    return (((5**n) % (10**9 + 7)) % 101) + 50

def calch(n):
    return calcr(3*n)

def calcl(n):
    return calcr(3*n + 1)

def calcq(n):
    return calcr(3*n + 2)

# def getRatio(n): # unused function for finding iq/height ratio
#     return calcq(n)/calch(n)

# test = Troll(0)
# print(test.getHeight(), test.getLength(), test.getIQ())

totalHeight = 0
totalIQ = 0

def generate_data(n):
    trollData = []
    for i in range(n):
        trollData.append((Troll(i).getHeight(), Troll(i).getLength(), Troll(i).getIQ()))
    totalHeight = sum(x[0] for x in trollData)
    DN = totalHeight/(2 ** (1/2))
    return (trollData, totalHeight, DN)

problemInfo = generate_data(N)

for i in range(N):
    trolls.append(Troll(i))

def dp(n):
    trolls, totalHeight, DN = problemInfo
    # Sort trolls by l + h:
    trolls.sort(key=lambda x: x[0] + x[1])
    maxHeight = int(totalHeight + reach - DN)

    # initialize array for dynamic programming
    arr = []
    for i in range(n + 1):
        arr.append([0] * (maxHeight + 1))
    
    # dynamic programming algorithm from 0/1 knapsack problem
    for i in range(n + 1):
        currHeight, currLength, currIQ = trolls[i - 1]
        newMaxHeight = maxHeight - (reach - currHeight - currLength)
        for j in range(newMaxHeight + 1):
            nonEscapingIQ = arr[i-1][j] # gets previous IQ if troll doesn't escape
            escapingIQ = -1 # to be changed if escape

            if j >= currHeight:
                escapingIQ = arr[i-1][j-currHeight] + currIQ
            
            arr[i][j] = max(nonEscapingIQ, escapingIQ)
    
    # return array when done for processing
    return arr

# old code (only works for small values of N):
def greedy(ls):
    greedyIQ = 0
    currHeight = sum([troll.getHeight() for troll in ls])
    maxLength = (max(troll.getLength() for troll in ls))
    # print("Height: ", currHeight + maxLength, "length:", maxLength, "depth: ", DN)
    highestIQ = [troll.getIQ() for troll in ls].index(max(troll.getIQ() for troll in ls))
    # print("IQ: ", finalIQ)
    return highestIQ

finalIQ = 0
DN = (1/2)**(1/2) + sum(calch(n) for n in range(N))
while True:
    currHeight = sum(troll.getHeight() for troll in trolls)
    maxLength = (max(troll.getLength() for troll in trolls))
    bestRemove = greedy(trolls)
    finalIQ += (trolls.pop(bestRemove).getIQ())
    if currHeight + maxLength < DN:
        break

# get answers

currArr = dp(N)
dynamic = [max(x) for x in currArr]
dynamicAns = max(dynamic)
print(max(dynamicAns, finalIQ))

# time 
print((time.time() - start), "seconds")


    
