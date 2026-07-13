print('''
Questioin:

  Helen and Ivan had the same number of coins. Helen had a number of
  50-cent coins, and 64 20-cent coins. These coins had a mass of 1.134kg.
  Ivan had a number of 50-cent coins and 104 20-cent coins.

  (a) Who has more money in coins and by how much? (2)
  (b) given that each 50-cent coin is 2.7g more heavier than a 20-cent
      coin, what is the mass of Ivan's coins in kilograms? (2)
''')
print('''
Define:
  x: no. of 50cents coin for Helen
  y: no. of 20cents coin for Helen
  a: no. of 50cents coin for Ivan
  b: no. of 20cents coin for Ivan
  m: weith of a 50cents coin
  n: weith of a 20cents coin
  e: Total money of Helen - Total money of Ivan : [Answer to a]
  w: Total weight of Ivan's coins : [Answer to b]
''')

from sympy import *
x,y,a,b,m,n,e,w=symbols('x y a b m n e w')
s = solve( [
    x+y     - (a+b),
    y       - 64,
    b       - 104,
    x*m+y*n - 1134,
    a*m+b*n - w,
    m-2.7   - n,
    x*50+y*20-(a*50+b*20) - e,
  ], [x,y,a,b,m,n,e,w], dict=True)

print('Results:')
for k in s[0]:
  print('  {} : {}'.format(k, s[0][k]))
