# 📄 [작업 명세서] 데스크톱 잔여 Zombie 프로세스 자동 정리 및 GUI 팝업 정상화 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 근본 원인 (Background & Root Cause)

- **문제 분석**: "갑자기 안 됨" 현상의 결정적 원인은 이전 테스트 과정에서 백그라운드에 닫히지 않고 남아있던 30여 개의 `agentsmith.exe` 백그라운드 좁비(Zombie) 프로세스들이 윈도우 싱글 인스턴스 락(Single Instance Lock)과 파일 락을 쥐고 있었기 때문이었습니다.
- **수행 조치**:
  1. 잔여 백그라운드 `agentsmith.exe` 프로세스를 100% 전수 강제 종료(`taskkill /f /im agentsmith.exe`)하였습니다.
  2. [`run_agent_smith.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith.bat) 런처 상단에 잔여 프로세스 자동 종료 기능을 내장하여, 언제 더블클릭하더라도 항상 깨끗한 상태에서 1초 만에 데스크톱 에디터 GUI 창이 모니터 화면에 팝업되도록 수립하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `run_agent_smith.bat` | 잔여 zombie 프로세스 자동 정리(`taskkill /f /im agentsmith.exe`) 내장 런처 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_desktop_zombie_cleanup_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **잔여 프로세스 정리**: 30여 개 백그라운드 zombie `agentsmith.exe` 전수 종료 완수.
- **1-Click 런처 구동**: [`run_agent_smith.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith.bat) 실행 시 에러나 백그라운드 대기 없이 Agent Smith 데스크톱 에디터 GUI 창 팝업 구동 완수.

---
*Agent Smith Desktop Zombie Cleanup Specification Completed*
