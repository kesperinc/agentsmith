# 📄 2026-08-19 Agentic 지능형 코어 엔진 & CortexOS 가드레일 로드맵 세분화 명세서

본 명세서는 2026년 8월 19일 진행된 Agent Smith IDE의 차세대 에이전틱 기능(Cursor, Windsurf, Continue, Antigravity 벤치마크) 및 CortexOS 가드레일/확장 체계의 세분화된 단계별 로드맵 개편 내역을 정의합니다.

---

## 📂 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 요약 |
| :--- | :--- | :--- |
| **[MODIFY]** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/TODO.md) | 5대 핵심 에이전틱 기능 및 CortexOS/gstack 가드레일 서브토픽 체크리스트로 전면 개편 |
| **[NEW]** | [`coding-agent/docs/specs/2026-08-19_agentic_core_roadmap_expansion_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-19_agentic_core_roadmap_expansion_spec.md) | 에이전틱 코어 엔진 및 CortexOS 가드레일 로드맵 명세서 (본 문서) |

---

## 🛠️ 2. 세분화된 5대 핵심 에이전틱 기능 구성 내역

### 1. UUID 기반 멀티테넌트 세션 & 대화 히스토리 DB 관리
- **세션 식별자 및 SQLite 영속화**: 신규 대화 시 고유 `UUID` 발급 및 `sessions.db` 테이블(`sessions`, `messages`, `artifacts`, `tool_calls`) 생성
- **타임스탬프 인덱싱 & 1-Click 복원**: 날짜/시간별 세션 목록화 및 과거 대화 이어쓰기
- **멀티테넌시 격리**: 프로젝트 및 사용자 계정별 작업 영역 격리
- **Mem0 연계 자동 요약/압축**: 토큰 한계 도달 시 과거 대화 자동 요약 및 컨텍스트 최적화

### 2. Mem0 장기 기억(Long-Term Memory) 프로필 및 개인화 엔진
- **벡터 메모리 영속화**: `.agentsmith/` 디렉터리 내 Qdrant/SQLite 벡터 DB 컬렉션(`agentsmith_default_memory`) 연동
- **개발자 코딩 프로필 자동 추출**: 코딩 스타일, 선호 라이브러리, 프로젝트 아키텍처 룰 학습
- **프롬프트 동적 주입**: 세션 시작 시 사용자 프로필을 시스템 프롬프트에 자동 바인딩

### 3. Graphify AST 지식 그래프 & 하이브리드 RAG
- **다국어 정적 AST 분석**: Python, TypeScript, Java, C++ 파서(Tree-sitter/Ast) 기반 Class, Function, Call Graph 노드/엣지 추출
- **증분 인덱싱 파이프라인**: 코드 변경 시 SQLite/NetworkX 기반 그래프 자동 업데이트 (`graphify update .`)
- **의존성 자동 역추적 & 하이브리드 검색**: 질의 시 상하위 호출 관계 역추적 및 BM25 + 시맨틱 임베딩 하이브리드 RAG 탑재

### 4. CortexOS & gstack 기본 내장 가드레일 및 유저 확장 체계
- **Built-in Core 가드레일**: 한국어 주석 강제, UTF-8 BOM-less, 작업 트라이어드([계획]-[코드]-[명세서]), SAST 보안 검사 엔진 기본 내장
- **gstack 전문가 페르소나**: `@pm`, `@sa`, `@se`, `@qa`, `@cso`, `@dba`, `@growth` 기본 탑재
- **gstack 라이프사이클 워크플로우**: `/office-hours`, `/plan-eng-review`, `/review`, `/debug`, `/qa`, `/ship` 내장
- **유저 확장 플러그인 로더**: `.agents/skills/` 및 `.agents/rules/` 동적 감지 및 런타임 핫 리로딩 지원

### 5. 다중 모델(Multi-LLM) 오케스트레이터 & Auto-Fallback
- **클라우드 및 온프레미스 통합 어댑터**: OpenAI, Claude, Gemini, DeepSeek, Ollama, LM Studio, 사내 vLLM
- **무중단 자동 전환 (Auto-Fallback)**: 네트워크 단절 또는 API 장애 시 사내 온프레미스/로컬 모델로 즉시 스위칭

### 6. Windsurf Cascade 스타일 Live Multi-File Diff & 안전 승인/롤백 UI
- **실시간 인라인 Diff 렌더러**: 에이전트 수정 다중 파일 목록 및 `+ / -` Diff 시각화
- **인터랙티브 승인 컨트롤**: 파일/코드블록별 **[Accept] / [Reject]** 및 에러 시 **[One-Click Rollback]** 지원
