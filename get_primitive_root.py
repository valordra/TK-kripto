# Utility function to store prime
# factors of a number
def prime_factorization(n):
    factors = set()
    d = 2
    while n > 1:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
        if d * d > n:
            if n > 1:
                factors.add((int(n)))
            break
    return factors


# Function to find smallest primitive
# root of n
def find_primitive(q):
    phi = q - 1

    # Find prime factors of phi
    prime_factors = prime_factorization(phi)
    print(prime_factors)

    # Check for every number from 2 to phi
    for x in range(2, phi + 1):

        for factors in prime_factors:
            a = phi // factors
            if pow(x, a, q) == 1:
                break

            return x


# Driver Code
# q = 119551754571012831577
# print("Smallest primitive root of",
#       q, "is", find_primitive(q))