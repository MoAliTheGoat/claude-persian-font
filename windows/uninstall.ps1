# Removes the Persian font installed by install.ps1.
$file = Join-Path $env:LOCALAPPDATA 'Microsoft\Windows\Fonts\Vazirmatn-Persian.ttf'
Remove-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts' -Name 'Noto Sans Hebrew (Persian, TrueType)' -ErrorAction SilentlyContinue
Remove-Item $file -Force -ErrorAction SilentlyContinue
Write-Host 'Removed. Restart Claude.'
