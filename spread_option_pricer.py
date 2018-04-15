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

====== TEST1 ======

K \ Rho|                 -1.00              |                 -0.50              |                  0.00              |                  0.30              |                  0.80              |                  1.00              
       |      MC,   Kirk, Num.Slice, Num.GLQ|      MC,   Kirk, Num.Slice, Num.GLQ|      MC,   Kirk, Num.Slice, Num.GLQ|      MC,   Kirk, Num.Slice, Num.GLQ|      MC,   Kirk, Num.Slice, Num.GLQ|      MC,   Kirk, Num.Slice, Num.GLQ
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
K= -20 | 29.7512, 29.7149, 29.6474, 29.8115 | 28.9831, 29.0445, 28.9892, 29.0693 | 28.4542, 28.4183, 28.3753, 28.3840 | 27.8013, 28.0970, 28.0641, 28.0763 | 27.8057, 27.7720, 27.7638, 27.7635 | 27.6596, 27.7478, 27.7474, 27.7470
K= -10 | 21.6973, 21.8883, 21.8661, 21.1663 | 20.8373, 20.9229, 20.9000, 20.6936 | 20.2723, 19.9044, 19.8836, 19.8540 | 19.1476, 19.2835, 19.2646, 19.2964 | 18.3493, 18.3863, 18.3749, 18.3706 | 18.1331, 18.2394, 18.2375, 18.2352
K=   0 | 15.2335, 15.1293, 15.1321, 15.2180 | 14.0341, 13.9139, 13.9138, 14.1048 | 12.4652, 12.5194, 12.5195, 12.6128 | 11.5418, 11.5573, 11.5573, 11.5316 |  9.6600,  9.6273,  9.6273,  9.5868 |  8.8272,  8.8152,  8.8153,  8.7805
K=   5 | 12.3668, 12.2390, 12.2405, 12.8399 | 10.7278, 10.9507, 10.9527, 10.9260 |  9.3715,  9.4394,  9.4417,  9.4381 |  8.3792,  8.3611,  8.3636,  8.3020 |  5.8640,  5.9586,  5.9628,  5.8192 |  4.4850,  4.4369,  4.4482,  4.4579
K=  15 |  7.5361,  7.5351,  7.5117,  8.0839 |  6.3095,  6.2534,  6.2397,  6.1957 |  4.8348,  4.7539,  4.7422,  4.8298 |  3.6230,  3.6885,  3.6779,  3.6485 |  1.3802,  1.3529,  1.3410,  1.0446 |  0.0442,  0.0721,  0.0484,  0.0632
K=  25 |  4.0701,  4.2458,  4.1987,  3.3278 |  3.0990,  3.1672,  3.1285,  3.1886 |  1.9228,  1.9911,  1.9609,  1.8128 |  1.2301,  1.2431,  1.2190,  1.1798 |  0.1134,  0.1122,  0.1039,  0.0844 |  0.0000,  0.0000,  0.0000,  0.0000

====== TEST2 ======

no.paths| Monte Carlo | Kirk's Approximation | Num.Slice,  | Num.GLQ
--------------------------------------------------------------------
     20 |   19.7817   | 19.2835              | 19.2646   | 19.2964
     24 |   19.1159   | 19.2835              | 19.2646   | 19.2964
     29 |   17.7505   | 19.2835              | 19.2646   | 19.2964
     36 |   15.4069   | 19.2835              | 19.2646   | 19.2964
     44 |   18.9405   | 19.2835              | 19.2646   | 19.2964
     54 |   21.0290   | 19.2835              | 19.2646   | 19.2964
     66 |   17.1551   | 19.2835              | 19.2646   | 19.2964
     81 |   17.1686   | 19.2835              | 19.2646   | 19.2964
     99 |   19.6217   | 19.2835              | 19.2646   | 19.2964
    121 |   19.2620   | 19.2835              | 19.2646   | 19.2964
    148 |   18.4132   | 19.2835              | 19.2646   | 19.2964
    181 |   19.1960   | 19.2835              | 19.2646   | 19.2964
    221 |   19.9849   | 19.2835              | 19.2646   | 19.2964
    270 |   20.5231   | 19.2835              | 19.2646   | 19.2964
    330 |   18.8010   | 19.2835              | 19.2646   | 19.2964
    403 |   20.7350   | 19.2835              | 19.2646   | 19.2964
    492 |   19.1022   | 19.2835              | 19.2646   | 19.2964
    601 |   18.9688   | 19.2835              | 19.2646   | 19.2964
    735 |   18.2864   | 19.2835              | 19.2646   | 19.2964
    897 |   18.9394   | 19.2835              | 19.2646   | 19.2964
   1096 |   18.8593   | 19.2835              | 19.2646   | 19.2964
   1339 |   20.3417   | 19.2835              | 19.2646   | 19.2964
   1635 |   19.4916   | 19.2835              | 19.2646   | 19.2964
   1998 |   19.8150   | 19.2835              | 19.2646   | 19.2964
   2440 |   19.6645   | 19.2835              | 19.2646   | 19.2964
   2980 |   19.1268   | 19.2835              | 19.2646   | 19.2964
   3640 |   19.0069   | 19.2835              | 19.2646   | 19.2964
   4447 |   19.0047   | 19.2835              | 19.2646   | 19.2964
   5431 |   19.5345   | 19.2835              | 19.2646   | 19.2964
   6634 |   19.1961   | 19.2835              | 19.2646   | 19.2964
   8103 |   19.2817   | 19.2835              | 19.2646   | 19.2964
   9897 |   19.2699   | 19.2835              | 19.2646   | 19.2964
  12088 |   19.3192   | 19.2835              | 19.2646   | 19.2964
  14764 |   19.2644   | 19.2835              | 19.2646   | 19.2964
  18033 |   19.2417   | 19.2835              | 19.2646   | 19.2964
  22026 |   19.1681   | 19.2835              | 19.2646   | 19.2964
  26903 |   19.2733   | 19.2835              | 19.2646   | 19.2964
  32859 |   19.2242   | 19.2835              | 19.2646   | 19.2964
  40134 |   19.2406   | 19.2835              | 19.2646   | 19.2964
  49020 |   19.2157   | 19.2835              | 19.2646   | 19.2964
  59874 |   19.2295   | 19.2835              | 19.2646   | 19.2964
  73130 |   19.3218   | 19.2835              | 19.2646   | 19.2964
  89321 |   19.1907   | 19.2835              | 19.2646   | 19.2964
 109097 |   19.2196   | 19.2835              | 19.2646   | 19.2964
 133252 |   19.2514   | 19.2835              | 19.2646   | 19.2964

====== TEST3 ======

NoOfPoints Dim.1  =  |      10 |      20 |      30 |      40 |      50 |      60 |      70 |      80 |      90 |     100 |     110 |     120
--------------------------------------------------------------------------------------------------------------------------------------------
NoOfPoints Dim2=  10 |  0.0889 |  1.0419 |  1.3262 |  1.3320 |  1.3249 |  1.3228 |  1.3188 |  1.3189 |  1.3183 |  1.3170 |  1.3177 |  1.3189
NoOfPoints Dim2=  20 |  1.1332 | 11.6905 | 14.7544 | 14.8736 | 14.9758 | 15.0749 | 15.1598 | 15.1697 | 15.1293 | 15.1379 | 15.1260 | 15.0954
NoOfPoints Dim2=  30 |  1.4553 | 14.4251 | 18.1484 | 18.7466 | 18.9979 | 18.9604 | 19.0486 | 19.0558 | 19.0015 | 18.9165 | 18.9582 | 18.9976
NoOfPoints Dim2=  40 |  1.4812 | 14.6239 | 18.2383 | 19.0896 | 19.3191 | 19.2687 | 19.2852 | 19.2909 | 19.2449 | 19.2151 | 19.2457 | 19.2828
NoOfPoints Dim2=  50 |  1.4819 | 14.7088 | 18.2042 | 19.1118 | 19.2964 | 19.2984 | 19.2774 | 19.2787 | 19.2337 | 19.2604 | 19.2570 | 19.2822
NoOfPoints Dim2=  60 |  1.4819 | 14.7410 | 18.2657 | 19.0886 | 19.3103 | 19.3098 | 19.2690 | 19.2696 | 19.2447 | 19.2743 | 19.2591 | 19.2701
NoOfPoints Dim2=  70 |  1.4819 | 14.7478 | 18.2974 | 19.0788 | 19.3156 | 19.3049 | 19.2642 | 19.2651 | 19.2578 | 19.2757 | 19.2598 | 19.2638
NoOfPoints Dim2=  80 |  1.4819 | 14.7423 | 18.3118 | 19.0926 | 19.3064 | 19.3041 | 19.2623 | 19.2617 | 19.2651 | 19.2702 | 19.2576 | 19.2669
NoOfPoints Dim2=  90 |  1.4819 | 14.7313 | 18.3166 | 19.0966 | 19.3096 | 19.2994 | 19.2592 | 19.2602 | 19.2680 | 19.2625 | 19.2653 | 19.2663
NoOfPoints Dim2= 100 |  1.4819 | 14.7180 | 18.3160 | 19.0919 | 19.3128 | 19.2951 | 19.2588 | 19.2585 | 19.2667 | 19.2561 | 19.2685 | 19.2652
NoOfPoints Dim2= 110 |  1.4819 | 14.7158 | 18.3123 | 19.0833 | 19.3100 | 19.3006 | 19.2597 | 19.2574 | 19.2661 | 19.2623 | 19.2690 | 19.2613
NoOfPoints Dim2= 120 |  1.4819 | 14.7258 | 18.3070 | 19.0903 | 19.3092 | 19.3023 | 19.2626 | 19.2570 | 19.2657 | 19.2660 | 19.2670 | 19.2627

====== TEST4 ======

Boundary Dim.1(a,b)    =   |  -0,  0 |  -1,  1 |  -2,  2 |  -3,  3 |  -5,  5 |  -8,  8 | -10, 10 | -15, 15 | -20, 20 | -30, 30 | -50, 50 | -80, 80
--------------------------------------------------------------------------------------------------------------------------------------------------
Boundary Dim.2(a,b)= -0  0 |  2.7500 |  4.8480 |  6.7765 |  7.1545 |  7.1833 |  7.1827 |  7.1843 |  7.1941 |  7.1537 |  7.2492 |  6.8396 |  5.3932
Boundary Dim.2(a,b)= -1  1 |  4.9265 |  8.6860 | 12.1591 | 12.8345 | 12.8856 | 12.8856 | 12.8839 | 12.8878 | 12.8653 | 12.9801 | 12.2656 |  9.6392
Boundary Dim.2(a,b)= -2  2 |  6.9646 | 12.2937 | 17.2491 | 18.1980 | 18.2694 | 18.2696 | 18.2696 | 18.2692 | 18.2675 | 18.3323 | 17.5168 | 13.6817
Boundary Dim.2(a,b)= -3  3 |  7.3103 | 12.9142 | 18.1298 | 19.1233 | 19.1979 | 19.1981 | 19.1982 | 19.1983 | 19.1937 | 19.2530 | 18.4476 | 14.3927
Boundary Dim.2(a,b)= -5  5 |  7.3348 | 12.9588 | 18.1930 | 19.1896 | 19.2647 | 19.2641 | 19.2649 | 19.2644 | 19.2606 | 19.3199 | 18.5152 | 14.4452
Boundary Dim.2(a,b)= -8  8 |  7.3348 | 12.9587 | 18.1932 | 19.1885 | 19.2646 | 19.2627 | 19.2644 | 19.2644 | 19.2598 | 19.3197 | 18.5117 | 14.4462
Boundary Dim.2(a,b)=-10 10 |  7.3348 | 12.9588 | 18.1932 | 19.1898 | 19.2645 | 19.2650 | 19.2664 | 19.2655 | 19.2568 | 19.3206 | 18.5187 | 14.4378
Boundary Dim.2(a,b)=-15 15 |  7.3348 | 12.9586 | 18.1930 | 19.1900 | 19.2687 | 19.2649 | 19.2610 | 19.2684 | 19.2574 | 19.3172 | 18.5084 | 14.4404
Boundary Dim.2(a,b)=-20 20 |  7.3349 | 12.9590 | 18.1932 | 19.1894 | 19.2643 | 19.2594 | 19.2621 | 19.2634 | 19.2617 | 19.3191 | 18.5328 | 14.4515
Boundary Dim.2(a,b)=-30 30 |  7.3349 | 12.9596 | 18.1932 | 19.1903 | 19.2592 | 19.2598 | 19.2591 | 19.2596 | 19.2758 | 19.3186 | 18.4906 | 14.4538
Boundary Dim.2(a,b)=-50 50 |  7.2719 | 12.8370 | 18.0515 | 19.0393 | 19.1139 | 19.1238 | 19.1126 | 19.0670 | 19.1757 | 19.1435 | 18.3301 | 14.1508
Boundary Dim.2(a,b)=-80 80 |  5.5786 |  9.8897 | 13.9741 | 14.7186 | 14.7761 | 14.7704 | 14.7761 | 14.7911 | 14.8234 | 14.6226 | 14.5189 | 11.1626

'''

def GBM(s1, s2, v1, v2, r, t, rho, random_walk=False):
    '''
    Geometric Brownian Motions (GBM) for 2 correlated assets
    '''
    if not random_walk:
        dw1 = np.random.normal(0., 1.)
        dw2 = rho * dw1 + sqrt(1. - rho**2) * np.random.normal(0., 1.)
        s1 = s1 * exp( -0.5*t*v1**2 + v1*sqrt(t)*dw1 )
        s2 = s2 * exp( -0.5*t*v2**2 + v2*sqrt(t)*dw2 )
    else:
        w1, w2 = 0., 0.
        dt = t/365.
        days = int(t * 365)
        for i in range(days):
            dw1 = np.random.normal(0., 1.)
            dw2 = rho * dw1 + sqrt(1. - rho**2) * np.random.normal(0., 1.)
            s1 = s1 * exp( -0.5*dt*v1**2 + v1*sqrt(dt)*dw1 )
            s2 = s2 * exp( -0.5*dt*v2**2 + v2*sqrt(dt)*dw2 )
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

def _element(w1, w3, s1, s2, v1, v2, t, rho, k):
    s1 = s1 * exp( -0.5*t*v1**2 + v1*sqrt(t)*w1 )
    w2 = rho * w1 + sqrt(1. - rho**2) * w3
    s2 = s2 * exp( -0.5*t*v2**2 + v2*sqrt(t)*w2 )
    return max(s1 - s2 - k, 0.)

def numerical_slices(r,t,k,s1,s2,v1,v2,rho):
    # numerical integrations for equal length slices
    # setup the steps independent random variable w1, w3
    # choosing a notation of '3' to identify the independent random var dw3
    nofs1,dw1,left1 = 200, 0.1, -10.
    nofs3,dw3,left3 = 200, 0.1, -10.
    # nofs : number of steps
    # left : starting point from left side
    # 1,3  : refer to the two independent var
    sums = 0.
    for i in range(nofs1):
        for j in range(nofs3):
            w1, w3 = left1 + i*dw1, left3 + j*dw3
            u = _element(w1, w3, s1, s2, v1, v2, t, rho, k) * stats.norm.pdf(w1) * stats.norm.pdf(w3) * dw1 * dw3
            sums += u
            
    return exp(-r*t) * sums

def numerical_gauss_legendre(r,t,k,s1,s2,v1,v2,rho, glq1=(-20., 20., 50), glq3=(-20., 20., 50)):
    # numerical integrations for equal length slices
    # setup the steps independent random variable w1, w3
    # choosing a notation of '3' to identify the independent random var dw3
    a1, b1, GL_DEGREE1 = glq1
    a3, b3, GL_DEGREE3 = glq3
    # a,b       : a, b defines the left and right end for each dimention
    # GL_DEGREE : number of points and weights for Gauss-Legendre quadrature
    # 1,3       : refer to the two independent var

    bma1, bpa1 = 0.5*(b1-a1), 0.5*(b1+a1)
    bma3, bpa3 = 0.5*(b3-a3), 0.5*(b3+a3)
    # bma : (b-a) / 2
    # bpa : (b+a) / 2

    pnw1 = zip(*np.polynomial.legendre.leggauss(GL_DEGREE1)) # points and weight of gauss legendre
    pnw3 = zip(*np.polynomial.legendre.leggauss(GL_DEGREE3)) # points and weight of gauss legendre

    sums = 0.
    for x1, dw1 in pnw1:
        for x3, dw3 in pnw3:
            w1 = bma1*x1 + bpa1
            w3 = bma3*x3 + bpa3
            u = bma1 * bma3 * _element(w1, w3, s1, s2, v1, v2, t, rho, k) * stats.norm.pdf(w1) * stats.norm.pdf(w3) * dw1 * dw3
            sums += u
            
    return exp(-r*t) * sums

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
    print('\n====== TEST1 ======\n')
    print('K \ Rho|' + '|'.join(['              {:8.2f}              '.format(i) for i in Rhos]))
    print('       |'+'|'.join(['      MC,   Kirk, Num.Slice, Num.GLQ']* len(Rhos)))
    print('-'*229)
    for k in Ks:
        res = []
        for rho in Rhos:
            mc_res = MC(10000,r,t,k,s1,s2,v1,v2,rho)
            kirk_res = Kirk(r,t,k,s1,s2,v1,v2,rho)
            numerical_slice_res = numerical_slices(r,t,k,s1,s2,v1,v2,rho)
            numerical_glq_res = numerical_gauss_legendre(r,t,k,s1,s2,v1,v2,rho)
            res.append('{:7.4f}, {:7.4f}, {:7.4f}, {:7.4f}'.format(mc_res, kirk_res, numerical_slice_res, numerical_glq_res))
        print('K={:4.0f} | '.format(k) + ' | '.join(res))

def test2():
    '''
    Tests 2: test convergence on MC paths against Kirk approximation
    Steps are increased gradually for each run. Choose below parameters for testing,
    r, t, k, s1, s2, v1, v2, rho = 0.05,1., -10., 112.22, 103.05, 0.1, 0.15, 0.3
    '''
    
    r, t, k, s1, s2, v1, v2, rho = 0.05,1., -10.,112.22, 103.05, 0.1, 0.15, 0.3

    kirk_res = Kirk(r,t,k,s1,s2,v1,v2,rho)
    numerical_slice_res = numerical_slices(r,t,k,s1,s2,v1,v2,rho)
    numerical_glq_res = numerical_gauss_legendre(r,t,k,s1,s2,v1,v2,rho)

    x,z0,z1,z2,z3 = [],[],[],[],[]
    print('\n====== TEST2 ======\n')
    print("no.paths| Monte Carlo | Kirk's Approximation | Num.Slice,  | Num.GLQ")
    print("--------------------------------------------------------------------")
    for i in range(15, 60):
        no_of_paths = int(exp(i/5.))
        mc_res = MC(no_of_paths,r,t,k,s1,s2,v1,v2,rho)
        x.append(no_of_paths)
        z0.append(mc_res)
        z1.append(kirk_res)
        z2.append(numerical_slice_res)
        z3.append(numerical_glq_res)
        print('{:7.0f} |   {:7.4f}   | {:7.4f}              | {:7.4f}   | {:7.4f}'.format(no_of_paths, mc_res, kirk_res, numerical_slice_res, numerical_glq_res))

    plt.plot(x,z0, 'o--')
    plt.plot(x,z1, '--')
    plt.plot(x,z2, '--')
    plt.plot(x,z3, '--')
    plt.show()

def test3():
    '''
    Tests 3: Simple search for better Degrees of Gauss Legendre Quadrature for degree1 and degree2
    Same parameters were choosen for comparison
        r, t, s1, s2, v1, v2 2 0.05,1.,112.22,103.05, 0.1, 0.15
    Result can be compare with "Table 1 Spread option value approximation" in the paper, which are consistent.
    '''
    r, t, k, s1, s2, v1, v2, rho = 0.05,1., -10.,112.22, 103.05, 0.1, 0.15, 0.3

    print('\n====== TEST3 ======\n')
    print('NoOfPoints Dim.1  =  | ' + ' | '.join(['{:7.0f}'.format(i) for i in range(10,121,10)]))
    print('-'*140)
    for d1 in range(10,121,10):
        res = []
        for d3 in range(10,121,10):
            glq1=(-20., 20., d1)
            glq3=(-20., 20., d3)
            numerical_glq_res = numerical_gauss_legendre(r,t,k,s1,s2,v1,v2,rho, glq1, glq3)
            res.append('{:7.4f}'.format(numerical_glq_res))
        print('NoOfPoints Dim2={:4.0f} | '.format(d1) + ' | '.join(res))

def test4():
    '''
    Tests 3: Simple search for better Degrees of Gauss Legendre Quadrature for degree1 and degree2
    Same parameters were choosen for comparison
        r, t, s1, s2, v1, v2 2 0.05,1.,112.22,103.05, 0.1, 0.15
    Result can be compare with "Table 1 Spread option value approximation" in the paper, which are consistent.
    '''
    r, t, k, s1, s2, v1, v2, rho = 0.05,1., -10.,112.22, 103.05, 0.1, 0.15, 0.3

    test_boundary = [0.5,1.,2.,3.,5.,8.,10.,15.,20.,30.,50.,80.]
    print('\n====== TEST4 ======\n')
    print('Boundary Dim.1(a,b)    =   | ' + ' | '.join(['{:3.0f},{:3.0f}'.format(-i,i) for i in test_boundary]))
    print('-'*146)
    for a1 in test_boundary:
        res = []
        for a3 in test_boundary:
            glq1=(-a1, a1, 80)
            glq3=(-a3, a3, 80)
            numerical_glq_res = numerical_gauss_legendre(r,t,k,s1,s2,v1,v2,rho, glq1, glq3)
            res.append('{:7.4f}'.format(numerical_glq_res))
        print('Boundary Dim.2(a,b)={:3.0f}{:3.0f} | '.format(-a1,a1) + ' | '.join(res))

# TEST RUN

test1()
test2()
test3()
test4()
