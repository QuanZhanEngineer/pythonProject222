import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_circular_prime(n):
    if not is_prime(n):
        return False
    s = str(n)
    for i in range(len(s)):
        if not is_prime(int(s[i:] + s[:i])):
            return False
    return True

def circular_primes(n):
    count = 0
    for i in range(2, n + 1):
        if is_circular_prime(i):
            count += 1
    return count    

