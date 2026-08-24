# 📋 2026-08-24 Agent Smith Studio 좌측 사이드바 중복 노출 제거 및 중앙 단독 마운트 수정 명세서

**문서 일자**: 2026-08-24  
**작업자**: Agent Smith AI Architecture & Engineering Team  
**관련 규칙**: AGENTS.md (규칙 5, 14, 15, 16 준수)  

---

## 1. 문제 증상 및 분석

### 🔴 문제점
- 데스크톱 IDE 실행 시, **좌측 사이드바(Primary Side Bar)** 에 "AGENT SMITH AI AGENT SMITH ASSISTANT" 패널이 생성되고, 동시에 **중앙 에디터 영역(ViewColumn 1, Welcome 위치)** 에도 "Agent Smith Studio" 탭이 열려 화면에 **동일한 채팅 창이 양쪽에 2개 중복 노출**되는 현상 발생.

### 🔍 원인 분석
1. `package.json`의 `contributes.viewsContainers.activitybar` 및 `views`에 `agentsmith-chat-view` 웹뷰가 등록되어 있어 사이드바에 채팅창이 자동으로 마운트됨.
2. `extension.js`에서 `registerWebviewViewProvider`를 통해 사이드바 웹뷰를 등록하고, 동시에 `createOrShowEditorPanel`을 호출하여 중앙에도 웹뷰를 생성함으로써 2개의 인스턴스가 나란히 렌더링됨.

---

## 2. 해결 및 수정 내역 (Specs Map)

| 구분 | 파일 경로 | 수정 내용 |
| :--- | :--- | :--- |
| **[MODIFY] 확장 설정** | [`extension/agentsmith-chat/package.json`](file:///c:/dev/antigravity-workspace/agentsmith/extension/agentsmith-chat/package.json) | 사이드바 `viewsContainers` 및 `views` 중복 웹뷰 등록 제거, 에디터 타이틀 툴바 메뉴 및 키바인딩(`Ctrl+Alt+A`) 등록 |
| **[MODIFY] 확장 진입점** | [`extension/agentsmith-chat/src/extension.js`](file:///c:/dev/antigravity-workspace/agentsmith/extension/agentsmith-chat/src/extension.js) | 사이드바 `registerWebviewViewProvider` 제거, 중앙 스튜디오 단독 마운트 및 좌측 사이드바 파일 탐색기(`workbench.view.explorer`) 자동 포커스, 상태표시줄 버튼 등록 |
| **[MODIFY] TS 확장 설정** | [`extensions/agentsmith-chat/package.json`](file:///c:/dev/antigravity-workspace/agentsmith/extensions/agentsmith-chat/package.json) | TypeScript 패키지 설정 동일 동기화 |
| **[MODIFY] TS 진입점** | [`extensions/agentsmith-chat/src/extension.ts`](file:///c:/dev/antigravity-workspace/agentsmith/extensions/agentsmith-chat/src/extension.ts) | TypeScript 진입점 동일 동기화 |
| **[HOTPATCH] 배포 번들** | [`dist/agentsmith-desktop-v1.0.0/...`](file:///c:/dev/antigravity-workspace/agentsmith/dist/agentsmith-desktop-v1.0.0) | 배포 디렉터리에 수정된 확장 즉시 핫패치 적용 완료 |

---

## 3. 최종 완성된 3창 분리 레이아웃 구조

```
┌─────────────────┬──────────────────────────────────────────┬─────────────────────────────┐
│  Primary Nav    │        Center Main Editor Area           │     Secondary Editor Area   │
│ (좌측 사이드바)  │       (Welcome 위치 / ViewColumn 1)      │      (코드 / 실시간 Diff)    │
├─────────────────┼──────────────────────────────────────────┼─────────────────────────────┤
│ 📁 파일 탐색기   │ 🚀 AGENT SMITH STUDIO (단독 AI 대시보드) │ 📄 main.py (Live Diff 뷰어)  │
│    - 워크스페이스 │   - 🧠 Plan & Goal 오케스트레이터        │   - 실시간 코드 변경 반영   │
│    - 프로젝트 트리│   - 💬 AI 스트리밍 채팅 & 피드백        │   - 1-Click 수락 / 롤백      │
│                 │   - 🕸️ 그래프 & 기억 메모리 드로어      │                             │
└─────────────────┴──────────────────────────────────────────┴─────────────────────────────┘
```

- **좌측**: 파일 탐색기 (Explorer)
- **중앙**: Agent Smith Studio (메인 AI 대시보드 단독 마운트)
- **우측**: 코드 에디터 및 Live Diff (3창 분리 완성)
- 언제든지 하단 상태표시줄의 `$(sparkle) Agent Smith Studio` 또는 `Ctrl+Alt+A`로 중앙 스튜디오 호출 가능

---

## 4. 검증 결과

- `scripts/verify_desktop_bundle.py --verify-dist`: **100% PASS**
- 사이드바 중복 웹뷰가 완전히 제거되고, 중앙 에디터 영역에만 Agent Smith Studio가 단독으로 기동됨을 확인.
