# 2026-08-17 데스크톱 단일 인스톨러 바이너리 구축 명세서 (Desktop Installer Spec)

**작성일자**: 2026-08-17  
**작성자**: Agent Smith Engineering Team  
**상태**: 완료 (Completed)

---

## 1. 개요 및 목적
본 명세서는 Agent Smith 데스크톱 버전의 1-Click 자동 설치를 지원하기 위해 윈도우 네이티브 C# 컴파일러(`csc.exe`) 기반으로 리소스가 임베딩된 **단일 설치 실행 파일(`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`)**을 구축한 기술적 내역을 기록합니다.

---

## 2. 세부 변경 및 구축 내역 (Specs Map)

### 2.1. 네이티브 인스톨러 빌더 스크립트 작성 (`scripts/build_desktop_installer.py`)
- Python 및 Windows 기본 내장 C# 컴파일러 (`C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe`)를 활용.
- Application Payload ZIP 스트림을 C# 윈도우 어셈블리 리소스(`payload.zip`)로 내장 및 임베드 컴파일.

### 2.2. 인스톨러 실행 로직 (Installer Executable Logic)
- **GUI 안내 팝업**: WinForms 설치 확인 창 팝업.
- **자동 파일 복사**: `%LOCALAPPDATA%\Programs\AgentSmith` 경로로 압축 해제 및 파일 인스톨.
- **바로가기 자동 등록**: PowerShell COM 객체를 동적으로 호출하여 바탕화면(`Desktop`) 및 시작 메뉴(`Start Menu`)에 삼엽 로고(`code.ico`)가 박힌 `Agent Smith Desktop IDE.lnk` 등록.
- **설치 후 자동 구동 선택 지원**: 설치 완료 팝업 시 `예(Y)` 선택 시 즉시 에디터 및 파이썬 백엔드 기동.

### 2.3. 단일 바이너리 생성 결과
- 파일 위치: [`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe)
- 용량: **256.96 MB**

---

## 3. 변경 파일 맵 (Specs File Map)

| 구분 | 파일 경로 | 변경 내용 |
| :--- | :--- | :--- |
| **NEW** | [`scripts/build_desktop_installer.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/build_desktop_installer.py) | C# 네이티브 단일 인스톨러 빌더 파이썬 스크립트 |
| **NEW** | [`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) | 단일 윈도우 설치 바이너리 (256.96MB) |
| **NEW** | [`docs/2026-08-17_desktop_installer_build_guide.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/2026-08-17_desktop_installer_build_guide.md) | 설치 가이드 문서 |
| **NEW** | [`coding-agent/docs/specs/2026-08-17_desktop_installer_build_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-17_desktop_installer_build_spec.md) | 설치 바이너리 구축 명세서 |

---

## 4. 검증 결과
- `dist/AgentSmith_Desktop_Setup_v1.0.0.exe` 파일 (256.96 MB) 무결성 확인.
- C# 어셈블리 리소스 임베딩 및 `.NET Framework 4.5` 호환 컴파일 확인.
