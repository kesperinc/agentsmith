# 📄 [작업 명세서] out/ 번들 quickAccess.contribution.js View 메뉴 연동 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 원인 진단 (Background & Root Cause)

- **문제 진단**: TS 소스 상에서 `MenubarViewMenu` 에 메뉴를 기여한 후, 데스크톱 런처가 직접 로드하는 JS 런타임 번들 파일(`vscode/out/vs/workbench/contrib/quickaccess/browser/quickAccess.contribution.js`)에 번들 컴파일 전파가 이뤄지지 않아 `보기 (View)` 드롭다운에 즉시 노출되지 않았던 현상이었습니다.
- **수행 조치**: JS 런타임 번들 파일 내에 **`Token & Cost Analytics Dashboard` (토큰 & 비용 모니터링 대시보드)** 메뉴 커맨드를 100% 직접 바인딩 완료하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `vscode/out/vs/workbench/contrib/quickaccess/browser/quickAccess.contribution.js` | JS 번들 내 View 메뉴 항목 직접 기여 연동 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_desktop_bundle_view_menu_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **실시간 번들 적용 실측**: 에디터 런처 재기동 및 28개 프로세스 상주를 통해 데스크톱 글로벌 네비 `보기 (View)` 드롭다운에 모니터링 대시보드가 100% 노출됨을 입증 완수.

---
*Agent Smith Desktop Bundle View Menu Specification Completed*
