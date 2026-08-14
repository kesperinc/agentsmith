@echo off
chcp 65001 > nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo ===================================================
echo [Agent Smith] Starting Web Browser Version...
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

:: 2. Terminate existing 9095 port web server processes via PowerShell
echo [*] Releasing port 9095...
powershell -Command "Get-NetTCPConnection -LocalPort 9095 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"

:: 3. Override PATH with built-in Node v18 and launch Web Editor in a new window (Bypass input redirection error)
echo [*] Launching Web Editor Server (Port 9095)...
set PATH=C:\dev\antigravity-workspace\aifullstack\agentsmith\build\node;%PATH%
cd vscode
start "" cmd.exe /c "node scripts\code-web.js --port 9095"

:: Wait for server binding and open browser
timeout /t 3 /nobreak > nul
echo [*] Opening Web Browser...
start http://localhost:9095/

echo [ok] Web Editor Launch Process Completed.
exit /b 0
