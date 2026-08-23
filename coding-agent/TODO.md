# 🚀 Agent Smith IDE 단계별 TODO 로드맵

본 문서는 **Agent Smith IDE (Custom Code-OSS AI Editor)**의 개발 과제 및 릴리즈 로드맵 현행화 목록입니다. 로컬 데스크톱 중심의 IDE 빌드, 브랜딩, 가드레일, 온프레미스 배포 호환성 확보 및 CLI/IDE 연동 기능에 집중하도록 작성되었습니다.

* **최종 현행화 일자**: 2026년 8월 23일
* **검증 시스템**: `MZC_SUNKIM317_L` / `HOME_SUNKIM` (Windows 11 x64, Python 3.14, Node v24.14.1, Bun 1.3.11, uv 0.11.19)
* **개발 기조**: Windows 빌드 및 기능 완성을 최우선(Phase 1)으로 진행하며, **Antigravity 스타일 아티팩트/챗 패널 및 지능형 코어 엔진 고도화(Phase 2 - 완료)**, **리눅스/온프레미스 Red Hat 배포 호환성(Phase 3)** 및 **AI Full Stack 세일즈 오퍼링(NVIDIA/Dell/MZC 비교 포털 & 4-Phase 로드맵)**을 전사 지원합니다.

---

## 🎯 0단계: PC 저장소 현행화, 바이너리 표준 운영 지침(SOG) & 장애 해결 (완료 - 2026-08-23)
- [x] **타 PC 작업내역 수령 및 저장소 현행화 (호스트: HOME_SUNKIM / MZC_SUNKIM317_L)**:
  - [x] 원격 저장소 `origin/feature/setup-git-guardrails` 동기화 완료
  - [x] 웹뷰 검은 화면(Black Screen) Zero-Dependency Vanilla JS 렌더러 전환으로 영구 해결
  - [x] **Trinity Air 브랜드 로고 기반 밝은 Edge 네온 벡터 로고 리마스터 및 UI 전면 적용**
  - [x] **Agent Smith Studio 중앙 Welcome(에디터) 위치 자동 마운트 및 3창 분리 레이아웃 완성**
  - [x] 포터블 데스크톱 패키지(`dist/agentsmith-desktop-v1.0.0.zip`) 및 C# Native 인스톨러(`AgentSmith_Desktop_Setup_v1.0.0.exe`) 빌드 성공 (무결성 정밀 진단 100% PASS)
  - [x] 2026-08-21 PC 현행화 및 빌드 완료 보고서 작성 ([docs/2026-08-21_pc_sync_and_build_report.md](file:///c:/dev/antigravity-workspace/agentsmith/docs/2026-08-21_pc_sync_and_build_report.md))
  - [x] 2026-08-21 PC 동기화 명세서 작성 ([coding-agent/docs/specs/2026-08-21_pc_synchronization_spec.md](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-21_pc_synchronization_spec.md))
- [x] **바이너리 빌드 반복 오류 분석 및 표준 운영 지침서(SOG) 수립 (/plan-eng-review)**:
  - [x] 8대 반복 오류(Spectre, ABI 불일치, out/main 누락, Black Screen, 콘솔 멈춤, 파일 잠금, BOM, csc 탐색) 분석표 정리
  - [x] 3단계 1-Click 표준 빌드 및 문제해결 종합 지침서 작성 ([2026-08-20_desktop_binary_build_and_troubleshooting_guide.md](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/2026-08-20_desktop_binary_build_and_troubleshooting_guide.md))
  - [x] 5초 자동 무결성 사전/사후 진단 도구 개발 ([scripts/verify_desktop_bundle.py](file:///c:/dev/antigravity-workspace/agentsmith/scripts/verify_desktop_bundle.py))
  - [x] 빌드 파이프라인 및 SOG 상세명세서 작성 ([2026-08-20_binary_build_pipeline_and_sog_spec.md](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-20_binary_build_pipeline_and_sog_spec.md))
- [x] **Electron 클라이언트 GUI 실행 장애 4단계 완벽 해결**:
  - [x] [장애 1] `out/main` 누락 ➔ `vscode/out` 복사 로직 추가로 해결
  - [x] [장애 2] 백엔드 콘솔 멈춤 ➔ PowerShell `Start-Process -WindowStyle Hidden` 비동기 백그라운드 런처 격리로 해결
  - [x] [장애 3] 창 튕김 (Crash) ➔ `Antigravity IDE` 내 Electron 27 ABI 118 호환 C++ 네이티브 모듈 14종 오버레이 복사로 해결
  - [x] [장애 4] 화면 검은색 멈춤 ➔ CJS loader 확장자 미지정 require 바이너리 별칭(Alias) 사본 생성 및 `node_modules.asar` 제거 후 100% Unpacked 모듈 구조로 해결
- [x] **상위(`../`) 프로젝트 연관 문서 및 제안서 이관 & 현행화**:
  - [x] 세일즈 오퍼링 포털 및 HTML 제안서 13종 복사 (`docs/offering/`)
  - [x] 상위 워크로그 및 핸드오버 문서 복사 (`docs/worklog/`)
  - [x] 아이디어 및 기초설계 문서 복사 (`docs/ideation/`)
  - [x] 에이전트 빌더, 코딩 에이전트 분석, 루프 운영 가이드 등 12종 가이드 복사 (`docs/guides/`)
  - [x] 전체 개요 문서 복사 (`docs/AI_FULLSTACK_OVERVIEW.md`)
  - [x] 상위 문서 이관 및 현행화 명세서 작성 ([2026-08-20_parent_docs_migration_and_sync_spec.md](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-20_parent_docs_migration_and_sync_spec.md))
- [x] **Windows 긴 파일 경로(Long Path/MAX_PATH) 및 깊은 폴더명 대응 방안 수립**:
  - [x] 5대 계층 방어 아키텍처 가이드 수립 ([2026-08-20_long_path_and_deep_folder_mitigation_guide.md](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/2026-08-20_long_path_and_deep_folder_mitigation_guide.md))
  - [x] C# 인스톨러에 `LongPathsEnabled` 레지스트리 자동 점검 및 `\\?\` 접두사, `C:\AgentSmith` 단축 경로 추천 다이얼로그 탑재
  - [x] 긴 경로 대응 상세명세서 작성 ([2026-08-20_long_path_and_installer_mitigation_spec.md](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-20_long_path_and_installer_mitigation_spec.md))
- [x] **데스크톱 검은 화면(Black Screen) 3대 결함 근본 원인 규명 및 패키징 스크립트 영구 개편**:
  - [x] [원인 1] 프로덕션 번들(29.5MB)을 7KB 스텁으로 덮어쓰던 결함 제거 및 `VSCode-win32-x64` 번들 보존 로직 추가
  - [x] [원인 2] 28바이트 더미 asar(`{"files":{}}`)를 자동 주입하여 asar 후킹 우회 및 Unpacked 모듈 자동 Fallback 구현
  - [x] [원인 3] Antigravity IDE의 C++ 네이티브 모듈 14종 및 의존성 일괄 복사 표준화
  - [x] [검증 도구] `verify_desktop_bundle.py` 번들 크기 정밀 검사 및 더미 asar 감지 로직 탑재
  - [x] [명세서] [`coding-agent/docs/specs/2026-08-20_desktop_blackscreen_root_cause_and_fix_spec.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-20_desktop_blackscreen_root_cause_and_fix_spec.md)
  - [x] [핸드오버] [`docs/2026-08-20_handover.md`](file:///c:/dev/antigravity-workspace/agentsmith/docs/2026-08-20_handover.md)
- [x] **C# Native 1-Click 단일 실행 설치 바이너리 컴파일 완료**:
  - [x] [`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) (442.69 MB) 구축 완료
- [x] **통합 인수인계 및 구현 요약 명세서 작성**:
  - [x] [`coding-agent/docs/specs/2026-08-20_agent_smith_implementation_summary_and_status_spec.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-20_agent_smith_implementation_summary_and_status_spec.md)
  - [x] [`docs/2026-08-20_handover.md`](file:///c:/dev/antigravity-workspace/agentsmith/docs/2026-08-20_handover.md)

---

## 🎯 0단계: AI Full Stack 세일즈 오퍼링 & 전략 제안 패키지 (완료)
- [x] **MZC AI Fullstack vs NVIDIA AI Factory 7대 레이어 비교 분석 구축**:
  - [x] 엔비디아 5계층(Compute -> Fabric -> Platform -> NIM -> Blueprints) vs MZC 소버린 7-Layer 1:1 정밀 비교 매트릭스 완성
- [x] **Dell AI Factory with NVIDIA 3자 심층 비교 탭 및 아키텍처 탑재**:
  - [x] Dell PowerEdge XE9680/XE9640, PowerScale 스토리지, APEX 과금 모델 및 MZC 소버린 SI 연동 융합 모델 수립
- [x] **11단계 세일즈 패키지의 '4대 핵심 Phase' 압축 그루핑 로드맵 개편**:
  - [x] Phase 1(진단/검증) ➔ Phase 2(코어전환) ➔ Phase 3(AI현대화) ➔ Phase 4(운영/확장) 인터랙티브 UI 구현
- [x] **인터랙티브 웹 제안서 포털 갱신 및 핸드오버 문서 작성**:
  - [x] [`docs/offering/nvidia_ai_factory_vs_mzc_fullstack_comparison.html`](file:///c:/dev/antigravity-workspace/agentsmith/docs/offering/nvidia_ai_factory_vs_mzc_fullstack_comparison.html)
  - [x] [`docs/worklog/2026-08-18_ai_fullstack_offering_handover.md`](file:///c:/dev/antigravity-workspace/agentsmith/docs/worklog/2026-08-18_ai_fullstack_offering_handover.md)
  - [x] [`coding-agent/docs/specs/2026-08-18_nvidia_ai_factory_vs_mzc_fullstack_spec.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-18_nvidia_ai_factory_vs_mzc_fullstack_spec.md)

---

## 🎯 1단계: 기반 설정 및 로컬 가드레일 (완료)
- [x] 프로젝트 메인 Git 브랜치 가드레일 전략 수립 및 원격 저장소 동기화 (`main`, `staging`, `feature/setup-git-guardrails`)
- [x] .gitignore 및 .stignore 파일 보완 (vscode/ 차단 해제, Syncthing 대용량 바이너리 제외 및 빌드 아티팩트 선별 차단)
- [x] AGENTS.md 프로젝트 개발/운영 수칙 단독 저장소 기준 상대경로 현행화
- [x] 1-Click 가상환경(uv) 및 Node.js 설치 감지 모듈 개발 완료
- [x] 2바이트 다국어 보장을 위한 UTF-8 Bom-less 강제화 및 cp949 환경 에러 방지 설정
- [x] 배포 타임스탬프 기반 버전 번호 규격(`Major.Minor.Patch-YYYYMMDD.HHMMSS`) 자동 생성 및 주입 스크립트 작성 ([update_version.py](file:///c:/dev/antigravity-workspace/agentsmith/build/update_version.py), [inject_version.bat](file:///c:/dev/antigravity-workspace/agentsmith/build/inject_version.bat))

---

## 🎯 Phase 1: Windows 에디터 빌드 & 브랜딩 (완료)
- [x] **Upstream Code-OSS 동기화 및 복구**:
  - [x] vscode/ 디렉터리 클린업 및 `.git` Upstream 재싱크 (microsoft/vscode 1.86.0 기준 완전한 형상 관리 저장소 확보)
  - [x] `yarn install`을 통한 100% 컴파일 의존성 모듈 설치 완료
- [x] **브랜드 로고 및 커스텀 브랜딩 적용**:
  - [x] 신규 확정 브랜드 로고([logo.png](file:///c:/dev/antigravity-workspace/agentsmith/docs/images/logo.png))를 IDE 액티비티 바 아이콘, 웰컴 페이지, 제품 로고(`app.ico` 등)로 이식
  - [x] product.json / package.json 내 제품명을 `Code - OSS`에서 `Agent Smith IDE`로 변경하는 커스텀 패치 파일 생성 및 적용
  - [x] 커스텀 패치 관리 및 JSON 무결성 검증 유틸리티 개발 ([apply_patches.py](file:///c:/dev/antigravity-workspace/agentsmith/build/apply_patches.py))
- [x] **에디터 표준 접근성 복원 및 선택적 사내 보안(Enterprise Auth) 기능화**:
  - [x] 기본 모드에서 무제한 즉시 대화창 진입 및 사용 가능한 표준 VS Code 접근성 100% 복원 (로그인 강제 차단 해제)
  - [x] 사내 폐쇄망/사내 LDAP 및 이메일 OTP 인증을 '선택적 Enterprise 기능(상단 🔐 모달 토글 및 상태 배지)'으로 전환 탑재
  - [x] Left Chat Panel(webview) 내 마이크 토글 버튼 탑재 및 로컬 STT(Web Audio/Whisper) 연동
  - [x] 대화창 모델 선택 드롭다운 UI 추가 및 백엔드 MCP 연동
- [x] **1-Click 윈도우 포터블 패키징 및 인스톨러 배포**:
  - [x] C# Native 단일 실행 설치 파일(`AgentSmith_Desktop_Setup_v1.0.0.exe`) 및 포터블 배포 패키지(`dist/agentsmith-desktop-v1.0.0`) 자동 빌드 파이프라인 완성

---

## 🎯 Phase 2: Antigravity 스타일 챗 패널 & 지능형 에이전틱 코어 엔진 (완료 - 2026-08-20)

### 📌 1. Antigravity 스타일 아티팩트(Artifacts) 관리 & 인터랙티브 뷰어 엔진 (완료)
- [x] **아티팩트 카드(Artifact Card) 렌더링 컴포넌트**:
  - [x] 에이전트가 생성한 구현계획서(`implementation_plan.md`), 상세명세서(`specs/`), 워크스루(`walkthrough.md`), 다이어그램 메타데이터를 감지하여 챗 메시지 내 전용 카드 UI로 렌더링
  - [x] 아티팩트 카드 내 요약 정보, 파일 크기, 상태 태그(계획/완료/피드백대기) 시각화
- [x] **에디터 네이티브 열기 연동 (VS Code Integration)**:
  - [x] 아티팩트 카드 내 **[에디터에서 열기]** 버튼 클릭 시 VS Code 본체 에디터 창(`vscode.window.showTextDocument`)으로 실시간 문서 오픈
- [x] **상단 아티팩트 서랍(Artifacts Drawer) 구축**:
  - [x] 챗 패널 상단 헤더에 현재 세션에서 생성/수정된 아티팩트 카운터 배지(`📋 아티팩트 (N)`) 탑재
  - [x] 클릭 시 아티팩트 목록이 슬라이드로 열리고 원하는 문서를 1-Click 네비게이션할 수 있는 드로어 UI 구현
- [x] **작업 트라이어드([계획]-[코드]-[명세서]) 자동 바인딩**:
  - [x] 코드 변경 작업 완료 시 `specs/` 하위에 명세서 자동 생성 및 아티팩트 맵(Specs Map) 기록

### 📌 2. Planning Mode & 대화형 승인 게이트 (Planning-to-Execution Gate) (완료)
- [x] **작업 모드 스위처(Mode Selector)**:
  - [x] `🧠 Planning Mode (계획 수립 후 승인 대기)`
  - [x] `⚡ Fast Direct Mode (단순 작업 즉시 실행)`
  - [x] `🧪 QA & Review Mode (코드 분석 및 테스트 검증)`
- [x] **인터랙티브 승인 게이트(Approval Gate) 상태 머신**:
  - [x] Planning Mode 동작 시 구현 계획서 생성 후 작업을 일시 정지하고 `⏳ [Planning Gate] 승인 대기` 배너 노출
  - [x] 계획서 카드 내에 **[✓ 승인하고 진행 (Proceed)]** 및 **[✎ 수정 피드백 입력]** 액션 버튼 렌더링
- [x] **자동 실행 페이즈 전환(Execution Loop)**:
  - [x] 사용자 승인 시 `[✓ 계획 승인됨 (Approved)]` 상태로 전환 및 자동으로 실행 단계(Execution Loop)로 전환

### 📌 3. 사고 과정(Thinking Process) & 도구 호출(Tool Calls) 모던 아코디언 (완료)
- [x] **실시간 추론(Thinking) 아코디언 UI**:
  - [x] DeepSeek R1, Claude, Gemini의 사고 과정(`Thinking Block`)을 기본 접이식(Accordion) 블록으로 렌더링
  - [x] 사고 소요 시간 뱃지(`⏱ 3.2s`) 노출 및 부드러운 토글 인터랙션
- [x] **도구 실행(Tool Execution) 상세 아코디언**:
  - [x] `replace_file_content`, `view_file`, `run_command` 등 도구 호출별 상태 뱃지(`[SUCCESS 110ms]`), 파라미터 및 반환 로그 아코디언 제공
  - [x] 도구 실행 실패 시 에러 감지 및 **자율 셀프코렉션(Self-Correction Loop)** 시각화 블록 탑재

### 📌 4. Windsurf Cascade 스타일 Live Multi-File Diff & 안전 승인/롤백 UI (완료)
- [x] **실시간 Multi-File Diff 및 변경 맵 렌더러**:
  - [x] 에이전트가 다중 파일을 생성/수정할 때 챗 패널에 실시간 변경 파일 목록과 `+ (추가)` / `- (삭제)` Diff 코드블록 시각화
- [x] **인터랙티브 제어 컨트롤**:
  - [x] 파일별 **[✓ Accept]** / **[✕ Reject]** 및 상단 **[✓ 모두 수락]** / **[↺ 전체 롤백]** 안전장치 탑재
- [x] **VS Code Native Diff 뷰어 연동**:
  - [x] [🔍 Diff 비교] 클릭 시 VS Code 내장 Diff 에디터(`vscode.diff`)를 호출하여 좌우 분할 화면으로 정밀 비교 지원

### 📌 5. UUID 기반 멀티테넌트 세션 & 대화 히스토리 DB 관리 (완료)
- [x] **세션 식별자 및 SQLite 영속화 스키마 구축**:
  - [x] 신규 대화 생성 시 고유 `UUID` 자동 발급 및 `sessions.db` SQLite 테이블(`sessions`, `messages`, `artifacts`, `diff_history`) 생성
  - [x] 상단 `[🕒 기록]` 드로어를 통해 과거 대화 세션 목록 실시간 조회, 1-Click 복원 및 삭제 지원
- [x] **멀티테넌시(Multi-Tenancy) 워크스페이스 격리**:
  - [x] 프로젝트별 세션 DB 및 아티팩트 저장소 격리 바인딩 및 컨텍스트 오염 방지 가드레일 구현

### 📌 6. Mem0 장기 기억(Long-Term Memory) 프로필 및 개인화 엔진 (완료)
- [x] **Mem0 벡터 메모리 영속화 파이프라인**:
  - [x] `.agentsmith/` 디렉터리 내 SQLite/Mem0 장기 기억 컬렉션(`mem0_memory.db`) 연동
  - [x] 상단 `[🧠 기억]` 드로어를 통해 저장된 개발자 코딩 스타일, 프로젝트 가드레일 실시간 시각화 및 관리
- [x] **세션 간 지식 연속성 및 프롬프트 동적 주입**:
  - [x] 새 세션 시작 시 사용자 프로필 및 프로젝트 맥락을 시스템 프롬프트에 자동 주입하여 일관된 코드 생성 보장

### 📌 7. Graphify AST 지식 그래프 & 하이브리드 RAG (완료)
- [x] **다국어 정적 AST 파싱 엔진 탑재**:
  - [x] Python 소스코드 정적 AST 파서(Tree-sitter/Ast) 기반 Class, Function, Method 노드 및 Call Graph 엣지 추출기 탑재
- [x] **SQLite / NetworkX 기반 코드 지식 그래프 구축**:
  - [x] 상단 `[🕸️ 그래프]` 드로어를 통해 인덱싱된 파일/심볼/노드/엣지 통계 및 AST 심볼 목록 실시간 시각화
- [x] **컨텍스트 의존성 자동 역추적 및 하이브리드 RAG**:
  - [x] 사용자 질의 및 함수 수정 요청 시 하이브리드 AST RAG를 통해 관련 심볼을 자동 탐색하고 에이전트 프롬프트에 바인딩

### 📌 8. CortexOS & gstack 기본 내장 가드레일 및 유저 확장 체계 (완료)
- [x] **Built-in Core 가드레일 기본 내장**:
  - [x] AI 코드 주석/설명/로그 **한국어 강제 출력** 프롬프트 가드레일 바인딩
  - [x] 2바이트 다국어 보장을 위한 UTF-8 BOM-less 파일 생성/수정 강제화
  - [x] 작업 트라이어드([작업계획서]-[개발코드]-[상세명세서] 1:1:1 쌍) 및 날짜 명명 규칙(`YYYY-MM-DD_`) 자동 검사기
  - [x] 코드 작성 후 SAST 정적 보안 검사(시크릿/eval/SQLi) 및 `🛡️ SAST Security: PASSED` 뱃지 렌더링
- [x] **gstack 전문가 페르소나 및 워크플로우 기본 탑재**:
  - [x] `@pm`, `@sa`, `@se`, `@qa`, `@cso`, `@dba`, `@growth`, `@ceo` 내장 및 `@` 자동완성
  - [x] `/office-hours`, `/plan-ceo-review`, `/plan-eng-review`, `/review`, `/investigate`, `/qa`, `/ship` 등 10종 내장 및 `/` 자동완성
- [x] **유저 확장 플러그인 로더 (.agents/ Customization)**:
  - [x] `.agents/skills/` 및 `.agents/rules/*.md` 동적 감지 로더 구축
  - [x] 상단 `[🧩 gstack]` 드로어를 통한 전체 페르소나 및 워크플로우 1-Click 주입 UI 탑재

### 📌 9. AI 모델 및 API 키 연동 체계 (완료 및 현행화)
- [x] **.env 중앙 집중식 환경설정 구축**:
  - [x] `.env.example` 템플릿 기반 독립 작업공간 및 API Key 관리 체계 수립
- [x] **글로벌/로컬 AI 모델 Auto-Discovery & Health Detector**:
  - [x] `model_detector.py`를 통한 미국, 중국(Kimi, GLM), 한국, HuggingFace 및 로컬(Ollama, LM Studio, vLLM) 실시간 헬스체크 구현
- [x] **REST API를 통한 동적 API 키 등록**:
  - [x] `POST /api/openrouter/key` 및 `POST /api/provider/switch` 엔드포인트 구축
- [ ] **사이드바 내 직접 API 키 설정 모달 (Settings Modal) 추가 UI 고도화**:
  - [ ] 향후 편의성을 위해 사이드바 상단 톱니바퀴 아이콘을 통한 실시간 API Key 입력/저장 팝업 지원 예정

---

## 🎯 Phase 3: Red Hat / Linux / 온프레미스(RHOAI) 배포 호환성 (진행 예정)
- [ ] **리눅스용 빌드 쉘 스크립트 작성**:
  - [ ] [`build_agent_smith.sh`](file:///c:/dev/antigravity-workspace/agentsmith/build/build_agent_smith.sh) 쉘 스크립트 신규 구현 및 LF 개행 지정
  - [ ] [`inject_version.sh`](file:///c:/dev/antigravity-workspace/agentsmith/build/inject_version.sh) 버전 주입 쉘 스크립트 신규 구현 및 LF 개행 지정
- [ ] **WSL / Rocky Linux / AlmaLinux 크로스 플랫폼 검증**:
  - [ ] WSL 내 Rocky Linux 또는 AlmaLinux 환경에서 작성한 쉘 스크립트 가동 및 컴파일 호환성 최종 검증
- [ ] **온프레미스(RHOAI SNO) 연동 및 1-Click 포팅**:
  - [ ] OpenShift AI 단일 노드(Baremetal)상의 vLLM ServingRuntime API 자동 스캔 및 모델 엔드포인트 연동 테스트

---

## 🧪 Phase 4: 종합 E2E 테스트 및 최종 QA (진행 예정)
- [ ] **QA 서브에이전트 스킬(`/qa`) 및 Headless 브라우저 검증**:
  - [ ] IDE 내부 챗 패널(webview) UI, STT 음성 인식, 모델 전환, Multi-File Diff 및 AST 지식그래프 연동 무결성 최종 검증

---

## 💻 호스트 환경별 성공 검증 이력 (Environment Verification Matrix)

| 검증 일자 | 호스트 식별자 (Host / OS) | 도구 버전 (Python / Node / uv / Bun) | 검증 산출물 및 무결성 결과 | 비고 |
| :--- | :--- | :--- | :--- | :--- |
| **2026-08-20** | 이전 개발 PC (Workstation) | Python 3.11 / Node v20 / uv 0.10 / Bun 1.3 | 바이너리 빌드 문제점 8대 원인 해결, Phase 2 코어 완성 | 최초 핸드오버 작성 |
| **2026-08-21** | `MZC_SUNKIM317_L`<br>(Windows 11 x64, 10.0.26200) | Python 3.14.4 / Node v24.14.1<br>uv 0.11.19 / Bun 1.3.11 | - Git 3개 브랜치 동기화 (`feature`, `staging`, `main`)<br>- Syncthing 충돌 0건<br>- 백엔드 6대 모듈 100% PASS<br>- `AgentSmith_Desktop_Setup_v1.0.0.exe` (442.69MB)<br>- `agentsmith-desktop-v1.0.0.zip` (444.72MB) | **동기화 및 1-Click 빌드 성공 검증 완료** |
| **2026-08-23** | `HOME_SUNKIM`<br>(Windows 11 x64, 10.0.26200) | Python 3.11.15 / Node v24.14.1<br>uv 0.11.19 / Bun 1.3.11 | - Git 3개 브랜치 동기화 (`feature`, `staging`, `main`)<br>- `.env` 독립 환경설정 생성<br>- **사이드바 웹뷰 검은 화면(Black Screen) 영구 해결** (Zero-Dependency 로컬 렌더러 전환)<br>- 백엔드 6대 모듈 100% PASS<br>- `AgentSmith_Desktop_Setup_v1.0.0.exe` (442.71MB)<br>- `agentsmith-desktop-v1.0.0.zip` (444.74MB) | **현행화 및 웹뷰 렌더러 복원 완료** |

---

© 2026 AI Architecture Engineering Team. All rights reserved.
