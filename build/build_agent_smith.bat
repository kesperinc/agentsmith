@echo off
title Agent Smith IDE - Custom VS Code Fork and Gulp Build System

echo =================================================================
echo Agent Smith IDE - 1-Click VS Code Fork and Gulp Builder
echo =================================================================
echo.

set BASE_DIR=%~dp0..\..
set AGENT_SMITH_DIR=%BASE_DIR%\agentsmith
set VSCODE_DIR=%AGENT_SMITH_DIR%\vscode
set PATCHES_DIR=%AGENT_SMITH_DIR%\patches
set BUILD_DIR=%AGENT_SMITH_DIR%\build
set EXTENSION_DIR=%AGENT_SMITH_DIR%\extension
set PATH=%BUILD_DIR%\node;%PATH%
set NODE_TLS_REJECT_UNAUTHORIZED=0
set SpectreMitigation=false
call yarn config set strict-ssl false > NUL 2>&1
call npm config set strict-ssl false > NUL 2>&1

:: 1. Create directories if not exist
if not exist "%VSCODE_DIR%" mkdir "%VSCODE_DIR%"
if not exist "%PATCHES_DIR%" mkdir "%PATCHES_DIR%"
if not exist "%EXTENSION_DIR%" mkdir "%EXTENSION_DIR%"

:: 2. Check compile dependencies
echo [1/4] Checking compile dependencies...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [FAIL] Node.js not found. Please install Node.js LTS first.
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('node -v') do set NODE_VER=%%i
    echo      [OK] Node.js Version: %NODE_VER%
)

where yarn >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Yarn not found. Installing yarn globally...
    call npm install -g yarn
) else (
    for /f "tokens=*" %%i in ('yarn -v') do set YARN_VER=%%i
    echo      [OK] Yarn Version: %YARN_VER%
)
echo      [Action] Pre-installing node-gyp globally to prevent Yarn auto-install errors...
call npm install -g node-gyp > NUL 2>&1


where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [FAIL] Git not found. Please install Git first.
    exit /b 1
)

echo.

:: 3. Clone and checkout Microsoft Code-OSS
echo [2/4] Cloning/Syncing Microsoft Code-OSS Upstream...
if not exist "%VSCODE_DIR%\.git" (
    echo      [Action] Cloning microsoft/vscode [Tag: 1.86.0] into %VSCODE_DIR%...
    git clone --depth 1 --branch 1.86.0 https://github.com/microsoft/vscode.git "%VSCODE_DIR%"
) else (
    echo      [OK] VS Code upstream already exists. Skipping clone.
)
echo.

:: 4. Apply custom patches
echo [3/4] Checking and applying Agent Smith custom branding patches...
set PATCH_APPLIED=0
if exist "%PATCHES_DIR%\*.patch" (
    echo      [Action] Applying custom patches inside %PATCHES_DIR%...
    cd /d "%VSCODE_DIR%"
    for %%f in ("%PATCHES_DIR%\*.patch") do (
        echo        Applying %%~nxf...
        git apply "%%f"
        set PATCH_APPLIED=1
    )
    if %PATCH_APPLIED% equ 1 (
        echo      [OK] Patches applied successfully.
    ) else (
        echo      [WARNING] Error applying patches or no changes.
    )
) else (
    echo      [NOTICE] No patch files found. Using clean Code-OSS.
)
echo.

:: 5. Create Directory.Build.props to bypass SpectreMitigation error
echo [4/5] Creating Directory.Build.props to bypass SpectreMitigation...
echo ^<Project^> > "%VSCODE_DIR%\Directory.Build.props"
echo   ^<PropertyGroup^> >> "%VSCODE_DIR%\Directory.Build.props"
echo     ^<SpectreMitigation^>false^</SpectreMitigation^> >> "%VSCODE_DIR%\Directory.Build.props"
echo   ^</PropertyGroup^> >> "%VSCODE_DIR%\Directory.Build.props"
echo ^</Project^> >> "%VSCODE_DIR%\Directory.Build.props"
echo.

:: 6. Install dependencies
echo [5/5] Installing Code-OSS compile dependencies...
cd /d "%VSCODE_DIR%"
call yarn install --frozen-lockfile

echo.
echo =================================================================
echo Agent Smith IDE compile environment setup complete!
echo   * Source Path: %VSCODE_DIR%
echo   * Run watch or compile in VS Code dir.
echo =================================================================
echo.
exit /b 0
