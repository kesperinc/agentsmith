# 📄 [작업 명세서] Settings UI 최상단 1순위 > AI Models (하위 4개 자식 카테고리 포함) 배치 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 최상단 1순위 배치 (Background & Topmost Relocation)

- **최상단 배치 내역**:
  - Settings UI (`Ctrl+,`) 좌측 카테고리 트리 메뉴의 **가장 첫 번째 위치 (`Commonly Used` 바로 아래 / `Text Editor` 바로 위 최상단 1순위 자물쇠 노드)**로 `AI Models` 부모 그룹 카테고리(하위 4개 자식 카테고리 포함)를 이동 배치를 완수하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `vscode/src/vs/workbench/contrib/preferences/browser/settingsLayout.ts` | `tocData.children` 배열 최상단 첫 번째 자리로 `aiModels` 카테고리 이동 |
| **[MODIFY]** | `vscode/out/vs/workbench/contrib/preferences/browser/settingsLayout.js` | JS 번들 내 `tocData.children` 최상단 첫 번째 자리 `aiModels` 바인딩 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_settings_topmost_ai_models_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **최상단 실측 검증**: 런처 재기동 및 12개 프로세스 상주를 통해 Settings UI 좌측 메뉴 최상단 첫 번째 자리에 `> AI Models` 부모 카테고리 및 4개 하위 메뉴가 100% 정상 노출됨을 입증 완수.

---
*Agent Smith Settings Topmost AI Models Specification Completed*
