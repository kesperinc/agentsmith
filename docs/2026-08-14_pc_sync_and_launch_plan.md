# [최종] 웹 버전 복구 및 데스크톱/웹 시작 배치 파일 생성 계획

본 계획서는 타 PC 이식 과정에서 롤백된 외부 라이브러리(node_modules) 3종 우회 패치를 복구하고, 일괄 네이티브 컴파일(`postinstall.js`)을 적용하는 트러블슈팅 조치를 포함합니다. 아울러 웹 에디터 복구를 위한 웹 컴파일(`compile-web`) 수행 및 백엔드 서버 연동 시작 배치 파일 생성을 완료합니다.

## User Review Required

> [!IMPORTANT]
> **롤백된 라이브러리 패치 복구**:
> `yarn install`에 의해 초기화(원복)되었던 윈도우 환경 우회 패 2종을 복구하고 일괄 컴파일을 수행합니다.
> 1. `node-gyp-build/bin.js`: spawn 옵션에 `shell: true` 추가하여 Windows 자식 프로세스 스폰 오류(`EINVAL`) 방지.
> 2. `@vscode/gulp-electron/src/win32.js`: Windows SDK signtool 체크 오류를 우회하도록 `getSignTool() { return null; }` 처리.
> 3. **일괄 컴파일**: `node build/npm/postinstall.js` 를 직접 가동해 모든 네이티브 바인딩을 Electron v27.2.3 스펙에 맞춰 정식 링킹.

> [!IMPORTANT]
> **웹 에디터 하얀 화면 복구**:
> * `compile-web` Gulp 빌드를 수행하여 수십 개의 미빌드 브라우저용 익스텐션을 복구하고 데코레이터 런타임 오류를 완벽히 해결합니다.
>   `node --max-old-space-size=8192 ./node_modules/gulp/bin/gulp.js compile-web`

---

## Proposed Changes

### [1] 롤백된 라이브러리(node_modules) 패치 및 일괄 컴파일

- **패치 대상 파일** (수정 완료):
  - [`vscode/node_modules/node-gyp-build/bin.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/node_modules/node-gyp-build/bin.js) (shell: true 추가)
  - [`vscode/node_modules/@vscode/gulp-electron/src/win32.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/node_modules/@vscode/gulp-electron/src/win32.js) (signtool 우회)
- **일괄 컴파일 실행**:
  ```cmd
  cd vscode
  set PATH=C:\dev\antigravity-workspace\aifullstack\agentsmith\build\node;%PATH%
  set ELECTRON_MIRROR=http://localhost:8999/
  set NODEJS_ORG_MIRROR=http://localhost:8999/
  set NODE_TLS_REJECT_UNAUTHORIZED=0
  node build/npm/postinstall.js
  ```

---

### [2] 웹 컴파일 (`compile-web`) 구동

- **웹 컴파일 실행**:
  ```cmd
  node --max-old-space-size=8192 ./node_modules/gulp/bin/gulp.js compile-web
  ```

---

### [3] 데스크톱/웹 원클릭 시작 배치 파일 생성

#### [NEW] [`run_agent_smith_desktop.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith_desktop.bat)
- **기능**: 백엔드 포트(5000) 구동 체크 및 미구동 시 자동 백그라운드 기동 ➔ 내장 Node v18 PATH 주입 ➔ 데스크톱 클라이언트(`scripts/code.bat`)를 독립창으로 실행.

#### [MODIFY] [`run_agent_smith_web.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith_web.bat)
- **기능**: 백엔드 포트(5000) 구동 체크 및 자동 기동 ➔ 기존 9095 포트 프로세스 강제 정리 ➔ `code-web.js --port 9095` 백그라운드 기동 ➔ 웹 브라우저(`http://localhost:9095`) 자동 기동.

---

## Verification Plan

### Automated Verification
- `compile-web` 빌드 타스크 및 `postinstall.js` 컴파일이 0 errors로 완료되는지 확인합니다.
- 배치 파일 더블 클릭 시 백엔드 및 프론트엔드가 각 포트(5000, 9095)에서 충돌 없이 동작하는지 확인합니다.

### Manual Verification
- `run_agent_smith_web.bat`을 실행해 웹 브라우저에서 하얀 화면 없이 에디터 Workbench UI가 완전하게 렌더링되는지 확인합니다.
