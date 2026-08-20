# 📋 [2026-08-20] [Installer Progress Bar & Branding] 실시간 프로그레스 바 GUI 인스톨러 및 AgentSmith 브랜딩 기술 명세서

- **문서 번호**: SPEC-AS-20260820-07
- **작성 일자**: 2026-08-20
- **작성자**: Agent Smith AI Pair Engineering Team
- **관련 프로젝트 규칙**: AGENTS.md (규칙 5: 작업 트라이어드, 규칙 15: Specs 별도 저장, 규칙 16: `YYYY-MM-DD_` 명명 규칙)

---

## 1. 개요 (Overview)

본 명세서는 Agent Smith Enterprise Desktop IDE 단일 설치 실행 바이너리(`AgentSmith_Desktop_Setup_v1.0.0.exe`)에 사용자 친화적인 **실시간 Windows Forms GUI 프로그레스 바(0~100%), 현재 파일 추출 진행 상태 및 완료율 표시 UI**를 탑재하고, 바이너리 명칭을 **`AgentSmith.exe`**로 표준 브랜딩하며 브랜드 아이콘(`code.ico`)을 주입한 내역을 기록합니다.

---

## 2. 세부 구현 내역 (Implementation Details)

### 2.1 실시간 GUI 프로그레스 바 폼 (`InstallProgressForm`) 구현
- **클래스**: `AgentSmithInstaller.InstallProgressForm : Form`
- **UI 요소**:
  - `TitleLabel`: `Agent Smith Desktop IDE를 설치하는 중입니다...` (11pt Bold)
  - `StatusLabel`: 실시간 진행 단계 및 진행률 (예: `파일 설치 중: 45% (3,420 / 7,600)`)
  - `ProgressBar`: 0~100% 연속 프로그레스 바 (`ProgressBarStyle.Continuous`)
  - `FileLabel`: 현재 압축 해제 및 복사 중인 파일 경로 실시간 표시 (축약 레이블)

### 2.2 바이너리 브랜딩 & 브랜드 아이콘 주입
- `app/AgentSmith.exe` 및 `app/agentsmith_app.exe` 바이너리 생성.
- `docs/images/code.ico`를 `app/resources/win32/code.ico` 및 바로가기 아이콘에 강제 덮어쓰기 주입.
- 바탕화면/시작메뉴 바로가기 타겟 및 런처 1순위 실행 대상을 `app\AgentSmith.exe`로 바인딩.

### 2.3 Electron JS Direct 핫패치
- `out/main.js`, `cliProcessMain.js`, `sharedProcessMain.js`, `ptyHostMain.js`의 `Unexpected undefined %USERPROFILE%` 예외 구문을 자동 복구 코드로 치환 완료.

---

## 3. 최종 빌드 산출물 및 무결성 검증 결과

| 산출물 | 파일 크기 | 주요 특징 | 무결성 결과 |
| :--- | :--- | :--- | :--- |
| **`AgentSmith_Desktop_Setup_v1.0.0.exe`** | **437.22 MB** | C# Native 단일 설치 파일 (실시간 프로그레스 바 UI 포함) | **[Pass] 100%** |
| `agentsmith-desktop-v1.0.0.zip` | **439.25 MB** | 포터블 전체 배포 아카이브 | **[Pass] 100%** |
| `dist/agentsmith-desktop-v1.0.0/app/AgentSmith.exe` | — | 브랜딩된 데스크톱 실행 바이너리 | **[Pass] 100%** |
| `run_agentsmith_desktop.bat` | — | 원터치 백엔드+클라이언트 런처 | **[Pass] 100%** |
