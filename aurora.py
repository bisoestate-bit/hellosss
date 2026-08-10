import socket
import threading
Class Listener:
Def __init__(self, ip, port):
Self.ip = ip
Self.port = port
Self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Self.server.bind((self.ip, self.port))
Self.server.listen()
Def handle_client(self, conn, addr):
Print(f"New Connection: {addr} connected.")
While True:
Try:
Request = conn.recv(1024).decode()
If not request:
Break
Elif request.lower() == 'exit':
Break
Print(f"Received: {request}")
Response = input("Shell> ")
Conn.send(response.encode())
Except Exception as e:
Print(f"Error occurred: {e}")
Break
Print(f"Lost Connection: {addr}")
Conn.close()
Def start(self):
Print(f"Server is listening on {self.ip}:{self.port}")
While True:
Conn, addr = self.server.accept()
Thread = threading.Thread(target=self.handle_client, args=(conn, addr))
Thread.start()
If __name__ == "__main__":
Listener = Listener('0.0.0.0', 4444) # Change IP and port as needed
Listener.start()
