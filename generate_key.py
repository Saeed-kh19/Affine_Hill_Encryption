import random
import json
from affine_hill import mat_inverse

MOD = 256

def random_invertible_matrix(n):
    while True:
        A = [[random.randint(0, MOD-1) for _ in range(n)] for _ in range(n)]
        try:
            _ = mat_inverse(A)
            return A
        except ValueError:
            continue

def random_vector(n):
    return [random.randint(0, MOD-1) for _ in range(n)]

if __name__ == "__main__":
    n = 4
    A = random_invertible_matrix(n)
    b = random_vector(n)

    key = {
        "n": n,
        "A": A,
        "b": b
    }

    with open("key.json", "w") as f:
        json.dump(key, f, indent=2)

    print("\nKey generated and saved to key.json\n")
    print("Matrix A:")
    for row in A:
        print(row)
    print("Vector b:", b,"\n")
