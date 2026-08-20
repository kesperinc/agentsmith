@echo off
chcp 65001 > nul
title Agent Smith IDE Web UI Launcher (UTF-8 Enforced)
echo =================================================================
echo Launching Agent Smith IDE (Web UI Engine on Port 9090 - UTF-8)...
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

powershell -Command "Get-Process -Id (Get-NetTCPConnection -LocalPort 9090 -ErrorAction SilentlyContinue).OwningProcess -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue"
cd /d "%~dp0vscode"
timeout /t 1 /nobreak > NUL
start http://localhost:9090
node scripts\code-web.js --port 9090
pause
