import sys


def print_table():
    table = '*'
    for char in alphabet:
        table += '\t' + char
    for key in DFA.keys():
        table += '\n' + str(key) + '\t'
        for char in alphabet:
            if char in DFA[key].keys():
                table += str(DFA[key][char])
            else:
                table += '_'
            table += '\t'
    print(table)

def process(string):
    currState = '0'
    for char in string:
        if char not in DFA[currState].keys():
            return False
        currState = DFA[currState][char]
    return currState in final


try:
    problem = int(sys.argv[1]) - 1
    
    alphabet1 = 'ab'
    dfa1 = {
        '0' : {'a' : '1'},
        '1' : {'a' : '2'}, 
        '2' : {'b' : '3'}
    }
    final1 = ['3']

    alphabet2 = '012'
    dfa2 = {
        '0' : {'0' : '0', '1' : '1', '2' : '0'},
        '1' : {'0' : '0', '1' : '1', '2' : '0'}
    }
    final2 = ['1']

    alphabet3 = 'abc'
    dfa3 = {
        '0' : {'a' : '0', 'b' : '1', 'c' : '0'},
        '1' : {'a' : '1', 'b' : '1', 'c' : '1'}
    }
    final3 = ['1']

    alphabet4 = '01'
    dfa4 = {
        '0' : {'0' : '1', '1' : '0'},
        '1' : {'0' : '0', '1' : '1'}
    }
    final4 = ['0']

    alphabet5 = '01'
    dfa5 = {
        '0' : {'0' : '2', '1' : '1'},
        '1' : {'0' : '3', '1' : '0'},
        '2' : {'0' : '0', '1' : '3'}, 
        '3' : {'0' : '1', '1' : '2'}
    }
    final5 = ['0']

    alphabet6 = 'abc'
    dfa6 = {
        '0' : {'a' : '1', 'b' : '0', 'c' : '0'},
        '1' : {'a' : '1', 'b' : '2', 'c' : '0'},
        '2' : {'a' : '1', 'b' : '0', 'c' : '3'},
        '3' : {'a' : '3', 'b' : '3', 'c' : '3'}
    }
    final6 = ['0', '1', '2']

    alphabet7 = '01'
    dfa7 = {
        '0' : {'0' : '0', '1' : '1'},
        '1' : {'0' : '2', '1' : '1'},
        '2' : {'0' : '2', '1' : '3'},
        '3' : {'0' : '2', '1' : '4'},
        '4' : {'0' : '4', '1' : '4'}
    }
    final7 = ['4']

    DFAList = [(alphabet1, dfa1, final1), (alphabet2, dfa2, final2), (alphabet3, dfa3, final3), (alphabet4, dfa4, final4), (alphabet5, dfa5, final5), (alphabet6, dfa6, final6), (alphabet7, dfa7, final7)]
    with open(sys.argv[2]) as f:
        lines = f.readlines()
    
    alphabet, DFA, final = DFAList[problem]
    print_table()
    print('Final nodes:', final)

    for line in lines:
        line = line.strip()
        res = process(line)
        print(res, line)
    
except:
    with open(sys.argv[1], 'r') as f:
        lines = f.read().split('\n\n')
        info, nodes = lines[0], lines[1:]

    alphabet, states, final = info.split('\n')
    final = final.split()
    DFA = dict()

    for node in nodes:
        nodeInfo = node.split('\n')
        currNodeDict = dict()
        if len(nodeInfo) == 1:
            DFA[nodeInfo[0]] = currNodeDict
            continue
        nodeName, children = nodeInfo[0], nodeInfo[1:]
        for child in children:
            childName, childDestination = child.split()
            currNodeDict[childName] = childDestination
        DFA[nodeName] = currNodeDict


    print_table()
    print('Final nodes:', final)


    with open(sys.argv[2], 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        res = process(line)
        print(res, line)


