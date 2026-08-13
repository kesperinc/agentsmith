@echo off
chcp 65001 > nul
title Agent Smith IDE Desktop Launcher
echo =================================================================
echo Launching Agent Smith Desktop IDE Client...
echo =================================================================
echo.

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

:: Change working directory to vscode root and launch Electron GUI Runner
cd /d "%~dp0vscode"

:: Run Node Official Electron Runner in dedicated standalone window
start "Agent Smith IDE" node build/lib/electron.js

echo [OK] Agent Smith Desktop IDE GUI Client launched!
