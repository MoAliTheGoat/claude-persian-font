# Persian font (Vazirmatn) for Claude's replies in the Claude desktop app on Windows.
# Installs for the current user only; no admin rights needed. Undo: windows/uninstall.ps1
# Run:  irm https://raw.githubusercontent.com/MoAliTheGoat/claude-persian-font/main/windows/install.ps1 | iex

$ErrorActionPreference = 'Stop'
$url  = 'https://raw.githubusercontent.com/MoAliTheGoat/claude-persian-font/main/windows/Vazirmatn-Persian.ttf'
$dir  = Join-Path $env:LOCALAPPDATA 'Microsoft\Windows\Fonts'
$file = Join-Path $dir 'Vazirmatn-Persian.ttf'
$key  = 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts'

New-Item -ItemType Directory -Force -Path $dir | Out-Null
Invoke-WebRequest -Uri $url -OutFile $file -UseBasicParsing
# Claude lists "Noto Sans Hebrew" ahead of Times New Roman for its replies;
# this file carries only Persian letters under that name, so Latin text is untouched.
New-ItemProperty -Path $key -Name 'Noto Sans Hebrew (Persian, TrueType)' -Value $file -PropertyType String -Force | Out-Null

Write-Host 'Done. Quit Claude completely (also from the tray icon) and open it again.'
Write-Host 'انجام شد. Claude را کامل ببند (از آیکون کنار ساعت هم) و دوباره باز کن.'
