# 📄 2026-08-19 Mem0 장기 기억 프로필 & Graphify AST 지식 그래프 구축 상세명세서

본 명세서는 2026년 8월 19일 진행된 Agent Smith IDE의 Mem0 기반 장기 기억(Long-Term Memory) 프로필 및 Graphify AST 지식 그래프 & 하이브리드 RAG 엔진, 그리고 이에 대응하는 프론트엔드 슬라이드 드로어 UI 구현 내역을 정의합니다.

---

## 📂 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 요약 |
| :--- | :--- | :--- |
| **[NEW]** | [`coding-agent/src/memory/mem0_manager.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/memory/mem0_manager.py) | Mem0 개발자 프로필 및 영속 코딩 규칙/가드레일 데이터베이스 관리자 |
| **[NEW]** | [`coding-agent/src/graphify/ast_engine.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/graphify/ast_engine.py) | 워크스페이스 Python 소스코드 정적 AST 파싱, Call Graph 노드/엣지 추출 및 하이브리드 RAG 엔진 |
| **[MODIFY]** | [`coding-agent/src/vibe/engine.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/vibe/engine.py) | Vibe 실행 시 Mem0 프로필 및 Graphify AST RAG 심볼 자동 주입 파이프라인 통합 |
| **[MODIFY]** | [`coding-agent/src/main.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/main.py) | Mem0 (`/api/mem0/*`), Graphify (`/api/graphify/*`) 및 웹뷰 정적 서빙 라우트(`/chat`) 탑재 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.html`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.html) | Mem0 드로어(`#mem0-drawer`), Graphify 드로어(`#graphify-drawer`) 및 헤더 토글 버튼(`[🧠 기억]`, `[🕸️ 그래프]`) 마크업 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.css`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.css) | Mem0 기억 카드 및 Graphify 통계 박스/AST 노드 뱃지 모던 스타일링 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.js) | 브라우저/VSCode 공용 브리지, Mem0/Graphify 드로어 데이터 바인딩 및 인터랙션 핸들러 구현 |
| **[NEW]** | [`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) | Mem0 장기 기억 및 Graphify AST RAG가 완전 탑재된 최신 단일 인스톨러 바이너리 컴파일 완료 (157.58 MB) |
| **[MODIFY]** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/TODO.md) | Phase 2 6번 및 7번 항목 완료(`[x]`) 현행화 |
| **[NEW]** | [`coding-agent/docs/specs/2026-08-19_mem0_and_graphify_ast_rag_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-19_mem0_and_graphify_ast_rag_spec.md) | Mem0 및 Graphify AST RAG 상세명세서 (본 문서) |

---

## 🛠️ 2. 상세 구현 기술 사양

### A. Mem0 장기 기억(Long-Term Memory) 프로필 시스템
- **데이터베이스**: `.agentsmith/mem0_memory.db` SQLite 스키마 (`memories`)
- **기억 카테고리**: `coding_style`, `project_rule`, `tech_stack`, `preference`
- **동적 프롬프트 주입**: 새 세션 시작 시 사용자 프로필 및 과거 프로젝트 룰(한글 주석, UTF-8 Bom-less, uv .venv 등)을 시스템 프롬프트에 자동 주입하여 일관된 코드 품질 유지.
- **UI 드로어**: 상단 `[🧠 기억]` 버튼 클릭 시 슬라이드 패널에 등록된 규칙 카드 실시간 시각화.

### B. Graphify AST 지식 그래프 & 하이브리드 RAG
- **정적 AST 분석기**: 워크스페이스 내 Python 소스코드를 순회하며 `ast.parse`를 통해 Class, Function, Method 노드 및 정의/호출 관계 엣지 자동 추출.
- **하이브리드 RAG**: 사용자 질의 시 AST 심볼 명칭 매칭과 그래프 관계 역추적을 결합하여 관련 모듈을 프롬프트에 자동 연계.
- **UI 드로어**: 상단 `[🕸️ 그래프]` 버튼 클릭 시 인덱싱된 파일 수, AST 심볼 수, 노드/엣지 통계 및 파싱된 심볼 목록 렌더링.
