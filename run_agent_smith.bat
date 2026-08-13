@echo off
chcp 65001 > nul
title Agent Smith IDE Desktop Launcher
echo =================================================================
echo Launching Agent Smith Desktop IDE Client...
echo =================================================================
echo.

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set VSCODE_DEV=1

:: Change working directory to vscode root and launch Code - OSS.exe in new foreground window
cd /d "%~dp0vscode"
start "" ".build\electron\Code - OSS.exe" "%~dp0vscode"

echo [OK] Agent Smith Desktop IDE launched successfully!
