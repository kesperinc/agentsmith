# 📋 2026-08-20 Agent Smith Phase 2 에이전틱 코어 엔진 & 3-Panel Studio 통합 명세서

- **작성 일자**: 2026-08-20
- **작업 브랜치**: `feature/setup-git-guardrails`
- **관련 스펙**: [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/TODO.md), [`docs/offering/coding_agent_ui_mockup.html`](file:///c:/dev/antigravity-workspace/agentsmith/docs/offering/coding_agent_ui_mockup.html)
- **작업자**: Agent Smith Engineering Team

---

## 1. 개요 및 구현 배경 (Overview)

순수 VS Code 바이너리 빌드 과정에서 분리되어 있던 **Phase 2 8대 에이전틱 코어 엔진**(아티팩트 엔진, Planning Gate, Thinking 아코디언, Live Multi-File Diff, UUID 세션 DB, Mem0 장기 기억, Graphify AST 지식 그래프, CortexOS & gstack 가드레일)을 VS Code 내장 확장 프로그램(`extensions/agentsmith-chat`) 및 백엔드(FastAPI Port 5000)와 100% 통합하고, **3열 + 하단 통합 터미널/모델 선택 바** 레이아웃을 구축하여 배포 패키지(`dist/`)에 번들링 완료하였습니다.

---

## 2. 레이아웃 아키텍처 (3-Column + Bottom Panel Studio)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│  [Top Menu Bar] Agent Smith IDE  │ [📋 아티팩트] [🕒 기록] [🧠 기억] [🕸️ 그래프] [🧩 gstack]  │
├─────────────────────────┬──────────────────────────────┬─────────────────────────────────────┤
│   [좌측 열] 탐색/컨트롤 │     [중앙 열] 챗 & 추론 로그 │       [우측 열] 에디터 & 브라우저   │
│                         │                              │                                     │
│ • 파일 탐색기(Explorer) │ • User/Agent 대화 말풍선     │ • Code Editor (Tab Bar)             │
│ • Vibe Prompt 입력창    │ • 사고 과정(Thinking) 아코디언│ • Live Multi-File Diff (+/- 코드)   │
│ • 작업 모드 스위처      │ • Planning Gate 승인 카드    │ • Subagent Browser (Headless 뷰어)  │
│   (Planning/Fast/QA)    │   ([✓ Proceed] / [✎ 피드백]) │ • 파일별 [Accept] / [Reject]        │
│ • 세션 히스토리 목록    │ • 도구 호출(Tool Calls) 로그 │ • [✓ 전체 수락] / [↺ 전체 롤백]     │
│ • @페르소나 / /스킬 팝업│ • 자율 Self-Correction 블록  │                                     │
├─────────────────────────┴──────────────────────────────┴─────────────────────────────────────┤
│ [하단 패널]                                                                                  │
│ • 샌드박스 실행 터미널 (Real-time stdout/stderr, SAST Security: PASSED 뱃지)                 │
│ • Model Selector Panel (OpenAI, Claude, Gemini, DeepSeek, Local Ollama 미니 카드 그리드)      │
│ • Status Bar (토큰 단가 실시간 통계, 응답 지연시간 ms, Mem0/AST 동기화 상태)                │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Phase 2 8대 에이전틱 코어 엔진 상세 구현 내역

### 1단계: Antigravity 스타일 아티팩트(Artifacts) 관리 & 인터랙티브 뷰어 엔진
- `implementation_plan.md`, `specs/`, `walkthrough.md` 생성 시 중앙 챗 창에 전용 아티팩트 카드 렌더링.
- **[📂 에디터에서 열기]** 클릭 시 `vscode.window.showTextDocument`를 통해 우측 에디터에 즉시 탭 오픈.
- 상단 `[📋 아티팩트]` 서랍을 통해 세션 중 생성된 문서 목록 실시간 네비게이션 지원.

### 2단계: Planning Mode & 대화형 승인 게이트 (Planning-to-Execution Gate)
- 좌측 상단 작업 모드 스위처 (`🧠 Plan`, `⚡ Fast`, `🧪 QA`).
- Planning Mode 시 구현 계획서 생성 후 일시 정지 및 `[✓ 승인하고 진행 (Proceed)]` / `[✎ 피드백]` 버튼 렌더링.
- 승인 클릭 시 백엔드 `VibeEngine`이 자율 파일 생성 및 샌드박스 검증 루프로 자동 전환.

### 3단계: 사고 과정(Thinking Process) & 도구 호출(Tool Calls) 모던 아코디언
- DeepSeek R1, Claude 3.7 Sonnet CoT 추론 과정을 중앙 챗 창에 접이식 아코디언(`⏱ 소요 시간` 표시)으로 렌더링.
- `gstack_persona_bind`, `mem0_retrieve`, `cortex_sast_scan` 등 도구 실행 상태 뱃지 및 Self-Correction 로그 표출.

### 4단계: Windsurf Cascade 스타일 Live Multi-File Diff & 안전 승인/롤백 UI
- 우측 열 상단 변경 파일 목록, 본문에 `+` (초록) / `-` (빨강) 인라인 Diff 렌더링.
- 파일별 **[✓ Accept]** / **[✕ Reject]** 및 **[↺ Rollback All]** 컨트롤을 통해 파일 반영 및 원본 복원.

### 5단계: UUID 기반 멀티테넌트 세션 & 대화 히스토리 DB 관리
- `coding-agent/src/db/session_manager.py` (SQLite `sessions.db`): `sessions`, `messages`, `artifacts`, `diff_history` 테이블 관리.
- 상단 `[🕒 기록]` 드로어를 통해 과거 세션 실시간 조회 및 1-Click 복원.

### 6단계: Mem0 장기 기억(Long-Term Memory) 프로필 및 개인화 엔진
- `coding-agent/src/memory/mem0_manager.py` (`.agentsmith/mem0_memory.db`): 기본 5대 가드레일(한국어 주석, UTF-8 BOM-less, uv .venv 등) 영속화.
- 상단 `[🧠 기억]` 드로어를 통해 저장된 프로필 실시간 조회 및 시스템 프롬프트 동적 주입.

### 7단계: Graphify AST 지식 그래프 & 하이브리드 RAG
- `coding-agent/src/graphify/ast_engine.py`: Python/TS 정적 AST 파싱, Class/Function/Method 노드 및 Call Graph 추출.
- 상단 `[🕸️ 그래프]` 드로어를 통해 인덱싱된 파일/심볼/노드/엣지 통계 실시간 시각화 및 하이브리드 RAG 질의.

### 8단계: CortexOS & gstack 기본 내장 가드레일 및 유저 확장 체계
- `coding-agent/src/guardrails/cortex_guard.py`: CORTEX-SEC-01(시크릿 탐지), CORTEX-SEC-02(eval/exec 차단), CORTEX-SEC-03(SQLi 검사) 및 `🛡️ SAST Security: PASSED` 뱃지 렌더링.
- `coding-agent/src/plugins/gstack_loader.py`: 8대 페르소나, 10대 워크플로우 내장 및 상단 `[🧩 gstack]` 드로어 1-Click 주입.

---

## 4. 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[NEW]** | `extensions/agentsmith-chat/package.json` | VS Code Webview Extension 매니페스트 |
| **[NEW]** | `extensions/agentsmith-chat/src/extension.ts` | 익스텐션 진입점 및 명령어 등록 |
| **[NEW]** | `extensions/agentsmith-chat/src/chatViewProvider.ts` | Webview View Provider & VS Code API 브릿지 |
| **[NEW]** | `extensions/agentsmith-chat/out/extension.js` | 컴파일된 CommonJS 익스텐션 런타임 |
| **[NEW]** | `extensions/agentsmith-chat/out/chatViewProvider.js` | 컴파일된 CommonJS Webview 프로바이더 |
| **[NEW]** | `extensions/agentsmith-chat/media/index.html` | 3열 + 하단 통합 터미널 Webview 마크업 |
| **[NEW]** | `extensions/agentsmith-chat/media/app.js` | React 18 챗/Thinking/Diff/5대 드로어 컨트롤러 |
| **[NEW]** | `extensions/agentsmith-chat/media/style.css` | Glassmorphism Dark Theme & 3-Column CSS |
| **[NEW]** | `extensions/agentsmith-chat/media/logo.svg` | 브랜드 액티비티 바 아이콘 |
| **[MODIFY]** | `coding-agent/src/main.py` | Media 디렉터리 경로 마운트 및 index.html 서빙 연동 |
| **[MODIFY]** | `scripts/package_desktop_dist.py` | `extensions/agentsmith-chat` 내장 번들링 로직 추가 |
| **[NEW]** | `scripts/test_backend_integrity.py` | 백엔드 6대 핵심 모듈 E2E 무결성 자동 검증 도구 |

---

## 5. 검증 결과 (Verification Results)

```
[1/6] SessionManager init...
      Created session ID: 48a9b9a5-0b44-42f1-900b-362cb3ea850f  [PASSED]
[2/6] Mem0Manager init...
      Loaded 5 persistent memories.                             [PASSED]
[3/6] GraphifyASTEngine scan...
      AST Graph files: 1, symbols: 1, nodes: 2, edges: 1       [PASSED]
[4/6] CortexGuard security scan...
      SAST status on leak test: warning (detected 2 issues)    [PASSED]
[5/6] GstackLoader scan...
      gstack personas: 8, workflows: 10, custom: 0              [PASSED]
[6/6] VibeEngine test...                                        [PASSED]
[SUCCESS] All 6 Phase 2 Core Agentic Modules Passed Integrity Check!
[BUILD] Desktop Distribution & ZIP Bundle Built with Embedded Extension!
```

---

*CortexOS Rule 5 (Plan-Code-Doc Triad) 및 Rule 16 (날짜 명명 규칙)을 100% 준수하여 작성되었습니다.*
