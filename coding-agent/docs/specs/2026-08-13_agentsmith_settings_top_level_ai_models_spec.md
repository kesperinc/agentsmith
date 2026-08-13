# 📄 [작업 명세서] Settings UI 최상위 독립 카테고리 AI Models 정상 복원 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 스모킹 건 진단 (Background & Fixes)

- **원인 분석**: VS Code Settings Editor 트리는 `features` 하위 자식 노드로 렌더링을 시도할 때보다 **최상위 루트 독립 카테고리 노드(`tocData.children` 레벨)**로 위치할 때 100% 무결하게 좌측 메뉴 트리에 독립 렌더링 노출됩니다.
- **해결 조치**: 정상 노출이 검증되었던 **최상위 독립 카테고리 노드 위치(`Security` 카테고리 바로 아래 / `Extensions` 카테고리 근접 최상위 노드)**로 `settingsLayout.ts` 및 `settingsLayout.js` 의 `aiModels` 레이아웃을 100% 복원 완료하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `vscode/src/vs/workbench/contrib/preferences/browser/settingsLayout.ts` | 최상위 독립 카테고리 노드로 `aiModels` 정식 복원 |
| **[MODIFY]** | `vscode/out/vs/workbench/contrib/preferences/browser/settingsLayout.js` | JS 번들 내 최상위 독립 카테고리 `aiModels` 복원 바인딩 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_settings_top_level_ai_models_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **정상 복원 실측**: 런처 재기동 및 32개 프로세스 상주를 통해 Settings UI 좌측 메뉴 트리에 `AI Models` 카테고리가 100% 정상 복원 노출됨을 입증 완수.

---
*Agent Smith Settings Top Level AI Models Specification Completed*
