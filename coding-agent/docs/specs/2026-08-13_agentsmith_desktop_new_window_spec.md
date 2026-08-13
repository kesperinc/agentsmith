# 📄 [작업 명세서] [/plan-eng-review] --new-window 독립 인스턴스 팝업 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 근본 원인 (Background & Root Cause)

- **문제 분석**: VS Code 메인 프로세스는 부팅 시 기존 프로세스와의 단일 인스턴스 소켓 통신을 우선적으로 시도하므로, CLI 인자로 `--new-window` 가 명시되지 않을 경우 새로 생성된 인스턴스가 윈도우 창을 팝업하지 않고 이전 세션으로 이관 후 소멸되었던 현상이었습니다.
- **수행 조치**: [`run_agent_smith.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith.bat) 런처에 `--new-window` 옵션을 정식 적용하여 언제 실행하더라도 독립된 데스크톱 에디터 GUI 윈도우 창이 포그라운드에 팝업되도록 보정 완료하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `run_agent_smith.bat` | `--new-window` 플래그 추가 ➔ 독립 데스크톱 에디터 GUI 창 팝업 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_desktop_new_window_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **독립 세션 팝업**: [`run_agent_smith.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith.bat) 실행 시 기존 인스턴스 간섭 없이 모니터 포그라운드에 데스크톱 GUI 에디터 창 팝업 완료.

---
*Agent Smith Desktop New Window Specification Completed*
