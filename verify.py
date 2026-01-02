import sys
import hashlib

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    if len(sys.argv) != 3:
        print("Usage: python verify.py <original_file> <decrypted_file>")
        sys.exit(1)

    orig_path, dec_path = sys.argv[1], sys.argv[2]

    with open(orig_path, "rb") as f1, open(dec_path, "rb") as f2:
        orig_data = f1.read()
        dec_data = f2.read()

    if orig_data == dec_data:
        print("\nVerification successful: decrypted file matches the original.\n")
    else:
        print("Verification failed: files differ.")
        print(f"- Original length: {len(orig_data)} bytes")
        print(f"- Decrypted length: {len(dec_data)} bytes")
        print(f"- Original SHA256: {file_hash(orig_path)}")
        print(f"- Decrypted SHA256: {file_hash(dec_path)}")
        min_len = min(len(orig_data), len(dec_data))
        for i in range(min_len):
            if orig_data[i] != dec_data[i]:
                print(f"- First mismatch at byte {i}: "
                      f"original={orig_data[i]}, decrypted={dec_data[i]}")
                break

if __name__ == "__main__":
    main()
    