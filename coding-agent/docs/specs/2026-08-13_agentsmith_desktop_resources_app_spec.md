# 📄 [작업 명세서] Electron resources/app 패키지 구성 및 데스크톱 GUI 스플래시 우회 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 근본 원인 (Background & Root Cause)

- **문제 분석**: 사용자께서 보내주신 스크린샷의 `To run a local app, execute the following on the command line: $ agentsmith.exe path-to-app` 메시지는 Electron 엔진 바이너리 자체는 100% 정상 작동하나, `.build/electron/` 디렉터리 내에 표준 Electron 앱 패키지 폴더인 `resources/app` 이 존재하지 않아 디폴트 Electron 스플래시 화면이 출력되었던 현상이었습니다.
- **수행 조치**:
  1. `vscode/.build/electron/resources/app/` 표준 디렉터리를 생성하였습니다.
  2. `package.json` 파일 배치 및 `out/`, `node_modules/` 폴더를 Junction 심볼릭 링크로 결합하여 Electron 엔진이 더블클릭만으로도 자신의 소스코드 번들을 100% 탐색하도록 수립하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[NEW]** | `vscode/.build/electron/resources/app/package.json` | Electron 메인 패키지 디스크립터 |
| **[NEW]** | `vscode/.build/electron/resources/app/out` | `vscode/out` 컴파일 결과물 Junction 심볼릭 링크 |
| **[NEW]** | `vscode/.build/electron/resources/app/node_modules` | `vscode/node_modules` 의존성 Junction 심볼릭 링크 |
| **[MODIFY]** | `run_agent_smith.bat` | `resources/app` 번들 연동 1-Click GUI 런처 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_desktop_resources_app_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **`resources/app` 구성 유무**: `package.json`, `out`, `node_modules` 연결 완수.
- **스플래시 우회 및 GUI 출현**: [`agentsmith.exe`](file:///C:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/.build/electron/agentsmith.exe) 더블클릭 시 디폴트 스플래시 화면 대신 VS Code 데스크톱 에디터 GUI 창 팝업 구동 완수.

---
*Agent Smith Desktop Resources App Specification Completed*
