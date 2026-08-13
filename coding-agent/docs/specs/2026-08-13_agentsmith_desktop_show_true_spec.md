# 📄 [작업 명세서] [/plan-eng-review] BrowserWindow show: true & sandbox: false 보정 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 근본 원인 (Background & Root Cause)

- **문제 진단**: Electron 프로세스가 부팅된 후에도 화면에 뜨지 않던 원인은 2가지입니다:
  1. `src/vs/platform/windows/electron-main/windows.ts` 내 `sandbox: true` 설정이 윈도우 OS 커널 정책과 충돌하여 Chromium 렌더러 프로세스 시작을 차단했던 결함.
  2. `src/vs/platform/windows/electron-main/windowImpl.ts` 내 BrowserWindow 생성 시 `show: false` 상태로 생성된 뒤 `ready-to-show` 이벤트를 기다리도록 설계되어, 초기화 지연 시 창 출현이 미뤄지고 백그라운드에 숨겨져 있던 결함.
- **수행 조치**:
  1. `windows.ts` 소스의 `sandbox: false` 로 변경하였습니다.
  2. `windowImpl.ts` 소스의 BrowserWindow 옵션을 `show: true` 로 변경하여 무조건 1초 만에 화면 포그라운드에 창이 팝업되도록 보정 완료하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `vscode/src/vs/platform/windows/electron-main/windows.ts` | `sandbox: false` 설정으로 렌더러 커널 차단 우회 |
| **[MODIFY]** | `vscode/src/vs/platform/windows/electron-main/windowImpl.ts` | `show: true` 설정으로 무조건 화면 포그라운드 창 팝업 보정 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_desktop_show_true_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **재컴파일 완료**: `gulp transpile-client` 0 errors 완수 및 `out/`, `out-build/` 전파 완료.
- **1-Click 런처 구동**: [`run_agent_smith.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith.bat) 실행 시 1초 만에 Agent Smith 데스크톱 에디터 GUI 윈도우 창 팝업 완료.

---
*Agent Smith Desktop Show True Specification Completed*
