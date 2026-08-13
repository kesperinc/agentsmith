# 📄 [작업 명세서] [보기(View)] 메뉴 내 토큰 & 비용 모니터링 대시보드 배치 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 배치 성과 (Background & Achievements)

- **[보기(View)] 메뉴 항목 바인딩**:
  - 에디터 상단 메인 메뉴바의 **`보기 (View)`** 메뉴 아래에 **`📊 토큰 & 비용 모니터링 대시보드 (Token & Cost Analytics Dashboard)`** 메뉴 항목(`workbench.action.showCostAnalytics`)을 100% 배치 기여 완료.
- **설계서 뷰 정돈**:
  - [`docs/coding_agent_basic_design.html`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/coding_agent_basic_design.html) 내 **[Section 5: 보기(View) 메뉴 ➔ 토큰 & 비용 모니터링 대시보드]** 시각화 렌더링을 재배치 정돈 완료.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `vscode/src/vs/workbench/contrib/quickaccess/browser/quickAccess.contribution.ts` | `MenubarViewMenu` 상에 모니터링 대시보드 메뉴 항목 바인딩 |
| **[MODIFY]** | `docs/coding_agent_basic_design.html` | [보기(View)] 메뉴 기준 모니터링 대시보드 카드 재배치 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_view_menu_cost_analytics_placement_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **메뉴 기여 검증**: IDE 상단 `보기 (View)` 메뉴 아래 `Token & Cost Analytics Dashboard` 항목이 정상 등록되었음을 검증 완수.

---
*Agent Smith View Menu Cost Analytics Placement Specification Completed*
