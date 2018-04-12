#!/usr/bin/python
# implemented in python 2.7

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from math import exp, sqrt, log
'''
Question:
1) Implement Monte Carlo (MC) simulation to solve the below spread option,
    => E[(S2 - S1 - K)^+]
    => Given S1, S2 are dependent GBMs with correlation 'rho'
2) Find a closed form approximation and implement the logic
3) Show MC convergence graph to the approximation

Answer:
1) The Monte Carlo simulation was written in below function MC(). Use cases can be found in test1(), test2()
2) Implemented Kirk's approximation in function kirk(), referring to, Kirk, E. (1995): "Correlation in the energy markets," In Managing Energy Price Risk (First Edition)
3) test2() produces the MC convergence graph to Kirk approximation for given parameters

Potential improvements:
This code is for demonstration purpose. Below points can be implemented if needed,
1) performance tweeks
2) improve the matplotlib result plotting
3) use OptionParser class for easier user inputs for testing
    => from optparse import OptionParser

Variables:
    s1, s2: asset prices
    v1, v2: daily volatilities
    r:      riskless interest rate
    rho:    correlation btw w1 and w2
    t:      time (in years)

Given,
    corr(dw1, dw2) = rho
Let w1 be an independent Geometric Brownian Motion(GBM), we have,
    w2 = rho * w1 + sqrt(1-rho**2) * w3
where w1 and w3 are independent GBMs
    Since s1, s2 follows GBM, we have,
    d ln(S1) = (r - (v1**2)/2)*dt + v1*dw1
    d ln(S2) = (r - (v2**2)/2)*dt + v1*dw2

Output:
    Test 1:
    -------
zzheng@JamesPC ~/code/OtherStuff $ python spread_option_pricer3.py
K \ Rho|            -1.00 |            -0.50 |             0.00 |             0.30 |             0.80 |             1.00 
K= -20 | 29.3664, 29.7149 | 29.1221, 29.0445 | 28.3414, 28.4183 | 27.9773, 28.0970 | 27.9868, 27.7720 | 27.7015, 27.7478
K= -10 | 21.6289, 21.8883 | 20.7654, 20.9229 | 19.7874, 19.9044 | 19.3029, 19.2835 | 18.4068, 18.3863 | 18.2538, 18.2394
K=   0 | 15.1039, 15.1293 | 13.8869, 13.9139 | 12.4034, 12.5194 | 11.5424, 11.5573 |  9.6684,  9.6273 |  8.8657,  8.8152
K=   5 | 11.9469, 12.2390 | 11.0576, 10.9507 |  9.2829,  9.4394 |  8.3224,  8.3611 |  5.8960,  5.9586 |  4.4427,  4.4369
K=  15 |  7.4275,  7.5351 |  6.3347,  6.2534 |  4.9427,  4.7539 |  3.6652,  3.6885 |  1.2972,  1.3529 |  0.0457,  0.0721
K=  25 |  4.2547,  4.2458 |  3.1829,  3.1672 |  1.9740,  1.9911 |  1.2000,  1.2431 |  0.0954,  0.1122 |  0.0000,  0.0000
    
    Test 2:
    -------
no.paths| Monte Carlo | Kirk's Approximation
     20 |   18.8894   | 19.2835
     24 |   22.5547   | 19.2835
     29 |   21.2421   | 19.2835
     36 |   19.3842   | 19.2835
     44 |   15.9945   | 19.2835
     54 |   19.2223   | 19.2835
     66 |   21.2414   | 19.2835
     81 |   21.1814   | 19.2835
     99 |   17.9478   | 19.2835
    121 |   21.4866   | 19.2835
    148 |   18.3487   | 19.2835
    181 |   20.0745   | 19.2835
    221 |   20.2213   | 19.2835
    270 |   19.8273   | 19.2835
    330 |   18.9882   | 19.2835
    403 |   18.8934   | 19.2835
    492 |   19.0496   | 19.2835
    601 |   18.9223   | 19.2835
    735 |   19.2819   | 19.2835
    897 |   19.2154   | 19.2835
   1096 |   20.0615   | 19.2835
   1339 |   19.1763   | 19.2835
   1635 |   19.1543   | 19.2835
   1998 |   20.0120   | 19.2835
   2440 |   19.5092   | 19.2835
   2980 |   18.7682   | 19.2835
   3640 |   19.5189   | 19.2835
   4447 |   19.0096   | 19.2835
   5431 |   19.0296   | 19.2835
   6634 |   19.1334   | 19.2835
   8103 |   19.2045   | 19.2835
   9897 |   19.2806   | 19.2835
  12088 |   19.1905   | 19.2835
  14764 |   19.1676   | 19.2835
  18033 |   19.3427   | 19.2835
  22026 |   19.2837   | 19.2835
  26903 |   19.3665   | 19.2835
  32859 |   19.1885   | 19.2835
  40134 |   19.2393   | 19.2835
  49020 |   19.3321   | 19.2835
  59874 |   19.3546   | 19.2835
  73130 |   19.1946   | 19.2835
  89321 |   19.2510   | 19.2835
 109097 |   19.2571   | 19.2835
 133252 |   19.3624   | 19.2835
'''

def GBM(s1, s2, v1, v2, r, t, rho):
    '''
    Geometric Brownian Motions (GBM) for 2 correlated assets
    '''
    dw1 = np.random.normal(0., 1.)
    dw2 = rho * dw1 + sqrt(1. - rho**2) * np.random.normal(0., 1.)
    s1 = s1 * exp( -0.5*t*v1**2 + v1*sqrt(t)*dw1 )
    s2 = s2 * exp( -0.5*t*v2**2 + v2*sqrt(t)*dw2 )
    return s1, s2

def MC(paths, r, t, k, s1, s2, v1, v2, rho):
    '''
    monte carlo simulation for given number of paths
    '''
    count, sums = 0, 0.
    for i in range(paths):
        _s1, _s2 = GBM(s1, s2, v1, v2, r, t, rho)
        sums += max(_s1 - _s2 - k, 0.)
        count += 1
    return exp(-r*t) * sums/float(count)

def Kirk(r, t, k, s1, s2, v1, v2, rho):
    '''
    Kirk suggested the following approximation to spread call options
        => Kirk, E. (1995): "Correlation in the energy markets," In Managing Energy Price Risk (First Edition)
    '''
    s2k = s2/(s2 + k)
    sigk = sqrt(v1**2 - 2.*s2k*rho*v1*v2 + s2k**2 * v2**2)
    dk1 = (log(s1/(s2 + k)) + 0.5*t*sigk**2) / sigk * sqrt(t)
    dk2 = dk1 - sigk * sqrt(t)
    result = exp(-r * t) * (s1*stats.norm.cdf(dk1) - (s2+k)*stats.norm.cdf(dk2))
    return result

def test1():
    '''
    Tests 1: Comparing test results with P. Bjerksund & G. Stensland's paper,
    Link: http://www.opus-finance.com/sites/default/files/Fichier_Site_Opus/Article_recherche/Articles_externes/2013/Closed_form_spread_option_valuation/Closed_form_spread_option_valuation.pdf
    Same parameters were choosen for comparison
        r, t, s1, s2, v1, v2 2 0.05,1.,112.22,103.05, 0.1, 0.15
    Result can be compare with "Table 1 Spread option value approximation" in the paper, which are consistent.
    '''
    r, t, s1, s2, v1, v2 = 0.05, 1.,112.22, 103.05, 0.1, 0.15

    Ks = [-20, -10, 0, 5,15, 25]
    Rhos = [-1., -0.5, 0., 0.3, 0.8, 1.]
    print('K \ Rho|' + '|'.join(['         {:8.2f} '.format(i) for i in Rhos]))
    for k in Ks:
        res = []
        for rho in Rhos:
            mc_res = MC(10000,r,t,k,s1,s2,v1,v2,rho)
            kirk_res = Kirk(r,t,k,s1,s2,v1,v2,rho)
            res.append('{:7.4f}, {:7.4f}'.format(mc_res, kirk_res))
        print('K={:4.0f} | '.format(k) + ' | '.join(res))

def test2():
    '''
    Tests 2: test convergence on MC paths against Kirk approximation
    Steps are increased gradually for each run. Choose below parameters for testing,
    r, t, k, s1, s2, v1, v2, rho = 0.05,1., -10., 112.22, 103.05, 0.1, 0.15, 0.3
    '''
    
    r, t, k, s1, s2, v1, v2, rho = 0.05,1., -10.,112.22, 103.05, 0.1, 0.15, 0.3
    kirk_res = Kirk(r,t,k,s1,s2,v1,v2,rho)

    x,y,z = [], [], []
    print("no.paths| Monte Carlo | Kirk's Approximation")
    for i in range(15, 60):
        no_of_paths = int(exp(i/5.))
        mc_res = MC(no_of_paths,r,t,k,s1,s2,v1,v2,rho)
        x.append(no_of_paths)
        y.append(mc_res)
        z.append(kirk_res)
        print('{:7.0f} |   {:7.4f}   | {:7.4f}'.format(no_of_paths, mc_res, kirk_res))

    plt.plot(x,y, 'o--')
    plt.plot(x,z, '--')
    plt.show()

# TEST RUN

test1()
test2()
