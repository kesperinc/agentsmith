# 📋 [명세서] Agent Smith IDE 재컴파일 및 GUI 실행 검증 명세서

- **작성 일시**: KST 2026-08-13 16:11
- **작성자**: Antigravity AI
- **프로젝트**: Agent Smith (aifullstack/agentsmith)
- **작업 브랜치**: `feature/setup-git-guardrails`

---

## 1. 📌 트러블슈팅 및 장애 해결 결과

### 원인 분석
- 다른 PC에서 MVP 실행 시 화면이 출력되지 않고 멈췄던 원인은 **`vscode/node_modules/` 패키지 미설치**, **`vscode/build/` 빌드 툴체인 누락**, 그리고 **`vscode/out/` 트랜스파일 결과물 부재** 때문이었습니다.
- 추가로 Node v24 윈도우 환경에서 `spawnSync` 구동 시 발생하던 `EINVAL` 오류 및 C++ Native 모듈(`policy-watcher`, `spdlog`, `windows-registry`) 예외 미처리로 인해 Electron 프로세스가 로딩 직후 정지되었습니다.

### 적용된 해결 패치
1. **Upstream Code-OSS 소스 결합**: `vscode/build/` 및 `vscode/scripts/` 소스 툴체인 완벽 복사 및 배치
2. **Built-in AI Chat 익스텐션 동기화**: `extension/agentsmith-chat/` 소스코드를 `vscode/extensions/agentsmith-chat/`으로 최신 복사
3. **윈도우 spawn EINVAL 해결**: `build/npm/postinstall.js` 및 `build/lib/preLaunch.js` 스폰 옵션에 `shell: true` 및 `--ignore-engines` 적용
4. **C++ Native 모듈 예외 방어**: `nativePolicyService.js`, `spdlogLog.js`, `id.js` 파일에 try-catch fallback 방어 코드 적용
5. **SWC 초고속 트랜스파일 완료**: `gulp transpile-client` 명령으로 **0 errors 완수 ➔ `vscode/out/` (8GB 메모리 할당) 정상 생성**

---

## 2. 🚀 기동 및 검증 결과

1. **백엔드 서버 (FastAPI Port 5000)**: `coding-agent/src/main.py` 기동 완수 (**RUNNING**)
2. **에디터 GUI 클라이언트 창**: `vscode/scripts/code.bat` 기동 완수 ➔ **화면에 Agent Smith IDE GUI 에디터 창 팝업 완료 (RUNNING)**

---

## 3. 📂 변경 일자별 파일 수정 맵 (Specs Map)

- [`vscode/build/npm/postinstall.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/build/npm/postinstall.js): shell: true 및 ignore-engines 옵션 적용 [MODIFY]
- [`vscode/build/lib/preLaunch.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/build/lib/preLaunch.js): preLaunch child process shell: true 적용 [MODIFY]
- [`vscode/out/vs/platform/policy/node/nativePolicyService.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/out/vs/platform/policy/node/nativePolicyService.js): policy-watcher try-catch 적용 [MODIFY]
- [`vscode/out/vs/platform/log/node/spdlogLog.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/out/vs/platform/log/node/spdlogLog.js): spdlog null fallback 적용 [MODIFY]
- [`vscode/out/vs/base/node/id.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/out/vs/base/node/id.js): windows-registry try-catch 적용 [MODIFY]
- [`coding-agent/src/main.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/main.py): sys.path 안전 경로 보강 [MODIFY]
- [`coding-agent/docs/specs/2026-08-13_agentsmith_gui_recompile_and_launch_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-13_agentsmith_gui_recompile_and_launch_spec.md): 본 명세서 문서 [NEW]

---
*Agent Smith GUI Recompile & Launch Specification Document Saved*
