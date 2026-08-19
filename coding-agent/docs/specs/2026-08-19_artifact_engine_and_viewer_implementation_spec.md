# 📄 2026-08-19 Antigravity 스타일 아티팩트 관리 및 인터랙티브 뷰어 엔진 구현 상세명세서

본 명세서는 2026년 8월 19일 진행된 Agent Smith IDE의 Antigravity 스타일 아티팩트(Artifacts) 관리 시스템, 메시지 내 아티팩트 카드 렌더링, 상단 슬라이드 아티팩트 서랍(Drawer), VS Code 네이티브 에디터 열기 연동 및 바이너리 인스톨러 컴파일 내역을 정의합니다.

---

## 📂 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 요약 |
| :--- | :--- | :--- |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.html`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.html) | 상단 툴바(새 대화, 아티팩트 드로어 토글, 모드 스위처) 및 슬라이드 아티팩트 드로어 마크업 구축 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.css`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.css) | Glassmorphism 아티팩트 카드, 슬라이드 드로어, 모드 스위처 및 접이식 아코디언 모던 스타일링 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.js) | 아티팩트 상태 관리, 카드 렌더링, [에디터에서 열기] 및 [승인하고 진행(Proceed)] 이벤트 연동 |
| **[MODIFY]** | [`extension/agentsmith-chat/src/extension.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/src/extension.js) | `openFile` (`vscode.window.showTextDocument`) 및 `scanArtifacts` 워크스페이스 문서 자동 수집기 구현 |
| **[MODIFY]** | [`coding-agent/src/vibe/engine.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/vibe/engine.py) | Vibe 실행 시 모드별(Planning/Direct) 아티팩트 메타데이터 구조화 생성 파이프라인 보강 |
| **[MODIFY]** | [`coding-agent/src/main.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/main.py) | `VibeRequest` 모델에 작업 모드(`mode`) 수용 및 아티팩트 응답 중계 |
| **[NEW]** | [`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) | 아티팩트 뷰어가 탑재된 최신 바이너리 C# Native 단일 실행 설치 파일 컴파일 완료 (156.31 MB) |
| **[MODIFY]** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/TODO.md) | Phase 2 1번 아티팩트 관리 및 인터랙티브 뷰어 엔진 완료(`[x]`) 현행화 |
| **[NEW]** | [`coding-agent/docs/specs/2026-08-19_artifact_engine_and_viewer_implementation_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-19_artifact_engine_and_viewer_implementation_spec.md) | 아티팩트 관리 및 인터랙티브 뷰어 엔진 구현 상세 명세서 (본 문서) |

---

## 🛠️ 2. 상세 구현 내역 및 기술 사양

### A. 아티팩트 카드(Artifact Card) 컴포넌트
- **역할**: 에이전트가 응답 시 생성한 작업 계획서(`implementation_plan.md`), 상세 명세서(`specs/`), 워크스루(`walkthrough.md`)를 감지하여 챗 메시지 내에 카드형 UI로 노출.
- **인터랙티브 기능**:
  - **[📄 에디터에서 열기 ↗]**: 클릭 시 VS Code 본체 에디터 영역으로 해당 파일을 즉시 오픈 (`vscode.window.showTextDocument`).
  - **[✓ 승인하고 진행 (Proceed)]**: 계획서 아티팩트의 경우 사용자가 승인 버튼을 클릭하면 즉시 에이전트 자율 실행 루프를 가동.

### B. 상단 슬라이드 아티팩트 서랍 (Artifacts Drawer)
- **역할**: 대화가 길어져 과거 아티팩트 카드가 위로 스크롤되어도, 상단 헤더의 `[📋 아티팩트 (N)]` 버튼을 클릭하여 세션 중 생성된 모든 아티팩트 목록을 언제든 확인 및 1-Click 열기 지원.
- **자동 스캔**: 챗 패널 초기화 시 `scanArtifacts` 명령을 통해 `coding-agent/docs/plans`, `coding-agent/docs/specs` 하위의 최신 마크다운 문서를 자동으로 로드하여 드로어에 등록.

### C. 작업 모드 스위처 (Mode Selector)
- **작업 모드**:
  1. `🧠 Planning Mode`: 계획 수립 후 사용자 승인 대기
  2. `⚡ Fast Direct`: 단순 작업 즉시 생성 및 실행
  3. `🧪 QA & Review`: 코드 분석 및 테스트 검증

---

## 🧪 3. 컴파일 및 검증 결과

1. **데스크톱 단일 인스톨러 바이너리 컴파일**:
   - `scripts/package_desktop_dist.py`를 통해 최신 앱 리소스 번들링 완료.
   - `scripts/build_desktop_installer.py`를 통해 C# Native 컴파일러(`csc.exe`)로 `dist/AgentSmith_Desktop_Setup_v1.0.0.exe` (156.31 MB) 생성 완료.
2. **백엔드 무결성 검증**:
   - FastAPI 백엔드 앱 (`coding-agent/src/main.py`) 임포트 및 REST API 엔드포인트 무결성 테스트 통과.
3. **소스 및 배포 런타임 동기화**:
   - `extension/agentsmith-chat/` -> `vscode/extensions/agentsmith-chat/` 및 `VSCode-win32-x64/` 100% 동기화 적용.
