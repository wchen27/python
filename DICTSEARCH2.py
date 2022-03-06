from cmath import inf
import sys
import re

with open("words_all.txt") as f:
       words = [line.strip() for line in f]

def printSolution(r,flag,num):
    print("#"+num+" re.compile("+r+", "+flag+")")
    matched = []
    for word in words:
        exp = bool(re.compile(r, re.I).match(word))
        if exp:
            matched.append(word.lower())
    print(str(len(matched)) + " total matches")
    if len(matched)<5:
        for match in matched:
            print(match)
    else:
        for i in range(5):
            print(matched[i].lower())
    print()
        
#1
print("#1 "+ "re.compile("+"(?=.*a.*)(?=.*e.*)(?=.*i.*)(?=.*o.*)(?=.*u.*).+"+", "+"i"+")")
matches = []
for word in words:
    if bool(re.compile("(?=.*a.*)(?=.*e.*)(?=.*i.*)(?=.*o.*)(?=.*u.*).+", re.I).match(word)):
        matches.append(word.lower())
x = inf        
for match in matches:
    if len(match)<x:
        x = len(match)
count = 0
shortMatch = []
for match in matches:
    if len(match) == x:
        shortMatch.append(match)
print(str(len(shortMatch))+ " total matches")
if len(shortMatch)<5:
        for match in shortMatch:
            print(match.lower())
else:
    for i in range(5):
        print(shortMatch[i].lower())
print()

#2
print("#2 "+ "re.compile("+"([b-df-hj-np-tv-z]*[aeiou][b-df-hj-np-tv-z]*){5}"+", "+"i"+")")
matches = []
for word in words:
    if bool(re.compile("([b-df-hj-np-tv-z]*[aeiou][b-df-hj-np-tv-z]*){5}", re.I).fullmatch(word)):
        matches.append(word.lower())
x = 0       
for match in matches:
    if len(match)>x:
        x = len(match)
count = 0
shortMatch = []
for match in matches:
    if len(match) == x:
        shortMatch.append(match)
print(str(len(shortMatch))+ " total matches")
if len(shortMatch)<5:
        for match in shortMatch:
            print(match.lower())
else:
    for i in range(5):
        print(shortMatch[i].lower())
print()

#3
print("#3 "+ "re.compile("+r"(?!(\w)\w*\1\w*\1)(?=(\w)\w*\1)\w+"+", "+"i"+")")
matches = []
for word in words:
    if bool(re.compile(r"(?!^(\w)\w*\1\w*\1$)(?=^(\w)\w*\1$)\w+", re.I).fullmatch(word)):
        matches.append(word.lower())
x = 0       
for match in matches:
    if len(match)>x:
        x = len(match)
count = 0
shortMatch = []
for match in matches:
    if len(match) == x:
        shortMatch.append(match)
print(str(len(shortMatch))+ " total matches")
if len(shortMatch)<5:
        for match in shortMatch:
            print(match.lower())
else:
    for i in range(5):
        print(shortMatch[i].lower())
print()
#4
printSolution(r"(?=(.)(.)(.).*)(?=.*\3\2\1\b).+","i","4")
#5
printSolution("(?!.*b.*b)(?!.*t.*t)(.*bt.*|.*tb.*)","i","5")
#6
print("#6 "+ "re.compile("+r"^\w*(\w)\1\w*$"+", "+"i"+")")
matches = []
for word in words:
    if bool(re.compile(r"^\w*(\w)\1\w*$", re.I).match(word)):
        matches.append(word.lower())
maxLen = 2
for word in matches:
    count = 0
    for i in range(1,len(word)):
        if word[i] == word[i-1]:
            count += 1
            if count>maxLen:
                maxLen = count
        else:
            count = 0
x = []
for word in matches:
    count = 0
    for i in range(1,len(word)):
        if word[i] == word[i-1]:
            count += 1
            if count == maxLen and word not in x:
                x.append(word)
        else:
            count = 0
print(str(len(x))+" total matches")  
if len(x)>5:
    for i in range(5):
        print(x[i].lower())
else:
    for word in x:
        print(word.lower())
print()
#7
print("#7 "+ "re.compile("+r"^\w*(\w)\w*\1\w*$"+", "+"i"+")")
matches = []
for word in words:
    if bool(re.compile(r"^\w*(\w)\w*\1\w*$", re.I).match(word)):
        matches.append(word.lower())

maxLen = 2
for word in matches:
    for i in range(len(word)):
        if word.count(word[i])>maxLen:
            maxLen = word.count(word[i])
m = []
for word in matches:
    for i in range(len(word)):
        if word.count(word[i])==maxLen and word not in m:
            m.append(word)
print(str(len(m))+" total matches")  
if len(m)>5:
    for i in range(5):
        print(m[i].lower())
else:
    for word in m:
        print(word.lower())
print()

#8
print("#8 "+ "re.compile("+r"^\w*(\w\w)\w*\1\w*$"+", "+"i"+")")
matches = []
for word in words:
    if bool(re.compile(r"^\w*(\w\w)\w*\1\w*$", re.I).match(word)):
        matches.append(word.lower())
maxLen = 2
for word in matches:
    for i in range(2,len(word)):
        if word.count(word[i-2:i])>maxLen:
            maxLen = word.count(word[i-2:i])

m = []
for word in matches:
    for i in range(2,len(word)):
        if word.count(word[i-2:i])==maxLen and word not in m:
            m.append(word)
print(str(len(m))+" total matches")  
if len(m)>5:
    for i in range(5):
        print(m[i].lower())
else:
    for word in m:
        print(word.lower())
print()
#9
print("#9 "+ "re.compile("+r"^\w*[qwrtypsdfghjklzxcvbnm]\w*[qwrtypsdfghjklzxcvbnm]\w*$"+", "+"i"+")")
matches = []
for word in words:
    if bool(re.compile(r"^\w*[qwrtypsdfghjklzxcvbnm]\w*[qwrtypsdfghjklzxcvbnm]\w*$", re.I).match(word)):
        matches.append(word.lower())

v = "aeiou"
maxLen = 2
for word in matches:
    for letter in word:
        if letter.lower() not in v:
            count+=1
    if count>maxLen:
        maxLen = count
    count = 0

m = []

for word in matches:
    for letter in word:
        if letter.lower() not in v:
            count+=1
    if count == maxLen:
        m.append(word)
    count = 0

print(str(len(m)) + " total matches")
if len(m)>5:
    for i in range(5):
        print(m[i].lower())
else:
    for word in m:
        print(word.lower())
print()

#10
print("#10 "+ "re.compile("+r"^((?!(\w)\w*\2\w*\2\w*)\w)+$"+", "+"i"+")")
matches = []
for word in words:
    if bool(re.compile(r"^((?!(\w)\w*\2\w*\2\w*)\w)+$", re.I).match(word)):
        matches.append(word.lower())

x = 0       
for match in matches:
    if len(match)>x:
        x = len(match)
count = 0
shortMatch = []
for match in matches:
    if len(match) == x:
        shortMatch.append(match)
print(str(len(shortMatch))+ " total matches")
if len(shortMatch)<5:
    for match in shortMatch:
        print(match)
else:
    for i in range(5):
        print(shortMatch[i].lower())