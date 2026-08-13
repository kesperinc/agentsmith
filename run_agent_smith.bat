@echo off
chcp 65001 > nul
title Agent Smith IDE Desktop Launcher
echo =================================================================
echo Launching Agent Smith Desktop IDE Client...
echo =================================================================
echo.

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

:: Change working directory to vscode root and run official electron launcher
cd /d "%~dp0vscode"
start "" node build/lib/electron.js

echo [OK] Agent Smith Desktop IDE launched successfully!
