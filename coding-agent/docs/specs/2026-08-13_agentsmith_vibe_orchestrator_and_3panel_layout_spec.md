# 📄 [작업 명세서] Task 2-1 Vibe Coding 오케스트레이터 및 3창 UI 레이아웃 구현 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 구현 성과 (Background & Accomplishments)

- **Vibe Coding 자율 오케스트레이터 구현**:
  - 개발자의 자연어 요구사항(Intent)을 분석하여 도메인/프레임워크 스키마를 자율 파싱하고, 멀티 파일 세트를 자동 생성한 뒤, 샌드박스 검증 및 셀프코렉션(Self-Correction) 루프를 전자율 집행하는 코어 모듈 구현 완료.
- **3창 UI 대시보드 레이아웃 완수**:
  - **[좌측 창]**: Vibe Prompt 요구사항 입력 & 탐색기 (File Explorer)
  - **[중앙 창]**: Trinity Air 로고 헤더 & 메인 코드 에디터 (Main Code Editor)
  - **[우측 창]**: Vibe Real-time Stream & Self-Correction 실시간 검증 로그 패널

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[NEW]** | `coding-agent/src/vibe_schema.py` | Vibe Coding 데이터 스키마 정의 |
| **[NEW]** | `coding-agent/src/vibe_orchestrator.py` | Vibe Coding 자율 오케스트레이터 엔진 코어 |
| **[MODIFY]** | `docs/coding_agent_basic_design.html` | 3창 UI 레이아웃 대시보드 설계 및 CSS 렌더링 반영 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_vibe_orchestrator_and_3panel_layout_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **vibe_orchestrator.py 실측 검증**: `python coding-agent/src/vibe_orchestrator.py` 구동 시 자연어 프롬프트 ➔ `['src/main.py', 'src/schemas.py', 'src/models.py']` 자율 생성 및 샌드박스 100% SUCCESS 리턴 실측 입증 완수.

---
*Agent Smith Vibe Orchestrator & 3-Panel Layout Specification Completed*
