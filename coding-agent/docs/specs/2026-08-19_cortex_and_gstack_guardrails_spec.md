# 📄 2026-08-19 CortexOS 가드레일, gstack 전문가 페르소나 및 자동완성 시스템 상세명세서

본 명세서는 2026년 8월 19일 진행된 Agent Smith IDE의 CortexOS 코어 가드레일(한국어 출력 강제, UTF-8 Bom-less, 트라이어드 무결성, SAST 보안 검사기)과 gstack 전문가 페르소나 8종 및 라이프사이클 워크플로우 10종, `@`/`/` 실시간 인터랙티브 자동완성 팝업, `[🧩 gstack]` 슬라이드 드로어 UI 구현 내역을 정의합니다.

---

## 📂 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 요약 |
| :--- | :--- | :--- |
| **[NEW]** | [`coding-agent/src/guardrails/cortex_guard.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/guardrails/cortex_guard.py) | CortexOS 가드레일, 한국어 시스템 프롬프트 합성기, SAST 정적 보안 검사기 및 트라이어드 검사기 |
| **[NEW]** | [`coding-agent/src/plugins/gstack_loader.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/plugins/gstack_loader.py) | 내장 페르소나 8종, 워크플로우 10종 및 `.agents/` 커스텀 확장 동적 로더 및 의도 파서 |
| **[MODIFY]** | [`coding-agent/src/vibe/engine.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/vibe/engine.py) | `@persona` 및 `/command` 자동 파싱, SAST 보안 검사 및 페르소나 역할 주입 파이프라인 통합 |
| **[MODIFY]** | [`coding-agent/src/main.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/main.py) | gstack 플러그인 목록(`/api/plugins/gstack`) 및 SAST 검사(`/api/guardrails/check`) API 엔드포인트 탑재 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.html`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.html) | `@`/`/` 자동완성 팝업(`#autocomplete-popup`), gstack 플러그인 드로어(`#plugins-drawer`), 헤더 `[🧩 gstack]` 버튼 마크업 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.css`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.css) | 자동완성 팝업, 페르소나 그리드 카드, 워크플로우 카드, 활성 페르소나 뱃지 및 SAST 보안 뱃지 스타일 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.js) | `@`/`/` 실시간 감지 및 키보드 자동완성 탐색, gstack 드로어 렌더러 및 페르소나/SAST 뱃지 시각화 |
| **[MODIFY]** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/TODO.md) | Phase 2 8번 항목 완료(`[x]`) 현행화 |
| **[NEW]** | [`coding-agent/docs/specs/2026-08-19_cortex_and_gstack_guardrails_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-19_cortex_and_gstack_guardrails_spec.md) | gstack 및 CortexOS 가드레일 상세명세서 (본 문서) |

---

## 🛠️ 2. 상세 구현 기술 사양

### A. CortexOS Core 가드레일 및 SAST 보안 검사기
- **한국어 출력 강제**: 시스템 프롬프트 가드레일을 통해 AI가 작성하는 코드 주석, 설명, 커밋 메시지 및 대화 출력을 100% 한국어로 제어.
- **인코딩 및 가상환경**: UTF-8 BOM-less 및 `.venv` (uv) 환경 강제.
- **SAST 정적 보안 검사 (Cortex Guard)**:
  - `CORTEX-SEC-01`: 하드코딩된 API Key 및 Secret 토큰 검출.
  - `CORTEX-SEC-02`: 임의 코드 실행 위험이 있는 `eval()` / `exec()` 검출.
  - `CORTEX-SEC-03`: 문자열 포매팅 기반 원시 SQL Injection 취약 패턴 검출.
  - 검사 결과에 따라 챗창에 `🛡️ SAST Security: PASSED` 뱃지 실시간 표출.

### B. gstack 전문가 페르소나 8종 & 라이프사이클 워크플로우 10종
- **내장 페르소나**:
  - `@pm` (Product Manager), `@sa` (System Architect), `@se` (Software Engineer), `@qa` (QA Lead), `@cso` (Chief Security Officer), `@dba` (Database Admin), `@growth` (Growth Lead), `@ceo` (CEO / Founder)
- **내장 워크플로우**:
  - `/office-hours`, `/plan-ceo-review`, `/plan-eng-review`, `/review`, `/investigate`, `/qa`, `/qa-only`, `/design-review`, `/ship`, `/document-release`

### C. 인터랙티브 `@` / `/` 실시간 자동완성 팝업
- 대화창 입력란에서 `@` 또는 `/` 입력 시 연관 페르소나/워크플로우 목록 팝업 실시간 노출.
- 키보드 방향키(`↑`/`↓`) 탐색, `Enter`/`Tab` 선택 및 원클릭 자동 삽입 지원.
- 상단 `[🧩 gstack]` 드로어를 통해 8개 페르소나와 10개 워크플로우를 한눈에 탐색하고 1-Click으로 프롬프트에 주입 가능.
