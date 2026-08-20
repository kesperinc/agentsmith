@echo off
chcp 65001 > nul
title Agent Smith IDE Desktop Launcher
echo =================================================================
echo Launching Agent Smith Desktop IDE Client...
echo =================================================================
echo.

if not defined USERPROFILE (
    if defined HOMEDRIVE if defined HOMEPATH (
        set "USERPROFILE=%HOMEDRIVE%%HOMEPATH%"
    ) else (
        set "USERPROFILE=%SystemDrive%\Users\%USERNAME%"
    )
)
if not defined APPDATA set "APPDATA=%USERPROFILE%\AppData\Roaming"
if not defined LOCALAPPDATA set "LOCALAPPDATA=%USERPROFILE%\AppData\Local"

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set AGENTSMITH_BACKEND_PORT=5000
set VSCODE_DEV=1

:: Change working directory to vscode root and launch Code - OSS.exe in new foreground window
cd /d "%~dp0vscode"
start "" ".build\electron\Code - OSS.exe" "%~dp0vscode"

echo [OK] Agent Smith Desktop IDE launched successfully!
