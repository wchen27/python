from cmath import inf
import sys
import random
from colorama import init, Back, Fore
init()

with open("wordle_answers.txt") as x:
    answers = [line.strip() for line in x]

def color(currWord, word):
    colWord = ""
    for i in range(len(currWord)):
        colWord += Back.RESET
        if currWord[i] == word[i]:
            colWord += Back.GREEN + word[i]
        elif currWord[i] in word:
            colWord += Back.YELLOW + currWord[i]
        else:
            colWord += Back.RESET + currWord[i]
    return colWord

def newWords(words, guess):
    d = {}
    for word in words:
        bucket = getBucket(word,guess)
        if bucket in d.keys():
            d[bucket].append(word)
        else:
            d[bucket] = [word]
    maxLen = 0
    maxList = ""
    maxKey = ""
    for key in d.keys():
        if len(d[key])>=maxLen:
            maxLen = len(d[key])
            maxList = d[key]
            maxKey = key
    return maxList,maxKey

def getBucket(word, guess):
    bucket = ["X","X","X","X","X"]
    y = []
    for i in range(5):
        if word[i] == guess[i]:
            bucket[i] = "G"
        elif guess[i] in word:
            bucket[i] = "Y"
            if guess[i] not in y:
                y.append(guess[i])
    for letter in y:
        count = 0
        index = []
        for x in range(5):
            if guess[x] == letter:
                index.append(x)
        for i in index:
            if word[i] == letter or letter in word:
                count += 1
            if count>word.count(letter):
                bucket[i] = "X"
    return "".join(bucket)   

def updateK(corr,half,wrong):
    k = ["qwertyuiop","asdfghjkl","zxcvbnm"]
    k2 = ["","",""]
    for i in range(3):
        for letter in k[i]:
            k2[i] += Back.RESET
            if letter in corr:
                k2[i] += Back.GREEN + letter + Back.RESET + "  "
            elif letter in half: 
                k2[i] += Back.YELLOW + letter + Back.RESET + "  "
            elif letter in wrong:
                k2[i] += Back.RED + letter + Back.RESET + "  "
            else: 
                k2[i] += letter + Back.RESET + "  "
    return k2

def pick_bucket(guess, pick):
    global answers
    buckets = dict()
    for word in answers:
        currBucket = getBucket(word,guess)
        if currBucket in buckets.keys():
            buckets[currBucket].add(word)
        else:
            buckets[currBucket] = {word}
    answers = buckets[pick]
    return buckets[pick]
    
if sys.argv[1] == '1':
    try:
        with open(sys.argv[2], 'r') as f:
            lines = [line.strip().split() for line in f.readlines()]
        for line in lines:
            answers = pick_bucket(line[0].lower(), line[1])
        for ans in answers:
            print(ans)
    except:
        x = sys.argv[1]

def getBest(words):
    sVal = inf
    sGuess = ""
    for guess in words:
        answers, key = newWords(words, guess)
        if len(answers) < sVal:  
            sVal = len(answers)
            sGuess = guess
    return sGuess

with open("wordle_guesses.txt") as f:
    words = [line.strip() for line in f]
    words.sort()
with open("wordle_answers.txt") as x:
    answers = [line.strip() for line in x]
words = set.union(set(answers), words)

x = sys.argv[1]

if x == "2" or x == "3":
    keeb = "qwertyuiopasdfghjklzxcvbnm"
    corr = []
    half = []
    wrong = []
    full = [] 
    tries = 0
    guess = []
    status = True

    while status:
        print("------------------------------")
        print("|\t   Absurdle!\t     |")
        print("|                            |")
        for i in range(len(guess)):
            try:
                print("|            " + full[i] + (16-len(guess[i]))*" " +"|")
            except:
                print("|                            |")
        print("|                            |")
        k = updateK(corr,half,wrong)
        for i in range(3):
            if i == 0:
                print("|"+ k[i][:len(k[i])-2] + "|")
            if i == 1:
                print("| "+ k[i] + "|")
            if i == 2:
                print("|    "+ k[i] + "   |")
        print("------------------------------")
        colWord = ""
        if x == "2":
            currWord = input("Guess a word: ")
        if x == "3":
            currWord = getBest(answers)
            print("Word guessed by ai: " + str(currWord))
        if len(currWord) > 5:
            print("Invalid input: too long.")
        elif currWord not in words:
            print("Invalid input: not a word.")
        else:
            answers,key = newWords(answers,currWord)
            for i in range(len(currWord)):
                if key[i] == "G":
                    colWord += Back.GREEN + currWord[i] + Back.RESET
                    corr.append(currWord[i]) 
                elif key[i] == "Y":
                    colWord += Back.YELLOW + currWord[i] + Back.RESET
                    half.append(currWord[i])
                else:
                    colWord += Back.RESET + currWord[i] + Back.RESET
                    wrong.append(currWord[i])
            full.append(colWord)
            guess.append(currWord)
            tries += 1
        if len(answers) == 1 and currWord == answers[0]:
            status = False


    print()
    print("------------------------------")
    print("|\t    Absurdle!\t     |")
    print("|                            |")
    for i in range(len(guess)):
        try:
            print("|            " + full[i] + (16-len(guess[i]))*" " +"|")
        except:
            print("|                            |")
    print("|                            |")
    k = updateK(corr,half,wrong)
    for i in range(3):
        if i == 0:
            print("|"+ k[i][:len(k[i])-2] + "|")
        if i == 1:
            print("| "+ k[i] + "|")
        if i == 2:
            print("|    "+ k[i] + "   |")
    print("------------------------------")
    

    print("You guessed the word in " + str(tries) + " tries!")


        
