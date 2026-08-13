@echo off
chcp 65001 > nul
title Agent Smith IDE Desktop Launcher
echo =================================================================
echo Cleaning lingering background processes and Launching Desktop Client...
echo =================================================================
echo.

:: Terminate any lingering background zombie processes first
taskkill /f /im agentsmith.exe > nul 2>&1

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

:: Launch Agent Smith Desktop IDE GUI Window with --new-window flag
start "" "%~dp0vscode\.build\electron\agentsmith.exe" "%~dp0vscode" --new-window

echo [OK] Agent Smith Desktop IDE GUI Client launched successfully!
