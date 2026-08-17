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

# 2. Copy Electron Desktop App Binaries (vscode/.build/electron)
ELECTRON_SRC = ROOT_DIR / "vscode" / ".build" / "electron"
APP_DEST = DIST_DIR / "app"

if ELECTRON_SRC.exists():
    print(f"[*] Copying Electron binaries from {ELECTRON_SRC} to {APP_DEST}...")
    shutil.copytree(ELECTRON_SRC, APP_DEST, symlinks=True)
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

# 6. Copy Launchers if exist
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
    start /b "" .venv\\Scripts\\python coding-agent/src/main.py
    timeout /t 3 /nobreak > nul
)

:: 2. Launch Desktop Client Binary
echo [*] Launching Desktop IDE Client...
if exist "agentsmith.exe" (
    start "" "agentsmith.exe"
) else if exist "app\\agentsmith_app.exe" (
    start "" "app\\agentsmith_app.exe"
) else (
    start "" "app\\Code - OSS.exe"
)

echo [ok] Agent Smith Desktop Client Launch Process Completed.
exit /b 0
"""

with open(DIST_DIR / "run_agentsmith_desktop.bat", "w", encoding="utf-8") as f:
    f.write(RUNNER_BAT_CONTENT)
print(f"[ok] Created run_agentsmith_desktop.bat launcher.")

# 8. Create .env.example
ENV_EXAMPLE_CONTENT = """# Agent Smith API Key Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Backend Server Configuration
PORT=5000
HOST=127.0.0.1
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
"""

with open(DIST_DIR / ".env.example", "w", encoding="utf-8") as f:
    f.write(ENV_EXAMPLE_CONTENT)

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
