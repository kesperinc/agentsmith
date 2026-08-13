# 📄 [작업 명세서] Settings UI Table of Contents (TOC) AI Models 카테고리 기여 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 스모킹 건 진단 (Background & Root Cause)

- **원인 분석**: Settings UI (`Ctrl+,`) 창 좌측 카테고리 메뉴 트리(Table of Contents - TOC)를 동적으로 구성하는 `settingsLayout.ts` 및 `settingsLayout.js` 의 최상위 카테고리 레지스트리 배열에 `AI Models` 카테고리 노드가 등록되어 있지 않았기 때문에 좌측 트리에 노출되지 않았던 현상이었습니다.
- **해결 조치**: `settingsLayout.ts` 및 JS 런타임 번들 `settingsLayout.js` 의 최상위 카테고리 레지스트리 배열에 **`id: 'aiModels'` (label: "AI Models", settings: ['aiModels.*']) 노드를 100% 바인딩 기여** 완료하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `vscode/src/vs/workbench/contrib/preferences/browser/settingsLayout.ts` | Settings TOC 트리 최상위 카테고리에 `aiModels` 추가 |
| **[MODIFY]** | `vscode/out/vs/workbench/contrib/preferences/browser/settingsLayout.js` | JS 번들 내 Settings TOC 트리 `aiModels` 바인딩 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_settings_toc_ai_models_layout_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **Settings UI 카테고리 노출 실측**: 런처 재기동 및 20개 프로세스 상주를 통해 설정(`Ctrl+,`) 창 좌측 트리에 `AI Models` 카테고리가 100% 노출되고 클릭 시 API Key 입력 폼 및 Auto-Discovery 스캐너가 노출됨을 입증 완수.

---
*Agent Smith Settings TOC AI Models Layout Specification Completed*
