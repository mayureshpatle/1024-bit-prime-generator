def multiply(a, b):
    """This function returns product of two 128-bit polynomials."""
    pos = 1<<127
    prod = 0
    for i in range(127, -1, -1):
        if pos & a:
            prod ^= b << i
        pos >>= 1
    return prod

def mod(p):
    """
    This function returns p mod (x^128 + x^7 + x^2 + x + 1),
    Here p is 256-bit polynomial (integer).
    """
    m = (1<<128) | (1<<7) | (1<<2) | (1<<1) | 1
    pos = 1 << 255
    curr = m << 127
    c=0
    for i in range(127, -1, -1):
        if pos & p:
            p ^= curr
        curr >>= 1
        pos >>= 1
        c += 1
    return p

def inp():
    """ 
    this function inputs polynomials from user
    and returns corresponding integers by setting the appropriate bits,
    same number if entered multiple times in sequence will be considered only once.
    """
    print("Enter the polynomials as a sequence of integers separated by spaces")
    p1 = list(map(int, input("Enter first polynomial: ").split()))
    p2 = list(map(int, input("Enter second polynomial: ").split()))
    p1, p2 = set(p1), set(p2)
    max1, max2 = max(p1), max(p2)
    if max1>127 or max2>127:
        print("ERROR: Polymomials should be 128-bit")
        raise Exception
    n1, n2 = 0, 0
    for i in p1:
        n1 |= 1<<i
    for i in p2:
        n2 |= 1<<i
    return n1, n2

def toSeq(num):
    """Converts 128-bit integer back to sequence representing polynomial"""
    res = []
    pos = 1<<127
    for i in range(127, -1, -1):
        if pos & num:
            res.append(i)
        pos >>= 1
    return res

def main():
    try:
        a, b = inp()
        prod = multiply(a, b)
        res = mod(prod)
        print("Result:",*toSeq(res))
    except:
        print("------------|| TERMINATED: Invalid Input ||------------")

#main loop
c = "1"
cnt = 1
while c=="1":
    print("INPUT #{}:".format(cnt))
    main()
    print()
    print("Enter 1 to enter next input or anything else to STOP")
    c = input().strip()
    print()
    cnt += 1

print("Press ENTER key to exit terminal/close program.")
input()
