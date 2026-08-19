# 📋 2026-08-19 Antigravity 스타일 챗 패널 및 아티팩트 관리 계획서

본 문서는 Agent Smith IDE에 Antigravity 핵심 사용자 경험(아티팩트 카드/드로어, 승인 게이트, 사고과정 아코디언)과 타 코딩 에이전트(Windsurf, Cursor)의 기능(Live Multi-File Diff, 다중 모델/모드 스위처, VS Code 네이티브 연동)을 체계적으로 탑재하기 위한 상세 계획서입니다.

---

## 1. 개요 및 목적
- **목적**: 
  - 단순 챗 인터페이스를 넘어, 계획 수립(Planning Mode) ➔ 구현 계획서 제시 ➔ 사용자 승인(Approval Gate) ➔ 자율 실행 및 실시간 아티팩트/Multi-File Diff 관리가 가능한 에이전틱 챗 UI 구축
  - Antigravity의 아티팩트 시스템(`implementation_plan.md`, `specs/`, `walkthrough.md`)을 IDE 내부 웹뷰와 100% 통합
- **일자**: 2026년 8월 19일

---

## 2. 세부 구성 모듈
1. **아티팩트 카드 & 서랍(Drawer) 엔진**:
   - 메시지 내 아티팩트 카드 렌더링 + [에디터에서 열기] + [승인하고 진행(Proceed)]
   - 상단 아티팩트 서랍 배지(`📋 아티팩트 (N)`) 및 1-Click 네비게이션
2. **Planning Mode & 승인 게이트 상태 머신**:
   - `🧠 Planning Mode` / `⚡ Fast Direct` / `🧪 QA & Review` 모드 스위처
   - 계획서 승인 대기 및 실행 페이즈 자동 전환
3. **사고 과정 & 도구 호출 접이식 아코디언**:
   - Thinking Block 접기/펼치기 및 소요 시간 뱃지
   - 도구 실행 내역 및 셀프코렉션 로그 렌더링
4. **Windsurf 스타일 Live Multi-File Diff & 제어 컨트롤**:
   - `+ / -` 인라인 Diff 시각화, [Accept] / [Reject] / [Rollback]
5. **VS Code Native 에디터 브리지 (`extension.js`)**:
   - `vscode.window.showTextDocument`, `vscode.diff` 네이티브 연동
