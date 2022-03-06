import sys

compiled = dict()

# alphabet, expr = sys.argv[1:]
# alphabet = set(alphabet)
alphabet = {'a','b'}
alphabet.add('eps')

modifiers = {'*', '+', '?'}

def NFAe(exp):
    NFAe = {exp : (1,)}
    status = True
    while status:
        newNFAe = NFAe.copy()
        for key in NFAe.keys():
            if key not in alphabet:
                break
            return NFAe
        
        for key in NFAe.keys():
            currVal = NFAe[key]
            if '|' in key:
                del newNFAe[key]
                orSplit = key.split('|')
                for newKey in orSplit:
                    newNFAe[newKey] = currVal
            
            elif len(key) == 2 and key[-1] in modifiers:
                pass

        
        NFAe = newNFAe

print(NFAe('a|b'))
