import math
import random

# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]


def random_odd_number(min_digit: int, max_digit: int):
    minimum = 10 ** (min_digit - 1) + 1
    maximum = 10 ** max_digit
    assert (minimum < maximum)
    return random.randrange(minimum, maximum, 2)


def get_low_level_prime(min_digit: int = 20, max_digit: int = 21):
    while True:
        # Obtain a random odd number
        prime_candidate = random_odd_number(min_digit, max_digit)
        print(f"Checking low-level candidate: {prime_candidate}")

        # Test divisibility by pre-generated primes
        for divisor in first_primes_list:
            if prime_candidate % divisor == 0 and divisor ** 2 <= prime_candidate:
                break
        # If no divisor found, return value
        else:
            print(f"Chose low-level candidate: {prime_candidate}")
            return prime_candidate


def pass_miller_rabin_test(miller_rabin_candidate, prime_error_probability=pow(1 / 2, 128)):
    max_divisions_by_two = 0  # k
    even_component = miller_rabin_candidate - 1  # n - 1
    while even_component % 2 == 0:
        print(f"Dividing {even_component} by 2")
        even_component //= 2  # q
        max_divisions_by_two += 1
    assert (2 ** max_divisions_by_two * even_component == miller_rabin_candidate - 1)

    def trial_composite(round_tester):
        print(f"Testing prime candidate: {miller_rabin_candidate} with round tester: {round_tester}")
        if pow(round_tester, even_component, miller_rabin_candidate) == 1:  # if a^q mod n == 1
            return False  # False means candidate might be prime
        for i in range(max_divisions_by_two):
            if pow(round_tester, 2 ** i * even_component, miller_rabin_candidate) == miller_rabin_candidate - 1:
                return False  # False means candidate might be prime
        return True

    # Set number of trials here
    # each trial has 75% of determining candidate is prime
    # in commercial applications, we require error probabilities to be less than {1/2}^{128}
    # Probability(n prime after t tests) = 1-4^(-t)
    # error probability = 4^(-t)
    # trials = -log4(error_probability)
    number_of_trials = int(-1 * math.log(prime_error_probability, 4))
    for i in range(number_of_trials):
        round_tester = random.randrange(2, miller_rabin_candidate)
        if trial_composite(round_tester):
            return False
    return True


def generate_prime_number(min_digit: int = 20, max_digit: int = 21, prime_error_probability: float = pow(1 / 2, 128)):
    while True:
        prime_candidate = get_low_level_prime(min_digit, max_digit)
        if not pass_miller_rabin_test(prime_candidate, prime_error_probability):
            continue
        else:
            print("Maybe prime is: \n", prime_candidate)
            return prime_candidate


if __name__ == '__main__':
    print(generate_prime_number())
