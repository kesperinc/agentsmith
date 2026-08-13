@echo off
chcp 65001 > nul
title Agent Smith IDE Web UI Launcher (UTF-8 Enforced)
echo =================================================================
echo Launching Agent Smith IDE (Web UI Engine on Port 9090 - UTF-8)...
echo =================================================================
echo.

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

powershell -Command "Get-Process -Id (Get-NetTCPConnection -LocalPort 9090 -ErrorAction SilentlyContinue).OwningProcess -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue"
cd /d "%~dp0vscode"
timeout /t 1 /nobreak > NUL
start http://localhost:9090
node scripts\code-web.js --port 9090
pause
