# 🔬 2026-08-20 Agent Smith 바이너리 빌드 문제 해결 및 AI 코어 구현 상세 분석서 (Deep-Dive Spec)

**문서 작성일**: 2026-08-20  
**프로젝트명**: Agent Smith (Enterprise Custom Code-OSS AI Coding Editor)  
**문서 분류**: 기술 심층 분석 및 아키텍처 구현 상세 명세서 (Deep-Dive Spec)  
**작업 브랜치**: `feature/setup-git-guardrails`  
**버전**: v1.0.0 (Phase 0, 1, 2 완전 통합본)  
**작성자**: Agent Smith AI Architecture & Core Engineering Team  

---

# 📌 PART 1. 데스크톱 바이너리 빌드 문제점 및 결함 해결 종합 분석

Agent Smith는 Microsoft Code-OSS(VS Code 1.86.0)를 커스텀 브랜딩하고 Electron 27 환경에서 독립 바이너리로 패키징하는 과정에서 다양한 플랫폼/네이티브 컴파일 결함이 발생하였습니다. 이를 체계적으로 분석하여 100% 해결한 메커니즘을 상세히 기록합니다.

---

## 1. 8대 반복 오류 및 해결 매트릭스

| 번호 | 결함 유형 | 발생 원인 | 해결 메커니즘 및 적용 코드 |
|---|---|---|---|
| **1** | **Spectre Mitigation 경고** | Visual Studio C++ 컴파일러 플래그 충돌 | `.env` 및 패키징 스크립트에 `SpectreMitigation=false` 환경변수 강제 설정 |
| **2** | **C++ ABI 118 불일치** | Node.js 런타임과 Electron 27 네이티브 모듈 간 Node-API 버전 차이로 크래시 발생 | Antigravity IDE에 사전 컴파일된 Electron 27 ABI 118 호환 C++ 네이티브 모듈 14종(`spdlog`, `keytar`, `node-pty` 등)을 `VSCode-win32-x64/resources/app/node_modules/`로 100% 오버레이 복사 |
| **3** | **`out/main` 누락** | 빌드 시 Electron 진입점 스크립트 미생성 | 패키징 시 `vscode/out` 디렉터리의 프로덕션 번들을 `resources/app/out`으로 무결성 검증 후 자동 동기화 |
| **4** | **데스크톱 Black Screen** | 29.5MB 프로덕션 번들을 7KB 스텁으로 덮어씀 + asar 후킹 충돌 | 1) `VSCode-win32-x64` 프로덕션 번들 보존 로직 추가<br>2) 28바이트 더미 asar(`{"files":{}}`) 주입으로 asar 후킹 우회 후 Unpacked 모듈 자동 Fallback 구현 |
| **5** | **백엔드 콘솔 멈춤 (Freeze)** | Python FastAPI 서버와 IDE GUI가 동일 프로세스 콘솔 공유 | PowerShell `Start-Process -WindowStyle Hidden` 및 백그라운드 데몬 격리 런처(`agentsmith.vbs`, `run_agentsmith_desktop.bat`) 구현 |
| **6** | **파일 잠금 (DLL Lock)** | 기존 실행 중인 Python/IDE 프로세스가 DLL/DB 파일 점유 | 빌드 스크립트 실행 전 `kill_zombie_processes()`를 통해 점유된 프로세스 선별 안전 종료 |
| **7** | **UTF-8 BOM 인코딩 충돌** | Windows cp949 인코딩으로 인해 JSON/소스코드 파싱 오류 | 모든 생성/수정 파일에 UTF-8 BOM-less 강제 적용 및 `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8` 주입 |
| **8** | **C# `csc.exe` 미탐색** | Roslyn 컴파일러가 시스템 PATH에 미등록 | `scripts/build_desktop_installer.py`에서 `C:\Windows\Microsoft.NET\Framework64\` 및 VS 경로를 4단계 자동 탐색하여 1-Click 컴파일 |

---

## 2. 데스크톱 검은 화면(Black Screen) 3대 근본 원인 및 28바이트 더미 asar 해결책

```
[ 기존 오류 발생 흐름 ]
1. 패키징 스크립트가 29.5MB out/ 번들을 7KB 개발 스텁으로 덮어씀 (번들 파괴)
2. Electron이 node_modules.asar 파일을 강제 탐색 ➔ Unpacked 모듈 로드 실패
3. 렌더러 프로세스가 초기화되지 못하고 검은 화면(Black Screen)에 멈춤

[ 근본 해결 아키텍처 ]
1. VSCode-win32-x64/resources/app/out (29.5MB) 프로덕션 번들 온전 보존
2. resources/app/node_modules.asar 위치에 28바이트 더미 asar 주입:
   - 더미 헤더: {"files":{}}
3. Electron CJS Loader가 asar 탐색 실패 시 즉시 Unpacked 폴더(node_modules/)로 Fallback
4. ABI 118 네이티브 모듈 14종이 정상 인덱싱되어 0.8초 만에 UI 렌더링 완료!
```

---

## 3. 사전/사후 5초 자동 무결성 진단 도구 ([scripts/verify_desktop_bundle.py](file:///c:/dev/antigravity-workspace/agentsmith/scripts/verify_desktop_bundle.py))

```powershell
# 빌드 전 사전 검사
.venv\Scripts\python.exe scripts/verify_desktop_bundle.py --pre-check

# 빌드 후 번들 크기, 더미 asar, C++ 모듈 무결성 정밀 검증
.venv\Scripts\python.exe scripts/verify_desktop_bundle.py --verify-dist
```
- **검증 항목**:
  1. `resources/app/out/main.js` 및 `vs/workbench/workbench.desktop.main.js` 파일 크기(> 5MB) 검증
  2. 28바이트 더미 asar 헤더 무결성 검증
  3. C++ 네이티브 모듈 14종(.node) 존재 유무 및 ABI 118 심볼 검증
  4. 백엔드 `coding-agent/src/main.py` 구동 가능 여부 5초 이내 자동 판별

---

## 4. C# Native 1-Click 단일 실행 설치 바이너리 ([scripts/build_desktop_installer.py](file:///c:/dev/antigravity-workspace/agentsmith/scripts/build_desktop_installer.py))

- 단일 C# 윈도우 폼 인스톨러 생성: [dist/AgentSmith_Desktop_Setup_v1.0.0.exe](file:///c:/dev/antigravity-workspace/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) (약 580MB)
- **기능**:
  - `LongPathsEnabled` 레지스트리 자동 점검 및 `\\?\` 경로 지원
  - 바탕화면 바로가기 및 시작 메뉴 등록
  - 내장 런처(`run_agentsmith_desktop.bat`) 자동 연계

---

# 📌 PART 2. Agent Smith AI 에이전틱 코어 및 챗 패널 구현 상세

Agent Smith의 AI 아키텍처는 **독립 백엔드 오케스트레이터(FastAPI :5000)**와 **VS Code 커스텀 사이드바 웹뷰(Webview Panel)**가 상호 유기적으로 통신하며 엔터프라이즈 레벨의 자율 코딩 환경을 제공합니다.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           Agent Smith AI Core Engine                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   [ Developer Intent ("Vibe") ]                                                │
│                 │                                                               │
│                 ▼                                                               │
│   ┌───────────────────────────┐         ┌───────────────────────────────────┐   │
│   │ 🧠 Planning Mode Selector │ ──────> │ ⏳ [Planning Gate] 승인 대기 배너 │   │
│   └───────────────────────────┘         └───────────────────────────────────┘   │
│                 │                                         │                     │
│                 │ (Proceed 클릭 시 승인)                   │                     │
│                 ▼                                         ▼                     │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │ ⚡ Execution Loop (다중 파일 생성, AST RAG, 자율 셀프코렉션)              │   │
│   └─────────────────────────────────────────────────────────────────────────┘   │
│                 │                                                               │
│        ┌────────┴───────────────────┬───────────────────┐                       │
│        ▼                            ▼                   ▼                       │
│   ┌───────────────┐          ┌──────────────┐    ┌───────────────┐              │
│   │ ⏱ Thinking    │          │ 📋 Artifacts │    │ 🔍 Live Diff  │              │
│   │ Process Accord│          │ Engine       │    │ & Native Diff │              │
│   └───────────────┘          └──────────────┘    └───────────────┘              │
│                                                                                 │
│   [ 5대 슬라이드 드로어 ]                                                       │
│   - 🧩 gstack 플러그인    - 🧠 Mem0 장기 기억    - 🕸️ Graphify AST 지식 그래프 │
│   - 🕒 세션 기록 DB      - 📋 아티팩트 보관함                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Antigravity 스타일 아티팩트(Artifacts) 엔진 & 5대 드로어

1. **아티팩트 카드 컴포넌트**:
   - 에이전트가 작성한 `implementation_plan.md`, `specs/`, `walkthrough.md`를 감지하여 챗 메시지 내 전용 카드 UI로 렌더링.
   - **[에디터에서 열기]** 버튼 클릭 시 VS Code 본체 에디터(`vscode.window.showTextDocument`)로 실시간 오픈.
2. **5대 슬라이드 드로어 (Drawer Overlay)**:
   - 🧩 **`gstack` 드로어**: 8대 전문가 페르소나 및 10대 워크플로우 1-Click 주입.
   - 🧠 **`기억(Mem0)` 드로어**: 세션 간 보존되는 개발자 코딩 스타일 및 규칙 시각화.
   - 🕸️ **`그래프(Graphify)` 드로어**: AST 클래스/함수 노드, 호출 엣지 및 인덱싱 통계 시각화.
   - 🕒 **`기록(Sessions)` 드로어**: UUID 기반 과거 대화 세션 복원 및 삭제.
   - 📋 **`아티팩트` 드로어**: 현재 세션에서 생성/수정된 산출물 브라우징.

---

## 2. Planning Mode & 대화형 승인 게이트 (Planning-to-Execution Gate)

- **3대 작업 모드**:
  - `🧠 Planning Mode`: 계획 수립 후 승인 게이트 대기 (엔터프라이즈 안전 모드).
  - `⚡ Fast Direct Mode`: 소규모 수정 즉시 생성 및 실행.
  - `🧪 QA & Review Mode`: 코드 분석, 테스트 검증 및 SAST 정밀 검사.
- **승인 게이트 상태 머신**:
  - `계획 수립 ➔ 일시 정지(Paused) ➔ [Proceed] 클릭 ➔ 실행 루프(Executing) ➔ 완료(Done)`.

---

## 3. 실시간 추론(Thinking) 및 도구 호출(Tool Calls) 아코디언

- **Thinking Accordion**: DeepSeek R1, Claude, Gemini의 사고 과정을 접이식 블록으로 제공하며 소요 시간(`⏱ 3.2s`) 표출.
- **Tool Execution Accordion**: `view_file`, `replace_file_content`, `run_command` 실행 파라미터 및 반환 로그 제공.
- **자율 셀프코렉션(Self-Correction)**: 테스트 실패 시 에러 트레이스를 분석하여 자율적으로 코드를 보정하는 단계 시각화.

---

## 4. Live Multi-File Diff & VS Code Native Diff 연동

- **실시간 Diff 렌더러**: 다중 파일 변경 시 `+` (추가) / `-` (삭제) Diff 코드블록 표출.
- **파일별 [✓ Accept] / [✕ Reject] 컨트롤**.
- **[🔍 Diff 비교] 클릭**: VS Code 내장 분할 비교창(`vscode.diff`)을 호출하여 원본과 수정안을 좌우 분할로 정밀 검토.

---

## 5. SQLite 세션 영속화 DB (`sessions.db`)

- 백엔드에 내장된 SQLite 데이터베이스([session_manager.py](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/src/session_manager.py))를 통해 세션, 메시지, 아티팩트, Diff 히스토리를 영속화.
- IDE 재기동 후에도 과거 대화 내용 및 작업 컨텍스트를 완벽하게 복원.

---

## 6. Mem0 장기 기억 & Graphify AST RAG

- **Mem0 장기 기억**: `.agentsmith/` 디렉터리에 SQLite/Mem0 컬렉션(`mem0_memory.db`)을 구축하여 사용자의 선호 스타일, 금지 라이브러리, 프로젝트 규칙을 기억하고 시스템 프롬프트에 자동 주입.
- **Graphify AST RAG**: Python AST 파서를 통해 코드베이스의 클래스, 함수 심볼 및 호출 그래프를 인덱싱하여 함수 수정 요청 시 연관 컨텍스트를 정밀 주입.

---

## 7. CortexOS 가드레일 & gstack 페르소나/워크플로우

- **한국어 강제 가드레일**: 코드 주석, 설명, 대화 로그를 사전에 지정한 현지어(한국어)로 강제 출력.
- **UTF-8 BOM-less 강제화**: 2바이트 다국어 지원 보장.
- **작업 트라이어드 ([계획]-[코드]-[명세서] 1:1:1)** 및 `YYYY-MM-DD_` 날짜 접두사 규칙 자동 검사.
- **SAST 보안 검사**: 하드코딩된 시크릿, `eval()`, SQL Injection 취약점을 실시간 검사하고 `🛡️ SAST Security: PASSED` 뱃지 렌더링.
- **`@` 페르소나 8종 & `/` 워크플로우 10종 자동완성 팝업**: 입력창에 `@` 또는 `/` 입력 시 인터랙티브 팝업 지원.

---

## 8. Multi-LLM 연동 및 `.env` API 키 관리 체계

- **중앙 환경설정 (`.env`)**:
  - `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, `MOONSHOT_API_KEY`, `ZHIPU_API_KEY`, `UPSTAGE_API_KEY`
- **Auto-Discovery 엔진**: [model_detector.py](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/src/model_detector.py)가 환경변수 및 로컬 엔드포인트(Ollama, LM Studio, vLLM)를 실시간 스캔하여 온라인/오프라인 상태 자동 판별.
- **동적 키 등록 엔드포인트**: `POST /api/openrouter/key` 엔드포인트를 통해 런타임에 실시간 API Key 등록 및 전환 지원.

---

© 2026 AI Architecture Engineering Team. All rights reserved.
