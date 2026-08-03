# encrypt.py
from Crypto.Cipher import AES
import os

key = b'12345678901234567890123456789012'
nonce = os.urandom(12)
with open("/tmp/implant.bin", "rb") as f:
    data = f.read()

cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
ciphertext, tag = cipher.encrypt_and_digest(data)

with open("payload.enc", "wb") as f:
    f.write(nonce + tag + ciphertext)
