# 📄 문서 이관 및 현행화 명세서 (Specs): 상위 프로젝트 연관 문서 동기화

- **문서 일자**: 2026-08-20
- **작성자**: Agent Smith AI Lead / Pair Engineer
- **대상 브랜치**: `feature/setup-git-guardrails`
- **목적**: `agentsmith` 프로젝트의 단독 프로젝트 분리(Standalone Migration)에 대비하여, 상위 `aifullstack` 디렉터리에 분산되어 있던 연관 기획서, 세일즈 오퍼링, 아키텍처 가이드, 워크로그 문서들을 `agentsmith/docs/` 하위 체계로 이관하고 내부 참조 링크를 현행화함.

---

## 🛠️ 1. 이관 및 구성된 디렉터리 구조 (Specs Map)

| 구분 | 목적지 경로 | 원본 상위 경로 | 설명 |
| :--- | :--- | :--- | :--- |
| **세일즈 오퍼링** | [`docs/offering/`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/offering/) | `../offering/` | NVIDIA/Dell/MZC 비교 포털, 코딩 에이전트 제안서, 아키텍처 가이드라인 등 HTML 13종 |
| **워크로그** | [`docs/worklog/`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/worklog/) | `../docs/worklog/` | AI Fullstack 오퍼링 핸드오버(`2026-08-18_ai_fullstack_offering_handover.md`) 등 |
| **아이디어/설계** | [`docs/ideation/`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/ideation/) | `../docs/IDEATION/` | 코딩 에이전트 기본 설계 및 Top 3 분석 마크다운 문서 |
| **개발/운영 가이드** | [`docs/guides/`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/guides/) | `../docs/*.md` | 에이전트 빌더 가이드, 시연 기획서, 트리플 루프 운영 가이드(`LIFECYCLE_LOOPS_KR.md`) 등 12종 마크다운 |
| **전체 개요** | [`docs/AI_FULLSTACK_OVERVIEW.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/AI_FULLSTACK_OVERVIEW.md) | `../README.md` | AI Fullstack 상위 프로젝트 전체 아키텍처 및 로드맵 개요 |
| **명세서** | [`coding-agent/docs/specs/2026-08-20_parent_docs_migration_and_sync_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-20_parent_docs_migration_and_sync_spec.md) | - | 본 이관 및 현행화 명세서 |

---

## 🔍 2. 세부 이관 문서 목록

### 2.1 `docs/offering/` (세일즈 오퍼링 & 웹 제안서 포털)
1. `nvidia_ai_factory_vs_mzc_fullstack_comparison.html` (엔비디아 5계층 vs MZC 7-Layer 비교 포털)
2. `coding_agent_solution_proposal.html` (코딩 에이전트 솔루션 제안서)
3. `coding_agent_ui_mockup.html` (코딩 에이전트 인터랙티브 UI 목업)
4. `on_premise_ai_full_stack_master_proposal.html` (온프레미스 AI 풀스택 마스터 제안서)
5. `on_premise_ai_fullstack_architecture_guidelines.html` (온프레미스 AI 아키텍처 가이드라인)
6. `on_premise_ai_poc_and_production_architecture.html` (온프레미스 PoC 및 프로덕션 아키텍처)
7. `exhibition_pilot_solution_proposal.html` (전시회 파일럿 솔루션 제안서)
8. `korea_b2b_ai_agent_market.html` (국내 B2B AI 에이전트 시장 분석)
9. `articul8_ai_package_proposal.html` (Articul8 AI 패키지 제안서)
10. `document_pipeline_solution_proposal.html` (문서 파이프라인 솔루션 제안서)
11. `additional_ai_market_solutions.html` (추가 AI 시장 솔루션)
12. `index.html` (오퍼링 포털 인덱스)

### 2.2 `docs/guides/` (기술 및 운영 가이드라인)
1. `coding_agent_top3_analysis.md`
2. `exhibition_pilot_solution_plan.md`
3. `ai_agent_builder_guide.md`
4. `LIFECYCLE_LOOPS_KR.md`
5. `skill_prompt_mechanics_kr.md`
6. `skills.md` & `skills_kr.md`
7. `AGENTS_WORKFLOW_EXAMPLES.md`
8. `MARKETING_AUTOMATION_SOP.md`
9. `YOUTUBE_SEO_STRATEGY.md`
10. `tutorial_chinese_app.md`
11. `walkthrough_document_recovery.md`

---

## 🧪 3. 검증 결과 (Verification Results)
- `agentsmith/docs/` 디렉터리 내에 모든 하위 폴더(`offering/`, `worklog/`, `ideation/`, `guides/`)가 무결하게 생성 및 동기화됨.
- `coding-agent/TODO.md` 내 상위 경로 참조 링크가 내부 `docs/` 경로로 100% 현행화 완료.
