from colorama import init, Back, Fore
import re, sys

init()

exp, flags = sys.argv[1][1:].split('/')

if len(flags) == 0:
    rexp = re.compile(exp)
elif len(flags) == 1:
    flag = flags[0]
    if flag == 'i':
        args = re.I
    elif flag == 's':
        args = re.S
    elif flag == 'm':
        args = re.M
    rexp = re.compile(exp, args)
else:
    flag, flags = flags[0], flags[1:]
    if flag == 'i':
        args = re.I
    elif flag == 's':
        args = re.S
    elif flag == 'm':
        args = re.M
    for flag in flags:
        if flag == 'i':
            args = args | re.I
        elif flag == 's':
            args = args | re.S
        elif flag == 'm':
            args = args | re.M
        
    rexp = re.compile(exp, args)


s = "While inside they wined and dined, safe from the howling wind.\nAnd she whined, it seemed, for the 100th time, into the ear of her friend,\nWhy indeed should I wind the clocks up, if they all run down in the end?"
spans = []


for result in rexp.finditer(s):
    spans.append(result.span())

prev = 0
n = True
highlight = ""

for i in range(len(spans)):
    (x, y) = spans[i]
    x = int(x)
    y = int(y)
    
    highlight += Back.RESET + s[prev:x]
    if prev != x or prev == x and x == 0:
        highlight += Back.LIGHTYELLOW_EX + s[x:y]
    elif prev == x and prev != 0 and n:
        highlight += Back.LIGHTCYAN_EX + s[x:y]
        n = False
    elif prev == x and not n: 
        highlight += Back.LIGHTYELLOW_EX + s[x:y]
        n = True
    prev = y


highlight += Back.RESET + s[y:len(s)]
print(highlight)
