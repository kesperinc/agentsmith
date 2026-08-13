# 📄 [작업 명세서] 모델 설정 탭 및 다중 모델 토큰/비용 모니터링 모듈 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 구현 성과 (Background & Accomplishments)

- **모델 설정 탭 & 프로바이더 스키마 구현**:
  - `claude-3-5-sonnet`, `gpt-4o`, `qwen-2.5-coder-32b`, `deepseek-r1`, `local-vllm-qwen` 모델 프로바이더 및 1M 토큰 당 입력/출력 단가 테이블 수립.
- **실시간 토큰 및 USD/KRW 비용 트래킹 코어 모듈**:
  - 모델별 프롬프트/완결 토큰 누적 카운팅 및 실시간 예상 사용 비용($ USD / ₩ KRW) 자동 계산 및 통계 리포팅 구현.
- **설계서 HTML 뷰 반영**:
  - `docs/coding_agent_basic_design.html` 에 **[Section 5: 모델 설정 탭 & 다중 모델 토큰/비용 모니터링 카드]** 컴포넌트 시각화 렌더링 반영 완료.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[NEW]** | `coding-agent/src/model_config.py` | 지원 모델 디렉토리 및 단가 스키마 모듈 |
| **[NEW]** | `coding-agent/src/cost_tracker.py` | 실시간 토큰 카운터 및 USD/KRW 비용 산출 엔진 |
| **[MODIFY]** | `docs/coding_agent_basic_design.html` | 모델 설정 탭 & 토큰/비용 모니터링 카드 추가 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_model_settings_and_cost_tracker_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **cost_tracker.py 실측 연산 검증**: `python coding-agent/src/cost_tracker.py` 실행 시 5개 다중 모델의 2,595,000 토큰 누적 연산 ➔ `$1.9401 (₩2,677 KRW)` 실시간 정확 산출 및 CLI 보고서 출력 확인 완료.

---
*Agent Smith Model Settings & Cost Tracker Specification Completed*
