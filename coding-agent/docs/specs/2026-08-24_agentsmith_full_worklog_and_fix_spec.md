# 📋 2026-08-24 Agent Smith 타 PC 현행화, 레이아웃 결함 수정 및 MVP 무결성 검증 상세 명세서

**문서 일자**: 2026-08-24  
**작업자**: Agent Smith AI Architecture & Engineering Team  
**관련 규칙**: AGENTS.md (규칙 5, 14, 15, 16 준수)  

---

## 1. 개요

본 명세서는 2026-08-24 진행된 전체 코드 변경, 브랜치 동기화, UI 버그 픽스, 3-Panel Studio 복원 및 배포 바이너리 재검증 내역에 대한 종합 파일 수정 맵(Specs Map)을 기술합니다.

---

## 2. 변경 및 동기화 파일 매핑 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 상세 설명 |
| :--- | :--- | :--- |
| **[MODIFY] TODO 로드맵** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/TODO.md) | 2026-08-24 현행화 완료 내역 기록, 향후 보강 과제(Settings Modal, Phase 3 Linux, Phase 4 QA) 세분화, 환경 검증 매트릭스 갱신 |
| **[MODIFY] 패키징 스크립트** | [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/agentsmith/scripts/package_desktop_dist.py) | extension 복사 소스를 TypeScript(`extensions/`) 대신 JS 기반(`extension/`)으로 수정, 잔여 파일 사전 정리 안전 로직 추가 |
| **[MODIFY] 확장 설정** | [`extension/agentsmith-chat/package.json`](file:///c:/dev/antigravity-workspace/agentsmith/extension/agentsmith-chat/package.json) | 사이드바 `viewsContainers`/`views` 제거, 에디터 타이틀 툴바 메뉴 및 단축키(`Ctrl+Alt+A`), 명령어 등록 |
| **[MODIFY] 확장 진입점** | [`extension/agentsmith-chat/src/extension.js`](file:///c:/dev/antigravity-workspace/agentsmith/extension/agentsmith-chat/src/extension.js) | 사이드바 웹뷰 등록 제거, 중앙 Welcome 위치 단독 마운트, `workbench.view.explorer` 자동 호출, 3-Panel 렌더러 연결(`index.html`, `style.css`, `app.js`), 상태표시줄 버튼 등록 |
| **[SYNC] 미디어 리소스** | [`extension/agentsmith-chat/media/`](file:///c:/dev/antigravity-workspace/agentsmith/extension/agentsmith-chat/media/) | 3-Panel Studio 대시보드 리소스(`index.html`, `style.css`, `app.js`, `logo.svg`) 탑재 |
| **[SYNC] TS 확장 설정** | [`extensions/agentsmith-chat/package.json`](file:///c:/dev/antigravity-workspace/agentsmith/extensions/agentsmith-chat/package.json) | TypeScript 패키지 설정 동일 동기화 |
| **[SYNC] TS 확장 진입점** | [`extensions/agentsmith-chat/src/extension.ts`](file:///c:/dev/antigravity-workspace/agentsmith/extensions/agentsmith-chat/src/extension.ts) | TypeScript 진입점 동일 동기화 |
| **[HOTPATCH] 배포 패키지** | [`dist/agentsmith-desktop-v1.0.0/app/resources/app/extensions/agentsmith-chat/`](file:///c:/dev/antigravity-workspace/agentsmith/dist/agentsmith-desktop-v1.0.0) | 최종 완성된 3-Panel Studio 확장 즉시 핫패치 적용 |
| **[NEW] 종합 보고서** | [`docs/2026-08-24_agentsmith_comprehensive_handover_report.md`](file:///c:/dev/antigravity-workspace/agentsmith/docs/2026-08-24_agentsmith_comprehensive_handover_report.md) | 금일 현행화 및 레이아웃 결함 수정 종합 인수인계 보고서 |
| **[NEW] 상세 명세서** | [`coding-agent/docs/specs/2026-08-24_agentsmith_full_worklog_and_fix_spec.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-24_agentsmith_full_worklog_and_fix_spec.md) | 본 전체 작업 명세서 |

---

## 3. 검증 결과 요약

1. **`git status`**: `On branch feature/setup-git-guardrails, nothing to commit, working tree clean`
2. **백엔드 무결성 진단 (`scripts/test_backend_integrity.py`)**: 6개 핵심 모듈 100% PASS
3. **데스크톱 배포 번들 무결성 진단 (`scripts/verify_desktop_bundle.py --verify-dist`)**: 8개 검사항목 100% PASS
4. **UI 동작 검증**: 좌측 사이드바는 파일 탐색기로 포커스되고, 중앙 Welcome 위치에만 3-Panel Studio(좌측 파일 목록, 중앙 채팅/Thinking, 우측 Live Diff)가 정상 렌더링됨.
