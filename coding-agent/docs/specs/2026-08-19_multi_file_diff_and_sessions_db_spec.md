# 📄 2026-08-19 Live Multi-File Diff 및 UUID 멀티테넌트 세션 DB 구축 상세명세서

본 명세서는 2026년 8월 19일 진행된 Agent Smith IDE의 Windsurf 스타일 Live Multi-File Diff(실시간 변경 맵, 파일별 Accept/Reject, One-Click Rollback, vscode.diff 연동) 및 SQLite 기반 UUID 세션 히스토리 DB 관리 시스템 구축 내역을 정의합니다.

---

## 📂 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 요약 |
| :--- | :--- | :--- |
| **[NEW]** | [`coding-agent/src/db/session_manager.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/db/session_manager.py) | SQLite 기반 UUID 세션, 메시지, 아티팩트 및 Diff 롤백 히스토리 영속화 매니저 구축 |
| **[MODIFY]** | [`coding-agent/src/main.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/main.py) | `/api/sessions` (목록, 생성, 복원, 삭제) 및 `/api/diff/apply`, `/api/diff/rollback` 엔드포인트 탑재 |
| **[MODIFY]** | [`coding-agent/src/vibe/engine.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/vibe/engine.py) | 다중 파일 수정 시 `file_diffs` 구조화 및 세션 ID 연동 파이프라인 확장 |
| **[MODIFY]** | [`extension/agentsmith-chat/src/extension.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/src/extension.js) | `openDiff` (`vscode.diff`), `acceptDiff`, `rollbackDiff` 및 세션 복원 중계 로직 탑재 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.html`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.html) | 세션 히스토리 슬라이드 드로어(`#sessions-drawer`) 및 헤더 `[🕒 기록]` 토글 버튼 구축 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.css`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.css) | Multi-File Diff 카드, 파일별 상태 뱃지, 통계(`+N/-N`), 세션 아이템 모던 스타일링 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.js) | Multi-File Diff 렌더링, [Accept], [Reject], [Diff 비교], 세션 목록/복원/삭제 인터랙션 구현 |
| **[NEW]** | [`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) | Multi-File Diff 및 세션 DB가 탑재된 최신 단일 인스톨러 바이너리 컴파일 완료 (157.57 MB) |
| **[MODIFY]** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/TODO.md) | Phase 2 4번 및 5번 항목 완료(`[x]`) 현행화 |
| **[NEW]** | [`coding-agent/docs/specs/2026-08-19_multi_file_diff_and_sessions_db_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-19_multi_file_diff_and_sessions_db_spec.md) | Multi-File Diff 및 세션 DB 상세명세서 (본 문서) |

---

## 🛠️ 2. 상세 구현 기술 사양

### A. Windsurf Cascade 스타일 Live Multi-File Diff
- **파일별 변경 카드 렌더링**: 다중 파일 변경 시 `+ (추가)` / `- (삭제)` 통계와 함께 파일별 인라인 Diff 코드블록 시각화.
- **세부 제어 컨트롤**:
  - **[🔍 Diff 비교]**: `vscode.diff` 명령을 호출하여 VS Code 네이티브 분할 뷰어로 원본과 수정본을 1:1 정밀 비교.
  - **[✓ Accept]**: 해당 파일의 변경사항을 실제 워크스페이스에 즉시 반영 및 저장.
  - **[✕ Reject]**: 변경 사항을 거절하고 파일 원본 상태 유지.
  - **[✓ 모두 수락] / [↺ 전체 롤백]**: 일괄 변경 및 원클릭 복원 지원.

### B. UUID 기반 멀티테넌트 세션 & 대화 히스토리 DB (`sessions.db`)
- **SQLite 영속화 스키마**: `sessions`, `messages`, `artifacts`, `diff_history` 4대 테이블을 통해 과거 대화 내용, 생성된 아티팩트 및 Diff 이력을 영구 보존.
- **세션 서랍 (`[🕒 기록]`)**: 상단 헤더의 `[🕒 기록]` 버튼 클릭 시 슬라이드 드로어가 열려 이전 세션 목록을 조회하고 1-Click으로 과거 대화와 아티팩트를 복원.
