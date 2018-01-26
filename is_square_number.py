def is_square(n):
    bl = n.bit_length()
    half_bl = (bl-1)//2 if n < (1<<(bl//2))**2 else bl//2

    x = 1<<half_bl
    for i in range(half_bl)[::-1]:
        if (x|1<<i)**2 <= n: x = x|1<<i
        if x**2 == n: return True

    return False

for x in range(1, 1000):
    if is_square(x):
        print x, is_square(x)


'''
### OUTPUT ###
4 True
9 True
16 True
25 True
36 True
49 True
64 True
81 True
100 True
121 True
144 True
169 True
196 True
225 True
256 True
289 True
324 True
361 True
400 True
441 True
484 True
529 True
576 True
625 True
676 True
729 True
784 True
841 True
900 True
961 True
>>> 
'''
