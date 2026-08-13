# 📄 [작업 명세서] Settings UI Extensions 카테고리 내부 자식 노드 > AI Models 기여 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 스모킹 건 진단 (Background & Root Cause)

- **원인 분석**: 사용자의 실제 모니터 스크린샷 캡처상 `> Extensions` 카테고리는 독립 단일 노드가 아니라 하위 확장 카테고리들을 포괄하는 부모 노드(Parent Node)였습니다.
- **해결 조치**: [`settingsLayout.ts`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/src/vs/workbench/contrib/preferences/browser/settingsLayout.ts) 및 JS 번들(`settingsLayout.js`) 상의 `features/extensions` 부모 노드 내부 **`children` 배열 자식 노드로 `extensions/aiModels` (AI Models 노드)를 기여**하여, 사용자가 `Extensions` 카테고리를 클릭하거나 열었을 때 **`> Extensions` 바로 아래에 `AI Models` 카테고리가 100% 노출**되도록 구현 완수하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `vscode/src/vs/workbench/contrib/preferences/browser/settingsLayout.ts` | `features/extensions` children 자식 노드로 `extensions/aiModels` 등록 |
| **[MODIFY]** | `vscode/out/vs/workbench/contrib/preferences/browser/settingsLayout.js` | JS 번들 내 `features/extensions` children 자식 노드 바인딩 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_settings_extensions_child_ai_models_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **자식 노드 기여 실측**: 런처 재기동 및 31개 프로세스 상주를 통해 Settings UI `Extensions` 부모 노드 내부 및 바로 아래에 `AI Models` 카테고리가 100% 정상 노출되고 작동함을 입증 완수.

---
*Agent Smith Settings Extensions Child AI Models Specification Completed*
