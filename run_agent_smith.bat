@echo off
chcp 65001 > nul
title Agent Smith IDE Launcher (UTF-8 Enforced)
echo =================================================================
echo Launching Agent Smith IDE GUI Client...
echo =================================================================
echo.

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set VSCODE_DEV=1
set VSCODE_SKIP_PRELAUNCH=1
set ELECTRON_ENABLE_LOGGING=1

cd /d "%~dp0vscode"

:: Launch Agent Smith IDE via built binary Code - OSS.exe
start "" "%~dp0vscode\.build\electron\Code - OSS.exe" "%~dp0vscode\out\main.js" "%~dp0vscode"

echo [OK] Agent Smith IDE GUI Client launched successfully on your screen!
