# 📘 [인수인계 문서] Agent Smith IDE AI Models & Cost Dashboard 통합 핸드오버 보고서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **저장 위치**: `docs/2026-08-13_agentsmith_comprehensive_handover_report.md`
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 (Executive Summary)

본 문서는 2026년 8월 13일 수행된 **Agent Smith 데스크톱 플랫폼 내 AI 모델 설정(AI Models), 전 세계/오픈소스/로컬 엔드포인트 연동, 실시간 Auto-Discovery 헬스 탐지기, 토큰 & 비용 대시보드(Token & Cost Analytics Dashboard)** 구현 및 UI/UX 정밀 배치에 관한 종합 핸드오버 문서입니다.

특히, 추후 작업 시 **"설정 화면에서 카테고리가 보이지 않는 문제"가 재발하지 않도록 VS Code Settings UI 렌더링 엔진 특성과 해결 지침**을 명확히 기록합니다.

---

## 2. 오늘 완성된 주요 구현 내역 (Completed Features)

### 2.1. 토큰 사용량 & 비용 모니터링 대시보드 (View 메뉴)
- **위치**: 메인 메뉴 바 **`보기 (View)` ➔ `Token & Cost Analytics Dashboard`**
- **기능**:
  - Prompt/Completion 토큰 실시간 카운팅
  - USD 및 KRW 비용 자동 환산 (환율: 1,380 KRW/USD)
  - 10개 모델별 비용 모니터링 시각화

### 2.2. AI Models 설정 카테고리 & API Key 입력 매니저 (Settings UI 최상단)
- **위치**: 설정 창(`Ctrl+,`) 좌측 트리 메뉴 **가장 맨 위 첫 번째 자물쇠 위치 (`Commonly Used` 바로 아래 / `Text Editor` 바로 위 최상단 1순위!)**
- **구조 (하위 자식 메뉴 4개)**:
  - **`▼ AI Models`** (최상단 1순위 부모 그룹 카테고리)
    - 🇺🇸 **`USA Models`**: OpenAI (GPT-4o), Anthropic (Claude 3.5), Google Gemini, OpenRouter
    - 🇨🇳 **`China Models`**: DeepSeek (R1/V3), **Moonshot Kimi**, **Zhipu GLM-4**
    - 🇰🇷 **`Korea & OpenSource`**: Naver HyperCLOVA X, Upstage Solar, Hugging Face Token (`HF_TOKEN`)
    - 🖥️ **`Local & On-Premise`**: Local Ollama (`:11434`), LM Studio (`:1234`), Custom vLLM (`:8000`)
- **실시간 Auto-Discovery 탐지기**: API Key 유효성 및 로컬 HTTP 핑 스캔으로 `[ONLINE - Ready]` / `[OFFLINE - Key Needed]` 실시간 상태 렌더링

---

## 3. 🔥 [핵심] 화면 미노출 방지 및 기술 핸드오버 지침 (Preventing UI Missing Issues)

오늘 작업 중 발생했던 **"설정 카테고리가 보이지 않던 문제"**의 2가지 핵심 기술적 원인과 해결 지침입니다.

### 3.1. 원인 1: Electron JS 번들 파일 (`vscode/out/...`) 미갱신 문제
- **문제 현상**: TS 파일(`vscode/src/...`)만 수정하고 데스크톱 애플리케이션을 구동하면 변경 내용이 적용되지 않음.
- **기술적 이유**: Electron 런더러(`Code - OSS.exe`)는 컴파일된 JS 번들 파일(`vscode/out/...`)을 직접 실행하기 때문입니다.
- **해결 지침**: TS 소스 수정 시 **동일한 위치의 JS 번들 파일(`vscode/out/vs/workbench/contrib/preferences/browser/settingsLayout.js` 등)**에 1:1로 동일하게 수정을 적용하거나 컴파일을 거쳐야 합니다.

### 3.2. 원인 2: VS Code Settings TOC 렌더러의 동적 `Extensions` 생성 매커니즘
- **문제 현상**: `AI Models` 카테고리를 `Extensions` 아래로 이동시키면 화면에서 사라지는 문제.
- **기술적 이유**:
  1. VS Code Settings UI 좌측 메뉴의 `Extensions` 카테고리는 정적 메뉴가 아니라 런타임에 설치된 확장 기능들을 비동기로 긁어모아 맨 마지막에 생성하는 **동적 합성 노드(Dynamic Synthetic Node)**입니다.
  2. VS Code 엔진은 정적 카테고리들(`Text Editor`, `Workbench`, `Window` 등)을 먼저 그려낸 후 맨 마지막에 동적으로 `Extensions` 트리를 부착합니다.
  3. 또한, `children` 배열(하위 자식 메뉴 목록)이 없는 노드는 독립 부모 그룹 카테고리로 트리 상에 그려지지 않습니다.
- **해결 지침**:
  - `AI Models` 카테고리는 **하위 4개 자식 카테고리(`children`)를 포함하는 정식 부모 카테고리 노드**로 구성해야 함.
  - 최상단 첫 번째 위치인 **`tocData.children` 맨 앞(`editor` 위)**에 배치하여 렌더링 엔진이 100% 최우선 노드로 그려내도록 강제함.

---

## 4. 변경된 파일 명세서 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[CODE]** | `coding-agent/src/cost_tracker.py` | 토큰 및 비용 계산기 엔진 |
| **[CODE]** | `coding-agent/src/model_detector.py` | 실시간 Auto-Discovery 헬스 탐지기 모듈 |
| **[CODE]** | `coding-agent/src/model_config.py` | 전 세계/로컬 11개 모델 스키마 |
| **[CODE]** | `vscode/package.json` | `contributes.configuration` AI Models 기여 스키마 |
| **[CODE]** | `vscode/src/vs/workbench/contrib/preferences/browser/settingsLayout.ts` | Settings TOC 최상단 1순위 AI Models 노드 배치 |
| **[CODE]** | `vscode/out/vs/workbench/contrib/preferences/browser/settingsLayout.js` | JS 번들 Settings TOC 최상단 AI Models 배치 |
| **[CODE]** | `vscode/src/vs/workbench/contrib/quickaccess/browser/quickAccess.contribution.ts` | View 메뉴 Token Dashboard 기여 |
| **[SPEC]** | `coding-agent/docs/specs/2026-08-13_agentsmith_settings_topmost_ai_models_spec.md` | 최상단 AI Models 배치 명세서 |
| **[SPEC]** | `coding-agent/docs/specs/2026-08-13_agentsmith_settings_dynamic_extensions_analysis_spec.md` | 동적 Extensions 분석 명세서 |
| **[DOC]** | `docs/2026-08-13_agentsmith_comprehensive_handover_report.md` | 본 핸드오버 보고서 |

---

## 5. 실행 및 가동 확인 방법 (How to Run & Verify)

1. **데스크톱 애플리케이션 실행**:
   ```cmd
   run_agent_smith.bat
   ```
2. **AI Models 설정 확인**:
   - 데스크톱 창에서 `Ctrl+,` (설정) 키를 입력합니다.
   - 좌측 메뉴 맨 첫 번째에 있는 **`▼ AI Models`**를 확인하고 화살표를 열어 4개 세부 국가/엔진별 API Key 입력 및 Auto-Discovery 패널을 이용합니다.
3. **토큰 대시보드 확인**:
   - 상단 메뉴 바 `보기 (View)` ➔ `Token & Cost Analytics Dashboard` 클릭.

---
*Agent Smith Comprehensive Handover Report Completed*
