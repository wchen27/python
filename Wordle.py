import sys
from turtle import update
from colorama import init, Back
import random, re
init()

with open("wordle_guesses.txt", 'r') as f:
    guesses = {line.strip() for line in f.readlines()}
f.close()

with open('wordle_answers.txt', 'r') as f:
    answers = [line.strip() for line in f.readlines()]
f.close()
guesses = set.union(set(answers), guesses)

def color(currWord, colors):
    colWord = ""
    for i in range(len(currWord)):
        colWord += Back.RESET
        if colors[i] == 'G':
            colWord += Back.GREEN + currWord[i]
        elif colors[i] == 'Y':
            colWord += Back.YELLOW + currWord[i]
        else:
            colWord += Back.RESET + currWord[i]
    try:
        colWord += Back.RESET
    except:
        pass
    return colWord

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
            #k2[i] += Back.RESET
    return k2


def get_bucket(guess, word):
    yellowWord = []
    currBucket = ['X', 'X', 'X', 'X', 'X']
    for i in range(len(word)):
        if word[i] == guess[i]:
            currBucket[i] = 'G'
        else:
            yellowWord.append(word[i])
    for i in range(len(currBucket)):
        if currBucket[i] == 'G':
            continue
        if guess[i] in yellowWord:
            currBucket[i] = 'Y'
            yellowWord.remove(guess[i])
    return ''.join(currBucket)


def update_answers(guess):
    buckets = dict()
    for word in answers:
        currBucket = get_bucket(guess, word)
        if currBucket in buckets.keys():
            buckets[currBucket].add(word)
        else:
            buckets[currBucket] = {word}

    maxSize = -1
    maxBucket = ''
    if len(list(buckets.keys())) == 1:
        return [guess], 'GGGGG'
    for bucket in buckets.keys():
        if (size := len(buckets[bucket])) > maxSize:
            if bucket == 'GGGGG': continue
            maxSize = size
            maxBucket = bucket

    return list(buckets[maxBucket]), maxBucket

def pick_bucket(guess, pick):
    global answers
    buckets = dict()
    for word in answers:
        currBucket = get_bucket(guess, word)
        if currBucket in buckets.keys():
            buckets[currBucket].add(word)
        else:
            buckets[currBucket] = {word}
    answers = buckets[pick]
    return buckets[pick]

if sys.argv[1] == '1':
    with open(sys.argv[2], 'r') as f:
        lines = [line.strip().split() for line in f.readlines()]
    for line in lines:
        answers = pick_bucket(line[0].lower(), line[1])
    for ans in answers:
        print(ans)

# update_answers('terns')
# update_answers('aphid')
# update_answers('quick')
# update_answers('bight')
# update_answers('mazey')
# update_answers('foamy')
# update_answers('loamy')



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
    print("|\t   Absurdle\t     |")
    print("|                            |")
    for i in range(max(5, len(guess))):
        try:
            print("|           " + full[i] + "            |")
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
    # if tries < 5:
    currWord = input("Guess a word: ")
    # for i in range(len(currWord)):
    #     if currWord[i] == word[i]:
    #         colWord += Back.GREEN + word[i] + Back.RESET
    #         corr.append(word[i])
    #     elif currWord[i] in word:
    #         colWord += Back.YELLOW + currWord[i] + Back.RESET
    #         half.append(currWord[i])
    #     else:
    #         colWord += Back.RESET + currWord[i] + Back.RESET
    #         wrong.append(currWord[i])
    # full.append(colWord)
    # guess.append(colWord)
    if currWord not in guesses:
        print('Not a valid guess.')
        continue
    answers, maxBucket = update_answers(currWord)
    for i in range(5):
        if maxBucket[i] == 'G':
            corr.append(currWord[i])
        elif maxBucket[i] == 'Y':
            half.append(currWord[i])
        else:
            wrong.append(currWord[i])
    colWord = color(currWord, maxBucket)
    full.append(colWord)
    guess.append(colWord)
    if maxBucket == 'GGGGG':
        status = False
        print("------------------------------")
        print("|\t   Absurdle\t     |")
        print("|                            |")
        for i in range(max(5, len(guess))):
            try:
                print("|           " + full[i] + "            |")
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
    tries += 1
    


print()

if status:
    print("Sorry! u suck")
else:
    print("You got the word in " + str(len(guess)) + " tries!")

