import os

with open("test_plain.bin", "wb") as f:
    f.write(os.urandom(512))
