from math import floor, sqrt
from os.path import isfile

import matplotlib.pyplot as plt
import pickle

def is_prime(n):
    for i in range(2, floor(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def primes_smaller_n_gen(n):
    for i in range(2, n+1):
        if is_prime(i):
            yield i

def find_perfect_squares_mod_n(n):
    perfect_squares = set()
    for i in range(1, n):
        square = (i * i) % n
        if square != 0:
            perfect_squares.add(square)
    return perfect_squares

def get_perfect_square_info(n):
    perfect_squares = {}
    perfect_square_counts = {}
    perfect_square_counts_diffs = {}
    perfect_square_counts_diffs_normalized = {}

    last_prime = 0
    for p in primes_smaller_n_gen(n):
        perfect_squares[p] = find_perfect_squares_mod_n(p)
        perfect_square_counts[p] = len(perfect_squares[p])
        if p > 2:
            perfect_square_counts_diffs[p] = perfect_square_counts[p] - perfect_square_counts[last_prime]
            perfect_square_counts_diffs_normalized[p] = perfect_square_counts_diffs[p] / (p - last_prime)
        last_prime = p
    return (
        perfect_squares, 
        perfect_square_counts, 
        perfect_square_counts_diffs, 
        perfect_square_counts_diffs_normalized
    )

def plot_perfect_square_counts(perfect_square_counts):
    _fig, ax = plt.subplots()
    x, y = zip(*perfect_square_counts.items())
    ax.scatter(x, y, s=2.0)
    plt.title("Number of perfect squares in Z(mod p_n).")
    plt.show()
    
def plot_perfect_square_count_difference(perfect_square_counts_diff):
    _fig, ax = plt.subplots()
    x, y = zip(*perfect_square_counts_diff.items())
    ax.scatter(x, y, s=2.0)
    plt.title("Increase in number of perfect squares from Z(mod p_{n-1}) to Z(mod p_n).")
    plt.show()

def plot_perfect_square_count_difference_normalized(perfect_square_counts_diffs_normalized):
    _fig, ax = plt.subplots()
    x, y = zip(*perfect_square_counts_diffs_normalized.items())
    ax.scatter(x, y, s=2.0)
    plt.title("Normalized increase in number of perfect squares from Z(mod p_{n-1}) to Z(mod p_n).")
    plt.show()

def pickle_save_perfect_square_info(n):
    perfect_squares, counts, diffs, diffs_normalized = get_perfect_square_info(n)
    with open(f"data/perfect_squares_{n}.pydict", "wb") as f:
        pickle.dump(perfect_squares, f)
    with open(f"data/perfect_square_counts_{n}.pydict", "wb") as f:
        pickle.dump(counts, f)
    with open(f"data/perfect_square_counts_diffs_{n}.pydict", "wb") as f:
        pickle.dump(diffs, f)
    with open(f"data/perfect_square_counts_diffs_normalized_{n}.pydict", "wb") as f:
        pickle.dump(diffs_normalized, f)

def get_dict_from_file(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

def pickle_load_perfect_square_info(n):
    perfect_squares = get_dict_from_file(f"data/perfect_squares_{n}.pydict")
    perfect_square_counts = get_dict_from_file(f"data/perfect_square_counts_{n}.pydict")
    perfect_square_counts_diffs = get_dict_from_file(f"data/perfect_square_counts_diffs_{n}.pydict")
    perfect_square_counts_diffs_normalized = get_dict_from_file(f"data/perfect_square_counts_diffs_normalized_{n}.pydict")
    return (
        perfect_squares, 
        perfect_square_counts, 
        perfect_square_counts_diffs, 
        perfect_square_counts_diffs_normalized
    )

def show_presentation(n):
    if not isfile(f"data/perfect_squares_{n}.pydict"):
        pickle_save_perfect_square_info(n)
    _perfect_squares, counts, diffs, diffs_norm = pickle_load_perfect_square_info(n)
    plot_perfect_square_counts(counts)
    plot_perfect_square_count_difference(diffs)
    plot_perfect_square_count_difference_normalized(diffs_norm)

def main():
    show_presentation(100)

if __name__ == "__main__":
    main()