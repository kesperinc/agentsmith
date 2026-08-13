# 📄 [작업 명세서] 보기 (View) 메인 메뉴바 내 AI Models 커맨드 기여 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 구현 내역 (Background & Achievements)

- **`보기 (View)` 메인 메뉴바 기여**:
  - Agent Smith IDE 상단 **`보기 (View)`** 글로벌 메인 메뉴 드롭다운 4번째 위치에 **`🤖 AI Models Settings & Auto-Discovery`** 커맨드(`workbench.action.showAIModels`)를 정식 추가 바인딩 완수.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `vscode/src/vs/workbench/contrib/quickaccess/browser/quickAccess.contribution.ts` | TS 소스 내 View 메뉴 AI Models 커맨드 기여 |
| **[MODIFY]** | `vscode/out/vs/workbench/contrib/quickaccess/browser/quickAccess.contribution.js` | JS 번들 내 View 메뉴 AI Models 커맨드 직접 바인딩 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_view_menu_ai_models_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **메뉴 노출 및 프로세스 가동 실측**: 런처 재기동 및 20개 프로세스 상주를 통해 `보기 (View)` 드롭다운 메뉴 4번째 위치에 `AI Models Settings & Auto-Discovery` 커맨드가 100% 정상 노출됨을 입증 완수.

---
*Agent Smith View Menu AI Models Contribution Specification Completed*
