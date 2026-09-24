import sys

"""
Compute GCD of two integers by successive integer divisions
allow negative inputs
output should always be non-negative
"""
def euclid_gcd(a: int, b: int) -> int:
    # print( f'computing GCD(a={a}, b={b}).' )
    if a<0:
        return euclid_gcd(-a, b)
    if b<0:
        return euclid_gcd(a, -b)
    if a<b:
        return euclid_gcd(b, a)
    if b==0:
        return a
    if b==a:
        return a

    assert a > b
    assert b > 0

    # a > b > 0
    # print('starting recursion')
    return euclid_gcd(b, a - b*(a//b))



""" 
default behaviors assuming a >= b:
    a==b -> (1,0,a)
    b==0 -> (1,0,a)

template:     r0 = q1*r1 + r2
r0 = a      r1 = b      r2 = r0 - q1*r1
s0 = 1      s1 = 0      s2 = s0 - q1*s1
t0 = 0      t1 = 1      t2 = t0 - q1*t1

signs:
run ext_gcd(|a|, |b|) to get (s1, t1, r1)
set 
    s1 = sgn(a)*a   if a!=0
    t1 = sgn(b)*b   if b!=0
"""


def do_ext_gcd(a:int, b:int) -> tuple[int,int,int]:
    r0 = a; s0 = 1; t0 = 0
    r1 = b; s1 = 0; t1 = 1

    q1 = r0//r1; r2 = r0 - q1*r1
    r2 = r0 - q1*r1
    s2 = s0 - q1*s1
    t2 = t0 - q1*t1

    while r2 != 0:
        # print(f""" 
        # beginning step with:
        # r0 = {r0}      r1 = {r1}      r2 = {r0 - q1*r1}
        # s0 = {s0}      s1 = {s1}      s2 = {s0 - q1*s1}
        # t0 = {t0}      t1 = {t1}      t2 = {t0 - q1*t1}
        # """)
        r0, s0, t0 = r1, s1, t1 
        r1, s1, t1 = r2, s2, t2 
        q1 = r0//r1; 
        r2 = r0 - q1*r1 
        s2 = s0 - q1*s1
        t2 = t0 - q1*t1
        assert r0 == q1*r1+r2

    """assert s1*a + t1*b == r1
    assert a%r1 == 0
    assert b%r1 == 0
    assert euclid_gcd(a,b) == r1"""

    return (s1, t1, r1)

def sgn(a:int):
    return 2*(a>0) - 1

def ext_gcd(a:int, b:int) -> tuple[int,int,int]:
    # print(f'ext_gcd(a={a}, b={b})')
    if (a==0) & (b==0):
        return (0,0,0)
    if a==0:
        if (b>0):
            return (0,1,b)
        elif (b<0):
            return (0,-1,-b)
    if b==0:
        if a>0:
            return (1,0,a)
        elif a<0:
            return (-1,0,-a)


    s1, t1, r1 = do_ext_gcd(sgn(a)*a, sgn(b)*b)
    s1 = sgn(a)*s1; t1 = sgn(b)*t1

    """assert s1*a + t1*b == r1
    assert a%r1 == 0
    assert b%r1 == 0
    assert euclid_gcd(a,b) == r1"""

    return (s1, t1, r1)






def check_all_pos(moduli:list[int]) -> bool:
    if not moduli:
        ValueError("empty moduli list given to check_all_pos().")
    prod = 1
    for m in moduli:
        prod = prod*m 

    return prod > 0


def check_all_coprime(moduli:list[int]) -> bool:
    if not moduli:
        ValueError("empty moduli list in check_all_coprime().")
    if not check_all_pos(moduli):
        sys.exit("non-positive moduli in check_all_coprime().")
    if len(list(set(moduli))) != len(moduli):
        return False

    if len(moduli) == 1:
        return True
    for i in range(len(moduli)):
        for j in range(i):
            if euclid_gcd(moduli[i], moduli[j]) != 1:
                ValueError(f'non-coprime moduli encountered. gcd(moduli[{i}]:{moduli[i]}, moduli[{j}]:{moduli[j]}) != 1.')
    return True


def check_less_than(remainders:list[int], moduli:list[int]) -> bool:
    if len(remainders) != len(moduli):
        sys.exit("unequal input lengths in check_less_than().")
    for i in range(len(remainders)):
        if remainders[i] >= moduli[i]:
            return False

    return True


def modular_inverse(k:int, modulus:int) -> int:
    assert modulus > 1
    result = ext_gcd(k, modulus) 
    if result[2] != 1:
        sys.exit("k must be coprime to modulus in modular_inverse().")

    assert (ext_gcd(k, modulus)[0]*k)%modulus == 1

    return result[0]%modulus


""" 
behavior: given a list of remainders and a list of moduli
    such that the moduli are pairwise coprime,
    return x, N such that
        x ~ r_i (mod m_i)
"""
def crt(remainders:list[int], moduli:list[int]) -> tuple[int, int]:
    if not check_all_pos(moduli):
        sys.exit("crt() requires moduli to be positive.")
    if not check_all_coprime(moduli):
        sys.exit("crt() required moduli to be coprime.")
    if not check_less_than(remainders, moduli):
        sys.exit("crt() requires remainders < moduli.")

    k = len(moduli)
    N = 1
    for ni in moduli:
        N = N*ni 
    M = [N//moduli[i] for i in range(k)]
    y = [modular_inverse(M[i], moduli[i]) for i in range(k)]
    e = [(y[i]*M[i])%N for i in range(k)]

    x = 0
    for i in range(k):
        x = x + e[i]*remainders[i] 
    x = x%N

    for i in range(k):
        assert x%moduli[i] == remainders[i]%moduli[i]
    return (x, N)
    