# 📄 코드 및 산출물 변경 명세서 (Specs): 데스크톱 바이너리 리빌딩 및 무결성 진단

- **작성 일자**: 2026-08-20
- **작성자**: Agent Smith AI Pair Engineer
- **대상 브랜치**: `feature/setup-git-guardrails`
- **목적**: 현재 작업 디렉터리(`c:\dev\antigravity-workspace\agentsmith`)에서 데스크톱 IDE 실행 번들 및 C# Native 단일 설치 바이너리의 전체 재빌드(Rebuilding)를 수행하고, 사전/사후 100% 무결성 검증을 완료함.

---

## 🛠️ 1. 변경 및 생성된 파일 목록 (Specs Map)

| 구분 | 파일 경로 | 변경 요약 |
| :--- | :--- | :--- |
| **[NEW] 설정** | [`vscode/Directory.Build.props`](file:///c:/dev/antigravity-workspace/agentsmith/vscode/Directory.Build.props) | SpectreMitigation 경고(`MSB8040`) 방지를 위한 C++ 프로젝트 빌드 프로퍼티 주입 |
| **[MODIFY] 패키징** | [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/agentsmith/scripts/package_desktop_dist.py) | CJS 확장자 미지정 로드 방어를 위한 C++ 네이티브 `.node` 확장자 없는 별칭 파일 동적 생성 로직 추가 |
| **[REBUILT] 배포번들** | [`dist/agentsmith-desktop-v1.0.0`](file:///c:/dev/antigravity-workspace/agentsmith/dist/agentsmith-desktop-v1.0.0) | Pure Unpacked 모듈 구조, Electron 27 ABI 118 모듈 14종, coding-agent 백엔드 및 .venv 탑재 포터블 배포 디렉터리 |
| **[REBUILT] ZIP번들** | [`dist/agentsmith-desktop-v1.0.0.zip`](file:///c:/dev/antigravity-workspace/agentsmith/dist/agentsmith-desktop-v1.0.0.zip) | 포터블 배포용 압축 아카이브 (**583.90 MB**) |
| **[REBUILT] 인스톨러** | [`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) | C# Native 단일 실행 파일 형태의 1-Click GUI 설치 프로그램 (**580.43 MB**) |
| **[NEW] 명세서** | [`coding-agent/docs/specs/2026-08-20_desktop_binary_rebuild_and_verification_spec.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-20_desktop_binary_rebuild_and_verification_spec.md) | 본 바이너리 리빌딩 및 무결성 진단 명세서 |

---

## 🔍 2. 리빌딩 수행 단계 및 상세 결과

### 2.1 1단계: 사전 빌드 환경 점검 (`verify_desktop_bundle.py --pre-check`)
- **Node.js**: `v24.14.1` 감지 확인
- **Yarn**: `1.22.22` 감지 확인
- **Python .venv**: `FastAPI / Uvicorn` 정상 로드 확인
- **C# 컴파일러**: `C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe` 감지 확인
- **VS Code 소스 및 out**: `vscode/out` 컴파일 아티팩트 유효성 확인
- **SpectreMitigation**: `vscode/Directory.Build.props` 정상 설정 확인

### 2.2 2단계: 포터블 배포 패키징 (`package_desktop_dist.py`)
- Electron 런처 바이너리 동기화 및 `resources/app` 언팩 구조 생성
- `vscode/out` 렌더러 모듈 및 `vscode/extensions` 복사
- Electron 27 ABI 118 C++ 네이티브 모듈 14종 오버레이 복사
- 터미널 네이티브 모듈 `node-pty/build/Release/conpty.node` 무결성 확보
- CJS 확장자 미지정 탐색 대비 모든 `.node` 파일의 동명 별칭 사본 생성
- `node_modules.asar` 삭제를 통한 순수 Unpacked 모듈 구조 확정
- `coding-agent` 백엔드 파이썬 엔진 및 경량 `.venv` 번들링
- PowerShell `WindowStyle Hidden` 비동기 백그라운드 런처(`run_agentsmith_desktop.bat`) 탑재
- `dist/agentsmith-desktop-v1.0.0.zip` 포터블 아카이브 생성 완료

### 2.3 3단계: C# 단일 인스톨러 바이너리 컴파일 (`build_desktop_installer.py`)
- 배포 번들 인메모리 스트리밍 압축 (`payload.zip`, 580.34 MB)
- C# `Installer.cs` 소스 자동 구성:
  - 프로세스 자동 종료(`KillLockedProcesses`)
  - 5회 Safe Multi-Retry 및 `.old` Rename 안전망
  - Long Path 레지스트리 점검 및 `C:\AgentSmith` 단축 경로 추천 다이얼로그
- `csc.exe`를 통해 브랜드 로고(`code.ico`)가 내장된 단일 실행 파일 컴파일 완료
- 최종 산출물: `dist/AgentSmith_Desktop_Setup_v1.0.0.exe` (**580.43 MB**)

### 2.4 4단계: 사후 산출물 무결성 종합 진단 (`verify_desktop_bundle.py --all`)
- 모든 검증 항목 100% 정상 통과 (`🎯 [산출물 무결성 진단 통과]`)

---

## 🧪 3. 최종 검증 출력 로그

```text
============================================================
🔍 [Pre-flight Check] 데스크톱 빌드 환경 사전 점검
============================================================
 [✓] Node.js 감지: v24.14.1 (C:\Program Files\nodejs\node.EXE)
 [✓] Yarn 감지: 1.22.22 (C:\Users\MZC01-SUNKIM317\AppData\Roaming\npm\yarn.CMD)
 [✓] Python 가상환경 감지: C:\dev\antigravity-workspace\agentsmith\.venv\Scripts\python.exe
     -> 백엔드 필수 라이브러리(FastAPI, Uvicorn) 정상 로드
 [✓] C# 컴파일러 감지: C:\WINDOWS\Microsoft.NET\Framework64\v4.0.30319\csc.exe
 [✓] VS Code 소스 디렉터리 존재: C:\dev\antigravity-workspace\agentsmith\vscode
     -> [✓] vscode/out 컴파일 결과물 존재 확인
 [✓] SpectreMitigation 우회 설정 확인: C:\dev\antigravity-workspace\agentsmith\vscode\Directory.Build.props
------------------------------------------------------------
✅ [사전 점검 완료] 빌드 환경 기본 무결성 검증 통과!
============================================================

============================================================
📦 [Post-build Verification] 배포 산출물 및 바이너리 무결성 정밀 진단
============================================================
 [✓] 배포 폴더 확인: C:\dev\antigravity-workspace\agentsmith\dist\agentsmith-desktop-v1.0.0
 [✓] 메인 렌더러 모듈 확인: C:\dev\antigravity-workspace\agentsmith\dist\agentsmith-desktop-v1.0.0\app\resources\app\out\main.js (21587 bytes)
 [✓] Pure Unpacked 모듈 구조 확인 (node_modules.asar 미존재)
 [✓] node_modules 디렉터리 확인: C:\dev\antigravity-workspace\agentsmith\dist\agentsmith-desktop-v1.0.0\app\resources\app\node_modules
 [✓] 필수 C++ 네이티브 모듈 14종 전체 탑재 확인
 [✓] 비동기 백그라운드 PowerShell 런처 설정 확인 (run_agentsmith_desktop.bat)
 [✓] coding-agent 백엔드 및 가상환경 번들 확인
 [✓] 포터블 배포 ZIP 확인: agentsmith-desktop-v1.0.0.zip (583.90 MB)
 [✓] C# Native 단일 실행 설치 파일 확인: AgentSmith_Desktop_Setup_v1.0.0.exe (580.43 MB)
------------------------------------------------------------
🎯 [산출물 무결성 진단 통과] 데스크톱 바이너리 패키지가 안정적으로 빌드되었습니다!
============================================================
```
