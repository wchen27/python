import sys
from time import perf_counter
words = set()
dictionaryName = sys.argv[1]
minLength = int(sys.argv[2])
wordlist = []
endwords = set()

try:
    currentWord = sys.argv[3]
except IndexError:
    currentWord = ""

with open(dictionaryName, 'r') as f:
    for line in f.readlines():
        curr = line.strip().upper()
        currLen = len(currentWord)
        if curr.isalpha() and len(curr)>currLen and curr[:currLen] == currentWord:
            if len(curr) >= minLength:
                endwords.add(curr)
                words.add(curr)
                wordlist.append(curr)

def possible_next_words(curr,wl):
    temp = []
    currLen = len(curr)
    if currLen == 0:
        return (set('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),wordlist)
    for w in wl:
        if len(w)>len(curr) and w[:currLen] == curr:
            temp.append(w)
    pw = set()
    for w in temp: 
        if w[:currLen] == curr:
            if len(w) == len(curr) + 1:
                continue
            cw = w[:len(curr) + 1]
            if cw in words and len(cw)>=minLength:
                continue
            if w[len(curr)] == cw[-1]:
                pw.add(cw)
    return (list(pw),temp)

def max_step(word,wl):
    (nextWordSet,nwl) = possible_next_words(word,wl)
    if (len(word) >= minLength and (word in endwords)):
        return (word,1)
    elif (len(nextWordSet) == 0):
        return (word,-1)
    results = []
    for next_word in nextWordSet:
        results.append((min_step(next_word,nwl)))
    maxVal = -1
    finalW = ""
    for result in results:
        (w,val) = result
        finalW = w
        if val>maxVal:
            maxVal = val
            break
    return (finalW,maxVal)

def min_step(word,wl):
    (nextWordSet,nwl) = (possible_next_words(word,wl))
    if (len(word) >= minLength and (word in endwords)):
        return (word,-1)
    elif (len(nextWordSet) == 0):
        return (word,1)
    results = []
    for next_word in nextWordSet:
        results.append(max_step(next_word,nwl))
    minVal = 1
    finalW = ""
    for result in results:
        (w,val) = result
        finalW = w
        if val<minVal:
            minVal = val
            break
    return (finalW,minVal)

def print_results(word):
    (nextWords,wl) = possible_next_words(word,wordlist)
    successful = set()
    for nextWord in nextWords:
        (word,res) = max_step(nextWord,wl)
        print(word)
        if (len(word)-len(currentWord)+3)%3!=0:
            successful.add(nextWord[-1])
    if successful == set():
        print('Next player will lose!')
    else:
        successful = list(successful)
        successful.sort()
        print('Next player can win with any of these letters: ', (successful))


print_results(currentWord)