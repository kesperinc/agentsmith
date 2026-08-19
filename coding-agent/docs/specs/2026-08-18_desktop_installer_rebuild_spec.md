# 2026-08-18 Agent Smith 데스크톱 에디터 리빌드 및 설치 파일 재생성 명세서 (Desktop Installer & Editor Rebuild Spec)

**작성일자**: 2026-08-18  
**작성자**: Antigravity AI Coding Agent  
**상태**: 완료 (Completed)  

---

## 1. 개요 및 목적
본 명세서는 Electron 기본 웰컴 화면만 노출되던 문제를 근본적으로 해결하기 위해, 로컬 `vscode` 독립 리포지토리의 소스 코드 꼬임 현상을 클린업하고 `gulp`를 통해 Code-OSS 에디터 본체 코드를 100% 컴파일/번들링하여, 최종적으로 에디터 GUI가 정상 팝업되는 Windows Native C# 기반 단일 설치 파일(`AgentSmith_Desktop_Setup_v1.0.0.exe`)을 재생성한 상세 내역을 기록합니다.

---

## 2. 세부 빌드 및 컴파일 내역 (Specs Map)

### 2.1. 독립 깃 소스코드 복구 및 Gulp 클라이언트 번들링 (`yarn gulp vscode-win32-x64`)
- **문제 해결**: `vscode` 디렉터리 내부에 로컬에서 꼬여있던 `preferencesContribution.ts` 등 임시 수정 파일들을 폐기(`git restore .` 및 `git clean -fd`)하여 순정 상태로 돌려놓은 후, 루트 저장소가 추적하는 최신 커스텀 패치 파일들(`src/vs/...`)을 강제로 재적용.
- **Gulp 빌드**: `yarn gulp vscode-win32-x64` 실행을 통해 TypeScript 컴파일, 소스 맹글링(Mangler 3,586개 파일 처리), 확장 프로그램 번들링 및 `VSCode-win32-x64/resources/app/` 에디터 소스 주입을 무결하게 완주(Done in 3607.84s).

### 2.2. 독립 배포 패키지 구성 및 압축 (`package_desktop_dist.py`)
- **수정 사항**: `package_desktop_dist.py`가 빈 Electron 껍데기가 아닌, 새로 컴파일된 `VSCode-win32-x64` 에디터 패키지를 우선 복사하도록 경로 로직 패치.
- **배포판 위치**: `dist/agentsmith-desktop-v1.0.0/`
- **산출물**:
  - `dist/agentsmith-desktop-v1.0.0/app/` (컴파일된 VSCode 에디터 본체 포함)
  - `dist/agentsmith-desktop-v1.0.0.zip` (전체 아카이브)

### 2.3. Windows Native C# 인스톨러 컴파일 (`build_desktop_installer.py`)
- **컴파일러**: Windows Native C# Compiler `csc.exe` (`C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe`)
- **컴파일 방식**: 에디터 본체와 백엔드가 모두 담긴 배포본을 `payload.zip` 스트림으로 압축한 뒤 C# 바이너리 내에 Manifest 리소스로 임베드하여 단일 인스톨러 생성.
- **결과 파일**: `dist/AgentSmith_Desktop_Setup_v1.0.0.exe` (155.28 MB)

---

## 3. 변경 및 생성 파일 맵 (Specs File Map)

| 구분 | 파일/폴더 경로 | 변경 및 빌드 내용 |
| :--- | :--- | :--- |
| **MODIFY** | [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/package_desktop_dist.py) | `VSCode-win32-x64` 에디터 번들을 우선 복사하도록 경로 로직 수정 |
| **NEW/OVERWRITE** | [`dist/agentsmith-desktop-v1.0.0/`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/agentsmith-desktop-v1.0.0) | 정식 컴파일된 에디터가 포함된 독립 배포 폴더 |
| **NEW/OVERWRITE** | [`dist/agentsmith-desktop-v1.0.0.zip`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/agentsmith-desktop-v1.0.0.zip) | 독립 배포 zip 아카이브 |
| **NEW/OVERWRITE** | [`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) | **정식 에디터가 내장된 Windows Native C# 단일 설치 실행파일 (155.28 MB)** |
| **NEW** | [`coding-agent/docs/specs/2026-08-18_desktop_installer_rebuild_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-18_desktop_installer_rebuild_spec.md) | 에디터 리빌드 및 설치 실행파일 재생성 명세서 |

---

## 4. 빌드 결과 검증
- **Gulp 빌드 성공 코드**: `0` (에러 0개 완주)
- **C# 컴파일 성공 코드**: `0`
- **최종 인스톨러 바이너리 크기**: `155.28 MB` (에디터 본체 코드, 백엔드 엔진, 파이썬 실행환경 완전 탑재)
