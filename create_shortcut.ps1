$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "PDF Converter.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Projects\dev\pdf-to-text\run_app.bat"
$Shortcut.WorkingDirectory = "C:\Projects\dev\pdf-to-text"
$Shortcut.IconLocation = "C:\Projects\dev\pdf-to-text\run_app.bat,0"
$Shortcut.Save()
Write-Host "Shortcut created at $ShortcutPath"
