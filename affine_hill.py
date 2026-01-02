import os
from typing import Tuple, List

MOD = 256

def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)

def inv_mod(a: int, m: int = MOD) -> int:
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError(f"No modular inverse for {a} modulo {m}")
    return x % m

def mat_mul(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    r, k = len(A), len(A[0])
    k2, c = len(B), len(B[0])
    assert k == k2, "Dimension mismatch for mat_mul"
    out = [[0] * c for _ in range(r)]
    for i in range(r):
        for j in range(c):
            s = 0
            for t in range(k):
                s += A[i][t] * B[t][j]
            out[i][j] = s % MOD
    return out

def mat_vec_mul(A: List[List[int]], x: List[int]) -> List[int]:
    assert len(A[0]) == len(x), "Dimension mismatch for mat_vec_mul"
    y = []
    for i in range(len(A)):
        s = 0
        for j in range(len(x)):
            s += A[i][j] * x[j]
        y.append(s % MOD)
    return y

def mat_identity(n: int) -> List[List[int]]:
    I = [[0]*n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    return I

def mat_copy(A: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in A]

def mat_inverse(A: List[List[int]]) -> List[List[int]]:

    n = len(A)
    assert all(len(row) == n for row in A), "A must be square"
    aug = [A[i][:] + mat_identity(n)[i] for i in range(n)]

    row = 0
    for col in range(n):
        pivot = None
        for r in range(row, n):
            if egcd(aug[r][col] % MOD, MOD)[0] == 1:
                pivot = r
                break
        if pivot is None:
            raise ValueError("Matrix not invertible modulo 256 (no invertible pivot)")
        aug[row], aug[pivot] = aug[pivot], aug[row]
        inv_pivot = inv_mod(aug[row][col] % MOD, MOD)
        for c in range(2*n):
            aug[row][c] = (aug[row][c] * inv_pivot) % MOD
        for r in range(n):
            if r == row:
                continue
            factor = aug[r][col] % MOD
            for c in range(2*n):
                aug[r][c] = (aug[r][c] - factor * aug[row][c]) % MOD
        row += 1

    inv = [aug[i][n:] for i in range(n)]
    return inv

def chunk_bytes(data: bytes, n: int) -> List[List[int]]:
    blocks = []
    for i in range(0, len(data), n):
        block = list(data[i:i+n])
        if len(block) < n:
            block += [0] * (n - len(block))
        blocks.append(block)
    return blocks

def unchunk_bytes(blocks: List[List[int]], original_len: int) -> bytes:
    flat = []
    for b in blocks:
        flat.extend(b)
    return bytes(flat[:original_len])

def encrypt_blocks(A: List[List[int]], b: List[int], blocks: List[List[int]]) -> List[List[int]]:
    n = len(A)
    assert len(b) == n, "b dimension mismatch"
    out = []
    for x in blocks:
        y = mat_vec_mul(A, x)
        y = [(y[i] + b[i]) % MOD for i in range(n)]
        out.append(y)
    return out

def decrypt_blocks(A_inv: List[List[int]], b: List[int], blocks: List[List[int]]) -> List[List[int]]:
    n = len(A_inv)
    assert len(b) == n, "b dimension mismatch"
    out = []
    for y in blocks:
        z = [(y[i] - b[i]) % MOD for i in range(n)]
        x = mat_vec_mul(A_inv, z)
        out.append(x)
    return out
