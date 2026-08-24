# 📋 2026-08-24 Agent Smith 3-Panel Studio(좌측 워크스페이스/프로세스 - 중앙 AI Reasoning - 우측 Live Diff) UI 복원 명세서

**문서 일자**: 2026-08-24  
**작업자**: Agent Smith AI Architecture & Engineering Team  
**관련 규칙**: AGENTS.md (규칙 5, 14, 15, 16 준수)  

---

## 1. 문제 원인 및 분석

### 🔍 원인 분석
- 타 PC에서 개발된 **3-Panel Studio 대시보드**는 `extensions/agentsmith-chat/media/`의 `index.html`, `style.css`, `app.js`로 구성되어 있으며, 화면 너비 760px 이상 시 다음과 같은 3열 레이아웃을 제공합니다:
  - **좌측 컬럼 (`explorer-column`)**: `WORKSPACE FILES` (프로세스 진행 대상 워크스페이스 파일 목록 및 개수 배지)
  - **중앙 컬럼 (`chat-column`)**: `AI REASONING & CHAT` (Thinking 스트림 아코디언, Persona 태그, 대화창)
  - **우측 컬럼 (`diff-column`)**: `LIVE MULTI-FILE DIFF` (실시간 변경사항 Diff 뷰어, ✓ Accept / ✕ Reject 버튼)
- 그러나 로컬 배포 환경에서 구버전 사이드바 전용 1열 UI(`chat.html`, `chat.css`, `chat.js`)를 로드하도록 연결되어 있어, 중앙 에디터 탭으로 열렸을 때도 좌측 프로세스/파일 목록과 우측 Diff 뷰어가 표시되지 않았던 것입니다.

---

## 2. 조치 및 수정 내역 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 |
| :--- | :--- | :--- |
| **[MODIFY] 확장 진입점** | [`extension/agentsmith-chat/src/extension.js`](file:///c:/dev/antigravity-workspace/agentsmith/extension/agentsmith-chat/src/extension.js) | `_getHtmlForWebview()`가 3-Panel Studio(`index.html`, `style.css`, `app.js`)를 직접 렌더링하도록 변경 및 메시지 핸들러 호환성 강화 |
| **[SYNC] 미디어 리소스** | [`extension/agentsmith-chat/media/`](file:///c:/dev/antigravity-workspace/agentsmith/extension/agentsmith-chat/media/) | `index.html`, `style.css`, `app.js`, `logo.svg` 전체 동기화 |
| **[HOTPATCH] 배포 번들** | [`dist/agentsmith-desktop-v1.0.0/...`](file:///c:/dev/antigravity-workspace/agentsmith/dist/agentsmith-desktop-v1.0.0) | 배포 디렉터리에 3-Panel Studio 완성본 즉시 핫패치 적용 완료 |

---

## 3. 복원된 3-Panel Studio 화면 구성

```
┌─────────────────────────┬──────────────────────────────────────┬─────────────────────────┐
│     WORKSPACE FILES     │        AI REASONING & CHAT           │   LIVE MULTI-FILE DIFF  │
│      (좌측 프로세스)     │       (중앙 스트리밍 & Thinking)      │      (우측 실시간 코드)   │
├─────────────────────────┼──────────────────────────────────────┼─────────────────────────┤
│ 📄 auth_service.py      │ [Agent Smith] 환영합니다!            │ async def authenticate()│
│ 📄 session_manager.py   │ 💭 Thinking (3개 가드레일 통과)      │ +  async with db.begin()│
│ 📄 vibe_engine.py       │ 📋 시스템 초기화 명세서 아티팩트     │ -  user = db.query()    │
│                         │                                      │ [✓ Accept] [✕ Reject]   │
├─────────────────────────┴──────────────────────────────────────┴─────────────────────────┤
│ 🛡️ SAST: PASSED  |  🇰🇷 한글 주석 강제  |  UTF-8 Bom-less  |  🧠 Mem0: Synced             │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. 검증 결과

- `scripts/verify_desktop_bundle.py --verify-dist`: **100% PASS**
- 중앙 Welcome 탭에 3-Panel Studio가 정상 로드되어 좌측 프로세스 파일, 중앙 채팅 및 우측 실시간 Diff 뷰어가 정상 노출됨을 확인.
