
INTERNAL = {
    '+' : ''  ,
    '-' : ''  ,
    '=' : ''  ,
    '0' : '69',
    '1' : ''  ,
    '2' : '3' ,
    '3' : '25',
    '4' : ''  ,
    '5' : '3' ,
    '6' : '0' ,
    '7' : ''  ,
    '8' : ''  ,
    '9' : '0' ,
  }

ADD = {
    '+' : '' ,
    '-' : '+',
    '=' : ''  ,
    '0' : '8',
    '1' : '7',
    '2' : '' ,
    '3' : '9',
    '4' : '' ,
    '5' : '9',
    '6' : '8',
    '7' : '' ,
    '8' : '' ,
    '9' : '8',
  }

SUB = {
    '+' : '-'  ,
    '-' : ''   ,
    '=' : ''   ,
    '0' : ''   ,
    '1' : ''   ,
    '2' : ''   ,
    '3' : ''   ,
    '4' : ''   ,
    '5' : ''   ,
    '6' : '5'  ,
    '7' : '1'  ,
    '8' : '069',
    '9' : '3'  ,
  }

print('Type in your question:')
eqn = input()

print('Original Equation:', eqn)
# internal move
for i in range(len(eqn)):
  c = eqn[i]
  new_eqn = list(eqn)
  for t in INTERNAL[c]:
    new_eqn[i] = t
    eq = ''.join(new_eqn)
    r = eval(eq.replace('=','=='))
    print('Internal move:', c, 'to', t, 'New Equation:', eq, 'Solved?', r)
    if r:
      exit(0)

# add-sub move
for i in range(len(eqn)):
  for j in range(i+1, len(eqn)):
    c1 = eqn[i]
    c2 = eqn[j]
    new_eqn = list(eqn)
    for t1 in ADD[c1]:
      for t2 in SUB[c2]:
        new_eqn[i] = t1
        new_eqn[j] = t2
        eq = ''.join(new_eqn)
        r = eval(eq.replace('=','=='))
        print('Add-Sub move:', c1, 'to', t1,'&',c2,'to', t2, 'New Equation:', eq, 'Solved?', r)
        if r:
          exit(0)

    for t1 in SUB[c1]:
      for t2 in ADD[c2]:
        new_eqn[i] = t1
        new_eqn[j] = t2
        eq = ''.join(new_eqn)
        r = eval(eq.replace('=','=='))
        print('Add-Sub move:', c1, 'to', t1,'&',c2,'to', t2, 'New Equation:', eq, 'Solved?', r)
        if r:
          exit(0)

