import time
from typing import Callable, Any, Iterable, Optional

def timed(fn: Callable) -> Callable:
    def inner(*args, **kwargs) -> Any:
        start = time.perf_counter()
        value = fn(*args, **kwargs)
        end = time.perf_counter()
        #print(f"Function {fn.__name__} ran in {(end-start):.10f}s")
        return value
    return inner

def gcd(a: int, b: int) -> int:
    """ Find the greatest common divisor of integers a and b """
    while a % b != 0:
        temp = a
        a = b
        b = temp % b
    return b

def is_coprime(a: int, b: int) -> bool:
    """ Whether or not integers a and b are relatively prime """
    return gcd(a, b) == 1

def is_prime(n: int) -> bool:
    """ Whether or not integer n is a prime """
    return len(factors(n)) == 2

def euclidean_algorithm(a: int, b: int) -> tuple[int, int]:
    """ Euclid's algorithm to find integers x and y such that ax + by = gcd(a, b) """
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    x, y = old_s, old_t
    return x, y

def multiplicative_inverse(a: int, m: int, check_coprime: Optional[bool] = True) -> int:
    """ Find integer n such that an ≡ 1 (mod m) """
    if check_coprime:
        assert is_coprime(a, m), f"no multiplicative inverse exists for {a} (mod {m})"
    return euclidean_algorithm(a, m)[0] % m

def solve_congruence(a: int, b: int, m: int) -> list[int]:
    """ Solve for integers x such that ax ≡ b (mod m)
        where x is in the set of least residues modulo m [0, m-1]"""
    d = gcd(a, m)
    if (b % d != 0):
        return []
    a, b, m = a // d, b // d, m // d
    n = multiplicative_inverse(a, m, check_coprime=False)
    x = (b * n) % m
    solutions = [x + i * m for i in range(d)]
    return solutions

def chinese_remainder(remainders: list[int], moduli: list[int]) -> int:
    """ Use the Chinese Remainder Theorem to solve for x (mod N)
        where x ≡ b1 (mod n1), x ≡ b2 (mod n2), ... """
    assert len(remainders) == len(moduli), "remainders and moduli arrays must be the same length"
    x = 0
    N = 1
    for m in moduli:
        N *= m
    for rem, mod in zip(remainders, moduli):
        N_i = N // mod
        n = multiplicative_inverse(N_i, mod)
        x += rem * N_i * n
    return x % N

def product(iterable: Iterable[int]) -> int:
    """ Find the product of all elements in a collection of integers """
    n = 1
    for item in iterable:
        n *= item
    return n

def factors(n: int) -> list[int]:
    """ List the factors of an integer """
    square = (n ** (1/2)) % 1 == 0.0
    f = [i for i in range(1, int(n ** (1/2)) + 1) if n % i == 0]
    for i in range(len(f) - (2 if square else 1), -1, -1):
        f.append(n // f[i])
    return f

def prime_factors(n: int) -> list[int]:
    """ Find the unique combination of prime factors that make up an integer n (F.T.O.A.) """
    f = factors(n)[1:-1]
    if not f:
        return [n]
    for k in f:
        if not is_prime(k):
            return prime_factors(k) + prime_factors(n//k)
    else:
        return f if len(f) != 1 else [f[0], f[0]]

def euler_totient(n: int, prime: Optional[bool] = True) -> int:
    """ Euler's totient function φ - counts the number of positive integers
        up to positive integer n that are relatively prime to n.
        φ(p) = p - 1, φ(pq) = φ(p)φ(q) if and only if p and q are distinct primes """
    distinct_prime_factors = set(prime_factors(n))
    return n // product(distinct_prime_factors) * product([(p - 1) for p in distinct_prime_factors])

n = 943272197412
pfs = prime_factors(n)
print(pfs)
assert product(pfs) == n
