# 📄 2026-08-19 Planning Mode 승인 게이트, 사고과정/도구호출 아코디언 및 conpty 터미널 복구 상세명세서

본 명세서는 2026년 8월 19일 진행된 Agent Smith IDE의 `conpty.node` 터미널 네이티브 모듈 복구와 Phase 2 2번(Planning Mode & 대화형 승인 게이트) 및 3번(사고 과정 & 도구 호출 모던 아코디언 및 셀프코렉션) 구현 내역을 정의합니다.

---

## 📂 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 요약 |
| :--- | :--- | :--- |
| **[FIX]** | [`VSCode-win32-x64/resources/app/node_modules.asar.unpacked/node-pty/build/Release/`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/VSCode-win32-x64/resources/app/node_modules.asar.unpacked/node-pty/build/Release/) | `conpty.node`, `conpty_console_list.node`, `winpty-agent.exe` 등 터미널 필수 네이티브 바이너리 100% 동기화 |
| **[MODIFY]** | [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/package_desktop_dist.py) | 배포 번들링 시 터미널 conpty 바이너리 자동 감지 및 패키징 파이프라인 탑재 |
| **[MODIFY]** | [`coding-agent/src/vibe/engine.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/vibe/engine.py) | Planning Mode 승인 대기 플래그, 도구 호출(Tool Calls) 배열, 셀프코렉션 메타데이터 생성 로직 구축 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.html`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.html) | 작업 모드 스위처(Planning/Direct/Review) 및 메인 대화창 레이아웃 보강 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.css`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.css) | `approval-gate-banner`, `thinking-timer`, `tool-call-item`, `self-correction-box` 모던 스타일링 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.js) | 승인 게이트 상태 머신, [승인하고 진행]/[피드백 입력] 인터랙션, 도구 호출/사고과정 아코디언 렌더러 탑재 |
| **[NEW]** | [`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) | conpty 터미널 복구 및 Planning Gate/도구호출 아코디언이 완전 탑재된 최신 인스톨러 바이너리 컴파일 완료 (157.57 MB) |
| **[MODIFY]** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/TODO.md) | Phase 2 2번 및 3번 항목 완료(`[x]`) 현행화 |
| **[NEW]** | [`coding-agent/docs/specs/2026-08-19_planning_gate_and_thinking_accordion_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-19_planning_gate_and_thinking_accordion_spec.md) | Planning Gate 및 아코디언 구현 상세명세서 (본 문서) |

---

## 🛠️ 2. 상세 구현 사양

### A. 터미널 conpty.node 바이너리 에러 해결
- **문제**: 배포 바이너리에서 `node_modules.asar.unpacked/node-pty/build/Release/conpty.node` 파일이 누락되어 IDE 구동 시 터미널 프로세스 시작 실패 에러가 팝업됨.
- **해결**: 검증된 네이티브 바이너리 세트(`conpty.node`, `conpty_console_list.node`, `pty.node`, `winpty-agent.exe`, `winpty.dll`)를 런타임 및 패키징 스크립트에 통합하여 터미널 에러를 근본적으로 해결.

### B. Planning Mode & 대화형 승인 게이트
- **상태 머신 흐름**:
  1. `[User Prompt]` ➔ 2. `[Plan Generation]` ➔ 3. `[Planning Gate: 승인 대기 배너]` ➔ 4. 사용자가 `[✓ 승인하고 진행 (Proceed)]` 클릭 ➔ 5. `[Execution Loop: 파일 수정 & 테스트 자율 실행]`.
- **피드백 지원**: `[✎ 수정 피드백 입력]` 클릭 시 입력창으로 포커스 이동 및 재계획(Re-plan) 연계.

### C. 사고 과정 & 도구 호출 모던 아코디언
- **🧠 사고 과정 (Thinking Process)**: 접이식 아코디언 + 총 추론 소요 시간 뱃지(`⏱ 3.2s`) 실시간 시각화.
- **🛠️ 도구 호출 (Tool Calls)**: 실행된 개별 도구(`replace_file_content`, `run_command` 등)의 호출 인자, 실행 소요 시간(`duration_ms`), 상태 뱃지(`[SUCCESS 110ms]`) 및 출력 로그 제공.
- **🔄 자율 셀프코렉션 (Self-Correction)**: 오류 감지 및 자동 복구 내역을 시각적 블록으로 표시.
