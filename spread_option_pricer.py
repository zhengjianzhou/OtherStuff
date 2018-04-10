#!/usr/bin/python
# implemented in python 2.7

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from math import exp, sqrt, log

def BM(w1, w2, rho):
    '''brownian motion'''
    dw1 = np.random.normal(0,1)
    dw2 = rho * dw1 + np.sqrt(1 - rho**2) * np.random.normal(0,1)

    print w1+dw1, w2+dw2
    return w1+dw1, w2+dw2

def MC(steps, r, t, k, f1, f2, sig1, sig2, rho):
    '''monte carlo'''
    count, sums = 0, 0.
    for i in range(steps):
        w1, w2 = 0., 0.
        for j in range(int(t)):
            w1, w2 = BM(w1, w2, rho)

        # result = f1 * exp(r*t) * sig1 * exp(w1) - f2 * exp(r*t) * sig2 * exp(w2) - k
        result = sig1 * w1 - sig2 * w2 - k
        sums += max(result, 0.)
        count += 1

    return sums / float(count)

def Kirk(r, t, k, f1, f2, sig1, sig2, rho):
    '''Kirk (1995) suggested the following approximation to spread call options'''
    f2k = f2/(f2 + k)
    sigk = sqrt(sig1**2 - 2. * f2k * sig1 * sig2 + f2k**2 * sig2**2)
    dk1 = (log(f2k) + 0.5 * t * sigk**2) / sigk * sqrt(t)
    dk2 = dk1 - sigk * sqrt(t)
    result = exp(-r * t) * ( f1 * stats.norm.cdf(dk1) - (f2+k) * stats.norm.cdf(dk2) )
    return result

r,t,k,f1,f2,sig1,sig2,rho = 0., 3., 1., 1., 1., 1., 1., 0.3

kirk_res = Kirk(r,t,k,f1,f2,sig1,sig2,rho)

# test the convergence of MC steps
x,y,z = [], [], []
for i in range(1, 21):
    step = i * 1000
    mc_res = MC(step,r,t,k,f1,f2,sig1,sig2,rho)
    x.append(step)
    y.append(mc_res)
    z.append(kirk_res)
    print step, mc_res, kirk_res

plt.plot(x,y, 'o--')
plt.plot(x,z, '--')
plt.show()
