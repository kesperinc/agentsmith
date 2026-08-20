# 📄 코드 및 가이드라인 변경 명세서 (Specs): 바이너리 빌드 파이프라인 고도화 및 표준 운영 지침(SOG) 구축

- **문서 일자**: 2026-08-20
- **작성자**: Agent Smith AI Lead / Pair Engineer
- **대상 브랜치**: `feature/setup-git-guardrails`
- **목적**: 타 PC 및 로컬 개발 환경에서 바이너리 빌드 및 패키징 시 발생하던 8대 반복 오류의 근본 원인을 파악하고, 사전/사후 5초 자동 무결성 진단 도구(`verify_desktop_bundle.py`)와 표준 운영 지침서(`2026-08-20_desktop_binary_build_and_troubleshooting_guide.md`)를 수립하여 영구적인 빌드 재현성을 확보함.

---

## 🛠️ 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 설명 |
| :--- | :--- | :--- |
| **[NEW] 지침서** | [`coding-agent/docs/2026-08-20_desktop_binary_build_and_troubleshooting_guide.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/2026-08-20_desktop_binary_build_and_troubleshooting_guide.md) | 8대 반복 오류 분석표, 3단계 1-Click 표준 빌드 절차서, 자가 복구 체크리스트 및 타 PC 이관 가이드가 포함된 종합 표준 운영 지침서(SOG) |
| **[NEW] 검증도구** | [`scripts/verify_desktop_bundle.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/verify_desktop_bundle.py) | 빌드 사전 환경(Node.js, Yarn, venv, csc, vscode) 및 사후 산출물(ABI 버전, C++ 모듈 14종, 별칭 바이너리, 런처, 인스톨러)을 5초 내에 자동 진단하는 무결성 검증 도구 |
| **[MODIFY] 패키징** | [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/package_desktop_dist.py) | Electron 27 ABI 118 네이티브 모듈 14종 자동 오버레이, CJS 확장자 미지정 별칭 사본 생성, `node_modules.asar` 제거 후 100% Unpacked 모듈 구조 반영 |
| **[MODIFY] 인스톨러** | [`scripts/build_desktop_installer.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/build_desktop_installer.py) | C# `Installer.cs` 대용량 페이로드 스트리밍 압축 해제, 파일 잠금 자동 해제(`KillLockedProcesses`), Safe Multi-Retry 및 .NET csc.exe 자동 탐색 |
| **[NEW] 명세서** | [`coding-agent/docs/specs/2026-08-20_binary_build_pipeline_and_sog_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-20_binary_build_pipeline_and_sog_spec.md) | 본 변경 명세서 |
| **[MODIFY] 로드맵** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/TODO.md) | 바이너리 빌드 오류 분석 및 표준 운영 지침 수립 과제 완료 반영 |

---

## 🔍 2. 핵심 해결 내역 및 엔지니어링 가드레일

### 2.1 8대 반복 오류 해결 매트릭스
1. **Spectre 완화 라이브러리 에러 (`MSB8040`)**: `Directory.Build.props`로 `<SpectreMitigation>false</SpectreMitigation>` 강제 오버라이드.
2. **Node ABI 버전 미스매치 (`ABI 116 vs 118`)**: Electron 27 호환 C++ 모듈 14종을 `resources/app/node_modules/`에 직접 오버레이 복사.
3. **`out/main` 모듈 누락**: `vscode/out` 복사를 패키징 필수 단계로 강제화.
4. **CJS Loader 확장자 미지정 require 실패 & Black Screen**: 동명 확장자 없는 별칭 파일 생성 및 `asar` 완전 제거.
5. **백엔드 콘솔 창 멈춤 (Console Hijacking)**: PowerShell `Start-Process -WindowStyle Hidden`으로 비동기 백그라운드 프로세스 격리.
6. **인스톨러 파일 잠금 (`IOException`)**: C# 인스톨러 내 `KillLockedProcesses`, 5회 Safe Multi-Retry, `.old` Rename 3중 안전망 구축.
7. **BOM/한글 인코딩 깨짐**: UTF-8 BOM-less 강제화 및 `chcp 65001`, `PYTHONUTF8=1` 환경변수 세팅.
8. **C# 컴파일러 (`csc.exe`) 미발견**: .NET Framework 4.0~4.8 및 VS Roslyn 다중 자동 탐색.

### 2.2 사전/사후 5초 자동 무결성 검증 도구 (`verify_desktop_bundle.py`)
- **사전 점검 (`--pre-check`)**: Node.js, Yarn, Python venv, C# 컴파일러, VS Code 소스 경로의 존재 여부 및 정상 구동 검증.
- **사후 점검 (`--verify-dist`)**: 메인 렌더러 모듈 존재, asar 미존재, 14종 네이티브 모듈 탑재, 비동기 런처 설정, 백엔드 엔진, 포터블 ZIP 및 단일 설치 파일 크기 검증.

---

## 🧪 3. 검증 결과 (Verification Results)

```text
============================================================
🔍 [Pre-flight Check] 데스크톱 빌드 환경 사전 점검
============================================================
 [✓] Node.js 감지: v24.14.1 (C:\Program Files\nodejs\node.EXE)
 [✓] Yarn 감지: 1.22.22 (C:\Users\MZC01-SUNKIM317\AppData\Roaming\npm\yarn.CMD)
 [✓] Python 가상환경 감지: C:\dev\antigravity-workspace\aifullstack\agentsmith\.venv\Scripts\python.exe
     -> 백엔드 필수 라이브러리(FastAPI, Uvicorn) 정상 로드
 [✓] C# 컴파일러 감지: C:\WINDOWS\Microsoft.NET\Framework64\v4.0.30319\csc.exe
 [✓] VS Code 소스 디렉터리 존재: C:\dev\antigravity-workspace\aifullstack\agentsmith\vscode
     -> [✓] vscode/out 컴파일 결과물 존재 확인
------------------------------------------------------------
✅ [사전 점검 완료] 빌드 환경 기본 무결성 검증 통과!
============================================================

============================================================
📦 [Post-build Verification] 배포 산출물 및 바이너리 무결성 정밀 진단
============================================================
 [✓] 배포 폴더 확인: C:\dev\antigravity-workspace\aifullstack\agentsmith\dist\agentsmith-desktop-v1.0.0
 [✓] 메인 렌더러 모듈 확인: C:\dev\antigravity-workspace\aifullstack\agentsmith\dist\agentsmith-desktop-v1.0.0\app\resources\app\out\main.js (21587 bytes)
 [✓] Pure Unpacked 모듈 구조 확인 (node_modules.asar 미존재)
 [✓] node_modules 디렉터리 확인: C:\dev\antigravity-workspace\aifullstack\agentsmith\dist\agentsmith-desktop-v1.0.0\app\resources\app\node_modules
 [✓] 필수 C++ 네이티브 모듈 14종 전체 탑재 확인
 [✓] 비동기 백그라운드 PowerShell 런처 설정 확인 (run_agentsmith_desktop.bat)
 [✓] coding-agent 백엔드 및 가상환경 번들 확인
 [✓] 포터블 배포 ZIP 확인: agentsmith-desktop-v1.0.0.zip (567.69 MB)
 [✓] C# Native 단일 실행 설치 파일 확인: AgentSmith_Desktop_Setup_v1.0.0.exe (564.21 MB)
------------------------------------------------------------
🎯 [산출물 무결성 진단 통과] 데스크톱 바이너리 패키지가 안정적으로 빌드되었습니다!
============================================================
```
