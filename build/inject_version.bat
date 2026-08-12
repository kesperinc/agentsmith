@echo off
title Agent Smith IDE - Version Injection
echo =================================================================
echo Agent Smith IDE - Auto Version Injection
echo =================================================================
echo.

set BUILD_DIR=%~dp0
set VENV_PYTHON=%BUILD_DIR%..\.venv\Scripts\python.exe

if exist "%VENV_PYTHON%" (
    echo [Action] Running version injector with virtualenv python...
    "%VENV_PYTHON%" "%BUILD_DIR%update_version.py"
) else (
    echo [Action] Running version injector with system python...
    python "%BUILD_DIR%update_version.py"
)

echo.
exit /b 0
