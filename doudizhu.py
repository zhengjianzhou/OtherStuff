import random

pai_char = '3456789XJQKA2'*4+'&@'
pai_color = 'R'*13+'B'*13+'F'*13+'C'*13+'--'
pai_grade = range(13)*4 + [13,14]
pai = zip(pai_char,pai_color, pai_grade)

PLAYERS_INIT = {
    3: ((0,17), (17,34), (34, 51), (51,55)),
    4: ((0,12), (12,24), (24, 36), (36,48), (48,55)),
}

def fenpai(p, nop):
    random.shuffle(p)
    slots = PLAYERS_INIT[nop]
    return [sorted(p[s[0]:s[1]], key=lambda x:x[2]) for s in slots]

p4 = fenpai(pai, 4)
p3 = fenpai(pai, 3)

for i in p3: print [''.join(x[:2]) for x in i]
for i in p4: print [''.join(x[:2]) for x in i]

def groupings(p):
    g2 = [(p[i], p[i+1]) for i,_ in enumerate(p) if i < len(p) - 1 and p[i][0] == p[i+1][0]]
    g3 = [(p[i], p[i+1], p[i+2]) for i,_ in enumerate(p) if i < len(p) - 2 and p[i][0] == p[i+1][0] and p[i][0] == p[i+2][0]]
    g4 = [(p[i], p[i+1], p[i+2], p[i+3]) for i,_ in enumerate(p) if i < len(p) - 3 and p[i][0] == p[i+1][0] and p[i][0] == p[i+2][0] and p[i][0] == p[i+3][0]]
    l4 = [] #to be added
    return g2,g3,g4

gs = groupings(p3[0])

for i in gs: print ['|'.join([''.join(x[:2]) for x in ii]) for ii in i]

'''
### Run OUTPUT ###
['3R', '4B', '4C', '5F', '6F', '6R', '6B', '7C', '8C', '8R', 'XF', 'QC', 'AC', 'AR', 'AF', '2B', '@-']
['4F', '5B', '5R', '8B', '9F', '9C', '9B', 'XR', 'JF', 'JB', 'QR', 'QF', 'KR', 'KB', 'KF', 'AB', '2F']
['3C', '3F', '4R', '5C', '6C', '7R', '7B', '7F', '9R', 'XC', 'JR', 'JC', 'QB', 'KC', '2C', '2R', '&-']
['3B', '8F', 'XB']
['3F', '4F', '8R', '9B', '9F', 'XF', 'JR', 'JC', 'JB', 'QF', 'QC', 'AF']
['3R', '4C', '5C', '7C', '7B', 'QR', 'KC', 'KB', 'AC', '2R', '2B', '@-']
['3C', '4B', '4R', '5B', '6F', '8C', '9R', '9C', 'XR', 'JF', 'KR', 'AB']
['3B', '5F', '5R', '6R', '6B', '7R', '7F', '8B', 'XB', 'QB', 'KF', '&-']
['6C', '8F', 'XC', 'AR', '2F', '2C']
['4B|4C', '6F|6R', '6R|6B', '8C|8R', 'AC|AR', 'AR|AF']
['6F|6R|6B', 'AC|AR|AF']
[]
'''
