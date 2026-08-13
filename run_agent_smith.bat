@echo off
chcp 65001 > nul
title Agent Smith IDE Desktop Launcher
echo =================================================================
echo Launching Agent Smith Desktop IDE Client...
echo =================================================================
echo.

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set VSCODE_SKIP_PRELAUNCH=1

:: Change working directory to vscode root and launch Official Code Launcher
cd /d "%~dp0vscode"
call scripts\code.bat

echo [OK] Agent Smith Desktop IDE launched successfully!
