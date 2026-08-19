# 📄 2026-08-19 표준 접근성 복원 및 선택적 사내 보안(Enterprise Auth) 기능화 상세명세서

본 명세서는 2026년 8월 19일 진행된 Agent Smith IDE의 기본 접근성 복원(로그인 강제 차단 해제) 및 사내 폐쇄망 전용 인증(이메일 OTP / LDAP)의 선택적 Enterprise 기능 전환 작업 내역을 정의합니다.

---

## 📂 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 요약 |
| :--- | :--- | :--- |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.html`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.html) | 로그인 강제 차단 오버레이 제거, 헤더에 사내 보안 모달 토글(🔐) 버튼 및 상태 배지 탑재 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.js) | 기본 실행 시 즉시 대화창 사용 지원, 사내 인증 모달 열기/닫기/건너뛰기 핸들러 및 인증 배지 상태 연동 |
| **[MODIFY]** | [`extension/agentsmith-chat/media/chat.css`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/extension/agentsmith-chat/media/chat.css) | 헤더 분할 레이아웃, `auth-badge` (표준/사내인증됨), 모달 닫기 버튼(✕) 스타일 추가 |
| **[MODIFY]** | [`vscode/extensions/agentsmith-chat/`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/extensions/agentsmith-chat/) | 소스 빌드 트리 내 익스텐션 정적 리소스 동기화 |
| **[MODIFY]** | [`VSCode-win32-x64/resources/app/extensions/agentsmith-chat/`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/VSCode-win32-x64/resources/app/extensions/agentsmith-chat/) | 배포 런타임 내 익스텐션 정적 리소스 동기화 |
| **[MODIFY]** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/TODO.md) | 표준 접근성 100% 복원 및 선택적 사내 보안 기능화 로드맵 현행화 |
| **[NEW]** | [`coding-agent/docs/specs/2026-08-19_restore_standard_access_and_optional_enterprise_auth_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-19_restore_standard_access_and_optional_enterprise_auth_spec.md) | 표준 접근성 복원 및 선택적 인증 명세서 (본 문서) |

---

## 🛠️ 2. 상세 수정 내역 및 구조 개선

### A. 표준 VS Code 스타일 즉시 사용 접근성 100% 복원
- **기존 한계점**: 웹뷰 실행 시 `auth-overlay`가 기본 `active` 상태로 화면 전체를 가로막아, 반드시 사내 이메일 OTP를 인증해야만 대화창 기능을 사용할 수 있었음.
- **개선 내용**:
  - `auth-overlay`의 기본 활성화 상태를 해제하여, 에디터 구동 즉시 누구나 프롬프트 입력, AI 모델 전환, STT 음성 인식, Vibe 코드 생성을 자유롭게 사용할 수 있도록 복원.

### B. 사내 폐쇄망 전용 인증(Enterprise Auth)의 선택적 모달 전환
- **구현 내용**:
  - 챗 헤더 우측에 **[🔐 보안 인증 관리 버튼]** 및 **[인증 상태 배지]** 탑재.
  - 기본 상태에서는 `[표준 모드]` 배지가 표시되며, 사내망 정책이나 LDAP 연동이 필요한 경우 🔐 버튼을 클릭하여 모달을 열고 이메일 OTP 인증 수행 가능.
  - 인증 성공 시 배지가 `[사내 인증됨 (user@company.com)]`으로 실시간 갱신.
  - 모달 내에 **[✕ 닫기]** 및 **[로컬/표준 모드로 계속]** 버튼을 제공하여 사용자 편의성 극대화.

---

## 🧪 3. 검증 결과

1. **초기 로딩 검증**:
   - Left Chat Panel 웹뷰 진입 시 로그인 차단 모달 없이 즉시 프롬프트 입력 및 모델 선택 드롭다운 사용 가능 확인.
2. **모달 토글 및 인증 플로우 검증**:
   - 우측 상단 🔐 버튼 클릭 시 사내 인증 모달이 정상 팝업되며, 닫기(✕) 및 건너뛰기 버튼으로 자유롭게 제어 가능.
   - OTP 검증 성공 시 `auth-badge`가 `사내 인증됨` 녹색 배지로 동적 갱신됨을 확인.
3. **바이너리 및 빌드 디렉터리 동기화 완료**:
   - `vscode/extensions/agentsmith-chat/` 및 `VSCode-win32-x64/resources/app/extensions/agentsmith-chat/`에 변경된 UI 파일 100% 동기화 완료.
