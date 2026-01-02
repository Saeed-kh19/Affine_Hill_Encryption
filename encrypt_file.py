import json
import sys
from affine_hill import chunk_bytes, encrypt_blocks, unchunk_bytes

def load_key(key_path):
    
    with open(key_path, "r") as f:
        key = json.load(f)
    A = key["A"]
    b = key["b"]
    n = key["n"]
    assert len(A) == n and all(len(row) == n for row in A), "A must be n x n"
    assert len(b) == n, "b must be length n"
    return n, A, b

def main():
    if len(sys.argv) != 4:
        print("Usage: python encrypt_file.py <plaintext_path> <ciphertext_path> <key_json>")
        sys.exit(1)
    pt_path, ct_path, key_path = sys.argv[1], sys.argv[2], sys.argv[3]
    n, A, b = load_key(key_path)

    with open(pt_path, "rb") as f:
        data = f.read()

    blocks = chunk_bytes(data, n)
    enc_blocks = encrypt_blocks(A, b, blocks)
    out = unchunk_bytes(enc_blocks, len(blocks) * n)
    with open(ct_path, "wb") as f:
        f.write(out)
    print(f"\nEncrypted {pt_path} -> {ct_path} with block size {n}\n")

if __name__ == "__main__":
    main()
