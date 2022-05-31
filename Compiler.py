import sys

compiled = dict()

# alphabet, expr = sys.argv[1:]
# alphabet = set(alphabet)
alphabet = {'a','b'}
alphabet.add('eps')

modifiers = {'*', '+', '?'}

def split(exp):

    dfae = dict()
    dfae[0] = {exp : 1}

    # split on or
    orBranches = exp.split('|')
    if len(orBranches) > 1:
        dfae = {0 : {}}
        for branch in orBranches:
            dfae[0][branch] = 1

    currNode = 2

    return dfae


print(split('ab|b'))
