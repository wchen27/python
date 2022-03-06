import random, sys
from math import log

POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROB = .6
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = 0.8
NGRAMS_SIZE = 4



def encode(cipher, msg):
    msg = msg.upper()
    cipherDict = dict()
    for i in range(len(alphabet)):
        cipherDict[alphabet[i]] = cipher[i]
    enc = ""
    for char in msg:
        if char not in cipherDict.keys():
            enc += char
        else: 
            enc += cipherDict[char]
    return enc

def decode(cipher, msg):
    msg = msg.upper()
    cipherDict = dict()
    for i in range(len(alphabet)):
        cipherDict[cipher[i]] = alphabet[i]
    dec = ""
    for char in msg:
        if char not in cipherDict.keys():
            dec += char
        else: 
            dec += cipherDict[char]
    return dec

alphabet = 'ETAOINSHRDLCUMWFGYPBVKXJQZ'
cipher = list(alphabet)
random.shuffle(cipher)
cipher = ''.join(cipher)

ngrams = dict()
with open('ngrams.txt', 'r') as f:
    lines = [line.strip().split() for line in f.readlines()]
    for line in lines:
        ngrams[line[0]] = int(line[1])
f.close()

def fitness(n, cipher, msg):
    score = 0
    decMsg = decode(cipher, msg)
    for i in range(len(msg) - n - 1):
        curr = decMsg[i : i + n]
        if not curr.isalpha() or curr not in ngrams.keys():
            continue
        score += log(ngrams[curr], 2)
    return score

encoded = sys.argv[1]

def hill_climb(start, msg):
    cipher = start
    currScore = -1
    currMsg = msg
    while True:
        s1 = random.choice(list(range(len(alphabet))))
        s2 = random.choice(list(range(len(alphabet))))
        if s1 == s2:
            s2 = random.choice(list(range(len(alphabet))))
        tempcipher = list(cipher)
        tempcipher[s1], tempcipher[s2] = tempcipher[s2], tempcipher[s1]
        tempcipher = ''.join(tempcipher)
        score = fitness(1, tempcipher, currMsg)
        if score > currScore:
            decMsg = decode(cipher, currMsg)
            print(decMsg)
            currScore = score
            cipher = tempcipher
        
def generate_starting_pop():
    pop = dict()
    while len(list(pop.keys())) < POPULATION_SIZE:
        cipher = list(alphabet)
        random.shuffle(cipher)
        pop[''.join(cipher)] = fitness(NGRAMS_SIZE, ''.join(cipher), encoded)
    return pop

def create_tournament(pop):
    popList = []
    for key, val in pop.items():
        popList.append((val, key))
    tournamentPop = random.sample(popList, TOURNAMENT_SIZE * 2)
    random.shuffle(tournamentPop)
    p1 = tournamentPop[:TOURNAMENT_SIZE]
    p2 = tournamentPop[TOURNAMENT_SIZE:]
    p1.sort() ; p2.sort()
    while p1:
        if random.random() < TOURNAMENT_WIN_PROB:
            p1winner = p1.pop()
            break
        p1winner = p1.pop()

    while p2:
        if random.random() < TOURNAMENT_WIN_PROB:
            p2winner = p2.pop()
            break
        p2winner = p2.pop()
    return p1winner[1], p2winner[1]

def breed(p1, p2):
    child = [''] * len(p1)
    crossovers = random.sample(list(range(len(p1))), CROSSOVER_LOCATIONS)
    for i in crossovers:
        child[i] = p1[i]

    for letter in p2:
        if letter in child:
            continue
        for i in range(len(child)):
            if child[i] == '':
                child[i] = letter
                break


    if random.random() < MUTATION_RATE:

        s1 = random.randint(0, len(alphabet) - 1)
        s2 = random.randint(0, len(alphabet) - 1)
        while s2 == s1:
            s2 = random.randint(0, len(alphabet) - 1)
        child[s1], child[s2] = child[s2], child[s1]


    return ''.join(child)

def get_next_generation(pop):
    reversePop = {value : key for (key, value) in pop.items()}
    reversePop = dict(sorted(reversePop.items(), reverse=True))
    nextGen = dict()
    i = 0
    for key in reversePop.keys():
        if i >= NUM_CLONES:
            break
        nextGen[reversePop[key]] = key
        i += 1
    
    while len(list(nextGen.keys())) < POPULATION_SIZE:
        p1, p2 = create_tournament(pop)
        child = breed(p1, p2)
        if child in nextGen.keys():
            continue
        nextGen[child] = fitness(NGRAMS_SIZE, child, encoded)
    
    return nextGen

def get_best(pop):
    reversePop = {value : key for (key, value) in pop.items()}
    reversePop = dict(sorted(reversePop.items()))
    for key in reversed(list(reversePop.keys())):
        return [reversePop[key]], key

def get_avg(gen, i):
    avg = 0
    for key in gen.keys():
        avg += gen[key]
    print('gen', i, 'pop avg', avg/POPULATION_SIZE)


start = generate_starting_pop()

nextGen = get_next_generation(start)
for i in range(500):
    nextGen = get_next_generation(nextGen)
    print(i)
    print(get_best(nextGen))
    print(decode(get_best(nextGen)[0][0], encoded))
    print()

# print(nextGen)

# # print(get_best(nextGen))
# print(decode(get_best(nextGen)[0][0], encoded))
