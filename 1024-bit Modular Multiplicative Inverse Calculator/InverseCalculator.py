from random import uniform

line = "=="*50

#binary: string -> decimal: int
def toDecimal(binary):
    binary = list(binary)[::-1]
    decimal = 0
    pow2 = 1
    for i in binary:
        if i=='1': decimal += pow2
        pow2 <<= 1
    return decimal

#decimal: int -> binary: string
def toBinary(decimal):
    if decimal == 0: return "0"
    binary = []
    while decimal:
        binary.append(decimal & 1)
        decimal >>= 1
    binary = ''.join(map(str,binary[::-1]))
    return binary

#generates 1 bit randomly
def random1():
    return int(uniform(0,1) < 0.5)

#generates random 1024 bit odd integer
def random1024():
    binary = [1]
    for i in range(1, 1023):
        binary.append(random1())
    binary.append(1)
    binary = "".join(map(str,binary))
    return toDecimal(binary)

#generates random number >=minN and <maxN
def rangedRandom(minN, maxN):
    n = minN + random1024() % maxN
    return n

#modular exponentiation -> returns (a^b) mod m
def modex(a, b, m):
    ans = 1
    a %= m
    while b:
        if b & 1: ans = (ans * a) % m
        b >>= 1
        a = (a * a) % m
    return ans

#miller rabin test for possible prime
""" Arguments:
n: number to test,
a: Integer such that 1 < a < n-1
k & q: integers such that (n - 1) = (2^k)*q
q must be odd +ve integer
"""
def Miller_Rabin(a, n, k, q):                       #as given in notes
    if modex(a, q, n) == 1:
        return True
    exp = q
    for j in range(k):
        if modex(a, exp, n) == n-1:
            return True
        exp <<= 1
    return False

#returns (result: boolean, test_count: integer)
def Test(n, limit):
    q, k = n-1, 1
    while not (q&1):
        k += 1
        q >>= 1
    for i in range(limit):
        a = int(rangedRandom(2, n-1))               #1 < a < n-1
        if not Miller_Rabin(a, n, k, q):
            return False, i+1
    return True, limit

#returns a possibly prime integer
def generatePrime():
    print("GENERATING 1024 BIT PRIME NUMBER")
    total_tries, total_tests, avg = 0, 0, 0
    found = False
    n = random1024()
    while not found:
        limit = int(10*avg) if total_tries else 40  #set limit to 40 for first test and 10*average for other tests
        found, tests = Test(n, limit)               #test n till limit
        total_tests += tests                        #update number of times the test function (Miller_Rabin()) is invoked
        total_tries += 1                            #update number of odd numbers tested
        print("Attempt #",total_tries,sep="")
        print("Result:","SUCCESS" if found else "FAILED"," |  Tests Done:", tests)
        if not found:
            avg = total_tests / total_tries
            n += 2
            if n > 1<<1024:                                         #overflow
                n = rangedRandom(1<<1023, n-2*total_tries-1000)
                n |= 1                                              #make n odd
    print(line)
    print("GENERATED 1024 BIT PRIME NUMBER (further referred as N):")
    print(n)
    return n

#extendedEuclid algorithm: returns {gcd(d,f), multiplicative inverse of f modulo d
"""
first argument (d) : modulus value
second argument (f): number whose multiplicative inverse if to be calculated
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

#returns (num1 * num2) mod modulus 
def multiply(num1, num2, modulus):          #used for checking correctness
    num1 %= modulus
    num2 %= modulus
    return (num1 * num2) % modulus

def main(N, A):
    gcd, inv = extendedEuclid(N, A)         #calculate gcd(N,A) & multiplicative inverse of A modulo N
    if gcd != 1: inv = None                 #if gcd(N,A) is not 1 then multiplicative inverse does not exist
    if inv is None:
        print("\nMultiplicative inverse of A modulo N DOES NOT EXIST.")
    else:
        print("\nMultiplicative inverse of A modulo N (further referred as inv):")
        print("DECIMAL")
        print(inv)
        print("\nBINARY")
        print(toBinary(inv))
        print("\nCheck for correctness: Performing (A * inv) mod N")
        print("RESULT:",multiply(A, inv, N))                        #print (A * inv) mod N
        print("(Further verification: Calculate the multiplicative inverse of inv (DECIMAL) printed above.)")

prime = generatePrime()
next = True
count = 0
while next:
    count += 1
    print("\n"+line)
    print("INPUT #{}".format(count))
    print(line)
    print("Enter a number (further referred as A) to find multiplicative inverse modulo N\n(OR Enter anything else to STOP)")
    inp = input().strip()
    try:
        A = int(inp)
        next = True
        main(prime, A)    
    except:
        next = False

print("Press ENTER key to stop / close program completely")
input()