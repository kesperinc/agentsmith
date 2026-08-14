# 📄 2026-08-14 Agentsmith Full Setup Runbook (환경 구축 및 실행 가이드)

본 문서는 다른 Windows PC 환경에서 `aifullstack/agentsmith` 저장소를 처음부터 다운로드하고, C++ 네이티브 모듈 컴파일, 웹 빌드, 시작 배치 파일 셋업까지 원스톱으로 완수하여 실행하기 위한 단일 런북(Runbook)입니다.

---

## 📋 1. 사전 요구 조건 (Prerequisites)

1. **Node.js**: `v18.17.1` 설치 권장 (VS Code 에디터 및 관련 라이브러리 빌드 정합용).
2. **Python**: `v3.10` ~ `v3.14` 설치 및 PATH 등록.
3. **C++ 컴파일 환경**: Visual Studio 2022 Build Tools 설치 (개별 구성 요소에서 `MSVC v143 VS 2022 C++ 빌드 도구` 필수 체크).
4. **패키지 매니저**: `yarn` 전역 설치 (`npm install -g yarn`).

---

## 🔒 2. 사내망 SSL 프록시 및 Mirror 서버 우회 셋업

사내망 환경에서 Electron 및 Node 헤더 다운로드 시 발생하는 SSL 인증서 오류(`unable to get local issuer certificate`)를 우회하기 위해 로컬 HTTP 캐시 서버를 구동합니다.

1. **로컬 HTTP 헤더 서버 기동**:
   - `vscode/build/headers/` 내부에 미리 받아둔 캐시 파일이 존재합니다. 다음 명령으로 8999 포트에서 로컬 서버를 기동합니다.
   ```cmd
   python -m http.server 8999
   ```
2. **SSL 검증 차단 및 Mirror 주입**:
   - 터미널 쉘에 아래 환경변수를 적재하여 로컬 서버를 바라보게 강제합니다.
   ```cmd
   set ELECTRON_MIRROR=http://localhost:8999/
   set NODEJS_ORG_MIRROR=http://localhost:8999/
   set NODE_TLS_REJECT_UNAUTHORIZED=0
   ```

---

## 🛠️ 3. node_modules 외부 라이브러리 2종 우회 패치

`yarn install` 이후 윈도우 환경 컴파일 오류 및 서명 검증 오류를 예방하기 위해 아래 2개 외부 모듈 소스코드를 정밀 수정(패치)합니다.

### A. node-gyp-build 자식 프로세스 스폰 에러 (`EINVAL`) 방지
- **대상 파일**: [`vscode/node_modules/node-gyp-build/bin.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/node_modules/node-gyp-build/bin.js)
- **수정 위치** (L29 부근): `proc.spawn` 호출 시 옵션 객체에 `shell: true` 속성을 강제 주입합니다.
  ```javascript
  // 변경 전
  proc.spawn(args[0], args.slice(1), { stdio: 'inherit' })
  // 변경 후
  proc.spawn(args[0], args.slice(1), { stdio: 'inherit', shell: true })
  ```

### B. gulp-electron 윈도우 서명 툴(`signtool.exe`) 검출 에러 방지
- **대상 파일**: [`vscode/node_modules/@vscode/gulp-electron/src/win32.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/node_modules/@vscode/gulp-electron/src/win32.js)
- **수정 위치 1** (L20 부근): `getSignTool` 메소드가 항시 `null` 을 반환하게 변경.
  ```javascript
  function getSignTool() {
    return null;
  }
  ```
- **수정 위치 2** (L61 부근): `spawnSync` 를 호출할 때 `signToolPath` 가 `null` 인 경우의 TypeError 크래시 방어 코드를 적용합니다.
  ```javascript
  // 변경 후 (방어 코드 추가)
  const signToolPath = getSignTool();
  if (signToolPath) {
    const {error} = spawnSync(signToolPath, ["remove", "/s", tempPath]);
    if (error) {
      return cb(error);
    }
  }
  ```

---

## 🔨 4. C++ 네이티브 모듈 일괄 컴파일 및 캐시 정리

`yarn install` 은 변경된 `binding.gyp` 파일을 원복시키므로, 의존성 설치가 끝난 후 아래 스크립트를 사용해 개별 수동 빌드하여 Spectre 완화 라이브러리 결함(`MSB8040`)을 우회합니다.

1. **gyp 파일 SpectreMitigation 비활성화 일괄 자동 치환**:
   - `node_modules` 하위의 모든 `binding.gyp` 에서 `'SpectreMitigation': 'Spectre'` 설정을 찾아 `'SpectreMitigation': 'false'` 로 자동 변경하는 파이썬 스크립트(`patch_gyp.py`)를 기동합니다.
2. **MSBuild 캐시 정리**:
   - 컴파일 성공을 위해 에러 이력이 있는 모듈 하위의 `build/` 폴더를 강제 삭제합니다.
3. **Electron ABI 타겟 개별 리빌딩**:
   - 아래 명령을 각 네이티브 모듈(`windows-registry`, `spdlog`, `windows-process-tree`) 폴더에서 기동합니다.
   ```cmd
   node-gyp rebuild --target=27.2.3 --disturl=http://localhost:8999 --arch=x64
   ```

---

## 🌐 5. 웹 컴파일 및 데코레이터 순환 의존성 해결 (TypeScript)

### A. 웹 컴파일 메모리 증가 기동
웹 번들 컴파일 시의 OOM을 해결하기 위해 메모리를 상향하여 Gulp 빌드를 돌립니다.
```cmd
node --max-old-space-size=8192 ./node_modules/gulp/bin/gulp.js compile-web
```

### B. 데코레이터 TypeError 해결 (EUREKA)
웹 빌드가 0 errors로 완료된 후 브라우저 렌더링 시 AMD 모듈 의존성 순환으로 인해 `ITelemetryService` 등이 `undefined`로 호출되어 화면 백화 현상이 일어납니다. 이를 예방하기 위해 빌드물 아티팩트인 `vscode/out/vs/` 하위의 모든 JS 파일의 `__param` 정의를 타입 방어 코드로 패치합니다.
* **패치 적용 자동화 스크립트**: [`patch_helpers_vs.py`](file:///C:/Users/MZC01-SUNKIM317/.gemini/antigravity-ide/brain/ceddd73a-8db0-46eb-a6db-f91e7da4d691/scratch/patch_helpers_vs.py) 실행.
  ```python
  # decorator 실행 전 function 인지 안전 체크
  replacement = "if (typeof decorator === 'function') decorator(target, key, paramIndex)"
  ```

---

## 🚀 6. 에디터 및 백엔드 실행 검증

1. **웹 에디터 기동**:
   - `2026-08-14_run_web.bat` 구동 ➔ 백엔드(5000) 자동 상주 기동 ➔ 9095 웹 서버 백그라운드 구동 ➔ 브라우저에서 `http://localhost:9095/?cb=12345` (캐시 무력화 쿼리 포함)로 접속하여 화면 무결 렌더링 검증.
2. **데스크톱 에디터 기동**:
   - `2026-08-14_run_desktop.bat` 구동 ➔ 데스크톱 Electron 클라이언트 팝업 확인.
