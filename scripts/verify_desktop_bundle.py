# -*- coding: utf-8 -*-
"""
Agent Smith Desktop Build & Bundle Verification Suite
Performs pre-flight checks before building and verifies final packaging artifacts.
Usage:
    python scripts/verify_desktop_bundle.py --pre-check
    python scripts/verify_desktop_bundle.py --verify-dist
    python scripts/verify_desktop_bundle.py --all
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Force UTF-8 Output
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT_DIR / "dist" / "agentsmith-desktop-v1.0.0"
SETUP_EXE = ROOT_DIR / "dist" / "AgentSmith_Desktop_Setup_v1.0.0.exe"
ZIP_BUNDLE = ROOT_DIR / "dist" / "agentsmith-desktop-v1.0.0.zip"
VSCODE_DIR = ROOT_DIR / "vscode"

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


def check_preflight():
    print("=" * 60)
    print("🔍 [Pre-flight Check] 데스크톱 빌드 환경 사전 점검")
    print("=" * 60)
    
    passed = True
    
    # 1. Node.js & Yarn
    node_path = shutil.which("node")
    if node_path:
        res = subprocess.run(["node", "-v"], capture_output=True, text=True, shell=True)
        print(f" [✓] Node.js 감지: {res.stdout.strip()} ({node_path})")
    else:
        print(" [✗] Node.js 미설치! (Node.js LTS v18+ 필요)")
        passed = False

    yarn_path = shutil.which("yarn")
    if yarn_path:
        try:
            res = subprocess.run(["yarn", "-v"], capture_output=True, text=True, shell=True)
            print(f" [✓] Yarn 감지: {res.stdout.strip()} ({yarn_path})")
        except Exception:
            print(f" [✓] Yarn 경로 감지: {yarn_path}")
    else:
        print(" [!] Yarn 미설치 (npm install -g yarn 권장)")

    # 2. Python & .venv
    venv_python = ROOT_DIR / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        print(f" [✓] Python 가상환경 감지: {venv_python}")
        try:
            res = subprocess.run(
                [str(venv_python), "-c", "import fastapi, uvicorn; print('FastAPI/Uvicorn OK')"],
                capture_output=True, text=True
            )
            if "FastAPI/Uvicorn OK" in res.stdout:
                print("     -> 백엔드 필수 라이브러리(FastAPI, Uvicorn) 정상 로드")
            else:
                print(f" [!] 백엔드 모듈 테스트 실패: {res.stderr.strip()}")
                passed = False
        except Exception as e:
            print(f" [!] 백엔드 검증 에러: {e}")
            passed = False
    else:
        print(" [✗] .venv 파이썬 가상환경 미존재! (uv venv 생성 및 의존성 설치 필요)")
        passed = False

    # 3. C# Compiler (csc.exe)
    csc_candidates = [
        Path(os.environ.get("WINDIR", "C:\\Windows")) / "Microsoft.NET" / "Framework64" / "v4.0.30319" / "csc.exe",
        Path(os.environ.get("WINDIR", "C:\\Windows")) / "Microsoft.NET" / "Framework" / "v4.0.30319" / "csc.exe",
        Path(os.environ.get("ProgramFiles", "C:\\Program Files")) / "Microsoft Visual Studio" / "2022" / "Community" / "MSBuild" / "Current" / "Bin" / "Roslyn" / "csc.exe",
        Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")) / "Microsoft Visual Studio" / "2019" / "Community" / "MSBuild" / "Current" / "Bin" / "Roslyn" / "csc.exe"
    ]
    csc_found = None
    for cand in csc_candidates:
        if cand.exists():
            csc_found = cand
            break
    
    if csc_found:
        print(f" [✓] C# 컴파일러 감지: {csc_found}")
    else:
        print(" [!] C# 컴파일러(csc.exe) 자동 경로 미발견 (인스톨러 빌드 시 확인 필요)")

    # 4. VS Code Upstream / Compilation
    if VSCODE_DIR.exists():
        print(f" [✓] VS Code 소스 디렉터리 존재: {VSCODE_DIR}")
        if (VSCODE_DIR / "out").exists():
            print(f"     -> [✓] vscode/out 컴파일 결과물 존재 확인")
        else:
            print(f"     -> [!] vscode/out 컴파일 결과물 부재 (yarn compile 필요)")
    else:
        print(f" [!] VS Code 소스 디렉터리 부재 ({VSCODE_DIR})")

    # 5. Directory.Build.props (Spectre Mitigation Bypass)
    props_file = VSCODE_DIR / "Directory.Build.props"
    if props_file.exists():
        print(f" [✓] SpectreMitigation 우회 설정 확인: {props_file}")
    else:
        print(f" [!] Directory.Build.props 부재 (빌드 시 자동 생성 권장)")

    print("-" * 60)
    if passed:
        print("✅ [사전 점검 완료] 빌드 환경 기본 무결성 검증 통과!")
    else:
        print("⚠️ [사전 점검 주의] 일부 필수 의존성이 누락되었습니다. 위의 [✗] 항목을 확인하세요.")
    print("=" * 60 + "\n")
    return passed


def check_dist_artifacts():
    print("=" * 60)
    print("📦 [Post-build Verification] 배포 산출물 및 바이너리 무결성 정밀 진단")
    print("=" * 60)

    success = True

    # 1. Dist Directory
    if not DIST_DIR.exists():
        print(f" [✗] 배포 폴더가 존재하지 않습니다: {DIST_DIR}")
        return False
    print(f" [✓] 배포 폴더 확인: {DIST_DIR}")

    # 2. Main Electron Entry & out/ directory
    resources_app = DIST_DIR / "app" / "resources" / "app"
    out_main = resources_app / "out" / "main.js"
    if out_main.exists():
        print(f" [✓] 메인 렌더러 모듈 확인: {out_main} ({out_main.stat().st_size} bytes)")
    else:
        print(f" [✗] 핵심 모듈 누락: {out_main} (Black Screen / Cannot find module 원인)")
        success = False

    # 3. node_modules.asar Removal Check
    asar_path = resources_app / "node_modules.asar"
    if asar_path.exists():
        print(f" [!] 경고: node_modules.asar 파일이 존재합니다! (Unpacked 모듈과의 충돌 방지를 위해 삭제 권장)")
    else:
        print(f" [✓] Pure Unpacked 모듈 구조 확인 (node_modules.asar 미존재)")

    # 4. Native Modules & CJS Aliases
    node_modules = resources_app / "node_modules"
    if node_modules.exists():
        print(f" [✓] node_modules 디렉터리 확인: {node_modules}")
        missing_native = []
        for mod in NATIVE_MODULE_NAMES:
            mod_path = node_modules / Path(mod)
            if not mod_path.exists():
                missing_native.append(mod)
        if missing_native:
            print(f" [!] 일부 C++ 네이티브 모듈 누락: {', '.join(missing_native)}")
        else:
            print(f" [✓] 필수 C++ 네이티브 모듈 14종 전체 탑재 확인")
    else:
        print(f" [✗] resources/app/node_modules 디렉터리 부재!")
        success = False

    # 5. Launcher Batch Script & Background Runner
    runner_bat = DIST_DIR / "run_agentsmith_desktop.bat"
    if runner_bat.exists():
        bat_text = runner_bat.read_text(encoding='utf-8', errors='ignore')
        if "WindowStyle Hidden" in bat_text:
            print(f" [✓] 비동기 백그라운드 PowerShell 런처 설정 확인 ({runner_bat.name})")
        else:
            print(f" [!] 런처에 WindowStyle Hidden 설정이 누락되어 콘솔 하이재킹 위험이 있습니다.")
    else:
        print(f" [✗] 런처 배치 파일 누락: {runner_bat}")
        success = False

    # 6. Backend Engine & .venv
    backend_main = DIST_DIR / "coding-agent" / "src" / "main.py"
    dist_venv = DIST_DIR / ".venv"
    if backend_main.exists() and dist_venv.exists():
        print(f" [✓] coding-agent 백엔드 및 가상환경 번들 확인")
    else:
        print(f" [✗] 백엔드 코드 또는 가상환경 번들 누락! (main.py={backend_main.exists()}, venv={dist_venv.exists()})")
        success = False

    # 7. Zip & Setup Binary
    if ZIP_BUNDLE.exists():
        print(f" [✓] 포터블 배포 ZIP 확인: {ZIP_BUNDLE.name} ({ZIP_BUNDLE.stat().st_size / (1024*1024):.2f} MB)")
    else:
        print(f" [!] ZIP 번들 파일 부재 ({ZIP_BUNDLE})")

    if SETUP_EXE.exists():
        print(f" [✓] C# Native 단일 실행 설치 파일 확인: {SETUP_EXE.name} ({SETUP_EXE.stat().st_size / (1024*1024):.2f} MB)")
    else:
        print(f" [!] C# Native 인스톨러 바이너리 부재 ({SETUP_EXE})")

    print("-" * 60)
    if success:
        print("🎯 [산출물 무결성 진단 통과] 데스크톱 바이너리 패키지가 안정적으로 빌드되었습니다!")
    else:
        print("❌ [산출물 무결성 진단 실패] 배포 번들에 치명적인 누락이 발견되었습니다.")
    print("=" * 60 + "\n")
    return success


if __name__ == "__main__":
    mode = "--all"
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    if mode in ["--pre-check", "-p"]:
        check_preflight()
    elif mode in ["--verify-dist", "-v"]:
        check_dist_artifacts()
    else:
        p_ok = check_preflight()
        d_ok = check_dist_artifacts()
        if not (p_ok and d_ok):
            sys.exit(1)
