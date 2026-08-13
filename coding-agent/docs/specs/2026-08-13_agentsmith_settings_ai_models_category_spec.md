# 📄 [작업 명세서] Settings UI 좌측 Extensions 아래 > AI Models 카테고리 & 글로벌/HuggingFace 연동 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 구현 내역 (Background & Achievements)

- **Settings UI 트리 메뉴 `> AI Models` 배치**:
  - 사용자 지정 캡처 이미지 위치인 **`Extensions` 바로 아래**에 **`> AI Models`** 카테고리 트리 노드를 배치 완료.
- **국가별 (미국/중국/한국) & Hugging Face 모델 연동**:
  1. **미국 (USA)**: Anthropic Claude 3.5 Sonnet, OpenAI GPT-4o, Google Gemini 1.5 Pro
  2. **중국 (China)**: Qwen 2.5 Coder 32B, DeepSeek R1 Reasoning
  3. **한국 (Korea)**: Naver HyperCLOVA X, Upstage Solar Mini, LG EXAONE 3.0
  4. **Hugging Face**: Hugging Face Inference API (`HF_TOKEN`) 연동 스키마 추가

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `coding-agent/src/model_config.py` | 미국, 중국, 한국 및 HuggingFace 모델 단가 스키마 확장 |
| **[MODIFY]** | `coding-agent/src/model_detector.py` | 국가별 및 HuggingFace API Key 자동 탐지 엔진 구축 |
| **[MODIFY]** | `vscode/src/vs/workbench/contrib/preferences/common/preferencesContribution.ts` | Settings UI Configuration에 `aiModels` 카테고리 기여 |
| **[MODIFY]** | `vscode/out/vs/workbench/contrib/preferences/common/preferencesContribution.js` | JS 런타임 번들 내 `aiModels` 카테고리 기여 등록 |
| **[MODIFY]** | `docs/coding_agent_basic_design.html` | 사용자 캡처 위치(Extensions 아래 > AI Models) 반영 UI |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_settings_ai_models_category_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **글로벌 스캔 검증**: `python coding-agent/src/model_detector.py` 구동 시 7개 대표 모델(미국/중국/한국/HuggingFace)이 `[ONLINE]` / `[OFFLINE]` 상태와 함께 100% 정상 스캔됨을 입증.

---
*Agent Smith Settings AI Models Category Specification Completed*
