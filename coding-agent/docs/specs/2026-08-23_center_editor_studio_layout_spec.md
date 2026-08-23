# 📄 코드 변경 명세서 (Specs): Agent Smith Studio 중앙 에디터(Welcome 위치) 배치 및 3창 분리 레이아웃 적용

- **문서 번호**: `SPEC-2026-08-23-CENTER-STUDIO-LAYOUT`
- **작성 일자**: 2026-08-23
- **작성자**: Agent Smith AI Architecture & Pair Engineering Team
- **대상 브랜치**: `feature/setup-git-guardrails`
- **목적**: 앱 기동 시 좁은 사이드바 대신 **중앙 Welcome(에디터) 위치에 Agent Smith Studio(AI 채팅 & 바이브 코딩 3-Panel 대시보드)가 기본 자동 마운트**되도록 개편하고, 초기 3창 분리 설계([좌측: 탐색기 / 중앙: Agent Smith Studio & Chat / 우측·하단: Diff & 코드 뷰])를 구현함.

---

## 🛠️ 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 설명 |
| :--- | :--- | :--- |
| **[MODIFY] 확장 진입점** | [`extensions/agentsmith-chat/src/extension.ts`](file:///c:/dev/antigravity-workspace/agentsmith/extensions/agentsmith-chat/src/extension.ts) | `activate()` 시점에 중앙 에디터 탭 자동 기동(`createOrShowEditorPanel()`) 및 `openChat` 명령어 바인딩 |
| **[MODIFY] 뷰 프로바이더** | [`extensions/agentsmith-chat/src/chatViewProvider.ts`](file:///c:/dev/antigravity-workspace/agentsmith/extensions/agentsmith-chat/src/chatViewProvider.ts) | 탭 아이콘(`media/logo.svg`) 탑재 및 `openFile` 시 3창 분할(`ViewColumn.Beside`) 지원 |
| **[MODIFY] CJS 번들** | [`extensions/agentsmith-chat/out/extension.js`](file:///c:/dev/antigravity-workspace/agentsmith/extensions/agentsmith-chat/out/extension.js), [`extensions/agentsmith-chat/out/chatViewProvider.js`](file:///c:/dev/antigravity-workspace/agentsmith/extensions/agentsmith-chat/out/chatViewProvider.js) | TypeScript 컴파일된 CJS 프로덕션 번들 갱신 |
| **[MODIFY] 패키징** | [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/agentsmith/scripts/package_desktop_dist.py) | 포터블 `settings.json`에 `workbench.startupEditor: "none"` 탑재하여 기본 Welcome 중복 노출 억제 |
| **[NEW] 명세서** | [`coding-agent/docs/specs/2026-08-23_center_editor_studio_layout_spec.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-23_center_editor_studio_layout_spec.md) | 본 중앙 스튜디오 배치 및 3창 분리 명세서 |

---

## 🏗️ 2. 3창 분리(3-Panel Layout) 동작 메커니즘

```
┌─────────────────┬──────────────────────────────────────────┬─────────────────────────────┐
│  Primary Nav    │        Center Main Editor Area           │     Secondary Editor Area   │
│ (좌측 사이드바)  │       (Welcome 위치 / ViewColumn 1)      │      (코드 / 실시간 Diff)    │
├─────────────────┼──────────────────────────────────────────┼─────────────────────────────┤
│ 📁 파일 탐색기   │ 🚀 AGENT SMITH STUDIO (메인 AI 대시보드)   │ 📄 main.py (Live Diff 뷰어)  │
│    - 워크스페이스 │   - 🧠 Plan & Goal 오케스트레이터        │   - 실시간 코드 변경 반영   │
│    - 프로젝트 트리│   - 💬 AI 스트리밍 채팅 & 피드백        │   - 1-Click 수락 / 롤백      │
│                 │   - 🕸️ 그래프 & 기억 메모리 드로어      │                             │
└─────────────────┴──────────────────────────────────────────┴─────────────────────────────┘
```

1. **중앙 에디터 영역 단독 마운트**:
   - 데스크톱 실행 시 기본 Welcome walkthrough 페이지 대신 `Agent Smith Studio` 에디터 탭이 중앙 메인 화면에 풀사이즈로 표시됩니다.
   - 탭 헤더에 Trinity Air 밝은 Edge 로고 아이콘이 각인되어 표시됩니다.
2. **사이드바 독립 탐색기(Explorer) 연동**:
   - 좌측 사이드바는 파일 탐색기(`workbench.view.explorer`)로 동작하여 프로젝트 파일을 빠르게 탐색할 수 있습니다.
3. **우측 분할 창 코드 연동**:
   - 중앙 스튜디오에서 아티팩트 파일 또는 Diff 검토 클릭 시, 중앙 Studio 대화창을 유지한 채 우측 분할 에디터(`ViewColumn.Beside`)로 파일이 열려 실시간 코드 수정 및 수락/롤백 작업을 지원합니다.

---

## 🧪 3. 빌드 및 산출물 정밀 진단 결과

- `verify_desktop_bundle.py --verify-dist`: **100% PASS**
- **포터블 번들**: [`dist/agentsmith-desktop-v1.0.0.zip`](file:///c:/dev/antigravity-workspace/agentsmith/dist/agentsmith-desktop-v1.0.0.zip) (450.40 MB)
- **C# Native 인스톨러**: [`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) (448.34 MB)
