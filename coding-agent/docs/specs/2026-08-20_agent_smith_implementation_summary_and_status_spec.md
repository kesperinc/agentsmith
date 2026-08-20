# 📋 2026-08-20 Agent Smith 전체 구현 내용 및 현황 상세 명세서 (Implementation Spec)

**문서 작성일**: 2026-08-20  
**프로젝트명**: Agent Smith (Enterprise Custom Code-OSS AI Coding Editor)  
**작업 브랜치**: `feature/setup-git-guardrails`  
**버전**: v1.0.0 (Phase 2 Full Integration Completed)  
**작성자**: Agent Smith AI Architecture & Engineering Team  

---

## 1. 프로젝트 개요 및 핵심 목표

Agent Smith는 **Vibe Coding(의도 중심 자율 개발)** 패러다임을 지원하는 **엔터프라이즈 맞춤형 AI 코딩 에디터(Desktop IDE)**입니다.
Microsoft Code-OSS(VS Code 1.86.0)를 기반으로 자체 브랜딩, 멀티 LLM 연동, 사내 보안 및 엔터프라이즈 가드레일, 인터랙티브 AI 사이드바(Webview Chat), 아티팩트 관리자, Mem0 장기 기억 및 Graphify AST 지식 그래프를 100% 내장하였습니다.

---

## 2. 페이즈별 구현 내용 상세 정리

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Agent Smith Architecture                           │
├────────────────────────────────┬────────────────────────────────────────────┤
│  🖥️ Desktop IDE Client (VSCodium)│  🧠 Agentic Backend Server (FastAPI :5000)  │
│  - Code-OSS 1.86.0 Custom      │  - Intent-Driven Vibe Engine               │
│  - Custom Branding & App Icon  │  - Multi-LLM Adapter (OpenRouter/RHOAI)    │
│  - C++ Native Modules (ABI 118)│  - Multi-Tenancy SQLite DB (sessions.db)   │
│  - AI Chat Sidebar Webview     │  - Mem0 Long-Term Vector Memory            │
│  - Native Diff Viewer (vs.diff)│  - Graphify AST Static RAG Engine          │
│  - Slide-over Drawers (5종)    │  - CortexOS Security & Korean Guardrails   │
└────────────────────────────────┴────────────────────────────────────────────┘
```

### 🎯 Phase 0: 빌드 파이프라인, 바이너리 SOG 및 장애 해결 (완료)
1. **데스크톱 검은 화면(Black Screen) 3대 원인 근본 해결**:
   - `VSCode-win32-x64`의 프로덕션 번들 `out/`을 온전히 보존하도록 패키징 스크립트([package_desktop_dist.py](file:///c:/dev/antigravity-workspace/agentsmith/scripts/package_desktop_dist.py)) 전면 개편.
   - 28바이트 더미 asar(`{"files":{}}`)를 자동 주입하여 asar 후킹을 우회하고 Antigravity IDE의 Electron 27 ABI 118 C++ 네이티브 모듈 14종이 100% 정상 로드되도록 Unpacked 모듈 Fallback 완성.
2. **5초 자동 무결성 사전/사후 진단 도구**:
   - [scripts/verify_desktop_bundle.py](file:///c:/dev/antigravity-workspace/agentsmith/scripts/verify_desktop_bundle.py)를 통해 번들 크기, 더미 asar 유무, 의존성 누락 여부를 5초 내 자동 검증.
3. **C# Native 1-Click 단일 실행 설치 바이너리**:
   - [scripts/build_desktop_installer.py](file:///c:/dev/antigravity-workspace/agentsmith/scripts/build_desktop_installer.py)로 [dist/AgentSmith_Desktop_Setup_v1.0.0.exe](file:///c:/dev/antigravity-workspace/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) 자동 빌드 파이프라인 완성.
4. **세일즈 오퍼링 & 전략 제안 패키지 이관**:
   - NVIDIA AI Factory vs MZC 소버린 7-Layer 비교 포털 및 4-Phase 로드맵 웹 제안서 구축 완료 (`docs/offering/`).

---

### 🎯 Phase 1: Windows 에디터 빌드 & 브랜딩 & 표준 접근성 (완료)
1. **커스텀 브랜딩 패치**:
   - [product.json](file:///c:/dev/antigravity-workspace/agentsmith/vscode/product.json), [package.json](file:///c:/dev/antigravity-workspace/agentsmith/vscode/package.json) 내 제품명을 `Agent Smith IDE`로 변경 및 로고([logo.png](file:///c:/dev/antigravity-workspace/agentsmith/docs/images/logo.png)) 적용.
   - [apply_patches.py](file:///c:/dev/antigravity-workspace/agentsmith/build/apply_patches.py) 유틸리티를 통한 패치 무결성 관리.
2. **에디터 표준 접근성 복원 및 선택적 사내 보안(Enterprise Auth)**:
   - 기본 모드에서 로그인 없이 즉시 사용 가능한 VS Code 표준 에디터 접근성 100% 복원.
   - 사내 LDAP/이메일 OTP 인증을 상단 🔐 모달 토글 및 상태 배지 형태의 선택적 기능으로 전환.
3. **로컬 STT(음성 인식)**:
   - Webview Chat 마이크 버튼 클릭 시 브라우저 Web Audio / Whisper 백엔드 연동 음성 명령 지원.

---

### 🎯 Phase 2: Antigravity 스타일 챗 패널 & 지능형 에이전틱 코어 엔진 (완료)

1. **Antigravity 스타일 아티팩트(Artifacts) 관리 & 인터랙티브 뷰어 엔진**:
   - 에이전트가 생성한 구현계획서(`implementation_plan.md`), 상세명세서(`specs/`), 워크스루(`walkthrough.md`)를 전용 카드 UI로 렌더링.
   - **[에디터에서 열기]** 클릭 시 VS Code 본체 에디터(`vscode.window.showTextDocument`)로 실시간 오픈.
   - 상단 `[📋 아티팩트]` 드로어로 전체 산출물 목록 실시간 브라우징 및 1-Click 네비게이션.

2. **Planning Mode & 대화형 승인 게이트 (Planning-to-Execution Gate)**:
   - 3대 작업 모드 스위처 탑재: `🧠 Planning Mode`, `⚡ Fast Direct Mode`, `🧪 QA & Review Mode`.
   - Planning Mode 시 구현 계획서 생성 후 작업을 일시 정지하고 `⏳ 승인 대기` 배너와 **[✓ 승인하고 진행]** / **[✎ 수정 피드백]** 버튼 렌더링.
   - 사용자 승인 시 자동으로 실행 단계(Execution Loop)로 전환.

3. **사고 과정(Thinking Process) & 도구 호출(Tool Calls) 모던 아코디언**:
   - DeepSeek R1, Claude, Gemini의 Thinking 과정을 접이식(Accordion) 블록으로 실시간 렌더링 (`⏱ 소요시간` 뱃지 표출).
   - `replace_file_content`, `view_file`, `run_command` 등 도구 실행 파라미터, 반환 로그 아코디언 및 자율 셀프코렉션(Self-Correction) 시각화.

4. **Live Multi-File Diff & 안전 승인/롤백 UI**:
   - 실시간 다중 파일 변경 내역과 `+` / `-` Diff 코드블록 렌더링.
   - 파일별 **[✓ Accept]** / **[✕ Reject]** 및 **[🔍 Diff 비교]** 클릭 시 VS Code 내장 분할 비교창(`vscode.diff`) 호출.

5. **UUID 기반 멀티테넌트 세션 & 대화 히스토리 DB 관리**:
   - SQLite `sessions.db` (`sessions`, `messages`, `artifacts`, `diff_history` 테이블) 영속화.
   - 상단 `[🕒 기록]` 드로어를 통한 세션 목록 조회, 1-Click 복원 및 삭제.

6. **Mem0 장기 기억(Long-Term Memory) 프로필 엔진**:
   - `.agentsmith/` 디렉터리 내 SQLite/Mem0 장기 기억 컬렉션(`mem0_memory.db`) 연동.
   - 상단 `[🧠 기억]` 드로어로 저장된 코딩 스타일 및 규칙 시각화.
   - 시스템 프롬프트에 개발자 기억 자동 주입.

7. **Graphify AST 지식 그래프 & 하이브리드 RAG**:
   - Python 정적 AST 파서 기반 Class, Function, Method 노드 및 Call Graph 추출.
   - 상단 `[🕸️ 그래프]` 드로어로 인덱싱된 파일/심볼/노드/엣지 통계 및 AST 심볼 목록 실시간 시각화.

8. **CortexOS & gstack 기본 내장 가드레일 및 확장 체계**:
   - **한국어 강제 출력** 프롬프트 가드레일 바인딩.
   - UTF-8 BOM-less 파일 생성 강제화.
   - 작업 트라이어드([계획]-[코드]-[명세서] 1:1:1 쌍) 및 `YYYY-MM-DD_` 날짜 접두사 강제 규칙.
   - SAST 정적 보안 검사(시크릿/eval/SQLi) 및 `🛡️ SAST Security: PASSED` 뱃지 렌더링.
   - `@pm`, `@sa`, `@se`, `@qa`, `@cso`, `@dba`, `@growth`, `@ceo` 페르소나 및 `/review`, `/qa`, `/ship` 등 10종 워크플로우 내장 및 `@`, `/` 자동완성 팝업 탑재.
   - 상단 `[🧩 gstack]` 드로어를 통한 유저 확장 플러그인 로더 지원.

9. **AI 모델 및 API 키 연동 체계**:
   - [.env.example](file:///c:/dev/antigravity-workspace/agentsmith/.env.example) ➔ `.env` 기반 API 키 중앙 집중식 관리 (`GEMINI_API_KEY`, `GOOGLE_API_KEY`, `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, `MOONSHOT_API_KEY`, `ZHIPU_API_KEY`, `UPSTAGE_API_KEY`).
   - [model_detector.py](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/src/model_detector.py)를 통한 실시간 모델 헬스체크 및 Auto-Discovery.
   - [llm_adapter.py](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/src/adapters/llm_adapter.py) 및 `POST /api/openrouter/key` 엔드포인트를 통한 동적 API 키 등록 지원.

---

## 3. 백엔드 무결성 검증 결과

- **테스트 스크립트**: [scripts/test_backend_integrity.py](file:///c:/dev/antigravity-workspace/agentsmith/scripts/test_backend_integrity.py)
- **검증 항목**:
  1. Root 및 Workspace Status API (`/`, `/api/workspace/status`)
  2. 세션 생성 및 목록 조회 (`/api/sessions`, `/api/sessions/new`)
  3. Mem0 장기 기억 API (`/api/mem0/memories`)
  4. Graphify AST 지식 그래프 API (`/api/graphify/stats`)
  5. SAST 보안 가드레일 정적 검사 (`/api/guardrails/check`)
  6. Vibe Engine 코드 생성 및 Planning Gate (`/api/vibe/generate`)
  7. gstack 페르소나 및 워크플로우 API (`/api/plugins/gstack`)
- **결과**: **7개 전 핵심 기능 정상 응답 (100% PASSED)**

---

## 4. 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 주요 역할 |
|---|---|---|
| **백엔드 코어** | `coding-agent/src/main.py` | FastAPI REST & MCP 오케스트레이터 서버 |
| **LLM 어댑터** | `coding-agent/src/adapters/llm_adapter.py` | OpenRouter / RHOAI vLLM 연동 어댑터 |
| **모델 탐색기** | `coding-agent/src/model_detector.py` | 글로벌/로컬 AI 모델 자동 탐지 및 헬스체크 |
| **IDE 확장** | `extension/agentsmith-chat/src/extension.js` | VS Code Webview Provider & 네이티브 Diff 바인딩 |
| **챗 UI (HTML)** | `extension/agentsmith-chat/media/chat.html` | 5개 드로어, 아코디언, 승인 게이트, 모델 드롭다운 UI |
| **챗 UI (JS)** | `extension/agentsmith-chat/media/chat.js` | 렌더링, 이벤트 핸들링, 자동완성 팝업, STT 처리 |
| **챗 UI (CSS)** | `extension/agentsmith-chat/media/chat.css` | Glassmorphism 및 다크 테마 스타일링 |
| **패키징 스크립트** | `scripts/package_desktop_dist.py` | 포터블 데스크톱 IDE 번들 자동 빌드 도구 |
| **인스톨러 빌더** | `scripts/build_desktop_installer.py` | C# Native 단일 실행 설치 파일 컴파일러 |
| **무결성 진단** | `scripts/verify_desktop_bundle.py` | 데스크톱 번들 사전/사후 5초 자동 진단 도구 |
| **백엔드 검증** | `scripts/test_backend_integrity.py` | 백엔드 7대 핵심 엔드포인트 무결성 통합 테스트 |
| **환경 설정** | `.env.example` | 독립 작업 공간 및 AI Provider API 키 템플릿 |

---

© 2026 AI Architecture Engineering Team. All rights reserved.
