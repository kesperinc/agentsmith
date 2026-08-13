# 📄 [작업 명세서] Kimi, GLM-4 및 Local Engine (Ollama/LM Studio/vLLM) 연동 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 구현 내역 (Background & Achievements)

- **중국 신규 LLM 추가**:
  - **Moonshot Kimi Chat 128k**: `MOONSHOT_API_KEY` / `KIMI_API_KEY` 바인딩 (`https://api.moonshot.cn/v1`)
  - **Zhipu GLM-4 / GLM-4 Flash**: `ZHIPU_API_KEY` / `GLM_API_KEY` 바인딩 (`https://open.bigmodel.cn/api/paas/v4`)
- **Local Engine 연동 및 자동 헬스 스캔 파이프라인**:
  - **Local Ollama**: `http://localhost:11434` 실시간 헬스 핑 스캔
  - **Local LM Studio**: `http://localhost:1234/v1` 실시간 헬스 핑 스캔
  - **Local Custom vLLM**: `http://localhost:8000/v1` 온프레미스 GPU 스캔

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `coding-agent/src/model_config.py` | Kimi, GLM-4 및 Local Ollama/LM Studio 스키마 작성 |
| **[MODIFY]** | `coding-agent/src/model_detector.py` | Kimi, GLM-4 API Key 스캔 및 Local Ollama/LM Studio 헬스 핑 스캔 |
| **[MODIFY]** | `docs/coding_agent_basic_design.html` | Kimi, GLM-4 및 Local Engine 카드 반영 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_settings_kimi_glm_local_models_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **스캔 실측 입증**: `python coding-agent/src/model_detector.py` 실행 시 Kimi, GLM-4 및 Local Ollama/LM Studio 서버의 `[ONLINE]` / `[OFFLINE]` 생존 상태가 100% 자동 스캔되어 나열됨을 입증 완수.

---
*Agent Smith Kimi, GLM & Local Models Specification Completed*
