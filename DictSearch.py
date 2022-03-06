import sys, re

words = []
with open("wordlist.txt", 'r') as f:
    for line in f.readlines():
        words.append(line.strip().lower())

re1 = re.compile('(?=\w*a)(?=\w*e)(?=\w*i)(?=\w*o)(?=\w*u)(\w+)')
re2 = re.compile('([^aeiou]*[aieou][^aeiou]*){5})')
re3 = re.compile('(\w(?=\b))\1\w*?\1')
re4 = re.compile('(\w)(\w)(\w)\w*?\3\2\1')
re5 = re.compile('(^b^t)*?(bt|tb)(^b^t)*?')


