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

    # Copy Pure CommonJS Compiled Production out/ Directory from vscode/out-vscode
    OUT_VSC_SRC = VSCODE_DIR / "out-vscode"
    bundled_workbench = RESOURCES_APP_DEST / "out" / "vs" / "workbench" / "workbench.desktop.main.js"
    AGY_OUT_SRC = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Antigravity IDE" / "resources" / "app" / "out"

    if OUT_VSC_SRC.exists() and (OUT_VSC_SRC / "vs" / "workbench" / "workbench.desktop.main.js").exists():
        print(f"[*] Copying pure CommonJS compiled out/ directory from {OUT_VSC_SRC}...")
        shutil.rmtree(RESOURCES_APP_DEST / "out", ignore_errors=True)
        shutil.copytree(OUT_VSC_SRC, RESOURCES_APP_DEST / "out")
    elif (VSCODE_DIR / "out").exists():
        print(f"[*] Copying compiled out/ directory from vscode/out...")
        shutil.copytree(VSCODE_DIR / "out", RESOURCES_APP_DEST / "out", dirs_exist_ok=True)
    elif bundled_workbench.exists() and bundled_workbench.stat().st_size > 1024 * 1024:
        print(f"[*] Preserving existing production bundled out/ directory ({bundled_workbench.stat().st_size / (1024*1024):.2f} MB)...")
    elif AGY_OUT_SRC.exists():
        print(f"[*] Fallback: Overlaying production out/ directory from {AGY_OUT_SRC}...")
        shutil.copytree(AGY_OUT_SRC, RESOURCES_APP_DEST / "out", dirs_exist_ok=True)

    # Copy extensions/ Directory
    if (VSCODE_DIR / "extensions").exists():
        print(f"[*] Copying extensions/ directory...")
        shutil.copytree(VSCODE_DIR / "extensions", RESOURCES_APP_DEST / "extensions", dirs_exist_ok=True)

    # Set up 28-byte empty dummy node_modules.asar to allow Electron to fall through to unpacked node_modules
    DUMMY_ASAR_BYTES = b'\x04\x00\x00\x00\x14\x00\x00\x00\x10\x00\x00\x00\x0c\x00\x00\x00{"files":{}}'
    ASAR_FILE = RESOURCES_APP_DEST / "node_modules.asar"
    with open(ASAR_FILE, "wb") as f:
        f.write(DUMMY_ASAR_BYTES)
    print(f"[*] Created empty dummy node_modules.asar (28 bytes) for direct unpacked module fallback...")

    # Copy full working unpacked node_modules from Antigravity IDE
    AGY_MODULE_SRC = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Antigravity IDE" / "resources" / "app" / "node_modules"
    if AGY_MODULE_SRC.exists():
        print(f"[*] Copying full working unpacked node_modules from {AGY_MODULE_SRC}...")
        shutil.copytree(AGY_MODULE_SRC, RESOURCES_APP_DEST / "node_modules", dirs_exist_ok=True)
    elif (VSCODE_DIR / "node_modules").exists():
        print(f"[*] Copying full node_modules/ directory from vscode/node_modules...")
        shutil.copytree(VSCODE_DIR / "node_modules", RESOURCES_APP_DEST / "node_modules", dirs_exist_ok=True)

    # Ensure conpty.node in Release directory
    PTY_UNPACKED_DEST = RESOURCES_APP_DEST / "node_modules" / "node-pty" / "build" / "Release"
    PTY_UNPACKED_DEST.mkdir(parents=True, exist_ok=True)
    
    PTY_SOURCES = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Antigravity IDE" / "resources" / "app" / "node_modules" / "node-pty" / "build" / "Release",
        ROOT_DIR / "vscode" / "node_modules" / "node-pty" / "build" / "Release"
    ]
    for pty_src in PTY_SOURCES:
        if pty_src.exists() and (pty_src / "conpty.node").exists():
            print(f"[*] Ensuring terminal conpty.node binaries from {pty_src}...")
            shutil.copytree(pty_src, PTY_UNPACKED_DEST, dirs_exist_ok=True)
            break

    # Create extensionless alias for all .node native binary files to prevent CJS resolution issues
    print(f"[*] Creating extensionless aliases for C++ native .node binaries...")
    for node_binary in (RESOURCES_APP_DEST / "node_modules").rglob("*.node"):
        alias_path = node_binary.with_name(node_binary.stem)
        if not alias_path.exists():
            shutil.copy2(node_binary, alias_path)

    # Clean any nested out/out directory artifact
    nested_out = RESOURCES_APP_DEST / "out" / "out"
    if nested_out.exists():
        print(f"[*] Removing nested out/out directory...")
        shutil.rmtree(nested_out, ignore_errors=True)

    # --- VS Code Official Portable Mode (data/ Directory) ---
    portable_data_dir = APP_DEST / "data"
    portable_data_dir.mkdir(parents=True, exist_ok=True)
    print(f"[*] Created official VS Code Portable mode directory at {portable_data_dir}...")

    # --- JS Direct Hot-Patching for %USERPROFILE% Declaration (TypeError & Subprocess Crash Prevention) ---
    print(f"[*] Applying Universal Safe JS Declaration Hot-Patch for %USERPROFILE% guardrails...")
    import re
    patched_count = 0
    TARGET_OUT_DIR = RESOURCES_APP_DEST / "out"

    for js_file in TARGET_OUT_DIR.rglob("*.js"):
        try:
            with open(js_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            original_len = len(content)
            
            # Universal pattern: Replace any variable name (a, r, s, l, etc.)
            def replacer(match):
                var_name = match.group(1)
                return f'const {var_name}=process.env.USERPROFILE||(process.env.HOMEDRIVE&&process.env.HOMEPATH?process.env.HOMEDRIVE+process.env.HOMEPATH:"C:\\\\Users\\\\"+(process.env.USERNAME||"Default"));process.env.USERPROFILE={var_name};'

            content = re.sub(r'const\s+([a-zA-Z0-9_$]+)\s*=\s*process\.env\.USERPROFILE\s*;', replacer, content)

            # Eliminate dangling unsafe throw or /* safe */ conditionals
            content = re.sub(
                r'if\s*\(\s*typeof\s+[a-zA-Z0-9_$]+\s*!=\s*["\']string["\']\s*\)\s*(?:throw new Error\([^)]*\)|\/\* safe \*\/)\s*;?',
                '',
                content
            )
            content = content.replace(
                'throw new Error("Windows: Unexpected undefined %USERPROFILE% environment variable")',
                '/* safe */'
            )

            if len(content) != original_len:
                with open(js_file, "w", encoding="utf-8") as f:
                    f.write(content)
                patched_count += 1
                print(f"    -> Successfully hot-patched universal declaration: {js_file.name}")
        except Exception as e:
            print(f"    [!] Warning: Failed to patch {js_file}: {e}")
    print(f"[ok] Universal Safe JS Hot-Patching completed ({patched_count} files secured).")

    # --- UI Branding & SVG Logo Injection ---
    try:
        from apply_desktop_branding import apply_branding
        apply_branding(TARGET_OUT_DIR)
    except Exception as e:
        print(f"    [!] Error applying branding: {e}")

    # --- Verify 4 Core Renderer Files to Guarantee No Black Screen ---
    print(f"[*] Validating 4 Core Renderer Files (Black Screen Prevention)...")
    wb_js = TARGET_OUT_DIR / "vs" / "workbench" / "workbench.desktop.main.js"
    wb_css = TARGET_OUT_DIR / "vs" / "workbench" / "workbench.desktop.main.css"
    wb_html = TARGET_OUT_DIR / "vs" / "code" / "electron-sandbox" / "workbench" / "workbench.html"
    if not wb_html.exists():
        wb_html = TARGET_OUT_DIR / "vs" / "code" / "electron-browser" / "workbench" / "workbench.html"

    wb_loader = TARGET_OUT_DIR / "vs" / "code" / "electron-sandbox" / "workbench" / "workbench.js"
    if not wb_loader.exists():
        wb_loader = TARGET_OUT_DIR / "vs" / "code" / "electron-browser" / "workbench" / "workbench.js"

    assert wb_js.exists() and wb_js.stat().st_size > 20 * 1024 * 1024, f"Missing or truncated workbench.desktop.main.js ({wb_js})"
    assert wb_css.exists() and wb_css.stat().st_size > 500 * 1024, f"Missing or truncated workbench.desktop.main.css ({wb_css})"
    assert wb_html.exists(), f"Missing workbench.html ({wb_html})"
    assert wb_loader.exists(), f"Missing workbench.js ({wb_loader})"
    print(f"[ok] Core Renderer Verified: workbench.js ({wb_js.stat().st_size / (1024*1024):.2f} MB), CSS ({wb_css.stat().st_size / (1024*1024):.2f} MB), HTML ({wb_html.name}) & Loader OK.")

    # --- Binary Branding & Icon Injection ---
    print(f"[*] Branding Desktop Executables to AgentSmith.exe...")
    code_exe = APP_DEST / "Code - OSS.exe"
    if not code_exe.exists():
        code_exe = APP_DEST / "Code.exe"
    if code_exe.exists():
        shutil.copy2(code_exe, APP_DEST / "AgentSmith.exe")
        shutil.copy2(code_exe, APP_DEST / "agentsmith_app.exe")
        print(f"[ok] Created AgentSmith.exe & agentsmith_app.exe binaries.")

    # Inject brand icon
    brand_ico_src = ROOT_DIR / "docs" / "images" / "code.ico"
    if brand_ico_src.exists():
        win32_ico_dest1 = APP_DEST / "resources" / "win32" / "code.ico"
        win32_ico_dest2 = RESOURCES_APP_DEST / "resources" / "win32" / "code.ico"
        win32_ico_dest1.parent.mkdir(parents=True, exist_ok=True)
        win32_ico_dest2.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(brand_ico_src, win32_ico_dest1)
        shutil.copy2(brand_ico_src, win32_ico_dest2)
        print(f"[ok] Injected brand code.ico into executable resources.")
else:
    print(f"[!] Warning: {ELECTRON_SRC} not found. Please build electron first.")

# 3. Copy coding-agent Backend Engine
CODING_AGENT_SRC = ROOT_DIR / "coding-agent"
CODING_AGENT_DEST = DIST_DIR / "coding-agent"

print(f"[*] Copying coding-agent backend engine...")
shutil.copytree(
    CODING_AGENT_SRC, 
    CODING_AGENT_DEST, 
    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache", ".git"),
    dirs_exist_ok=True
)

# 4. Copy .venv Python Environment
VENV_SRC = ROOT_DIR / ".venv"
VENV_DEST = DIST_DIR / ".venv"

if VENV_SRC.exists():
    print(f"[*] Copying .venv Python virtual environment...")
    try:
        shutil.copytree(
            VENV_SRC,
            VENV_DEST,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            dirs_exist_ok=True
        )
    except Exception as e:
        print(f"    [!] Note: Some locked venv files were skipped ({e}), core virtualenv structure preserved.")

# 5. Copy .agentsmith Mem0 Config
AGENTSMITH_SRC = ROOT_DIR / ".agentsmith"
AGENTSMITH_DEST = DIST_DIR / ".agentsmith"

if AGENTSMITH_SRC.exists():
    print(f"[*] Copying .agentsmith configuration...")
    shutil.copytree(AGENTSMITH_SRC, AGENTSMITH_DEST, dirs_exist_ok=True)

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
if not defined USERPROFILE (
    if defined HOMEDRIVE if defined HOMEPATH (
        set "USERPROFILE=%HOMEDRIVE%%HOMEPATH%"
    ) else (
        set "USERPROFILE=%SystemDrive%\\Users\\%USERNAME%"
    )
)
if not defined APPDATA set "APPDATA=%USERPROFILE%\\AppData\\Roaming"
if not defined LOCALAPPDATA set "LOCALAPPDATA=%USERPROFILE%\\AppData\\Local"

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set AGENTSMITH_BACKEND_PORT=5000

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

:: 2. Launch Desktop Client Binary (with GPU Stability Flags)
echo [*] Launching Desktop IDE Client...
set "CLIENT_FLAGS=--disable-gpu-sandbox --new-window"

if exist "app\\AgentSmith.exe" (
    start "" "app\\AgentSmith.exe" %CLIENT_FLAGS% "%~dp0"
) else if exist "agentsmith.exe" (
    start "" "agentsmith.exe" %CLIENT_FLAGS% "%~dp0"
) else if exist "app\\agentsmith_app.exe" (
    start "" "app\\agentsmith_app.exe" %CLIENT_FLAGS% "%~dp0"
) else if exist "app\\Code - OSS.exe" (
    start "" "app\\Code - OSS.exe" %CLIENT_FLAGS% "%~dp0"
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
