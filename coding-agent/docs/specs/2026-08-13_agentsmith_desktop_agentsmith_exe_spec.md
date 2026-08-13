# 📄 [작업 명세서] [/plan-eng-review] agentsmith.exe 단일 바이너리 결함 해결 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 근본 원인 (Background & Root Cause)

- **문제 진단**: 윈도우 `cmd.exe` 및 `start` 명령어는 실행 파일 경로에 공백과 하이픈(`Code - OSS.exe`)이 포함되어 있을 경우, 파싱 결함으로 인해 `'.\.build\electron\Code' is not recognized as an internal or external command` 오류를 일으키고 데스크톱 프로세스 팝업을 중단시켰던 근본 원인이 포착되었습니다.
- **수행 조치**: 공백과 하이픈이 없는 단일 브랜딩 명칭인 **`agentsmith.exe`** 바이너리를 정식 배치하고, [`run_agent_smith.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith.bat) 런처 구문을 정정하여 윈도우 CLI 파싱 결함을 100% 근본 차단하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[NEW]** | `vscode/.build/electron/agentsmith.exe` | 윈도우 CLI 파싱 결함을 차단하는 단일 브랜딩 데스크톱 실행 바이너리 |
| **[MODIFY]** | `run_agent_smith.bat` | `agentsmith.exe` 바이너리를 연동하는 1-Click GUI 런처 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_desktop_agentsmith_exe_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **`agentsmith.exe` 실재 유무**: `Test-Path = True` 검증 완료.
- **1-Click 런처 구동**: `run_agent_smith.bat` 실행 시 윈도우 파싱 오류 없이 Agent Smith 데스크톱 에디터 GUI 윈도우 창 팝업 완료.

---
*Agent Smith Desktop Execution Specification Completed*
