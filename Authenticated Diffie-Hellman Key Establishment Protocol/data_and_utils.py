# -------------------------------X------------------------------- #
                    # PUBLIC DATA CONFIGURATION #
# -------------------------------X------------------------------- #

#all values should be in hexadecimal (as strings made of octets separated by spaces)

#prime p in hexadecimal (must me greater than 3)
p = "FFFFFFFF 00000001 00000000 00000000 00000000 FFFFFFFF FFFFFFFF FFFFFFFF"

#parameters a & b in EC y^2 = x^3 + ax + b
a = "FFFFFFFF 00000001 00000000 00000000 00000000 FFFFFFFF FFFFFFFF FFFFFFFC"
b = "5AC635D8 AA3A93E7 B3EBBD55 769886BC 651D06B0 CC53B0F6 3BCE3C3E 27D2604B"

# Generator (base point), Gx = X coordinate, and Gy = Y coordinate 
Gx = "6B17D1F2 E12C4247 F8BCE6E5 63A440F2 77037D81 2DEB33A0 F4A13945 D898C296"
Gy = "4FE342E2 FE1A7F9B 8EE7EB4A 7C0F9E16 2BCE3357 6B315ECE CBB64068 37BF51F5"

# Order of G
n = "FFFFFFFF 00000000 FFFFFFFF FFFFFFFF BCE6FAAD A7179E84 F3B9CAC2 FC632551"

# The used Elliptic Curve is taken from Page 16, SEC 2: Recommended Elliptic Curve Domain Parameters Ver. 1.0

def toInt(s):
    s = eval("0x" + "".join(s.split()))
    return s

hlen = 8*len(p.split()) #length of hexadecimal string of p
blen = 8*hlen           #number of bits in p

p, a, b, Gx, Gy, n = map(toInt, (p, a, b, Gx, Gy, n))
G = [Gx, Gy]


# -------------------------------X------------------------------- #
                           # UTILITIES #
# -------------------------------X------------------------------- #

import time

class Timer:
    """timer class for easy time calcuations"""
    def __init__(self):
        self.begin = time.time_ns()
    def start(self):
        self.begin = time.time_ns()
    def lap(self):
        return (time.time_ns() - self.begin)/10**6

#extendedEuclid algorithm: returns {gcd(d,f), multiplicative inverse of f modulo d
"""
first argument (d) : modulus value
second argument (f): number whose multiplicative inverse is to be calculated
"""
def extendedEuclid(d, f):                           #as given in notes
    x1, x2, x3 = 1, 0, f
    y1, y2, y3 = 0, 1, d
    t1, t2, t3 = 0, 1, d
    inv = None
    while d>1:
        if t3==0: 
            return x3, inv
        if t3==1:
            inv = y1 % d
            return y3, inv
        q = x3 // y3
        t1, t2, t3 = x1-q*y1, x2-q*y2, x3-q*y3
        x1, x2, x3 = y1, y2, y3
        y1, y2, y3 = t1, t2, t3
    return None, None

def intToPaddedHex(K):
    """converts integer to padded hexadecimal of n length (assuming |K| <= n)"""
    hexK = hex(K).replace("0x","")
    diff = hlen - len(hexK)
    hexK = "0"*diff + hexK
    return hexK

def pt_2x(pt):
    """function to double a point"""
    if pt == [0, 0]: return pt              # zero element
    x1, y1 = pt

    #slope calculation
    numr =  ( 3*(x1*x1)%p + a ) % p
    denr = (2*y1) % p
    gcd, den_inv = extendedEuclid(p, denr)
    assert(den_inv is not None)
    m = (numr * den_inv) % p

    #point 2pt
    x2 = ((m*m)%p - 2*x1) % p
    y2 = ((x1 - x2)*m - y1) % p
    return [x2, y2]

def pt_add(p1, p2):
    """function to add two points"""
    if p1 == [0, 0]: return p2              # p1 is zero element
    if p2 == [0, 0]: return p1              # p2 is zero element
    if p1 == p2: return pt_2x(p1)           # point double

    x1, y1 = p1
    x2, y2 = p2

    #slope calculation
    numr =  (y2-y1) % p
    denr = (x2-x1) % p
    gcd, den_inv = extendedEuclid(p, denr)
    assert(den_inv is not None)
    m = (numr * den_inv) % p

    #point 2pt
    x3 = ((m*m)%p - x1 - x2) % p
    y3 = ((x1 - x3)*m - y1) % p
    return [x3, y3]

def bin_multiply(k, pt):
    """point multiplication when k is a perfect power of 2"""
    if pt == [0, 0]: return pt              # zero element
    Q = pt.copy() if k else [0,0]
    while k>1:
        Q = pt_2x(Q)
        k >>= 1
    return Q

#referred from Algorithm IV.3: Modified m-ary method for point multiplication, Page 65, Elliptic Curves in Cryptography (by I.F. Blake, G. Seroussi and N.P. Smart)
def pt_multiply(k, pt):
    """function for point multiplication"""
    r = 5
    m = 2**r

    #precomputation
    P = [0 for _ in range(m+1)]
    P[1] = pt.copy()
    P[2] = pt_2x(pt)
    for i in range(1,m>>1):
        i2 = i<<1
        P[i2+1] = pt_add(P[i2-1],P[2])
    Q = [0,0]

    # decomposing k in base m
    K = k
    k = []
    mask = m - 1
    while K:
        k.append(K & mask)
        K >>= r

    k=k[::-1]
    
    # main loop, traversing base-m representation of k in reverse order
    for j in k:
        if j:
            s = j & -j                          #s=2^i, h is odd & j = s*h
            h = j//s
            scal = 1<<r
            while s>1: s, scal = s>>1, scal>>1
            Q = bin_multiply(scal, Q)           #Q = [2^(r-i)]Q
            Q = pt_add(Q, P[h])
        else:
            Q = bin_multiply(1<<r, Q)
    return Q