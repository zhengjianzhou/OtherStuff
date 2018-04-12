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
    K \ Rho|            -1.00 |            -0.50 |             0.00 |             0.30 |             0.80 |             1.00 
    K= -20 | 31.3015, 29.3951 | 30.3344, 28.7167 | 29.1159, 28.0965 | 29.2011, 27.7981 | 28.6341, 27.6195 | 28.5149, 27.7151
    K= -10 | 23.1038, 21.4238 | 21.4728, 20.4104 | 20.5830, 19.3292 | 19.5291, 18.6642 | 18.8533, 17.7606 | 18.6127, 17.8974
    K=   0 | 15.2947, 14.5463 | 13.7269, 13.2460 | 12.9778, 11.7150 | 12.2137, 10.6168 |  9.9006,  8.1259 |  8.5262,  6.4035
    K=   5 | 13.2245, 11.6228 | 11.6897, 10.2431 |  9.7496,  8.5834 |  8.6582,  7.3549 |  5.9585,  4.2996 |  4.3387,  1.5204
    K=  15 |  7.8769,  6.9242 |  6.3783,  5.5739 |  4.8585,  3.9813 |  3.6324,  2.8473 |  1.4169,  0.5408 |  0.0323,  0.0001
    K=  25 |  4.5764,  3.7301 |  3.2521,  2.6388 |  1.9444,  1.4803 |  1.1190,  0.7899 |  0.0879,  0.0165 |  0.0000,  0.0000
    
    Test 2:
    -------
    no.paths| Monte Carlo | Kirk's Approximation
       1000 |   19.0607    | 18.6642
       2000 |   19.7201    | 18.6642
       3000 |   19.7780    | 18.6642
       4000 |   19.5614    | 18.6642
       5000 |   19.7208    | 18.6642
       6000 |   19.8115    | 18.6642
       7000 |   19.8903    | 18.6642
       8000 |   19.7842    | 18.6642
       9000 |   19.7008    | 18.6642
      10000 |   20.0732    | 18.6642
      11000 |   19.8716    | 18.6642
      12000 |   19.6924    | 18.6642
      13000 |   19.7405    | 18.6642
      14000 |   19.6918    | 18.6642
      15000 |   19.8727    | 18.6642
      16000 |   19.9275    | 18.6642
      17000 |   19.7679    | 18.6642
      18000 |   19.8689    | 18.6642
      19000 |   19.7731    | 18.6642
      20000 |   19.7064    | 18.6642
'''

def GBM(s1, s2, v1, v2, r, t, rho):
    '''
    Geometric Brownian Motions (GBM) for 2 correlated assets
    '''
    dw1 = np.random.normal(0., 1.)
    dw2 = rho * dw1 + sqrt(1. - rho**2) * np.random.normal(0., 1.)
    s1 = s1 * exp( 0.5*dt*v1**2 + v1*sqrt(t)*dw1 )
    s2 = s2 * exp( 0.5*dt*v2**2 + v2*sqrt(t)*dw2 )
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
    print "no.paths| Monte Carlo | Kirk's Approximation"
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
