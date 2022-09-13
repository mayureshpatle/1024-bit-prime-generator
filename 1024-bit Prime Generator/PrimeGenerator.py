from random import uniform

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
def Miller_Rabin(a, n, k, q):                   #as given in notes
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
        a = int(rangedRandom(2, n-1))             #1 < a < n-1
        if not Miller_Rabin(a, n, k, q):
            return False, i+1
    return True, limit

#return a possibly prime integer
def generatePrime():
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
    return n

def main():
    print("GENERATING 1024 BIT PRIME NUMBER")
    prime = generatePrime()
    print("=="*50)
    print("GENERATED 1024 BIT PRIME NUMBER:")
    print("\nDECIMAL")
    print(prime)
    print("\nBINARY")
    print(toBinary(prime))

next = True
while next:
    main()
    print("=="*50)
    print("Enter 1 to generate another prime or any other input to stop")
    c = input().strip()
    next = c=='1'

print("Press ENTER key to stop / close program completely")
input()