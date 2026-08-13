# 📄 [작업 명세서] [/plan-eng-review] 데스크톱 CWD 디렉터리 고정 바인딩 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 원인 진단 (Background & Root Cause)

- **문제 분석**: 웹 버전은 정상 동작하는데 데스크톱 버전만 무응답 상태에 빠진 근본 원인은 런처 스크립트 실행 시 Electron 프로세스의 작업 디렉터리(CWD)가 `vscode/` 루트 폴더로 명시적 지정되지 않아, Electron 메인 프로세스가 `package.json` 의 `"main": "./out/main"` 상대 경로를 제대로 탐색하지 못하고 부팅 단계에서 멈추었던 결함이었습니다.
- **수행 조치**: [`run_agent_smith.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith.bat) 런처에 작업 디렉터리 변경(`cd /d "%~dp0vscode"`) 및 `start` 명령어의 `/D` 디렉터리 바인딩 옵션을 정식 적용하여 CWD 탐색 결함을 100% 근본 해결하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `run_agent_smith.bat` | CWD 작업 디렉터리 고정 바인딩(`start "" /D "%~dp0vscode" ...`) 런처 적용 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_desktop_cwd_binding_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **CWD 작업 디렉터리 인식**: `vscode/` 루트 바인딩 완료.
- **데스크톱 런처 기동**: [`run_agent_smith.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith.bat) 실행 시 에러 없이 Agent Smith 데스크톱 에디터 GUI 창 팝업 완료.

---
*Agent Smith Desktop CWD Binding Specification Completed*
