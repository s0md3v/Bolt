#!/usr/bin/env python3

import numpy as np
from math import floor, log
import scipy.special as spc
import scipy.fftpack as sff
import scipy.stats as sst
from functools import reduce


def sumi(x): return 2 * x - 1


def su(x, y): return x + y


def sus(x): return (x - 0.5) ** 2


def sq(x): return int(x) ** 2


def logo(x): return x * np.log(x)


def pr(u, x):
    if u == 0:
        out = 1.0 * np.exp(-x)
    else:
        out = 1.0 * x * np.exp(2*-x) * (2**-u) * spc.hyp1f1(u + 1, 2, x)
    return out


def stringpart(binin, num):
    blocks = [binin[xs * num:num + xs * num:]
              for xs in range(floor(len(binin) / num))]
    return blocks


def randgen(num):
    '''Spits out a stream of random numbers like '1001001' with the length num'''

    rn = open('/dev/urandom', 'r')
    random_chars = rn.read(num / 2)
    stream = ''
    for char in random_chars:
        c = ord(char)
        for i in range(0, 2):
            stream += str(c >> i & 1)
    return stream


def monobitfrequencytest(binin):
    ''' The focus of the test is the proportion of zeroes and ones for the entire sequence. The purpose of this test is to determine whether that number of ones and zeros in a sequence are approximately the same as would be expected for a truly random sequence. The test assesses the closeness of the fraction of ones to 1/2, that is, the number of ones and zeroes in a sequence should be about the same.'''

    ss = [int(el) for el in binin]
    sc = list(map(sumi, ss))
    sn = reduce(su, sc)
    sobs = np.abs(sn) / np.sqrt(len(binin))
    pval = spc.erfc(sobs / np.sqrt(2))
    return pval


def blockfrequencytest(binin, nu=20):
    ''' The focus of the test is the proportion of zeroes and ones within M-bit blocks. The purpose of this test is to determine whether the frequency of ones is an M-bit block is approximately M/2.'''
    ss = [int(el) for el in binin]
    tt = [1.0 * sum(ss[xs * nu:nu + xs * nu:]) /
          nu for xs in range(floor(len(ss) / nu))]
    uu = list(map(sus, tt))
    chisqr = 4 * nu * reduce(su, uu, 0)
    pval = spc.gammaincc(len(tt) / 2.0, chisqr / 2.0)
    return pval


def runstest(binin):
    ''' The focus of this test is the total number of zero and one runs in the entire sequence, where a run is an uninterrupted sequence of identical bits. A run of length k means that a run consists of exactly k identical bits and is bounded before and after with a bit of the opposite value. The purpose of the runs test is to determine whether the number of runs of ones and zeros of various lengths is as expected for a random sequence. In particular, this test determines whether the oscillation between such substrings is too fast or too slow.'''
    ss = [int(el) for el in binin]
    n = len(binin)
    pi = 1.0 * reduce(su, ss) / n
    vobs = len(binin.replace('0', ' ').split()) + \
        len(binin.replace('1', ' ').split())
    pval = spc.erfc(abs(vobs-2*n*pi*(1-pi)) /
                    (2 * pi * (1 - pi) * np.sqrt(2*n)))
    return pval


def longestrunones8(binin):
    ''' The focus of the test is the longest run of ones within M-bit blocks. The purpose of this test is to determine whether the length of the longest run of ones within the tested sequence is consistent with the length of the longest run of ones that would be expected in a random sequence. Note that an irregularity in the expected length of the longest run of ones implies that there is also an irregularity in the expected length of the longest run of zeroes. Long runs of zeroes were not evaluated separately due to a concern about statistical independence among the tests.'''
    m = 8
    k = 3
    pik = [0.2148, 0.3672, 0.2305, 0.1875]
    blocks = [binin[xs*m:m+xs*m:] for xs in range(len(binin) / m)]
    n = len(blocks)
    # append the string 01 to guarantee the length of 1
    counts1 = [xs+'01' for xs in blocks]
    counts = [xs.replace('0', ' ').split()
              for xs in counts1]  # split into all parts
    counts2 = [list(map(len, xx)) for xx in counts]
    counts4 = [(4 if xx > 4 else xx) for xx in map(max, counts2)]
    freqs = [counts4.count(spi) for spi in [1, 2, 3, 4]]
    chisqr1 = [(freqs[xx]-n*pik[xx])**2/(n*pik[xx]) for xx in range(4)]
    chisqr = reduce(su, chisqr1)
    pval = spc.gammaincc(k / 2.0, chisqr / 2.0)
    return pval


def longestrunones128(binin):  # not well tested yet
    if len(binin) > 128:
        m = 128
        k = 5
        n = len(binin)
        pik = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
        blocks = [binin[xs * m:m + xs * m:] for xs in range(len(binin) / m)]
        n = len(blocks)
        counts = [xs.replace('0', ' ').split() for xs in blocks]
        counts2 = [list(map(len, xx)) for xx in counts]
        counts3 = [(1 if xx < 1 else xx) for xx in map(max, counts2)]
        counts4 = [(4 if xx > 4 else xx) for xx in counts3]
        chisqr1 = [(counts4[xx] - n * pik[xx]) ** 2 / (n * pik[xx])
                   for xx in range(len(counts4))]
        chisqr = reduce(su, chisqr1)
        pval = spc.gammaincc(k / 2.0, chisqr / 2.0)
    else:
        print('longestrunones128 failed, too few bits:', len(binin))
        pval = 0
    return pval


def longestrunones10000(binin):  # not well tested yet
    ''' The focus of the test is the longest run of ones within M-bit blocks. The purpose of this test is to determine whether the length of the longest run of ones within the tested sequence is consistent with the length of the longest run of ones that would be expected in a random sequence. Note that an irregularity in the expected length of the longest run of ones implies that there is also an irregularity in the expected length of the longest run of zeroes. Long runs of zeroes were not evaluated separately due to a concern about statistical independence among the tests.'''
    if len(binin) > 128:
        m = 10000
        k = 6
        pik = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]
        blocks = [binin[xs * m:m + xs * m:]
                  for xs in range(floor(len(binin) / m))]
        n = len(blocks)
        counts = [xs.replace('0', ' ').split() for xs in blocks]
        counts2 = [list(map(len, xx)) for xx in counts]
        counts3 = [(10 if xx < 10 else xx) for xx in map(max, counts2)]
        counts4 = [(16 if xx > 16 else xx) for xx in counts3]
        freqs = [counts4.count(spi) for spi in [10, 11, 12, 13, 14, 15, 16]]
        chisqr1 = [(freqs[xx] - n * pik[xx]) ** 2 / (n * pik[xx])
                   for xx in range(len(freqs))]
        chisqr = reduce(su, chisqr1)
        pval = spc.gammaincc(k / 2.0, chisqr / 2.0)
    else:
        print('longestrunones10000 failed, too few bits:', len(binin))
        pval = 0
    return pval

# test 2.06


def spectraltest(binin):
    '''The focus of this test is the peak heights in the discrete Fast Fourier Transform. The purpose of this test is to detect periodic features (i.e., repetitive patterns that are near each other) in the tested sequence that would indicate a deviation from the assumption of randomness. '''

    n = len(binin)
    ss = [int(el) for el in binin]
    sc = list(map(sumi, ss))
    ft = sff.fft(sc)
    af = abs(ft)[1:floor(n/2)+1:]
    t = np.sqrt(np.log(1/0.05)*n)
    n0 = 0.95*n/2
    n1 = len(np.where(af < t)[0])
    d = (n1 - n0)/np.sqrt(n*0.95*0.05/4)
    pval = spc.erfc(abs(d)/np.sqrt(2))
    return pval


def nonoverlappingtemplatematchingtest(binin, mat="000000001", num=9):
    ''' The focus of this test is the number of occurrences of pre-defined target substrings. The purpose of this test is to reject sequences that exhibit too many occurrences of a given non-periodic (aperiodic) pattern. For this test and for the Overlapping Template Matching test, an m-bit window is used to search for a specific m-bit pattern. If the pattern is not found, the window slides one bit position. For this test, when the pattern is found, the window is reset to the bit after the found pattern, and the search resumes.'''
    n = len(binin)
    m = len(mat)
    M = floor(n/num)
    blocks = [binin[xs*M:M+xs*M:] for xs in range(floor(n/M))]
    counts = [xx.count(mat) for xx in blocks]
    avg = 1.0 * (M-m+1)/2 ** m
    var = M*(2**-m - (2*m-1)*2**(-2*m))
    chisqr = reduce(su, [(xs - avg) ** 2 for xs in counts]) / var
    pval = spc.gammaincc(1.0 * len(blocks) / 2, chisqr / 2)
    return pval


def occurances(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start)+1
        if start > 0:
            count += 1
        else:
            return count


def overlappingtemplatematchingtest(binin, mat="111111111", num=1032, numi=9):
    ''' The focus of this test is the number of pre-defined target substrings. The purpose of this test is to reject sequences that show deviations from the expected number of runs of ones of a given length. Note that when there is a deviation from the expected number of ones of a given length, there is also a deviation in the runs of zeroes. Runs of zeroes were not evaluated separately due to a concern about statistical independence among the tests. For this test and for the Non-overlapping Template Matching test, an m-bit window is used to search for a specific m-bit pattern. If the pattern is not found, the window slides one bit position. For this test, when the pattern is found, the window again slides one bit, and the search is resumed.'''
    n = len(binin)
    bign = int(n / num)
    m = len(mat)
    lamda = 1.0 * (num - m + 1) / 2 ** m
    eta = 0.5 * lamda
    pi = [pr(i, eta) for i in range(numi)]
    pi.append(1 - reduce(su, pi))
    v = [0 for x in range(numi + 1)]
    blocks = stringpart(binin, num)
    blocklen = len(blocks[0])
    counts = [occurances(i, mat) for i in blocks]
    counts2 = [(numi if xx > numi else xx) for xx in counts]
    for i in counts2:
        v[i] = v[i] + 1
    chisqr = reduce(su, [(v[i]-bign*pi[i]) ** 2 / (bign*pi[i])
                         for i in range(numi + 1)])
    pval = spc.gammaincc(0.5*numi, 0.5*chisqr)
    return pval


def maurersuniversalstatistictest(binin, l=6, q=640):
    ''' The focus of this test is the number of bits between matching patterns. The purpose of the test is to detect whether or not the sequence can be significantly compressed without loss of information. An overly compressible sequence is considered to be non-random.'''
    ru = [
        [0.7326495, 0.690],
        [1.5374383, 1.338],
        [2.4016068, 1.901],
        [3.3112247, 2.358],
        [4.2534266, 2.705],
        [5.2177052, 2.954],
        [6.1962507, 3.125],
        [7.1836656, 3.238],
        [8.1764248, 3.311],
        [9.1723243, 3.356],
        [10.170032, 3.384],
        [11.168765, 3.401],
        [12.168070, 3.410],
        [13.167693, 3.416],
        [14.167488, 3.419],
        [15.167379, 3.421],
    ]
    blocks = [int(li, 2) + 1 for li in stringpart(binin, l)]
    k = len(blocks) - q
    states = [0 for x in range(2**l)]
    for x in range(q):
        states[blocks[x]-1] = x+1
    sumi = 0.0
    for x in range(q, len(blocks)):
        sumi += np.log2((x+1)-states[blocks[x]-1])
        states[blocks[x]-1] = x+1
    fn = sumi / k
    c = 0.7-(0.8/l)+(4+(32.0/l))*((k**(-3.0/l))/15)
    sigma = c*np.sqrt((ru[l-1][1])/k)
    pval = spc.erfc(abs(fn-ru[l-1][0]) / (np.sqrt(2)*sigma))
    return pval


def lempelzivcompressiontest1(binin):
    ''' The focus of this test is the number of cumulatively distinct patterns (words) in the sequence. The purpose of the test is to determine how far the tested sequence can be compressed. The sequence is considered to be non-random if it can be significantly compressed. A random sequence will have a characteristic number of distinct patterns.'''
    i = 1
    j = 0
    n = len(binin)
    mu = 69586.25
    sigma = 70.448718
    words = []
    while (i+j) <= n:
        tmp = binin[i:i+j:]
        if words.count(tmp) > 0:
            j += 1
        else:
            words.append(tmp)
            i += j+1
            j = 0
    wobs = len(words)
    pval = 0.5*spc.erfc((mu-wobs)/np.sqrt(2.0*sigma))
    return pval

# test 2.11


def serialtest(binin):
    m = int(log(len(binin), 2) - 3)
    ''' The focus of this test is the frequency of each and every overlapping m-bit pattern across the entire sequence. The purpose of this test is to determine whether the number of occurrences of the 2m m-bit overlapping patterns is approximately the same as would be expected for a random sequence. The pattern can overlap.'''
    n = len(binin)
    hbin = binin+binin[0:m-1:]
    f1a = [hbin[xs:m+xs:] for xs in range(n)]
    oo = set(f1a)
    f1 = [f1a.count(xs)**2 for xs in oo]
    f1 = list(map(f1a.count, oo))
    cou = f1a.count
    f2a = [hbin[xs:m-1+xs:] for xs in range(n)]
    f2 = [f2a.count(xs)**2 for xs in set(f2a)]
    f3a = [hbin[xs:m-2+xs:] for xs in range(n)]
    f3 = [f3a.count(xs)**2 for xs in set(f3a)]
    psim1 = 0
    psim2 = 0
    psim3 = 0
    if m >= 0:
        suss = reduce(su, f1)
        psim1 = 1.0 * 2 ** m * suss / n - n
    if m >= 1:
        suss = reduce(su, f2)
        psim2 = 1.0 * 2 ** (m - 1) * suss / n - n
    if m >= 2:
        suss = reduce(su, f3)
        psim3 = 1.0 * 2 ** (m - 2) * suss / n - n
    d1 = psim1-psim2
    d2 = psim1-2 * psim2 + psim3
    pval1 = spc.gammaincc(2 ** (m - 2), d1 / 2.0)
    pval2 = spc.gammaincc(2 ** (m - 3), d2 / 2.0)
    return [pval1, pval2]


def cumultativesumstest(binin):
    ''' The focus of this test is the maximal excursion (from zero) of the random walk defined by the cumulative sum of adjusted (-1, +1) digits in the sequence. The purpose of the test is to determine whether the cumulative sum of the partial sequences occurring in the tested sequence is too large or too small relative to the expected behavior of that cumulative sum for random sequences.  This cumulative sum may be considered as a random walk. For a random sequence, the random walk should be near zero. For non-random sequences, the excursions of this random walk away from zero will be too large.'''
    n = len(binin)
    ss = [int(el) for el in binin]
    sc = list(map(sumi, ss))
    cs = np.cumsum(sc)
    z = max(abs(cs))
    ra = 0
    start = int(np.floor(0.25 * np.floor(-n / z) + 1))
    stop = int(np.floor(0.25 * np.floor(n / z) - 1))
    pv1 = []
    for k in range(start, stop + 1):
        pv1.append(sst.norm.cdf((4 * k + 1) * z / np.sqrt(n)) -
                   sst.norm.cdf((4 * k - 1) * z / np.sqrt(n)))
    start = int(np.floor(0.25 * np.floor(-n / z - 3)))
    stop = int(np.floor(0.25 * np.floor(n / z) - 1))
    pv2 = []
    for k in range(start, stop + 1):
        pv2.append(sst.norm.cdf((4 * k + 3) * z / np.sqrt(n)) -
                   sst.norm.cdf((4 * k + 1) * z / np.sqrt(n)))
    pval = 1
    pval -= reduce(su, pv1)
    pval += reduce(su, pv2)

    return pval


def cumultativesumstestreverse(binin):
    '''The focus of this test is the maximal excursion (from zero) of the random walk defined by the cumulative sum of adjusted (-1, +1) digits in the sequence. The purpose of the test is to determine whether the cumulative sum of the partial sequences occurring in the tested sequence is too large or too small relative to the expected behavior of that cumulative sum for random sequences.  This cumulative sum may be considered as a random walk. For a random sequence, the random walk should be near zero. For non-random sequences, the excursions of this random walk away from zero will be too large. '''
    pval = cumultativesumstest(binin[::-1])
    return pval


def pik(k, x):
    if k == 0:
        out = 1-1.0/(2*np.abs(x))
    elif k >= 5:
        out = (1.0/(2*np.abs(x)))*(1-1.0/(2*np.abs(x)))**4
    else:
        out = (1.0/(4*x*x))*(1-1.0/(2*np.abs(x)))**(k-1)
    return out


def randomexcursionstest(binin):
    ''' The focus of this test is the number of cycles having exactly K visits in a cumulative sum random walk. The cumulative sum random walk is found if partial sums of the (0,1) sequence are adjusted to (-1, +1). A random excursion of a random walk consists of a sequence of n steps of unit length taken at random that begin at and return to the origin. The purpose of this test is to determine if the number of visits to a state within a random walk exceeds what one would expect for a random sequence.'''
    xvals = [-4, -3, -2, -1, 1, 2, 3, 4]
    ss = [int(el) for el in binin]
    sc = list(map(sumi, ss))
    cumsum = np.cumsum(sc)
    cumsum = np.append(cumsum, 0)
    cumsum = np.append(0, cumsum)
    posi = np.where(cumsum == 0)[0]
    cycles = ([cumsum[posi[x]:posi[x+1]+1] for x in range(len(posi)-1)])
    j = len(cycles)
    sct = []
    for ii in cycles:
        sct.append(([len(np.where(ii == xx)[0]) for xx in xvals]))
    sct = np.transpose(np.clip(sct, 0, 5))
    su = []
    for ii in range(6):
        su.append([(xx == ii).sum() for xx in sct])
    su = np.transpose(su)
    pikt = ([([pik(uu, xx) for uu in range(6)]) for xx in xvals])
    # chitab=1.0*((su-j*pikt)**2)/(j*pikt)
    chitab = np.sum(1.0*(np.array(su)-j*np.array(pikt))
                    ** 2/(j*np.array(pikt)), axis=1)
    pval = ([spc.gammaincc(2.5, cs/2.0) for cs in chitab])
    return pval


def getfreq(linn, nu):
    val = 0
    for (x, y) in linn:
        if x == nu:
            val = y
    return val


def randomexcursionsvarianttest(binin):
    ''' The focus of this test is the number of times that a particular state occurs in a cumulative sum random walk. The purpose of this test is to detect deviations from the expected number of occurrences of various states in the random walk.'''
    ss = [int(el) for el in binin]
    sc = list(map(sumi, ss))
    cs = np.cumsum(sc)
    li = []
    for xs in sorted(set(cs)):
        if np.abs(xs) <= 9:
            li.append([xs, len(np.where(cs == xs)[0])])
    j = getfreq(li, 0) + 1
    pval = []
    for xs in range(-9, 9 + 1):
        if not xs == 0:
            # pval.append([xs, spc.erfc(np.abs(getfreq(li, xs) - j) / np.sqrt(2 * j * (4 * np.abs(xs) - 2)))])
            pval.append(spc.erfc(np.abs(getfreq(li, xs) - j) /
                                 np.sqrt(2 * j * (4 * np.abs(xs) - 2))))
    return pval


def aproximateentropytest(binin, m=5):
    ''' The focus of this test is the frequency of each and every overlapping m-bit pattern. The purpose of the test is to compare the frequency of overlapping blocks of two consecutive/adjacent lengths (m and m+1) against the expected result for a random sequence.'''
    n = len(binin)
    f1a = [(binin + binin[0:m - 1:])[xs:m + xs:] for xs in range(n)]
    f1 = [[xs, f1a.count(xs)] for xs in sorted(set(f1a))]
    f2a = [(binin + binin[0:m:])[xs:m + 1 + xs:] for xs in range(n)]
    f2 = [[xs, f2a.count(xs)] for xs in sorted(set(f2a))]
    c1 = [1.0 * f1[xs][1] / n for xs in range(len(f1))]
    c2 = [1.0 * f2[xs][1] / n for xs in range(len(f2))]
    phi1 = reduce(su, list(map(logo, c1)))
    phi2 = reduce(su, list(map(logo, c2)))
    apen = phi1 - phi2
    chisqr = 2.0 * n * (np.log(2) - apen)
    pval = spc.gammaincc(2 ** (m - 1), chisqr / 2.0)
    return pval


def matrank(mat):  # old function, does not work as advertized - gives the matrix rank, but not binary
    u, s, v = np.linalg.svd(mat)
    rank = np.sum(s > 1e-10)
    return rank


def mrank(matrix):  # matrix rank as defined in the NIST specification
    m = len(matrix)
    leni = len(matrix[0])

    def proc(mat):
        for i in range(m):
            if mat[i][i] == 0:
                for j in range(i+1, m):
                    if mat[j][i] == 1:
                        mat[j], mat[i] = mat[i], mat[j]
                        break
            if mat[i][i] == 1:
                for j in range(i+1, m):
                    if mat[j][i] == 1:
                        mat[j] = [mat[i][x] ^ mat[j][x] for x in range(leni)]
        return mat
    maa = proc(matrix)
    maa.reverse()
    mu = [i[::-1] for i in maa]
    muu = proc(mu)
    ra = np.sum(np.sign([xx.sum() for xx in np.array(mu)]))
    return ra


def binarymatrixranktest(binin, m=32, q=32):
    ''' The focus of the test is the rank of disjoint sub-matrices of the entire sequence. The purpose of this test is to check for linear dependence among fixed length substrings of the original sequence.'''
    p1 = 1.0
    for x in range(1, 50):
        p1 *= 1-(1.0/(2**x))
    p2 = 2*p1
    p3 = 1-p1-p2
    n = len(binin)
    # the input string as numbers, to generate the dot product
    u = [int(el) for el in binin]
    f1a = [u[xs*m:xs*m+m:] for xs in range(floor(n/m))]
    n = len(f1a)
    f2a = [f1a[xs*q:xs*q+q:] for xs in range(floor(n/q))]
    # r=map(matrank,f2a)
    r = list(map(mrank, f2a))
    n = len(r)
    fm = r.count(m)
    fm1 = r.count(m-1)
    chisqr = ((fm-p1*n)**2)/(p1*n)+((fm1-p2*n)**2) / \
        (p2*n)+((n-fm-fm1-p3*n)**2)/(p3*n)
    pval = np.exp(-0.5*chisqr)
    return pval


def lincomplex(binin):
    lenn = len(binin)
    c = b = np.zeros(lenn)
    c[0] = b[0] = 1
    l = 0
    m = -1
    n = 0
    # the input string as numbers, to generate the dot product
    u = [int(el) for el in binin]
    p = 99
    while n < lenn:
        v = u[(n-l):n]  # was n-l..n-1
        v.reverse()
        cc = c[1:l+1]  # was 2..l+1
        d = (u[n]+np.dot(v, cc)) % 2
        if d == 1:
            tmp = c
            p = np.zeros(lenn)
            for i in range(0, l):  # was 1..l+1
                if b[i] == 1:
                    p[i+n-m] = 1
            c = (c+p) % 2
            if l <= 0.5*n:  # was if 2l <= n
                l = n+1-l
                m = n
                b = tmp
        n += 1
    return l

# test 2.10


def linearcomplexitytest(binin, m=500):
    ''' The focus of this test is the length of a generating feedback register. The purpose of this test is to determine whether or not the sequence is complex enough to be considered random. Random sequences are characterized by a longer feedback register. A short feedback register implies non-randomness.'''
    k = 6
    pi = [0.01047, 0.03125, 0.125, 0.5, 0.25, 0.0625, 0.020833]
    avg = 0.5*m + (1.0/36)*(9 + (-1)**(m + 1)) - (m/3.0 + 2.0/9)/2**m
    blocks = stringpart(binin, m)
    bign = len(blocks)
    lc = ([lincomplex(chunk) for chunk in blocks])
    t = ([-1.0*(((-1)**m)*(chunk-avg)+2.0/9) for chunk in lc])
    vg = np.histogram(t, bins=[-9999999999, -2.5, -
                               1.5, -0.5, 0.5, 1.5, 2.5, 9999999999])[0][::-1]
    im = ([((vg[ii]-bign*pi[ii])**2)/(bign*pi[ii]) for ii in range(7)])
    chisqr = reduce(su, im)
    pval = spc.gammaincc(k/2.0, chisqr/2.0)
    return pval


def isRandom(bits):
    result = {}

    def adder(name, p):
        if 'list' in str(type(p)):
            count = 0
            for i in p:
                if 'nan' in str(i):
                    pass
                elif 'e' in str(i):
                    pass
                elif i > 0.01:
                    pass
                else:
                    count += 1
            if count >= (len(p)/2):
                result[name] = False
            else:
                result[name] = True
        elif 'e' in str(p):
            pass
        elif p > 0.01:
            result[name] = True
        else:
            result[name] = False
    try:
        adder('Monobit frequency test', monobitfrequencytest(bits[:100]))
    except:
        pass
    try:
        adder('Block frequency test', blockfrequencytest(bits[:2000]))
    except:
        pass
    try:
        adder('Runs test', runstest(bits))
    except:
        pass
    try:
        adder('Spectral test', spectraltest(bits[:1024]))
    except:
        pass
    try:
        adder('Non-overlapping template matching test',
              nonoverlappingtemplatematchingtest(bits[:1048576], '11111', 8))
    except:
        pass
    try:
        adder('Overlapping template matching test',
              overlappingtemplatematchingtest(bits[:998976], '0000001', 12, 5))
    except:
        pass
    try:
        adder('Serial test', serialtest(bits[:500]))
    except:
        pass
    try:
        adder('Cumultative sums test', cumultativesumstest(bits[:100]))
    except:
        pass
    try:
        adder('Aproximate entropy test', aproximateentropytest(bits[:500], 5))
    except:
        pass
    try:
        adder('Random excursions variant test',
              randomexcursionsvarianttest(bits[:1000000]))
    except:
        pass
    try:
        adder('Linear complexity test',
              linearcomplexitytest(bits[:1000000], 10))
    except:
        pass
    try:
        adder('Longest runs test', longestrunones10000(bits))
    except:
        pass
    try:
        adder('Maurers universal statistic test',
              maurersuniversalstatistictest(bits[:387840], 6, 640))
    except:
        pass
    try:
        adder('Random excursions test', randomexcursionstest(bits[:1000000]))
    except:
        pass
    return result
