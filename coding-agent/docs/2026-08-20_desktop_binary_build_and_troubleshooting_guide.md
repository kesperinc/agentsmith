# 📘 Agent Smith 데스크톱 바이너리 빌드 및 트러블슈팅 표준 운영 지침서 (SOG)

- **문서 번호**: SOG-AS-20260820-01
- **최종 개정일자**: 2026-08-20
- **문서 목적**: 개발 PC 환경(로컬 데스크톱, 노트북, 빌드 서버 등)이 바뀌더라도 누구나 동일한 오류 없이 1-Click으로 데스크톱 IDE 바이너리(포터블 번들 및 C# 단일 인스톨러)를 빌드, 패키징, 테스트할 수 있는 표준 운영 가이드라인을 제공함.

---

## 🏗️ 1. 바이너리 빌드 & 배포 파이프라인 아키텍처

```
+---------------------------------------------------------------------------------------------------+
|                        Agent Smith Unified Binary Build Pipeline Architecture                     |
+---------------------------------------------------------------------------------------------------+
                                                  │
    [Phase 1: Pre-flight Guard]                   ▼
    ├── Python 3.10+ & uv 가상환경 검증 (.venv)
    ├── Node.js LTS (v18+) & Yarn / node-gyp 글로벌 설치 검증
    ├── Visual Studio C++ Build Tools & .NET Framework csc.exe 자동 탐색
    └── Directory.Build.props (SpectreMitigation=false) 자동 주입
                                                  │
    [Phase 2: Code-OSS & Extension Build]         ▼
    ├── Upstream microsoft/vscode 1.86.0 태그 무결성 확인
    ├── Agent Smith 브랜딩 패치 적용 (apply_patches.py)
    ├── 내장 확장(agentsmith-chat) 및 프론트엔드 UI 복사
    └── yarn compile (vscode/out 빌드 아티팩트 생성)
                                                  │
    [Phase 3: Native Packaging & ABI Patch]       ▼
    ├── Electron 27 런처 리소스 (resources/app) 구성
    ├── vscode/out 및 필수 모듈 동기화 복사
    ├── Electron ABI 118 호환 C++ 네이티브 모듈 (14종) 정밀 오버레이
    ├── CJS Loader 호환 .node 바이너리 확장자 없는 별칭(Alias) 사본 자동 생성
    └── node_modules.asar 제거 및 100% Pure Unpacked 모듈 구조 확정
                                                  │
    [Phase 4: Backend & Runner Integration]       ▼
    ├── coding-agent 백엔드 엔진 & 경량 .venv 번들링
    ├── PowerShell WindowStyle Hidden 비동기 백그라운드 런처 (run_agentsmith_desktop.bat) 생성
    └── dist/agentsmith-desktop-v1.0.0 포터블 ZIP 아카이빙
                                                  │
    [Phase 5: C# Native Single-Setup Compiler]    ▼
    ├── C# Installer.cs 소스 동적 생성 (KillLockedProcesses, SafeMultiRetry, .old rename)
    ├── Brand Icon (code.ico) 임베딩 및 csc.exe 고압축 컴파일
    └── dist/AgentSmith_Desktop_Setup_v1.0.0.exe 산출물 최종 무결성 검증
```

---

## 💥 2. 지금까지 발생한 8대 반복 오류 및 영구 방지책 (Issue Archaeology)

| No | 에러 증상 및 현상 | 근본 원인 분석 | 영구 방지 조치 및 자동화 가드레일 |
| :--- | :--- | :--- | :--- |
| **1** | **`error MSB8040: Spectre-mitigated libraries are required`** | Visual Studio C++ 컴파일러의 Spectre mitigation 옵션 요구 | `vscode/Directory.Build.props`에 `<SpectreMitigation>false</SpectreMitigation>` 자동 주입 |
| **2** | **앱 가동 시 0.1초 만에 강제 종료 (`ERR_DLOPEN_FAILED`)** | Node.js v18 (`ABI 116`)과 Electron 27 (`ABI 118`) 네이티브 C++ 바이너리 불일치 | `Antigravity IDE` 내의 Electron 27 ABI 118 호환 모듈 14종을 `resources/app/node_modules/`에 오버레이 복사 |
| **3** | **`Cannot find module '.../out/main'` 팝업 오류** | Electron 런처의 `resources/app/out` 디렉토리에 컴파일된 JS 파일 누락 | `package_desktop_dist.py`에서 `vscode/out` 복사를 패키징 필수 단계로 강제화 |
| **4** | **클라이언트 창이 열리나 검은 화면(Black Screen)으로 멈춤** | 1. CJS require가 확장자 없는 `.node` 호출 시 탐색 실패<br>2. `node_modules.asar`의 asar loader 충돌 | 1. 모든 `.node` 바이너리에 동명 별칭 사본 자동 생성<br>2. `node_modules.asar` 삭제 후 100% Unpacked 모듈 구조 유지 |
| **5** | **CMD 콘솔 창 멈춤 & UI 미실행 (Console Hijacking)** | `start /b` 실행 시 FastAPI의 표준 입출력 스트림이 CMD 셸을 점유 | PowerShell `Start-Process -WindowStyle Hidden`으로 백엔드를 독립 백그라운드로 격리 기동 |
| **6** | **재설치 시 "파일이 사용 중이어서 설치 불가" (`IOException`)** | 이전 실행된 `Code - OSS.exe`, 백엔드 `python.exe` 프로세스가 파일 점유 | C# 인스톨러에 `KillLockedProcesses`, 5회 Safe Multi-Retry, `.old` Rename 3중 안전망 탑재 |
| **7** | **한글 주석/문자열 깨짐 및 배치 파일 문법 에러** | Windows 기본 ANSI (cp949)와 UTF-8 BOM 인코딩 충돌 | 소스 파일 UTF-8 BOM-less 강제, 배치 파일 상단 `chcp 65001`, 파이썬 `PYTHONUTF8=1` 지정 |
| **8** | **C# 컴파일러 `csc.exe` 미발견 오류** | 특정 PC에서 .NET Framework 또는 VS Roslyn 경로 상이 | `C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe` 및 VS 2019/2022 자동 폴백 탐색 |

---

## 📋 3. PC 환경 사전 준비 (Prerequisites Checklist)

새로운 PC에서 빌드를 시작하기 전에 아래 4가지 도구가 설치되어 있어야 합니다:

1. **Node.js LTS (v18 이상 권장)** & **Yarn**:
   ```cmd
   node -v
   npm install -g yarn node-gyp
   ```
2. **Python 3.10+ (uv 기반 가상환경 권장)**:
   ```cmd
   python -m venv .venv
   .\.venv\Scripts\pip install -r coding-agent/requirements.txt
   ```
3. **Git for Windows (UTF-8 활성화)**:
   ```cmd
   git --version
   ```
4. **.NET Framework 4.5+ (Windows 기본 내장)**:
   - `C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe` 존재 확인.

---

## 🚀 4. 3단계 1-Click 표준 빌드 절차서 (Step-by-Step Execution)

### 🔹 Step 1. 빌드 환경 사전 점검 (Pre-flight Check)
```cmd
python scripts/verify_desktop_bundle.py --pre-check
```
* **점검 결과**: Node.js, Yarn, Python venv, C# 컴파일러, VS Code 소스 경로가 모두 `[✓]`로 표시되는지 확인합니다.

### 🔹 Step 2. 포터블 번들 및 런처 패키징
```cmd
python scripts/package_desktop_dist.py
```
* **수행 작업**:
  - `VSCode-win32-x64` Electron 바이너리 복사
  - `vscode/out`, `vscode/extensions` 및 `vscode/node_modules` 언팩 구조 생성
  - Electron 27 ABI 118 네이티브 모듈 14종 자동 오버레이 및 확장자 없는 바이너리 별칭 생성
  - `coding-agent` 백엔드 및 `.venv` 번들링
  - 비동기 백그라운드 런처(`run_agentsmith_desktop.bat`) 및 ZIP 아카이브(`dist/agentsmith-desktop-v1.0.0.zip`) 생성

### 🔹 Step 3. C# Native 단일 인스톨러 컴파일
```cmd
python scripts/build_desktop_installer.py
```
* **수행 작업**:
  - `agentsmith-desktop-v1.0.0` 폴더를 인메모리 압축 스트림으로 패킹
  - 프로세스 자동 종료 및 잠금 해제 루틴이 포함된 C# `Installer.cs` 소스 생성
  - `csc.exe`를 통해 단일 실행 설치 파일(`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`) 컴파일

### 🔹 Step 4. 최종 산출물 무결성 진단 (Post-build Verification)
```cmd
python scripts/verify_desktop_bundle.py --verify-dist
```
* **점검 결과**: `🎯 [산출물 무결성 진단 통과]` 메시지 출력 확인.

---

## 🧪 5. 바이너리 실행 및 기능 테스트 가이드

### A. 포터블 모드 즉시 테스트
1. `dist/agentsmith-desktop-v1.0.0/run_agentsmith_desktop.bat` 실행
2. 백엔드(FastAPI)가 숨김 창으로 백그라운드에서 기동되는지 확인 (포트 5000)
3. Agent Smith IDE 윈도우가 검은 화면이나 튕김 없이 1~2초 내에 정상 렌더링되는지 확인
4. 좌측 액티비티 바에서 Agent Smith 로고 클릭 시 `Agent Smith Chat` 웹뷰 패널이 정상 열리는지 확인

### B. 단일 인스톨러 설치 테스트
1. `dist/AgentSmith_Desktop_Setup_v1.0.0.exe` 실행
2. 설치 다이얼로그 확인 후 [예(Yes)] 클릭
3. `%LOCALAPPDATA%\Programs\AgentSmith` 경로에 파일들이 무결하게 풀리고, 바탕화면/시작메뉴 바로가기가 생성되는지 확인
4. 바로가기 클릭 후 정상 실행 검증

---

## 🛠️ 6. 문제 발생 시 자가 복구 체크리스트 (Troubleshooting FAQ)

| 상황 | 확인 및 조치 방법 |
| :--- | :--- |
| **Q1. `node_modules` 복사 시 특정 파일 접근 거부 오류 발생** | `VSCode-win32-x64` 또는 이전 실행 프로세스가 남아있는 경우입니다. 작업 관리자에서 `Code - OSS.exe`, `node.exe`, `python.exe`를 강제 종료한 후 다시 실행하세요. |
| **Q2. Electron ABI 버전 미스매치로 앱이 튕길 때** | `Antigravity IDE`가 설치된 기본 경로(`%LOCALAPPDATA%\Programs\Antigravity IDE\resources\app\node_modules`)에서 모듈을 복사하거나 `package_desktop_dist.py`를 다시 실행하세요. |
| **Q3. 백엔드 포트 5000 충돌 시** | CMD에서 `netstat -ano \| findstr :5000`으로 PID를 확인 후 `taskkill /F /PID [PID]`로 기존 백엔드 프로세스를 종료하세요. |
| **Q4. C# 컴파일러를 찾지 못할 때** | `scripts/build_desktop_installer.py`의 `csc_candidates` 목록에 설치된 VS Roslyn 컴파일러 경로를 추가하세요. |

---

## 📦 7. 타 PC 이관 시 체크리스트 (Machine Transition Checklist)

1. **Git 저장소 최신화**:
   ```cmd
   git fetch --all
   git reset --hard origin/feature/setup-git-guardrails
   ```
2. **가상환경 의존성 설치**:
   ```cmd
   python -m venv .venv
   .\.venv\Scripts\pip install -r coding-agent/requirements.txt
   ```
3. **사전 진단 실행**:
   ```cmd
   python scripts/verify_desktop_bundle.py --all
   ```
4. **산출물 확인**:
   - `dist/AgentSmith_Desktop_Setup_v1.0.0.exe`
   - `dist/agentsmith-desktop-v1.0.0.zip`
