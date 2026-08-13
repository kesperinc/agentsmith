# 📄 [작업 명세서] [/review] VSCODE_DEV 노드 모드 제거 및 정식 데스크톱 GUI 윈도우 출현 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 근본 원인 (Background & Root Cause)

- **문제 분석**: `/review` 코드 검토 결과, 런처 스크립트 내에 `set VSCODE_DEV=1` 및 `ELECTRON_RUN_AS_NODE` 가 지정되어 있어, Electron 엔진이 Chromium GUI BrowserWindow(에디터 창)를 생성하지 않고 CLI 노드 전용 모드로 동작하여 창을 띄우지 않았던 근본 원인이 포착되었습니다.
- **수행 조치**: [`run_agent_smith.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith.bat) 파일에서 노드 전용 실행 플래그(`VSCODE_DEV`, `ELECTRON_RUN_AS_NODE`)를 비활성화하여 정식 Chromium GUI BrowserWindow 에디터 창이 모니터 포그라운드에 팝업되도록 보정하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `run_agent_smith.bat` | `VSCODE_DEV` 및 `ELECTRON_RUN_AS_NODE` 제거 ➔ 정식 GUI BrowserWindow 출현 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_desktop_gui_mode_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **런처 검증**: [`run_agent_smith.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith.bat) 실행 시 헤드리스 모드가 아닌 정식 데스크톱 에디터 GUI 창 팝업 구동 완수.

---
*Agent Smith Desktop GUI Mode Specification Completed*
