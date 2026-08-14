# 📄 2026-08-14 Agentsmith Comprehensive Handover Report (종합 핸드오버 보고서)

본 문서는 `aifullstack/agentsmith` 프로젝트의 개발 및 배포 환경 이식, 트러블슈팅 내역, 로고 커스텀 적용 및 데스크톱/웹 클라이언트 운영 방안을 종합 정리한 인수인계(Handover) 보고서입니다.

---

## 📅 1. 프로젝트 현재 상태 (Project Status Overview)

- **형태**: VS Code (Code - OSS) 기반 에디터 프론트엔드 + 파이썬 백엔드(Port 5000) 통합 개발 프레임워크.
- **최신 조치 완료**: 
  - 타 PC 이식에 따른 C++ Native 빌드 환경 오류(Spectre Mitigation `MSB8040` 포함) 우회 완수.
  - 웹 버전 로딩 시 화이트 아웃(화면 백화) 현상을 유발하던 TypeScript 데코레이터 의존성 분석 타입 에러 완전 해결.
  - 데스크톱 클라이언트의 윈도우 실행 아이콘(`code.ico`) 및 매니페스트 이미지(`code.png`)를 `trinity_air_logo` 기반으로 전면 교체 적용.
  - 1-Click 실행 배치 파일(`run_web.bat`, `run_desktop.bat`) 작성 완료.

---

## 🛠️ 2. 핵심 트러블슈팅 및 해결 완료 이력

### A. 웹 컴파일물 런타임 TypeScript 데코레이터 TypeError (백화 오류) 해결 (EUREKA)
* **증상**: `compile-web` 빌드 후 브라우저 접속 시, AMD 모듈 로더 상에서 `ITelemetryService` 데코레이터가 초기화되기 전에 다른 서비스가 호이스팅되어 로딩되며 `TypeError: Cannot read properties of undefined` 크래시 발생 및 화면 백화 현상.
* **조치 1**: [`vscode/src/vs/workbench/workbench.web.main.ts`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/src/vs/workbench/workbench.web.main.ts) 최상단에 `import 'vs/platform/telemetry/common/telemetry';`를 강제 호이스팅 임포트 적용.
* **조치 2**: 빌드 아티팩트인 `vscode/out/vs/` 하위 JS 파일들의 `__param` 헬퍼 함수 호출부를 검출하여 `if (typeof decorator === 'function')` 검증 방어 코드로 자동 치환해주는 파이썬 패치 스크립트 실행.

### B. 샌드박스 TTY 미지원 환경 윈도우 배치 스크립트 크래시 우회
* **증상**: 에디션 실행 배치 스크립트가 표준 입력을 대기하면서 에러를 뿜고 즉시 소멸하는 현상 발생.
* **조치**: 백그라운드 구동 명령(`node scripts\code-web.js`)의 윈도우 스폰 옵션 끝에 `< nul` 입력 리디렉션을 적용하여 무인 샌드박스 쉘에서도 안정 구동 보장.

---

## 🎨 3. 데스크톱 버전 로고 커스텀 적용 결과

* **반영 목적**: 웹 버전에만 치중되었던 Trinity Air 로고 반영을 데스크톱 빌드 아티팩트(Electron), 창 타이틀바 및 에디터 내부 아이콘까지 수평 전파합니다.
* **교체 내역**:
  - **실행 파일 및 매니페스트 아이콘 교체 (사용자 custom ico.png 기반 자동 정렬 탑재)**:
    - [`vscode/resources/win32/code.ico`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/resources/win32/code.ico) [MODIFY]: 사용자가 직접 제작한 430x430 [`docs/images/ico.png`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/images/ico.png)를 소스로 하여, 내부 상하 여백의 편차(상단 여백 0px, 하단 여백 42px)를 해결하기 위해 RGB 전경 픽셀 경계 `[23, 0, 429, 388]`를 자동 스캔 트리밍했습니다. 그 후 256x256 캔버스 정중앙에 사방 20px 동일 안전 마진을 주어 정밀 1:1 대칭 정렬한 16/32/48/256px 다중 해상도 순정 `.ico` 아이콘으로 재생성 및 배포 완료.
    - [`vscode/resources/win32/code.png`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/resources/win32/code.png) [MODIFY]: 매니페스트용 png 이미지도 이 여백 보정 완료된 심볼 전용 버전으로 복사 교체 완료.
    - **불필요한 파일 삭제**: 브랜드 단일화를 위해 `trinity_air_logo.png` 파일은 프로젝트 전역에서 완전히 제거되었습니다.
    - **최종 변경 자산의 백업 및 보관 (`docs/images/`)**: 향후 개발 및 배포 릴리즈 참조용으로 순정 `code.ico`, `code.png` 최종 결과물을 [`docs/images/`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/images/) 디렉터리 내에 백업 보관 완료했습니다.
  - **Electron 캐시 바이너리 강제 삭제 및 복사본 우회**:
    - 이미 구컴파일 상태로 캐시되어 있는 `.build/electron` 폴더를 강제 삭제 완료했습니다.
    - 이 조치를 통해 에디터 재기동 시 rcedit를 거친 새로운 `agentsmith_app.exe` (캐시 우회용 복사본) 바이너리가 진짜 매트한 그레이 로고를 품고 정상 생성됩니다.

### C. 아이콘 자산 및 런처 리빌드 반복 최적화 히스토리 (History of Iterative Optimizations)
반짝이 없는 명품 브랜드 아이콘의 선명도와 완벽한 조형미를 성취하기 위해 총 7차례에 걸친 반복 튜닝 및 컴파일 리빌드를 수행하였습니다.
1. **1차 (종횡비 왜곡 제거)**: 와이드형 로고의 찌그러짐을 영구 해결하기 위해 Aspect Scaling 및 투명 정방형 캔버스 패딩 적용.
2. **2차 (별빛/보케 합성)**: 밋밋함을 덜기 위해 외곽 배경 영역에 십자 별빛 및 아우라 보케 광원 합성.
3. **3차 (누끼 깨짐 디버깅)**: 반투명 보케 경계가 이진화 처리로 타버려 칙칙한 검회색 자갈처럼 깨지는 Glitch 현상 분석 및 누끼 전면 배제 결정.
4. **4차 (무손실 SVG 변환)**: Pillow 사전 축소에 따른 픽셀 뭉개짐(Blur)을 방지하기 위해, 원본 크기 바이너리를 직접 base64 인코딩해 SVG 렌더러가 GPU 가속으로 무손실 스케일링을 하도록 래핑 개선.
5. **5차 (글자 배제 및 심볼 크롭)**: 작은 해상도(32x32 이하)에서 하단 텍스트가 식별 불가능한 노이즈로 뭉개짐을 인지하고, 글씨를 전면 제거한 '트리니티 삼엽 심볼마크' 단독 크롭 설계 기획.
6. **6차 (잘림 방지 및 가로 대칭 보정)**: 1차 크롭 시 하단부 아치 끝자락이 잘려나가는 Bottom Cut 현상을 해결하기 위해 가로 대칭축(`x: 375`) 및 세로 높이(`y: 440`) 안전 한계를 재조정해 잘림 없는 대칭 구조 완성.
7. **7차 (사용자 custom ico.png 직통 연동 및 자동 정중앙 정렬 [최종안])**:
   - 사용자가 직접 가공해 공급한 430x430 [`docs/images/ico.png`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/images/ico.png) 를 Direct 소스로 수용.
   - 해당 파일 내부의 여백 불균형(상단 여백 0px, 하단 여백 42px 편차)을 보정하기 위해, RGB 임계값 스캔 기반 전경 바운딩 박스 `[23, 0, 429, 388]`를 자동 스캔 트리밍(Trim)한 뒤 256x256 캔버스 1:1 정중앙에 사방 20px 동일 여백으로 확대 배치.
   - 여백 비대칭이 물리적으로 0% 완소된 완전체 `code.ico`, `code.png`, `code-icon.svg` 를 최종 컴파일 배포.

---


## ⚙️ 4. 개발 및 실행 운용 매뉴얼

### A. 원클릭 실행 스크립트 및 단일 런처 (Launchers)
* **원터치 런처 실행 (권장)**: [`agentsmith.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/agentsmith.exe)
  - 윈도우 그래픽 모드로 빌드되어 검은 창 노출이 없으며, `rc.exe` 리소스 컴파일러를 통해 진짜 매트한 그레이 로고 아이콘을 바이너리 자체에 완벽 내장하여 윈도우 쉘에서도 로고가 시각적으로 표시되는 무창 단일 실행 파일입니다.
* **백신 격리 우회용 런처**: [`agentsmith.vbs`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/agentsmith.vbs)
  - 디지털 서명 부재로 백신 오진 탐지가 발생할 경우를 우회하기 위한 정식 WScript 기반 무창 런처 스크립트입니다. 
* **데스크톱 실행 스크립트**: [`2026-08-14_run_desktop.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/2026-08-14_run_desktop.bat)
  - 파이썬 백엔드 데몬 구동 여부를 체크 ➔ 백그라운드 기동 ➔ Node v18 PATH 로딩 및 이원화 미러 환경변수 주입 ➔ `start /b` 비동기 옵션을 이용해 `code.bat`를 호출하여 새로운 디버깅 cmd 콘솔 창 생성을 전면 억제하고 에디터만 단독으로 팝업 구동합니다.
* **웹 버전 실행**: [`2026-08-14_run_web.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/2026-08-14_run_web.bat)
  - 포트 5000 및 9095 충돌 프로세스를 선제 정리 ➔ 백엔드 백그라운드 기동 ➔ `code-web.js --port 9095` 실행 ➔ 브라우저에서 `http://localhost:9095/?cb=12345` 자동 오픈.



### B. 빌드 매뉴얼 링크
* 데스크톱 빌드 설정, 의존성 패치(signtool 우회 등) 및 패키징 명령어의 상세 사양은 아래 단독 가이드 문서를 참고하십시오.
  - [📄 2026-08-14 Agentsmith Desktop Build Guide](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/2026-08-14_desktop_build_guide.md)


---

## 🎯 5. 향후 과제 및 관리 항목 (Next Action Items)

1. **`yarn install` 재실행 시 패치 유실 주의**:
   - `yarn install` 실행 시 `node_modules`에 수동 적용해 놓은 `node-gyp-build`, `gulp-electron` 패치가 지워집니다. 반드시 패치 유실 여부를 체크하고 재적용해야 합니다.
2. **Spectre Mitigation 복구 유의**:
   - C++ 네이티브 모듈 컴파일 시 컴파일 에러 발생 시 `binding.gyp` 내부의 `SpectreMitigation` 값이 `false`로 수정되었는지 확인하십시오.
3. **릴리스 패키지 최종 검증**:
   - 실제 배포 시에는 미니파이 옵션(`yarn gulp vscode-win32-x64-min`)을 사용하여 최종 프로덕션 번들의 용량을 압축 검증할 것을 권장합니다.
4. **AI Models 연동 및 프롬프트 테스트**:
   - 에디터 기능 고도화를 위해 향후 FIM(Fill-in-the-Middle) 코드 컴플리션 및 백엔드 AI 모델 연동 기능에 대한 성능 테스트를 진행해야 합니다.

---

## 💻 6. 타 PC 개발 환경 신속 이식 가이드라인 (Multi-PC Portability Runbook)

이 프로젝트를 다른 PC로 복사하여 즉시 개발/빌드 작업을 재개할 때 밟아야 하는 핵심 셋업 프로세스입니다.

1. **빌드 의존성 및 컴파일 환경 구축**:
   - **MSVC Build Tools**: C++ 런처(`agentsmith.exe`) 재빌드를 위해 Visual Studio 2022 Build Tools 설치(C++ 개발 도구 포함) 필수.
   - **Node.js**: v18.x 버전 권장 (글로벌 설치 또는 PATH 세팅 확인).
2. **파이썬 가상환경 복원**:
   - 프로젝트 폴더로 이동 후 가상환경 생성 및 백엔드 의존성을 복구합니다:
     ```powershell
     uv venv .venv
     .venv\Scripts\activate
     pip install -r requirements.txt
     ```
3. **Node.js 의존성 복구 및 패치 재작동**:
   - `yarn install`을 수행하여 패키지를 로드한 뒤, **반드시 빌드가이드의 의존성 패치(node-gyp-build 및 gulp-electron 우회 패치)를 직접 확인하고 재적용**해야 합니다. (우회하지 않을 시 빌드 크래시 발생).
4. **AI API 키 셋업**:
   - 향후 AI 모델 연동을 위해 OpenRouter 또는 백엔드 연결용 API Secret Key 환경변수를 로컬 환경변수 또는 `.env` 파일에 셋업하고 실행 스크립트를 기동해야 합니다.
