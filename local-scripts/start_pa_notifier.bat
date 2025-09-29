@echo off
REM PA Notifier - Auto-start both scripts in background

REM Change to the script directory
cd /d "%~dp0"

REM Start the hotkey toggle script (hidden)
start /B pythonw hotkey_toggle.py

REM Start the Discord watcher script (hidden)
start /B pythonw discord_watcher.py

REM Optional: Show a quick notification that scripts started
echo PA Notifier started successfully!
timeout /t 2 /nobreak >nul

exit