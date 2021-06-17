import pyprimes
import sys

import random
import math


def extended_euclidean_algorithm(a, b):
    """
     Returns a three-tuple (gcd, x, y) such that
     a * x + b * y == gcd, where gcd is the greatest
     common divisor of a and b.
     """
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def inverse_of(n, p):
    """
    Returns the multiplicative inverse of
    n modulo p.

    This function returns an integer m such that
    (n * m) % p == 1.
    """
    gcd, x, y = extended_euclidean_algorithm(n, p)
    assert (n * x + p * y) % p == gcd

    if gcd != 1:
        # Either n is 0, or p is not a prime number.
        raise ValueError(
            '{} has no multiplicative inverse '
            'modulo {}'.format(n, p))
    else:
        return x % p


def rabinMiller(n):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    t, s = 0, n - 1

    while s % 2 == 0:
        t += 1
        s //= 2
    k = 0
    while k < 128:
        a = random.randrange(2, n - 1)
        v = pow(a, s, n)  # where values are (num,exp,mod)
        if v != 1:
            i = 0
            while v != (n - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % n
        k += 2
    return True


def isPrime(n):
    # lowPrimes is all primes (sans 2, which is covered by the bitwise and operator)
    # under 1000. taking n modulo each lowPrime allows us to remove a huge chunk
    # of composite numbers from our potential pool without resorting to Rabin-Miller
    lowPrimes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
        , 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179
        , 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269
        , 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367
        , 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461
        , 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571
        , 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661
        , 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773
        , 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883
        , 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    if n >= 3:
        if n & 1 != 0:
            for p in lowPrimes:
                if n == p:
                    return True
                if n % p == 0:
                    return False
            return rabinMiller(n)
    return False


def generateLargePrime(k):
    # k is the bit length
    r = 100 * (math.log(k, 2) + 1)  # number of attempts max
    r_ = r
    while r > 0:
        # randrange unusable for serious crypto purposes, deterministic
        n = random.randrange(2 ** (k - 1), 2 ** (k))
        r -= 1
        if isPrime(n):
            return n
    return "Failure after " + repr(r_) + " tries."


val = 0
nbits = 60

if len(sys.argv) > 1:
    val = int(sys.argv[1])

p = generateLargePrime(nbits)
q = generateLargePrime(nbits)

n = p * q

e = 65537

PHI = (p - 1) * (q - 1)

d = inverse_of(e, PHI)

a = 5
b = 30

print("RSA Encryption parameters. Public key: [e,N].")
cipher1 = pow(a, e, n)
cipher2 = pow(b, e, n)

cipher3 = (cipher1 * cipher2) % n

print("a:\t\t", a)
print("b:\t\t", b)

print("Cipher1:\t", cipher1)
print("Cipher2:\t", cipher2)
print("Cipher3:\t", cipher3)

print("e:\t\t", e)
print("N:\t\t", n)

val = pow(cipher3, d, n)

print("Result:\t\t", val)
