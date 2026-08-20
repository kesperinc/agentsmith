# -*- coding: utf-8 -*-
"""
Agent Smith Enterprise Desktop IDE Release Packaging Script
Creates a standalone distribution package in dist/agentsmith-desktop-v1.0.0/
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path

# Force UTF-8 Output
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT_DIR / "dist" / "agentsmith-desktop-v1.0.0"

print(f"==================================================")
print(f"[Agent Smith] Starting Desktop Distribution Build...")
print(f"Target Directory: {DIST_DIR}")
print(f"==================================================")

# 1. Clean / Prepare Target Directory
if DIST_DIR.exists():
    print(f"[*] Removing existing dist directory...")
    shutil.rmtree(DIST_DIR, ignore_errors=True)

DIST_DIR.mkdir(parents=True, exist_ok=True)

# # 2. Copy Electron Desktop App Binaries & Prepare Pure Unpacked App Structure
ELECTRON_SRC = ROOT_DIR / "VSCode-win32-x64"
if not ELECTRON_SRC.exists():
    ELECTRON_SRC = ROOT_DIR / "vscode" / ".build" / "electron"
APP_DEST = DIST_DIR / "app"

if ELECTRON_SRC.exists():
    print(f"[*] Copying Electron Runtime Binaries from {ELECTRON_SRC} to {APP_DEST}...")
    shutil.copytree(ELECTRON_SRC, APP_DEST, symlinks=True, dirs_exist_ok=True)

    # Prepare Pure Unpacked Resources/App Directory
    RESOURCES_APP_DEST = APP_DEST / "resources" / "app"
    VSCODE_DIR = ROOT_DIR / "vscode"

    print(f"[*] Constructing Pure Unpacked Editor App Structure at {RESOURCES_APP_DEST}...")

    # Copy Compiled out/ Directory
    if (VSCODE_DIR / "out").exists():
        print(f"[*] Copying compiled out/ directory...")
        shutil.copytree(VSCODE_DIR / "out", RESOURCES_APP_DEST / "out", dirs_exist_ok=True)

    # Copy package.json & product.json
    for json_file in ["package.json", "product.json"]:
        if (VSCODE_DIR / json_file).exists():
            shutil.copy2(VSCODE_DIR / json_file, RESOURCES_APP_DEST / json_file)

    # Copy extensions/ Directory
    if (VSCODE_DIR / "extensions").exists():
        print(f"[*] Copying extensions/ directory...")
        shutil.copytree(VSCODE_DIR / "extensions", RESOURCES_APP_DEST / "extensions", dirs_exist_ok=True)

    # Remove node_modules.asar if present to force direct unpacked node_modules loading
    ASAR_FILE = RESOURCES_APP_DEST / "node_modules.asar"
    if ASAR_FILE.exists():
        print(f"[*] Removing node_modules.asar to enforce direct unpacked node_modules loading...")
        try:
            ASAR_FILE.unlink()
        except Exception as e:
            print(f"[!] Note on removing asar: {e}")

    # Copy node_modules/ Directory for Direct Unpacked Native Loading
    if (VSCODE_DIR / "node_modules").exists():
        print(f"[*] Copying full node_modules/ directory for native module compatibility...")
        shutil.copytree(VSCODE_DIR / "node_modules", RESOURCES_APP_DEST / "node_modules", dirs_exist_ok=True)

    # Overlay Precompiled Electron 27 (NODE_MODULE_VERSION 118) Native Modules from Antigravity IDE
    AGY_MODULE_SRC = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Antigravity IDE" / "resources" / "app" / "node_modules"
    NATIVE_MODULE_NAMES = [
        "@vscode/policy-watcher",
        "@vscode/spdlog",
        "@vscode/sqlite3",
        "@vscode/windows-process-tree",
        "@vscode/windows-registry",
        "@vscode/windows-mutex",
        "@vscode/windows-ca-certs",
        "@vscode/deviceid",
        "native-keymap",
        "native-watchdog",
        "native-is-elevated",
        "kerberos",
        "node-pty",
        "windows-foreground-love"
    ]
    if AGY_MODULE_SRC.exists():
        print(f"[*] Overlaying Electron 27 (NODE_MODULE_VERSION 118) C++ native modules from {AGY_MODULE_SRC}...")
        for mod in NATIVE_MODULE_NAMES:
            src_mod = AGY_MODULE_SRC / Path(mod)
            dest_mod = RESOURCES_APP_DEST / "node_modules" / Path(mod)
            if src_mod.exists():
                print(f"    -> Overwriting {mod} with Electron 27 ABI version 118...")
                shutil.copytree(src_mod, dest_mod, dirs_exist_ok=True)

    # Ensure conpty.node in Release directory
    PTY_UNPACKED_DEST = RESOURCES_APP_DEST / "node_modules" / "node-pty" / "build" / "Release"
    PTY_UNPACKED_DEST.mkdir(parents=True, exist_ok=True)
    
    PTY_SOURCES = [
        ROOT_DIR / "vscode" / "node_modules" / "node-pty" / "build" / "Release",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Antigravity IDE" / "resources" / "app" / "node_modules" / "node-pty" / "build" / "Release"
    ]
    for pty_src in PTY_SOURCES:
        if pty_src.exists() and (pty_src / "conpty.node").exists():
            print(f"[*] Ensuring terminal conpty.node binaries from {pty_src}...")
            shutil.copytree(pty_src, PTY_UNPACKED_DEST, dirs_exist_ok=True)
            break
else:
    print(f"[!] Warning: {ELECTRON_SRC} not found. Please build electron first.")

# 3. Copy coding-agent Backend Engine
CODING_AGENT_SRC = ROOT_DIR / "coding-agent"
CODING_AGENT_DEST = DIST_DIR / "coding-agent"

print(f"[*] Copying coding-agent backend engine...")
shutil.copytree(
    CODING_AGENT_SRC, 
    CODING_AGENT_DEST, 
    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache", ".git")
)

# 4. Copy .venv Python Environment
VENV_SRC = ROOT_DIR / ".venv"
VENV_DEST = DIST_DIR / ".venv"

if VENV_SRC.exists():
    print(f"[*] Copying .venv Python virtual environment...")
    shutil.copytree(
        VENV_SRC,
        VENV_DEST,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
    )

# 5. Copy .agentsmith Mem0 Config
AGENTSMITH_SRC = ROOT_DIR / ".agentsmith"
AGENTSMITH_DEST = DIST_DIR / ".agentsmith"

if AGENTSMITH_SRC.exists():
    print(f"[*] Copying .agentsmith configuration...")
    shutil.copytree(AGENTSMITH_SRC, AGENTSMITH_DEST)

# 6. Copy Brand Logo Resources (docs/images/)
IMAGES_SRC = ROOT_DIR / "docs" / "images"
RESOURCES_DEST = DIST_DIR / "resources"

if IMAGES_SRC.exists():
    print(f"[*] Copying brand logo resources from {IMAGES_SRC} to {RESOURCES_DEST}...")
    RESOURCES_DEST.mkdir(parents=True, exist_ok=True)
    for img_file in ["code.ico", "code.png", "logo.png", "code-icon.svg", "ico.png"]:
        src_img = IMAGES_SRC / img_file
        if src_img.exists():
            shutil.copy2(src_img, RESOURCES_DEST / img_file)

# 7. Copy Launchers if exist
for launcher in ["agentsmith.exe", "agentsmith.vbs"]:
    src_file = ROOT_DIR / launcher
    if src_file.exists():
        print(f"[*] Copying launcher {launcher}...")
        shutil.copy2(src_file, DIST_DIR / launcher)

# 7. Create Release Runner Batch File: run_agentsmith_desktop.bat
RUNNER_BAT_CONTENT = """@echo off
chcp 65001 > nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo ===================================================
echo [Agent Smith] Launching Standalone Desktop IDE...
echo ===================================================

:: 1. Check Python Backend Server (Port 5000)
echo [*] Checking Backend Server Status...
C:\\Windows\\System32\\netstat.exe -ano | findstr LISTENING | findstr :5000 > nul
if %errorlevel% equ 0 (
    echo [ok] Backend Server is already running on port 5000.
) else (
    echo [!] Backend Server is offline. Starting in background...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '.\\.venv\\Scripts\\python.exe' -ArgumentList 'coding-agent/src/main.py' -WindowStyle Hidden -WorkingDirectory '%~dp0'"
    timeout /t 2 /nobreak > nul
)

:: 2. Launch Desktop Client Binary
echo [*] Launching Desktop IDE Client...
if exist "agentsmith.exe" (
    start "" "agentsmith.exe" --new-window "%~dp0"
) else if exist "app\\agentsmith_app.exe" (
    start "" "app\\agentsmith_app.exe" --new-window "%~dp0"
) else if exist "app\\Code - OSS.exe" (
    start "" "app\\Code - OSS.exe" --new-window "%~dp0"
) else (
    echo [ERROR] Desktop IDE Client binary not found!
    pause
)

echo [ok] Agent Smith Desktop Client Launch Process Completed.
exit /b 0
"""

with open(DIST_DIR / "run_agentsmith_desktop.bat", "w", encoding="utf-8") as f:
    f.write(RUNNER_BAT_CONTENT)
print(f"[ok] Created run_agentsmith_desktop.bat launcher.")

# 8. Copy .env.example and .env if available
ROOT_ENV_EXAMPLE = ROOT_DIR / ".env.example"
if ROOT_ENV_EXAMPLE.exists():
    shutil.copy2(ROOT_ENV_EXAMPLE, DIST_DIR / ".env.example")
    print(f"[ok] Copied root .env.example to release package.")
else:
    ENV_EXAMPLE_CONTENT = """# Agent Smith API Key Configuration
GEMINI_API_KEY=
GOOGLE_API_KEY=
OPENROUTER_API_KEY=
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# Backend Server Configuration
PORT=5000
HOST=127.0.0.1
AGENTSMITH_BACKEND_PORT=5000
AGENTSMITH_BACKEND_HOST=127.0.0.1
AGENTSMITH_MCP_PORT=3000
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
"""
    with open(DIST_DIR / ".env.example", "w", encoding="utf-8") as f:
        f.write(ENV_EXAMPLE_CONTENT)
    print(f"[ok] Created .env.example.")

# 9. Create Release README_RELEASE.md
README_RELEASE_CONTENT = """# Agent Smith Enterprise Desktop IDE Release Package (v1.0.0)

## 🚀 빠른 실행 가이드 (Quick Start Guide)

1. `.env.example` 파일을 복사하여 `.env` 파일로 이름을 변경하고, `GEMINI_API_KEY` 또는 `GOOGLE_API_KEY`를 설정하세요.
2. `run_agentsmith_desktop.bat` 배치 파일 또는 `agentsmith.exe`를 실행하세요.
3. 자동으로 백엔드 서버(Port 5000) 및 Agent Smith Desktop IDE 클라이언트가 실행됩니다.

## 📁 디렉터리 구성
- `app/`: Electron IDE 실행 바이너리 및 리소스
- `coding-agent/`: 백엔드 Vibe 코딩 파이썬 엔진
- `.venv/`: 실행 전용 경량 파이썬 가상환경
- `.agentsmith/`: Mem0 및 Qdrant 영속 기억 구성 디렉터리
- `run_agentsmith_desktop.bat`: 원터치 런처 배치 파일
"""

with open(DIST_DIR / "README_RELEASE.md", "w", encoding="utf-8") as f:
    f.write(README_RELEASE_CONTENT)
print(f"[ok] Created README_RELEASE.md.")

# 10. Zip Archiving
ZIP_DEST = ROOT_DIR / "dist" / "agentsmith-desktop-v1.0.0.zip"
print(f"[*] Creating ZIP archive: {ZIP_DEST}...")

with zipfile.ZipFile(ZIP_DEST, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(DIST_DIR):
        for file in files:
            file_path = Path(root) / file
            arcname = file_path.relative_to(DIST_DIR.parent)
            zipf.write(file_path, arcname)

print(f"==================================================")
print(f"[SUCCESS] Desktop Distribution Build Completed!")
print(f"Package Path: {DIST_DIR}")
print(f"Archive Path: {ZIP_DEST}")
print(f"==================================================")
