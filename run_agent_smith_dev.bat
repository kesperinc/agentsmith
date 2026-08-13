@echo off
title Agent Smith IDE Dev Launcher
echo =================================================================
echo Launching Agent Smith IDE (Development Mode)...
echo =================================================================
echo.
cd /d "%~dp0vscode"
call scripts\code.bat
