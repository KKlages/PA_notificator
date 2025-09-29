@echo off
REM Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM Change to the script directory
cd /d "%~dp0"

REM Start the hotkey toggle script (hidden, with admin rights)
start /B pythonw hotkey_toggle.py

REM Start the Discord watcher script (hidden)
start /B pythonw discord_watcher.py

REM Optional: Show a quick notification
echo PA Notifier started successfully with admin rights!
timeout /t 2 /nobreak >nul

exit