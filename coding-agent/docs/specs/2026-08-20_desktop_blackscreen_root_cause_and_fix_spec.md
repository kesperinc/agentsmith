# 📄 코드 변경 명세서 (Specs): 데스크톱 검은 화면(Black Screen) 원인 규명 및 영구 해결

- **작성 일자**: 2026-08-20
- **작성자**: Agent Smith AI Pair Engineer
- **대상 브랜치**: `feature/setup-git-guardrails`
- **목적**: 데스크톱 IDE 바이너리 실행 시 창 내부가 검은색으로 나타나던 문제의 근본 원인을 추적 및 규명하고, 패키징 스크립트(`scripts/package_desktop_dist.py`) 및 검증 도구(`scripts/verify_desktop_bundle.py`)에 영구 방지 코드를 적용함.

---

## 🛠️ 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 설명 |
| :--- | :--- | :--- |
| **[MODIFY] 패키징** | [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/agentsmith/scripts/package_desktop_dist.py) | 1. `VSCode-win32-x64`의 29.5MB 프로덕션 번들 `out/`을 개발용 7KB 스텁(`vscode/out`)으로 덮어쓰던 결함 제거<br>2. 28바이트 빈 더미 `node_modules.asar` (`{"files":{}}`)를 자동 생성하여 Electron asar 후킹 우회 및 100% Unpacked 모듈 자동 Fallback 구현<br>3. Antigravity IDE의 정상 검증된 Electron 27 ABI 118 네이티브 모듈 14종 및 의존성 전체를 `resources/app/node_modules`에 일괄 복사 |
| **[MODIFY] 검증도구** | [`scripts/verify_desktop_bundle.py`](file:///c:/dev/antigravity-workspace/agentsmith/scripts/verify_desktop_bundle.py) | `workbench.desktop.main.js`의 번들 크기(1MB 초과 여부) 정밀 검사 및 28바이트 더미 asar 감지 로직 추가 |
| **[NEW] 명세서** | [`coding-agent/docs/specs/2026-08-20_desktop_blackscreen_root_cause_and_fix_spec.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-20_desktop_blackscreen_root_cause_and_fix_spec.md) | 본 결함 분석 및 해결 명세서 |
| **[NEW] 핸드오버** | [`coding-agent/docs/2026-08-20_desktop_blackscreen_fix_and_handover_report.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/2026-08-20_desktop_blackscreen_fix_and_handover_report.md) | 검은 화면 결함 해결 상세 보고서 및 타 PC 작업 재개 가이드 |
| **[NEW] 인수인계** | [`docs/2026-08-20_handover.md`](file:///c:/dev/antigravity-workspace/agentsmith/docs/2026-08-20_handover.md) | 타 PC 작업 연속성 인수인계 종합 문서 |
| **[MODIFY] 로드맵** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/TODO.md) | 검은 화면 원인 규명 및 패키징 스크립트 수정 완료 반영 |

---

## 🔍 2. 검은 화면(Black Screen) 결함의 3대 근본 원인 분석

1. **원인 1: 번들링된 UI 결과물 덮어쓰기 (Bundle Overwrite Collision)**
   - `VSCode-win32-x64/resources/app/out/vs/workbench/workbench.desktop.main.js`는 **29.5 MB** 크기의 전체 번들 파일이었음.
   - 그러나 기존 `package_desktop_dist.py`가 개발용 임시 빌드 디렉터리인 `vscode/out`을 `resources/app/out`으로 무조건 덮어쓰면서, 실제 UI 코드가 7 KB짜리 스텁(Stub) 파일로 치환되어 렌더러가 아무것도 그리지 못하고 검은 화면이 됨.
2. **원인 2: `node_modules.asar` Asar Interceptor 충돌**
   - Electron은 `node_modules.asar` 파일이 존재할 경우 모듈 `require()` 요청을 내부 가상 파일시스템으로 가로챔.
   - 이로 인해 Unpacked 네이티브 모듈(`.node`)을 로드하지 못하고 `Cannot find module '../build/Release/vscode-sqlite3.node'` 등의 예외가 연속 발생함.
3. **원인 3: 더미 asar (`{"files":{}}`)를 통한 우회 기법**
   - Antigravity IDE 공식 빌드 구조와 동일하게 28바이트 크기의 `{"files":{}}` 구조를 가진 더미 asar 파일을 생성하여 Electron asar 인터셉터를 무력화하고, 실제 `resources/app/node_modules/` 하위의 네이티브 모듈 14종이 100% 정상 로딩되도록 변경.

---

## 🧪 3. 검증 결과

`VSCode-win32-x64` 디렉터리에 상기 3대 패치를 적용한 후 테스트 구동한 결과:
- `workbench#open()` 정상 호출
- SharedProcess 정상 연결
- Native Window 1 & 2 정상 렌더링
- 네이티브 C++ 모듈 14종(`sqlite3`, `windows-mutex`, `keymapping`, `conpty` 등) 0 에러 로딩 확인.
