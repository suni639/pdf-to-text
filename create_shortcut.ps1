$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "PDF Converter.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "c:\Users\sunil\dev\pdf-to-text\run_app.bat"
$Shortcut.WorkingDirectory = "c:\Users\sunil\dev\pdf-to-text"
$Shortcut.IconLocation = "c:\Users\sunil\dev\pdf-to-text\run_app.bat,0"
$Shortcut.Save()
Write-Host "Shortcut created at $ShortcutPath"
