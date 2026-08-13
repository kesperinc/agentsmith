@echo off
chcp 65001 > nul
title Agent Smith IDE Desktop Launcher
echo =================================================================
echo Launching Agent Smith IDE Desktop Client...
echo =================================================================
echo.

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set VSCODE_DEV=1
set VSCODE_SKIP_PRELAUNCH=1

:: Change working directory explicitly to vscode root
cd /d "%~dp0vscode"

:: Launch Desktop Client with explicit Working Directory (/D)
start "" /D "%~dp0vscode" "%~dp0vscode\.build\electron\agentsmith.exe" .

echo [OK] Agent Smith Desktop IDE launched successfully!
