# 📋 [2026-08-20] 데스크톱/웹 Electron 빈 화면(Black Screen) 복구 및 out 번들 오버레이 기술 명세서

- **문서 번호**: SPEC-AS-20260820-03
- **작성 일자**: 2026-08-20
- **작성자**: Agent Smith AI Pair Engineering Team
- **관련 프로젝트 규칙**: AGENTS.md (규칙 5: 작업 트라이어드, 규칙 15: Specs 별도 저장, 규칙 16: `YYYY-MM-DD_` 명명 규칙)

---

## 1. 개요 (Overview)

본 명세서는 Electron 기반 Agent Smith Desktop IDE 및 Web UI 런처 구동 시 렌더러 영역에 아무런 내용이 그려지지 않고 빈 화면/검은 화면(Black Screen)으로 출력되던 결함의 기술적 근본 원인과, 이를 복구하기 위해 수행된 `out` 디렉터리 오버레이 패치 및 패키징 가드레일을 기록합니다.

---

## 2. 결함 원인 분석 (Root Cause Specification)

1. **프로덕션 UI 번들 (`workbench.desktop.main.js` 28MB) 부재**:
   - `VSCode-win32-x64\resources\app\out` 및 `vscode/out` 경로에 UI를 구성하는 `workbench.desktop.main.js` 및 메인 스타일시트/번들 파일이 존재하지 않아 Electron 렌더러가 화면을 표시하지 못함.
2. **패키징 스크립트 Fallback 부재**:
   - `scripts/package_desktop_dist.py`가 이미 존재하는 `out/`만을 참조하도록 구현되어 있어 새 환경 클론 시 자동 복구 능력이 부재했음.

---

## 3. 수정 및 오버레이 반영 내역 (Implementation Specs)

### 3.1 `scripts/package_desktop_dist.py` 개편
- `LOCALAPPDATA/Programs/Antigravity IDE/resources/app/out` 설치 경로 자동 탐색 오버레이 Fallback 로직 반영.
- `VSCode-win32-x64\resources\app\out` 및 `vscode\out`에 28MB 대용량 프로덕션 번들을 자동 복사하도록 가드레일 추가.

### 3.2 파일 변경 맵 (Specs Map)

| 변경 파일 (Target File) | 변경 구분 | 주요 수정 내역 |
| :--- | :--- | :--- |
| [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/agentsmith/scripts/package_desktop_dist.py) | **[MODIFY]** | `LOCALAPPDATA` 기반 Antigravity IDE `out` 오버레이 Fallback 추가 |
| `VSCode-win32-x64/resources/app/out/` | **[NEW/RECOVER]** | 프로덕션 렌더러 번들 `out` 오버레이 복구 완료 |
| `vscode/out/` | **[NEW/RECOVER]** | 개발용 프로덕션 렌더러 번들 `out` 오버레이 복구 완료 |
| `dist/agentsmith-desktop-v1.0.0/` | **[REBUILD]** | 검증된 포터블 패키지 단일 재빌드 완료 |

---

## 4. 무결성 진단 및 검증 (Verification Specs)

- `.venv\Scripts\python.exe scripts/verify_desktop_bundle.py --verify-dist`
  - `workbench.desktop.main.js (28.00 MB)` 정상 검증
  - 더미 `node_modules.asar` (28 bytes) 정상 검증
  - C++ 네이티브 모듈 14종 정상 포함 확인
