import json
import sys
from affine_hill import chunk_bytes, decrypt_blocks, unchunk_bytes, mat_inverse

def load_key(key_path):
    with open(key_path, "r") as f:
        key = json.load(f)
    n, A, b = key["n"], key["A"], key["b"]
    assert len(A) == n and all(len(row) == n for row in A), "A must be n x n"
    assert len(b) == n, "b must be length n"
    return n, A, b

def main():
    if len(sys.argv) != 5:
        print("Usage: python decrypt_file.py <ciphertext_path> <plaintext_out_path> <key_json> <original_length>")
        print("Note: original_length is the byte length of the original plaintext (to trim padding).")
        sys.exit(1)
    ct_path, pt_out_path, key_path, orig_len_str = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    original_len = int(orig_len_str)

    n, A, b = load_key(key_path)
    A_inv = mat_inverse(A)

    with open(ct_path, "rb") as f:
        data = f.read()

    blocks = chunk_bytes(data, n)
    dec_blocks = decrypt_blocks(A_inv, b, blocks)
    out = unchunk_bytes(dec_blocks, original_len)
    with open(pt_out_path, "wb") as f:
        f.write(out)
    print(f"\nDecrypted {ct_path} -> {pt_out_path} (trimmed to {original_len} bytes)\n")

if __name__ == "__main__":
    main()
