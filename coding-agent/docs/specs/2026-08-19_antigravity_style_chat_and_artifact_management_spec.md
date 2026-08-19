# 📄 2026-08-19 Antigravity 스타일 챗 패널 및 아티팩트 관리 상세명세서

본 명세서는 2026년 8월 19일 수립된 Agent Smith IDE의 Antigravity 스타일 아티팩트 관리, 플래닝 모드 승인 게이트, 사고 과정 아코디언 및 Live Multi-File Diff 연동에 관한 로드맵 및 아키텍처 명세를 정의합니다.

---

## 📂 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 요약 |
| :--- | :--- | :--- |
| **[MODIFY]** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/TODO.md) | Antigravity 아티팩트/승인게이트/아코디언/Diff 4대 신규 토픽을 포함한 9대 Phase 2 로드맵으로 전면 개편 |
| **[NEW]** | [`coding-agent/docs/plans/2026-08-19_antigravity_style_chat_and_artifact_management_plan.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/plans/2026-08-19_antigravity_style_chat_and_artifact_management_plan.md) | Antigravity 스타일 챗 패널 및 아티팩트 관리 작업 계획서 |
| **[NEW]** | [`coding-agent/docs/specs/2026-08-19_antigravity_style_chat_and_artifact_management_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-19_antigravity_style_chat_and_artifact_management_spec.md) | Antigravity 스타일 챗 패널 및 아티팩트 관리 상세 명세서 (본 문서) |

---

## 🛠️ 2. 세부 기능 명세

### 1. Antigravity 스타일 아티팩트(Artifacts) 관리 & 인터랙티브 뷰어
- **아티팩트 카드 렌더링**: 계획서(`implementation_plan.md`), 상세명세서(`specs/`), 워크스루(`walkthrough.md`) 파일 생성 시 메시지 내 카드 형태로 상태 태그(계획/완료/피드백대기)와 함께 렌더링.
- **VS Code 네이티브 연동**: [에디터에서 열기] 클릭 시 `vscode.window.showTextDocument` API를 호출하여 에디터 탭으로 즉각 오픈.
- **상단 아티팩트 드로어**: 챗 패널 상단 `📋 아티팩트 (N)` 카운터 배지 클릭 시 세션 중 생성된 아티팩트 전체 목록을 슬라이드로 조회 및 이동.

### 2. Planning Mode & 대화형 승인 게이트 (Planning-to-Execution Gate)
- **작업 모드 스위처**: `🧠 Planning Mode (계획)`, `⚡ Fast Direct (직접 생성)`, `🧪 QA & Review (검증)` 3대 작업 모드 제공.
- **승인 게이트 상태 머신**: Planning Mode에서 계획서 생성 후 사용자 **[승인하고 진행 (Proceed)]** 클릭 시 자율 실행 루프로 자동 전환.

### 3. 사고 과정(Thinking Process) & 도구 호출(Tool Calls) 모던 아코디언
- **추론 블록 접이식 UI**: DeepSeek R1, Claude의 내부 사고 과정을 기본 접이식 아코디언으로 렌더링하여 메시지 가독성 확보.
- **도구 실행 및 셀프코렉션 로그**: `run_command`, `replace_file_content`, `view_file` 실행 내역과 오류 복구 과정을 아코디언으로 노출.

### 4. Windsurf Cascade 스타일 Live Multi-File Diff & 안전 승인/롤백 UI
- **실시간 Multi-File Diff**: 다중 파일 수정 시 `+ / -` 인라인 Diff 코드블록 시각화.
- **인터랙티브 제어**: 파일별 **[Accept] / [Reject]** 및 에러 시 **[One-Click Rollback]** 안전장치 탑재.
- **Native Diff 에디터**: `vscode.diff` 명령을 연동하여 좌우 분할 비교 화면 제공.
