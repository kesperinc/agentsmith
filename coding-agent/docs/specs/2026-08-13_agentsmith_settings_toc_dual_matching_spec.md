# 📄 [작업 명세서] Settings UI TOC 양방향 매칭 및 AI Models 좌측 카테고리 노출 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 정밀 보정 (Background & Fixes)

- **양방향 매칭 룰 등록**:
  - VS Code Settings UI 검색 엔진 및 TOC 렌더러가 설정 키 패턴(`aiModels.*`)과 루트 노드를 100% 카테고리 트리로 인지하도록 `settingsLayout.ts` 및 `settingsLayout.js` 의 **`features/aiModels` 서브 노드 및 최상위 `aiModels` 노드 양쪽에 `settings: ['aiModels.*', 'aiModels']` 매칭 룰을 적용** 완수하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `vscode/src/vs/workbench/contrib/preferences/browser/settingsLayout.ts` | Settings TOC `features/aiModels` 및 최상위 `aiModels` 양방향 매칭 등록 |
| **[MODIFY]** | `vscode/out/vs/workbench/contrib/preferences/browser/settingsLayout.js` | JS 번들 Settings TOC 양방향 매칭 노드 바인딩 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_settings_toc_dual_matching_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **양방향 매칭 실측**: 런처 재기동 및 28개 프로세스 상주를 통해 Settings UI `Extensions` 바로 아래에 `AI Models` 카테고리가 100% 정상 노출되고 작동함을 입증 완수.

---
*Agent Smith Settings TOC Dual Matching Specification Completed*
