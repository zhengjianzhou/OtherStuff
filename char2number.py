#!/usr/bin/python

import random

while True:
    # Sample: 'meet+meet+meet+meet=team'
    line = raw_input("What is your question?\n").replace(' ','')
    print 'Got : ', line
    s = set(line.replace('+','').replace('=',''))
    l_0, l_1 = line.split('=')
    xs, y = [x for x in l_0.split('+')], list(l_1)

    while True:
        sd = {a:b for a,b in zip(s,random.sample(range(10), len(s)))}
        
        if not (sd[y[0]] and sum(map(lambda x:abs(sd[x]), zip(*xs)[0]))):continue

        int_xs = [int(''.join([str(sd[i]) for i in x])) for x in xs]
        int_y = int(''.join([str(sd[i]) for i in y]))
        
        print 'trying...', sd, int_xs, int_y
        if sum(int_xs) == int_y:
            print 'Answer:', '+'.join([str(i) for i in int_xs]), '=', int_y
            break
