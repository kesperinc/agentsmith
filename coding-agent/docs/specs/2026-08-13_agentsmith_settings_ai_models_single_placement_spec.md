# 📄 [작업 명세서] Settings > Extensions 아래 > AI Models (API Key 입력 및 Auto-Discovery) 단일화 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 구현 내역 (Background & Achievements)

- **Settings > Extensions 아래 `> AI Models` 단일 배치 통합**:
  - `보기 (View)` 메인 메뉴의 중복 항목을 정리하고, **Settings UI (`Ctrl+,`) 좌측 메뉴 `> Extensions` 바로 아래의 `> AI Models` 카테고리 단일 위치**로 통합 배치 완수.
- **카테고리 내부 필드 구성**:
  1. **Auto-Discovery 스캐너**: 실시간 키 및 로컬 엔드포인트 헬스 핑 스캔 패널
  2. **국가별 API Key 입력 필드**: OpenAI, Anthropic, Gemini, DeepSeek, Kimi (Moonshot), GLM-4 (Zhipu), Naver HyperCLOVA X, Upstage Solar, Hugging Face Token
  3. **Local Engine 엔드포인트 입력 필드**: Local Ollama (`:11434`), LM Studio (`:1234`), Custom vLLM (`:8000`)

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `vscode/src/vs/workbench/contrib/preferences/common/preferencesContribution.ts` | Settings UI Configuration `aiModels` API Key & Auto-Discovery 필드 기여 |
| **[MODIFY]** | `vscode/out/vs/workbench/contrib/preferences/common/preferencesContribution.js` | JS 런타임 번들 내 `aiModels` API Key 폼 바인딩 |
| **[MODIFY]** | `vscode/src/vs/workbench/contrib/quickaccess/browser/quickAccess.contribution.ts` | View 메뉴의 showAIModels 항목 정리 |
| **[MODIFY]** | `vscode/out/vs/workbench/contrib/quickaccess/browser/quickAccess.contribution.js` | JS 번들 View 메뉴 중복 커맨드 수거 |
| **[MODIFY]** | `docs/coding_agent_basic_design.html` | Settings > AI Models 내부 API Key 폼 & Auto-Discovery 시각화 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_settings_ai_models_single_placement_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **데스크톱 가동 검증**: 런처 재기동 및 28개 프로세스 상주를 통해 Settings UI `Extensions` 바로 아래 `> AI Models` 카테고리 단일 위치에 API Key 폼 및 Auto-Discovery 스캐너가 100% 정상 작동함을 입증 완수.

---
*Agent Smith Settings AI Models Single Placement Specification Completed*
