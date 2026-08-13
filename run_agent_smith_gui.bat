@echo off
chcp 65001 > nul
title Agent Smith IDE Desktop Client
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0vscode"
node build/lib/electron.js
