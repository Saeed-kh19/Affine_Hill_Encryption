import os
import sys
from typing import List, Tuple
from affine_hill import MOD, chunk_bytes, unchunk_bytes, mat_inverse, mat_mul, mat_vec_mul

def cols_from_blocks(blocks: List[List[int]], idxs: List[int]) -> List[List[int]]:
    n = len(blocks[0])
    k = len(idxs)
    M = [[0]*k for _ in range(n)]
    for col, idx in enumerate(idxs):
        v = blocks[idx]
        assert len(v) == n
        for row in range(n):
            M[row][col] = v[row]
    return M

def mat_sub(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    assert len(A) == len(B) and len(A[0]) == len(B[0])
    return [[(A[i][j] - B[i][j]) % MOD for j in range(len(A[0]))] for i in range(len(A))]

def mat_add_vec_repeat(b: List[int], k: int) -> List[List[int]]:
    n = len(b)
    M = [[0]*k for _ in range(n)]
    for j in range(k):
        for i in range(n):
            M[i][j] = b[i]
    return M

def recover_A_b(plain_blocks, cipher_blocks, n, anchor_idx, candidate_idxs):
    x0 = plain_blocks[anchor_idx]
    y0 = cipher_blocks[anchor_idx]

    from itertools import combinations

    for combo in combinations(candidate_idxs, n):
        try:
            Xd = [[0]*n for _ in range(n)]
            Yd = [[0]*n for _ in range(n)]

            for col, idx in enumerate(combo):
                xi = plain_blocks[idx]
                yi = cipher_blocks[idx]
                for r in range(n):
                    Xd[r][col] = (xi[r] - x0[r]) % MOD
                    Yd[r][col] = (yi[r] - y0[r]) % MOD

            Xd_inv = mat_inverse(Xd)

            A = mat_mul(Yd, Xd_inv)

            Ax0 = mat_vec_mul(A, x0)
            b = [(y0[i] - Ax0[i]) % MOD for i in range(n)]

            print(f"\nKey recovered using indices {combo}\n")
            return A, b

        except ValueError:
            continue

    raise ValueError("\nFailed to recover key: no invertible Xd found\n")

def main():
    if len(sys.argv) < 6:
        print("Usage: python recover_key_and_decrypt.py <plaintext_path> <ciphertext_path> <block_size_n> <anchor_idx> <sample_idx1> [<sample_idx2> ...]")
        print("Provide at least n sample indices alongside anchor_idx, all indices referencing aligned blocks.")
        sys.exit(1)

    pt_path = sys.argv[1]
    ct_path = sys.argv[2]
    n = int(sys.argv[3])
    anchor_idx = int(sys.argv[4])
    sample_idxs = list(map(int, sys.argv[5:]))

    with open(pt_path, "rb") as f:
        pt = f.read()
    with open(ct_path, "rb") as f:
        ct = f.read()

    pt_blocks = chunk_bytes(pt, n)
    ct_blocks = chunk_bytes(ct, n)
    if len(pt_blocks) != len(ct_blocks):
        raise ValueError("Plaintext and ciphertext must have same number of blocks for aligned pairs")

    A, b = recover_A_b(pt_blocks, ct_blocks, n, anchor_idx, sample_idxs)
    print("\nRecovered A:")
    for row in A:
        print(row)
    print("\nRecovered b:", b)

    from affine_hill import decrypt_blocks
    from affine_hill import mat_inverse
    A_inv = mat_inverse(A)
    dec_blocks = decrypt_blocks(A_inv, b, ct_blocks)
    out = unchunk_bytes(dec_blocks, len(pt))
    out_path = os.path.splitext(ct_path)[0] + ".recovered.bin"
    with open(out_path, "wb") as f:
        f.write(out)
    print(f"\nDecrypted with recovered key -> {out_path}\n")

if __name__ == "__main__":
    main()
