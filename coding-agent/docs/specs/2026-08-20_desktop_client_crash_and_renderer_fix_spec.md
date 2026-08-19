# 📄 코드 변경 명세서 (Specs): Electron 클라이언트 실행 장애 및 검은 화면 해결

- **작성 일자**: 2026-08-20
- **작성자**: Agent Smith AI Pair Engineer
- **관련 브랜치**: `feature/setup-git-guardrails`
- **목적**: 데스크톱 패키징 및 실행 과정에서 발생한 4단계 핵심 원인을 정밀 분석하고, 이에 대한 코드 및 파이프라인 변경 사항을 기록하여 추적성을 제공함.

---

## 🛠️ 1. 변경된 파일 목록 (Specs Map)

| 구분 | 파일 경로 | 변경 요약 |
| :--- | :--- | :--- |
| **[MODIFY]** | [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/package_desktop_dist.py) | `vscode/out` 복사, Electron 27 (`NODE_MODULE_VERSION 118`) 네이티브 모듈 14종 오버레이, CJS 확장자 미지정 바이너리 사본 생성, `node_modules.asar` 제거 및 백엔드 비동기 PowerShell 런처 반영 |
| **[MODIFY]** | [`scripts/build_desktop_installer.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/build_desktop_installer.py) | C# `Installer.cs` 소스 작성 시 대용량 페이로드 스트리밍 압축 해제 및 단일 압축 해제 로직 안정화 |
| **[MODIFY]** | [`agentsmith.vbs`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/agentsmith.vbs) | 런처 타겟을 `run_agentsmith_desktop.bat`로 교체하여 창 숨김 가동 보장 |
| **[NEW]** | [`coding-agent/docs/specs/2026-08-20_pc_synchronization_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-20_pc_synchronization_spec.md) | PC 현행화 및 Git 브랜치 동기화 명세서 |
| **[NEW]** | [`coding-agent/docs/specs/2026-08-20_desktop_client_crash_and_renderer_fix_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-20_desktop_client_crash_and_renderer_fix_spec.md) | 본 명세서 |
| **[NEW]** | [`coding-agent/docs/2026-08-20_project_handover_report.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/2026-08-20_project_handover_report.md) | 금일 진행된 전체 현행화, 장애 분석 및 조치 핸드오버 보고서 |
| **[MODIFY]** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/TODO.md) | 최근 조치 완료 태스크 및 진행 상황 업데이트 |

---

## 🔍 2. 상세 문제 원인 분석 및 해결 내용

### 2.1 [Issue 1] `Cannot find module '.../out/main'`
- **원인**: `package_desktop_dist.py` 빌드 과정에서 `VSCode-win32-x64/resources/app/out` 디렉토리에 빌드된 JS 파일이 누락됨.
- **해결**: `vscode/out` 디렉토리를 탐색하여 `resources/app/out` 디렉토리로 동기화 복사하는 단계 추가.

### 2.2 [Issue 2] CMD 콘솔 창 멈춤 (Uvicorn 표준 출력 점유)
- **원인**: `start /b` 명령으로 FastAPI 백엔드 실행 시 표준 입출력 스트림이 CMD 셸과 결합되어 콘솔이 대기 상태로 유지됨.
- **해결**: `powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '.\.venv\Scripts\python.exe' -ArgumentList 'coding-agent/src/main.py' -WindowStyle Hidden"`으로 완전 비동기 백그라운드 프로세스로 분리.

### 2.3 [Issue 3] 실행 시 0.1초 만에 튕김 (`NODE_MODULE_VERSION 116 vs 118` 미스매치)
- **원인**: Electron 27 런처는 Node ABI 버전 `118`을 요구하나, `vscode/node_modules`에 내장된 모듈은 Node v18 (`116`)용으로 빌드되어 `ERR_DLOPEN_FAILED` 예외 발생.
- **해결**: `Antigravity IDE` 내의 Electron 27 호환 precompiled C++ 모듈 14종(`@vscode/policy-watcher`, `spdlog`, `sqlite3`, `windows-mutex`, `native-keymap` 등)을 `resources/app/node_modules/`에 오버레이 복사.

### 2.4 [Issue 4] 클라이언트 윈도우 검은 화면 (Renderer Process Loading Failure)
- **원인**: 
  1. CJS 로더가 `require('./build/Release/foreground_love')`와 같이 확장자(`.node`) 없이 동적 로드 시 파일 미발견.
  2. `node_modules.asar` 파일 존재 시 asar loader가 `unpacked` 경로 탐색 중 실패.
- **해결**:
  1. 모든 `.node` 바이너리에 대해 확장자 없는 동명 별칭 사본 생성.
  2. `node_modules.asar`를 제거하고 순수 unpacked `resources/app/node_modules` 구조로 100% 직접 로딩하도록 변경.
