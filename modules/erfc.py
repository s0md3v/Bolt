from math import *

tiny= 1e-300
half=  5.00000000000000000000e-01
one =  1.00000000000000000000e+00
two =  2.00000000000000000000e+00
erx =  8.45062911510467529297e-01

## Coefficients for approximation to  erf on [0,0.84375]

efx =  1.28379167095512586316e-01
efx8=  1.02703333676410069053e+00
pp0  =  1.28379167095512558561e-01
pp1  = -3.25042107247001499370e-01
pp2  = -2.84817495755985104766e-02
pp3  = -5.77027029648944159157e-03
pp4  = -2.37630166566501626084e-05
qq1  =  3.97917223959155352819e-01
qq2  =  6.50222499887672944485e-02
qq3  =  5.08130628187576562776e-03
qq4  =  1.32494738004321644526e-04
qq5  = -3.96022827877536812320e-06

def erf1(x):
    '''erf(x) for x in [0,0.84375]'''
    e, i = frexp(x)
    if abs(i)>28:
        if abs(i)>57:
            return 0.125*(8.0*x+efx8*x)
        return x + efx*x
    z = x*x
    r = pp0+z*(pp1+z*(pp2+z*(pp3+z*pp4)))
    s = one+z*(qq1+z*(qq2+z*(qq3+z*(qq4+z*qq5))))
    y = r/s
    return x + x*y

def erfc1(x):
    '''erfc(x)for x in [0,0.84375]'''
    e,i = frexp(x)
    if abs(i)>56:
        return one-x
    z = x*x
    r = pp0+z*(pp1+z*(pp2+z*(pp3+z*pp4)))
    s = one+z*(qq1+z*(qq2+z*(qq3+z*(qq4+z*qq5))))
    y = r/s
    if (x<0.25):
        return one-(x+x*y)
    else:
        r = x*y
        r += (x-half)
        return half - r

## Coefficients for approximation to  erf  in [0.84375,1.25] 

pa0  = -2.36211856075265944077e-03
pa1  =  4.14856118683748331666e-01
pa2  = -3.72207876035701323847e-01
pa3  =  3.18346619901161753674e-01
pa4  = -1.10894694282396677476e-01
pa5  =  3.54783043256182359371e-02
pa6  = -2.16637559486879084300e-03
qa1  =  1.06420880400844228286e-01
qa2  =  5.40397917702171048937e-01
qa3  =  7.18286544141962662868e-02
qa4  =  1.26171219808761642112e-01
qa5  =  1.36370839120290507362e-02
qa6  =  1.19844998467991074170e-02

def erf2(x):
    '''erf(x) for x in [0.84375,1.25]'''
    s = fabs(x)-one
    P = pa0+s*(pa1+s*(pa2+s*(pa3+s*(pa4+s*(pa5+s*pa6)))))
    Q = one+s*(qa1+s*(qa2+s*(qa3+s*(qa4+s*(qa5+s*qa6)))))
    if x>=0:
        return erx + P/Q
    return -erx - P/Q

def erfc2(x):
    '''erfc(x) for x in [0.84375, 1.25]'''
    return one-erf2(x)

## Coefficients for approximation to  erfc in [1.25,1/0.35]

ra0  = -9.86494403484714822705e-03
ra1  = -6.93858572707181764372e-01
ra2  = -1.05586262253232909814e+01
ra3  = -6.23753324503260060396e+01
ra4  = -1.62396669462573470355e+02
ra5  = -1.84605092906711035994e+02
ra6  = -8.12874355063065934246e+01
ra7  = -9.81432934416914548592e+00
sa1  =  1.96512716674392571292e+01
sa2  =  1.37657754143519042600e+02
sa3  =  4.34565877475229228821e+02
sa4  =  6.45387271733267880336e+02
sa5  =  4.29008140027567833386e+02
sa6  =  1.08635005541779435134e+02
sa7  =  6.57024977031928170135e+00
sa8  = -6.04244152148580987438e-02

def erf3(x):
    '''erf(x) for x in [1.25,2.857142]'''
    x0=x
    x = fabs(x)
    s = one/(x*x)
    R=ra0+s*(ra1+s*(ra2+s*(ra3+s*(ra4+s*(ra5+s*(ra6+s*ra7))))))
    S=one+s*(sa1+s*(sa2+s*(sa3+s*(sa4+s*(sa5+s*(sa6+s*(sa7+s*sa8)))))))
    z = ldexp(x0,0)
    r = exp(-z*z-0.5625)*exp((z-x)*(z+x)+R/S)
    if(x0>=0):
        return one-r/x
    else:
        return  r/x-one;

def erfc3(x):
    '''erfc(x) for x in [1.25,1/0.35]'''
    return one-erf3(x)

## Coefficients for approximation to  erfc in [1/.35,28]

rb0  = -9.86494292470009928597e-03
rb1  = -7.99283237680523006574e-01
rb2  = -1.77579549177547519889e+01
rb3  = -1.60636384855821916062e+02
rb4  = -6.37566443368389627722e+02
rb5  = -1.02509513161107724954e+03
rb6  = -4.83519191608651397019e+02
sb1  =  3.03380607434824582924e+01
sb2  =  3.25792512996573918826e+02
sb3  =  1.53672958608443695994e+03
sb4  =  3.19985821950859553908e+03
sb5  =  2.55305040643316442583e+03
sb6  =  4.74528541206955367215e+02
sb7  = -2.24409524465858183362e+01

def erf4(x):
    '''erf(x) for x in [1/.35,6]'''
    x0=x
    x = fabs(x)
    s = one/(x*x)
    R=rb0+s*(rb1+s*(rb2+s*(rb3+s*(rb4+s*(rb5+s*rb6)))))
    S=one+s*(sb1+s*(sb2+s*(sb3+s*(sb4+s*(sb5+s*(sb6+s*sb7))))))
    z  = ldexp(x0,0)
    r  =  exp(-z*z-0.5625)*exp((z-x)*(z+x)+R/S)
    if(z>=0):
        return one-r/x
    else:
        return  r/x-one;

def erfc4(x):
    '''erfc(x) for x in [2.857142,6]'''
    return one-erf4(x)

def erf5(x):
    '''erf(x) for |x| in [6,inf)'''
    if x>0:
        return one-tiny
    return tiny-one

def erfc5(x):
    '''erfc(x) for |x| in [6,inf)'''
    if (x>0):
        return tiny*tiny
    return two-tiny

#############
##inf = float('inf')
##nan = float('nan')
###########
inf = float(9e999)

def Erf(x):
    '''return the error function of x'''
    f = float(x)
    if (f == inf):
        return 1.0
    elif (f == -inf):
        return -1.0
##    elif (f is nan):
##        return nan
    else:
        if (abs(x)<0.84375):
            return erf1(x)
        elif (0.84375<=abs(x)<1.25):
            return erf2(x)
        elif (1.25<=abs(x)<2.857142):
            return erf3(x)
        elif (2.857142<=abs(x)<6):
            return erf4(x)
        elif (abs(x)>=6):
            return erf5(x)
    
def Erfc(x):
    '''return the complementary of error function of x'''
    f = float(x)
    if (f == inf):
        return 0.0
    elif (f is -inf):
        return 2.0
##    elif (f == nan):
##        return nan
    else:
        if (abs(x)<0.84375):
            return erfc1(x)
        elif (0.84375<=abs(x)<1.25):
            return erfc2(x)
        elif (1.25<=abs(x)<2.857142):
            return erfc3(x)
        elif (2.857142<=abs(x)<6):
            return erfc4(x)
        elif (abs(x)>=6):
            return erfc5(x)
