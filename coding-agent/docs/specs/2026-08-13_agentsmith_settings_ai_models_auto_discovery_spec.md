# 📄 [작업 명세서] Settings -> AI Models 연동 및 사용 가능 모델 자동 탐지(Auto-Discovery) 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 구현 성과 (Background & Accomplishments)

- **`Settings ➔ AI Models` 카테고리 구성**:
  - 설정(Preferences / Settings) 내 `AI Models` 카테고리를 배치하여 프로바이더별 API Key 및 엔드포인트 세팅 구조 수립.
- **실시간 모델 자동 탐지(Auto-Detector) 엔진**:
  - API Key 유효성 및 네트워크 엔드포인트 헬스 핑 스캔을 통해 사용 가능한 모델을 `ONLINE (Ready)` / `OFFLINE (Key Needed)` 상태 및 안내 메시지와 함께 실시간 자동 나열.
- **설계서 HTML 연동**:
  - [`docs/coding_agent_basic_design.html`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/coding_agent_basic_design.html) 내 **[Section 5: 설정(Settings) ➔ AI Models 연동 및 사용 가능 모델 자동 체크]** 시각화 반영 완료.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[NEW]** | `coding-agent/src/model_detector.py` | AI Models 자동 탐지(Auto-Detector) 코어 모듈 |
| **[MODIFY]** | `docs/coding_agent_basic_design.html` | Settings -> AI Models 연동 및 자동 체크 대시보드 반영 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_settings_ai_models_auto_discovery_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **model_detector.py 실측 검증**: `python coding-agent/src/model_detector.py` 구동 시 `Qwen 2.5 Coder 32B`, `DeepSeek R1` `[ONLINE]` 포착 및 `Claude 3.5`, `GPT-4o` `[OFFLINE]` 리포트 자동 생성 입증 완수.

---
*Agent Smith AI Models Auto-Discovery Specification Completed*
