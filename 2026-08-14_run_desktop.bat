@echo off
chcp 65001 > nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo ===================================================
echo [Agent Smith] Starting Desktop Version...
echo ===================================================

:: 1. Check Python Backend Server (Port 5000)
echo [*] Checking Backend Server Status...
C:\Windows\System32\netstat.exe -ano | findstr LISTENING | findstr :5000 > nul
if %errorlevel% equ 0 (
    echo [ok] Backend Server is already running on port 5000.
) else (
    echo [!] Backend Server is offline. Starting in background...
    start /b "" .venv\Scripts\python coding-agent/src/main.py
    timeout /t 3 /nobreak > nul
)

:: 2. Override PATH with built-in Node v18, inject proxy mirrors, and launch Desktop Client
echo [*] Launching Desktop Client...
set PATH=%~dp0build\node;%PATH%
set ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
set NODEJS_ORG_MIRROR=http://localhost:8999/
set NODE_TLS_REJECT_UNAUTHORIZED=0

cd vscode
start /b "" .\scripts\code.bat


echo [ok] Desktop Client Launch Process Completed.
exit /b 0
