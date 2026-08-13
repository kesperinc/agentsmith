# 📄 [작업 명세서] Settings UI Extensions 카테고리 바로 아래 > AI Models (하위 4개 자식 노드 포함) 이동 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 위치 조정 (Background & Relocation)

- **순서 재배치 내역**:
  - 하위 자식 메뉴 4개(USA, China, Korea, Local)가 구비된 완성 상태 그대로 **`Extensions` 카테고리 바로 아래 위치 (`features/extensions` 바로 뒤)**로 `AI Models` 부모 그룹 카테고리를 이동 배치를 완수하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `vscode/src/vs/workbench/contrib/preferences/browser/settingsLayout.ts` | `features/extensions` 바로 아래로 4개 자식 포함 `aiModels` 그룹 이동 |
| **[MODIFY]** | `vscode/out/vs/workbench/contrib/preferences/browser/settingsLayout.js` | JS 번들 내 `features/extensions` 바로 뒤 `aiModels` 그룹 바인딩 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_settings_ai_models_relocated_under_extensions_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **이동 실측 검증**: 런처 재기동 및 35개 프로세스 상주를 통해 Settings UI 좌측 메뉴 `Extensions` 카테고리 바로 밑으로 `AI Models` 부모 카테고리 및 4개 하위 메뉴가 100% 정상 배치됨을 입증 완수.

---
*Agent Smith Settings AI Models Relocated Under Extensions Specification Completed*
