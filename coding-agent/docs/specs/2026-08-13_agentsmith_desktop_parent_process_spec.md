# 📄 [작업 명세서] 부모 셸 닫힘 프로세스 동귀어진 차단 및 데스크톱 GUI 상주 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 근본 원인 (Background & Root Cause)

- **문제 분석**: CMD 배치 파일이 실행된 후 창이 닫히면서 데스크톱 모드가 실행되지 않았던 원인은 배치 파일 실행 종료 시 부모 콘솔 프로세스(`cmd.exe`)가 닫히며 자식 프로세스인 Node Electron 러너 프로세스까지 윈도우 OS 커널에 의해 함께 동귀어진(Killed with Parent Process)되었던 현상이었습니다.
- **수행 조치**:
  1. [`run_agent_smith.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith.bat) 런처에 독립 콘솔 타이틀 지정을 적용하여 부모 프로세스 닫힘에 따른 자식 프로세스 사멸을 차단하였습니다.
  2. 직관적인 1-Click GUI 실행 파일인 [`run_agent_smith_gui.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith_gui.bat) 을 신규 작성하여, 실행 시 콘솔이 자식 프로세스를 100% 안전하게 구동 유지하도록 수립하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[NEW]** | `run_agent_smith_gui.bat` | 데스크톱 GUI 전용 1-Click 상주 런처 |
| **[MODIFY]** | `run_agent_smith.bat` | 자식 프로세스 동귀어진 차단 런처 적용 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_desktop_parent_process_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **독립 상주 검증**: [`run_agent_smith_gui.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith_gui.bat) 및 [`run_agent_smith.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith.bat) 실행 시 부모 프로세스 닫힘 현상 없이 Agent Smith 데스크톱 에디터 GUI 윈도우 창 팝업 완수.

---
*Agent Smith Desktop Parent Process Specification Completed*
