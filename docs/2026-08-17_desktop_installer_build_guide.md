# Agent Smith 데스크톱 단일 설치 파일 가이드 (Desktop Setup Installer Guide)

**작성 일자**: 2026-08-17  
**릴리즈 버전**: v1.0.0  
**단일 설치 실행 바이너리**: [`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) (**256.96 MB**)  
**설치 스크립트 작성자**: Agent Smith Engineering Team  
**관련 프로젝트 규칙**: AGENTS.md (규칙 14: 파이썬 가상환경 자동 셋업, 규칙 16: 날짜 명명 규칙)

---

## 1. 개요 (Overview)

본 문서는 다른 PC 및 사용자 환경에서 더블 클릭 한번으로 **Agent Smith Enterprise Desktop IDE** 및 파이썬 Vibe 코딩 엔진, Mem0 지속 기억 시스템을 자동 설치하고, 바탕화면과 시작 메뉴에 바로가기를 생성해 주는 **단일 윈도우 인스톨러 (`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`)** 구축 가이드입니다.

---

## 2. 인스톨러 바이너리 특징 (Installer Specifications)

| 항목 | 내용 |
| :--- | :--- |
| **설치 바이너리 명** | [`AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) |
| **바이너리 용량** | **256.96 MB** (Payload 100% 내장 단일 실행 파일) |
| **설치 대상 기본 경로** | `%LOCALAPPDATA%\Programs\AgentSmith` (UAC 관리자 권한 없이 설치 가능) |
| **자동 등록 바로가기** | 바탕화면(`Desktop`) 및 시작 메뉴(`Start Menu`)에 `code.ico` 삼엽 로고가 적용된 바로가기 생성 |
| **원터치 실행 매커니즘** | 백엔드 API 서버 (Port 5000) 감지 구동 + Desktop IDE GUI 무창 기동 |

---

## 3. 설치 및 실행 사용 방법 (Setup Instructions)

1. **설치 파일 구동**:
   - `AgentSmith_Desktop_Setup_v1.0.0.exe` 파일 double-click 구동.
2. **설치 확인 메시지 안내**:
   - 설치 경로 안내 메세지 창에서 `예(Y)` 선택.
3. **자동 압축 해제 및 바로가기 등록**:
   - `%LOCALAPPDATA%\Programs\AgentSmith` 디렉터리에 프로그램 복사 완료 후 바탕화면 및 시작 메뉴에 바로가기 파일 (`Agent Smith Desktop IDE.lnk`)이 자동 등록됩니다.
4. **즉시 실행 안내**:
   - 설치 완료 메세지 상자에서 `예(Y)`를 선택하면 Agent Smith Desktop IDE가 즉시 구동됩니다.

---

## 4. 인스톨러 빌드 자동화 스크립트 (Build Pipeline)

인스톨러 자동 재빌드는 다음 파이썬 명령어로 1-Click 실행할 수 있습니다:

```powershell
.venv\Scripts\python.exe scripts/build_desktop_installer.py
```

*빌드 내부 프로세스*:
1. `dist/agentsmith-desktop-v1.0.0` 폴더를 바이너리 zip 스트림으로 압축.
2. Windows 내장 64-bit C# 컴파일러 (`C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe`)를 호출하여 WinForms GUI 팝업 설치 로직과 리소스를 통합 컴파일.
3. 단일 바이너리 `dist/AgentSmith_Desktop_Setup_v1.0.0.exe` 출력.

---

**관련 문서**:
- 설치 가이드: [`docs/2026-08-17_desktop_installer_build_guide.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/2026-08-17_desktop_installer_build_guide.md)
- 설치 명세서: [`coding-agent/docs/specs/2026-08-17_desktop_installer_build_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-17_desktop_installer_build_spec.md)
