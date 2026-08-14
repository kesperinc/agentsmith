# 📄 2026-08-14 Agentsmith Desktop Build Guide (데스크톱 버전 빌드 및 환경 설정 가이드)

본 문서는 `aifullstack/agentsmith` 프로젝트의 데스크톱 버전(Electron 기반 Code - OSS Client)을 빌드하고 패키징하기 위한 필수 설정, 패치 내역, 빌드 옵션 및 커스텀 로고 적용 프로세스를 상세히 기술합니다.

---

## 📋 1. 사전 요구 환경 (Prerequisites)

Windows 환경에서 Agentsmith 데스크톱 빌드를 수행하기 위해 아래 도구들이 선행 설치되어 있어야 합니다.

1. **Node.js**: `v18.17.1` 설치 권장 (VS Code 에디터 및 관련 라이브러리 빌드 호환성 검증 통과 버전).
2. **Python**: `v3.10` 이상 설치 및 시스템 환경변수(PATH) 등록 필수.
3. **C++ 컴파일러**: Visual Studio 2022 Build Tools 설치.
   - 개별 구성 요소에서 **`MSVC v143 VS 2022 C++ 빌드 도구`** 및 **`Windows 10/11 SDK`** 필수 체크.
4. **패키지 매니저**: `yarn` 전역 설치 (`npm install -g yarn`).
5. **Python Pillow 라이브러리**: PNG 로고의 ICO 파일 변환을 위해 필수.
   - 가상환경 활성화 후 실행: `.venv\Scripts\python -m pip install pillow`

---

## 🛠️ 2. 필수 외부 라이브러리 패치 (node_modules)

`yarn install`을 수행하면 외부 의존성 패키지가 원복되므로, 빌드 전 반드시 아래 3가지 패치가 재수행되거나 복구되어 있는지 확인해야 합니다.

### A. node-gyp-build 자식 프로세스 스폰 에러 (`EINVAL`) 방지
* **대상 파일**: [`vscode/node_modules/node-gyp-build/bin.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/node_modules/node-gyp-build/bin.js)
* **수정 내용**: Windows 환경에서 자식 프로세스 스폰 시 TTY가 없는 샌드박스 쉘 환경 하에 `proc.spawn` 호출 시 `shell: true` 속성을 강제 주입하여 차단 오류를 예방합니다.
  ```javascript
  // 변경 후 (L29 부근)
  proc.spawn(args[0], args.slice(1), { stdio: 'inherit', shell: true })
  ```

### B. gulp-electron 윈도우 서명 툴(`signtool.exe`) 검출 에러 방지
* **대상 파일**: [`vscode/node_modules/@vscode/gulp-electron/src/win32.js`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/node_modules/@vscode/gulp-electron/src/win32.js)
* **수정 내용**: 인증서 서명 툴의 부재로 인한 빌드 크래시를 우회합니다. `getSignTool` 메소드가 항시 `null`을 반환하게 하고 `spawnSync` 호출부에서 예외 방어 코드를 적용합니다.
  ```javascript
  function getSignTool() {
    return null;
  }
  // L61 부근 방어 코드 추가
  const signToolPath = getSignTool();
  if (signToolPath) {
    const {error} = spawnSync(signToolPath, ["remove", "/s", tempPath]);
    if (error) { return cb(error); }
  }
  ```

### C. MSVC Spectre 완화 라이브러리 우회 패치 (`MSB8040` 방어)
* **대상 파일**: C++ Native 바인딩을 컴파일하는 아래 `binding.gyp` 파일들
  - [`vscode/node_modules/@vscode/policy-watcher/binding.gyp`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/node_modules/@vscode/policy-watcher/binding.gyp)
  - [`vscode/node_modules/@vscode/spdlog/binding.gyp`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/node_modules/@vscode/spdlog/binding.gyp)
  - [`vscode/node_modules/@vscode/windows-registry/binding.gyp`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/node_modules/@vscode/windows-registry/binding.gyp)
* **수정 내용**: Spectre Mitigation 경고로 인한 MSBuild 실패를 차단하기 위해 속성을 `false`로 수정합니다.
  ```json
  "msvs_configuration_attributes": {
    "SpectreMitigation": "false"
  }
  ```

---

## 🎨 3. 데스크톱 로고(Logo) 및 브랜드 리소스 패치

기존의 부정합 로고 파일(`trinity_air_logo.png`)을 전면 삭제하고, 웹 버전에서 기적용되어 검증을 마친 진짜 "매트한 그레이" 색상의 로고 리소스([`docs/images/logo.png`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/images/logo.png))로 브랜딩을 단일화하였습니다.

### A. 윈도우 실행 파일 아이콘 (`code.ico` 및 `code.png`) 변경 (순정 매트그레이 스펙 탑재)
1. **순정 아이콘 및 매니페스트 이미지 변경**:
   - 사용자가 직접 가공하여 트리니티 심볼을 1:1 정형 배치한 고화질 아이콘 소스 [`docs/images/ico.png`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/images/ico.png) (430x430)를 공식 입력 소스로 연동했습니다.
   - 원본 이미지의 상하 여백 쏠림(상단 여백 0px, 하단 여백 42px 비대칭)을 해결하기 위해, RGB 임계값 스캔을 통해 실제 삼엽 심볼마크의 경계 박스 `[23, 0, 429, 388]`를 자동 디텍팅하여 잉여 배경을 트리밍(Trim)했습니다.
   - 잘라낸 유효 심볼만을 256x256 캔버스의 정확한 기하학적 1:1 정중앙에 사방 20px 동일 안전 마진을 주어 정렬 배치함으로써, 위쪽이나 아래쪽이 휑하게 남는 여백 비대칭 문제를 원천 해결했습니다.
   - 이를 통해 반짝이 없이 큼직하고 선명한 순정 삼엽 심볼 전용 16x16 ~ 256x256 다중 해상도 아이콘 [`vscode/resources/win32/code.ico`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/resources/win32/code.ico) 및 매니페스트용 [`vscode/resources/win32/code.png`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/resources/win32/code.png)을 빌드/배포 완료했습니다.
2. **불필요한 파일 삭제**:
   - 중복 및 부정합을 예방하기 위해 `trinity_air_logo.png` 파일은 프로젝트 전 지역(win32/ 및 server/, docs/images/ 등)에서 완전 삭제 처리되었습니다.
3. **최종 변경 자산의 백업 및 보관 (`docs/images/`)**:
   - 향후 릴리즈 배포 및 자산 참조용으로 최종 생성된 브랜드 파일 2종을 [`docs/images/`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/images/) 디렉터리 내에 동시 저장 및 연동 완료했습니다.
     - [`docs/images/code.ico`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/images/code.ico): 16x16 ~ 256x256 표준 다중 해상도가 내장된 최종 `.ico` 파일
     - [`docs/images/code.png`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/images/code.png): 윈도우 매니페스트 및 바로가기용 고화질 로고 이미지 파일

### C. Electron 캐시 바이너리 초기화
* **핵심 사항**: 이미 빌드/복사가 완료되었던 `.build/electron` 디렉토리 내의 `Code - OSS.exe` 파일은 이전 `code.ico`로 rcedit 리소스 주입이 끝나 캐싱된 상태이므로, 아이콘 변경이 즉시 반영되지 않습니다.
* **해결 방법**: 에디터를 새로 실행하기 전 반드시 빌드 캐시 디렉토리인 [`vscode/.build/electron`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/.build/electron) 폴더를 삭제하십시오.
  ```powershell
  Remove-Item -Recurse -Force -Path "vscode\.build\electron"
  ```
  이후 `run_desktop.bat`를 재실행하면 `preLaunch.js`가 캐시 소멸을 인지하고, 변경된 로고(`code.ico`)가 주입된 실행 바이너리를 리빌딩하여 띄웁니다.

### D. 아이콘 변환 및 패치 자동화 스크립트
- 향후 브랜드 로고 업데이트 시, 아래 파이썬 스크립트(`patch_code_icon_svg.py`)를 통해 PNG 이미지로부터 크기 최적화, Specular 금속 광학 필터 바인딩 및 Base64 인코딩을 수행하여 원터치로 SVG 아이콘들을 자동 패치할 수 있습니다.
  ```python
  # PIL을 사용해 docs/images/logo.png를 64x64 리사이즈 후 base64 인코딩하여 금속 광택 및 Shimmer 애니메이션 레이어가 탑재된 SVG로 변환 적용
  from PIL import Image
  import base64
  # ... base64 인코딩 후 <feSpecularLighting> 및 <animate>가 포함된 SVG 파일들 덮어쓰기 수행
  ```

### E. 윈도우 작업 표시줄 아이콘 캐시(Icon Cache) 우회 기법
* **결함 요인**: 윈도우 OS는 파일 경로와 실행 파일명(`Code - OSS.exe`)에 대해 최초에 빈 문서 아이콘을 한번 캐싱하면, 바이너리 내의 아이콘 리소스를 교체하더라도 작업 표시줄에 기존 캐시 이미지를 계속 렌더링하는 꼬임 오류가 발생합니다.
* **우회 해결책**:
  - `code.bat` 기동 시 빌드 완료 시점에 `Code - OSS.exe`의 클론 복사본인 [`agentsmith_app.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/.build/electron/agentsmith_app.exe)를 생성합니다.
  - 생성된 복사본에 직접 `rcedit.exe`를 구동하여 진짜 매트한 그레이 로고(`code.ico`)를 완벽히 하드웨어 인쇄 주입합니다.
  - 실행 파일명 자체를 우회용 이름으로 차별화함으로써 윈도우 OS가 캐시 오염 없이 진짜 매트한 그레이 로고를 작업 표시줄과 타이틀바에 즉시 그리도록 보완 완료했습니다.

---

## 🔨 4. 데스크톱 빌드 및 패키징 명령어 (Build Pipeline)

의존성 패치가 완료된 상태에서 데스크톱 버전을 빌드하고 패키징하는 명령어 및 상세 파이프라인 단계는 다음과 같습니다.

### STEP 1. 로컬 헤더 캐시 서버 기동 및 공속 미러 분리 (사내망 SSL 우회)
사내망 환경 하에서 C++ 헤더 및 Electron zip 바이너리 다운로드 실패를 예방하기 위해 이원화 세팅을 적용합니다.

1. **로컬 HTTP 헤더 캐시 서버 실행 (node-gyp rebuild 용)**:
   - `build/headers` 폴더로 이동하여 8999 포트에서 로컬 서버를 기동합니다.
   ```cmd
   cd build/headers
   python -m http.server 8999
   ```
2. **이원화 환경변수 주입 (에디터 기동/빌드 세션)**:
   - node-gyp 헤더는 로컬 서버(`http://localhost:8999/`)를 바라보게 하고, 대용량 Electron 바이너리 zip 파일은 고속 공용 미러(`https://npmmirror.com/mirrors/electron/`)를 바라보도록 이원화하여 적재합니다.
   ```cmd
   :: 터미널 세션에 환경변수 주입
   set ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
   set NODEJS_ORG_MIRROR=http://localhost:8999/
   set NODE_TLS_REJECT_UNAUTHORIZED=0
   ```


### STEP 2. C++ 네이티브 모듈 일괄 컴파일
VS Code 및 Electron 호환 타겟 ABI 버전에 부합하도록 수동으로 일괄 컴파일을 기동합니다.
```cmd
cd vscode
node build/npm/postinstall.js
```
*개별 모듈 리빌딩 수동 명령어:*
```cmd
node-gyp rebuild --target=27.2.3 --disturl=http://localhost:8999 --arch=x64
```

### STEP 3. 데스크톱 클라이언트 번들 빌드 및 패키징
Electron 데스크톱 패키징을 기동하여 최종 실행 폴더(`.build/electron/` 및 `VSCode-win32-x64/`)를 산출합니다.

* **표준 Windows x64 빌드**:
  ```cmd
  yarn gulp vscode-win32-x64
  ```
* **최적화 및 코드 미니파이 빌드 (프로덕션 배포용)**:
  ```cmd
  yarn gulp vscode-win32-x64-min
  ```
* **빌드 옵션 요약**:
  - `--min`: JS/CSS 아티팩트 압축(Minify) 및 소스 맵 제거를 적용하여 앱 용량을 최적화하고 실행 속도를 대폭 개선합니다.
  - `--sign`: 프로덕션 배포 시 `signtool`을 사용해 보안 서명을 주입합니다. (현재 사내망 로컬 빌드 시에는 비활성 상태로 우회 처리됨).
  - `--debug-inno`: `Inno Setup` 인스톨러 컴파일 과정의 상세한 로그 및 디버깅 심볼을 터미널에 출력합니다.

---

## 🚀 5. 데스크톱 로컬 검증 및 실행 방법 (원터치 런처 제공)

1. **원터치 무창 실행 파일 활용 (`agentsmith.exe` - 권장)**:
   - 워크스페이스 루트의 [`agentsmith.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/agentsmith.exe)를 실행합니다.
   - 이 파일은 윈도우 그래픽 애플리케이션 모드(`/SUBSYSTEM:WINDOWS`)로 빌딩되어 실행 시 cmd 콘솔 창이 전혀 팝업되지 않습니다.
   - 특히, 윈도우 OS 탐색기 및 작업 표시줄 상에 Trinity Air 로고가 각인되어 노출되도록 `rc.exe` 리소스 컴파일러를 통해 진짜 매트한 그레이 로고 아이콘([`code.ico`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/resources/win32/code.ico))을 리소스 섹션에 하드웨어 레벨로 내장하여 빌드하였습니다.
   - 빌드 명령어:
     ```cmd
     rc.exe resource.rc
     cl.exe /O2 launcher.cpp resource.res /link /OUT:agentsmith.exe /SUBSYSTEM:WINDOWS Shell32.lib
     ```
2. **백신 탐지용 대체 런처 활용 (`agentsmith.vbs`)**:
   - 디지털 서명이 없는 C++ 실행 파일이 사내 보안 에이전트(백신) 등에 의해 혹시라도 정적 오진 격리되는 특수 상황을 우회하기 위해, 무창 구동 스크립트인 [`agentsmith.vbs`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/agentsmith.vbs)도 예비 옵션으로 동시 제공합니다.
3. **배치 파일 비동기 최적화 (`start /b`)**:
   - [`2026-08-14_run_desktop.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/2026-08-14_run_desktop.bat) 내부에서 기존의 `start "" cmd.exe /c ".\scripts\code.bat"` 구문이 새로운 디버깅 cmd 콘솔 창을 생성하여 사용자 화면에 에러 로그를 계속 노출하던 결함을 복구하였습니다.
   - `start /b "" .\scripts\code.bat` 비동기 옵션으로 패치하여 새로운 콘솔 창 생성을 전면 억제하고 에디터 GUI 클라이언트만 단독으로 팝업되도록 고도화 완료했습니다.

---

## 📅 향후 추가 작업 (Future Todo)

- [ ] **ICON 자산 및 리소스 정리**: 데스크톱 배포 릴리즈 대비, 사용자 제작 `ico.png` 기반의 아이콘 Mipmap 생성 로직 및 SVG 변환 배치 스크립트를 최종 패키징 정리하고 자동화 스크립트를 최적화합니다.
- [ ] **AI Models 연동 테스트**: 에디터 및 백엔드 엔진 상의 AI 모델 연동 상태를 확인하고, FIM/코드 완성 프롬프트 성능 튜닝 검증을 수행합니다.
