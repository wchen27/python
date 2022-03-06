import sys, re

words = []
with open(sys.argv[1], 'r') as f:
    for line in f.readlines():
        words.append(line.strip().lower())

vowels = 'aeiou'


exprs = []
exprs.append(r'(?=\w*a)(?=\w*e)(?=\w*i)(?=\w*o)(?=\w*u)\w+')
exprs.append(r'([^aeiou]*[aieou][^aeiou]*){5}')
exprs.append(r'(?!^(\w)\w*\1\w*\1$)(?=^(\w)\w*\1$)\w+')
exprs.append(r'(?=(\w)(\w)(\w)\w*)(?=\w*\3\2\1\b)\w+')
exprs.append(r'[^b^t]*?(bt|tb)[^b^t]*?')
exprs.append(r'\w*(\w)\1\w*')
exprs.append(r'\w*(\w)\w*\1\w*')
exprs.append(r'\w*(\w\w)\w*\1\w*')
exprs.append(r'\w*[^aeiou]\w*[^aeiou]\w*')
exprs.append(r'((?!(\w)\w*\2\w*\2\w*)\w)+')


def print_res(n):
    print('#' + str(n) + ' re.compile(' + exprs[n-1] + ')')
    matches = dict()
    curr = re.compile(exprs[n-1])
    for word in words:
        if bool(curr.fullmatch(word)):
            if len(word) in matches.keys():
                matches[len(word)].append(word)
            else:
                matches[len(word)] = [word]
    
    if n == 1:
        matched = matches[min(list(matches.keys()))]
        print(str(len(matched)), 'total matches.')
        for i in range(min(5, len(matched))):
            print(matched[i])
     
    elif n == 2 or n == 3 or n == 10:
        matched = matches[max(list(matches.keys()))]
        print(str(len(matched)), 'total matches.')
        for i in range(min(5, len(matched))):
            print(matched[i])

    elif n == 4 or n == 5:
        matched = []
        for key in matches.keys():
            matched += matches[key]
        matched.sort()
        print(len(matched), 'total matches.')
        for i in range(min(5, len(matched))):
            print(matched[i])
    
    elif n == 6:
        lenmatch = dict()
        matched = []
        for key in matches.keys():
            matched += matches[key]
        matched.sort()
        for word in matched:
            maxLen = -1
            count = 0
            for i in range(1,len(word)):
                if word[i] == word[i-1]:
                    count += 1
                    if count>maxLen:
                        maxLen = count
                else:
                    count = 0
            if maxLen in lenmatch.keys():
                lenmatch[maxLen].append(word)
            else:
                lenmatch[maxLen] = [word]

        matched = lenmatch[max(list(lenmatch.keys()))]
        print(len(matched), 'total matches.')
        for i in range(min(5, len(matched))):
            print(matched[i])
    
    elif n == 7:
        lenmatch = dict()
        matched = []
        for key in matches.keys():
            matched += matches[key]
        matched.sort()
        for word in matched:
            maxLen = -1
            count = 0
            for i in range(len(word)):
                if word.count(word[i])>maxLen:
                    maxLen = word.count(word[i])
            if maxLen in lenmatch.keys():
                lenmatch[maxLen].append(word)
            else:
                lenmatch[maxLen] = [word]

        matched = lenmatch[max(list(lenmatch.keys()))]
        print(len(matched), 'total matches.')
        for i in range(min(5, len(matched))):
            print(matched[i])

    elif n == 8:
        lenmatch = dict()
        matched = []
        for key in matches.keys():
            matched += matches[key]
        matched.sort()
        for word in matched:
            maxLen = -1
            count = 0
            for i in range(2,len(word)):
                if word.count(word[i-2 : i])>maxLen:
                    maxLen = word.count(word[i-2 : i])
            if maxLen in lenmatch.keys():
                lenmatch[maxLen].append(word)
            else:
                lenmatch[maxLen] = [word]

        matched = lenmatch[max(list(lenmatch.keys()))]
        print(len(matched), 'total matches.')
        for i in range(min(5, len(matched))):
            print(matched[i])

    elif n == 9:
        lenmatch = dict()
        matched = []
        for key in matches.keys():
            matched += matches[key]
        matched.sort()

        
        for word in matched:
            maxLen = -1
            count = 0
            for letter in word:
                if letter.lower() not in vowels:
                    count += 1
            if count > maxLen:
                maxLen = count
            
            if maxLen in lenmatch.keys():
                lenmatch[maxLen].append(word)
            else:
                lenmatch[maxLen] = [word]

        matched = lenmatch[max(list(lenmatch.keys()))]
        print(len(matched), 'total matches.')
        for i in range(min(5, len(matched))):
            print(matched[i])

    print()

for i in range(1, 11):
    print_res(i)