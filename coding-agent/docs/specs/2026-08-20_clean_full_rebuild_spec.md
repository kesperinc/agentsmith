# 📋 [2026-08-20] [Clean Full Rebuild] 타임스탬프 동기화 오류 해결 및 클린 전면 리빌딩 기술 명세서

- **문서 번호**: SPEC-AS-20260820-06
- **작성 일자**: 2026-08-20
- **작성자**: Agent Smith AI Pair Engineering Team
- **관련 프로젝트 규칙**: AGENTS.md (규칙 5: 작업 트라이어드, 규칙 15: Specs 별도 저장, 규칙 16: `YYYY-MM-DD_` 명명 규칙)

---

## 1. 개요 (Overview)

본 명세서는 Syncthing 동기화 시 소스 파일의 수정 시각(Timestamp)이 변경되지 않아 발생하던 빌드 캐시 누락 현상을 해결하기 위해, 기존 빌드 캐시 및 `dist/` 산출물을 100% 삭제(Clean)하고 프론트엔드 UI 번들, 포터블 패키지 및 C# 단일 설치 바이너리를 전면 강제 재컴파일(Clean Full Rebuild)한 내역을 기록합니다.

---

## 2. 클린 리빌드 이행 명세 (Implementation Specs)

### 2.1 기존 캐시 삭제 및 UI 렌더러 오버레이
- `dist/` 배포 디렉터리 완전 강제 삭제 (`Remove-Item -Recurse -Force`).
- Antigravity IDE 원본의 최신 28.00 MB 메인 렌더러 번들 `out`을 `VSCode-win32-x64\resources\app\out` 및 `vscode\out`에 100% 강제 오버레이 복구.

### 2.2 C# 런처 환경 변수 가드레일 주입
- `build_desktop_installer.py` 내 `ProcessStartInfo`에 `%USERPROFILE%`, `%APPDATA%`, `%LOCALAPPDATA%`, `PYTHONUTF8`, `PYTHONIOENCODING` 환경 변수 주입 C# 코드 반영.

### 2.3 8대 무결성 진단 100% 통과 결과 (`verify_desktop_bundle.py --verify-dist`)

| 산출물 및 진단 항목 | 용량 및 상태 | 무결성 결과 |
| :--- | :--- | :--- |
| `dist/agentsmith-desktop-v1.0.0` | 포터블 배포 디렉터리 | **[Pass] 정상** |
| `workbench.desktop.main.js` | UI 메인 렌더러 번들 | **[Pass] 28.00 MB** |
| `node_modules.asar` | Direct Unpacked 더미 asar | **[Pass] 28 bytes** |
| C++ 네이티브 모듈 14종 | ABI 118 바이너리 | **[Pass] 100% 탑재** |
| `run_agentsmith_desktop.bat` | `%USERPROFILE%` 주입 런처 | **[Pass] 방어막 적용** |
| 백엔드 Vibe 엔진 | `coding-agent` & `.venv` | **[Pass] 정상 바인딩** |
| `agentsmith-desktop-v1.0.0.zip` | 포터블 압축 파일 | **[Pass] 314.26 MB** |
| `AgentSmith_Desktop_Setup_v1.0.0.exe` | C# Native 단일 인스톨러 | **[Pass] 312.21 MB** |

---

## 3. 최종 변경 맵 (Specs Map)

| 변경 파일 (Target File) | 변경 구분 | 주요 수정 내역 |
| :--- | :--- | :--- |
| [`scripts/build_desktop_installer.py`](file:///c:/dev/antigravity-workspace/agentsmith/scripts/package_desktop_dist.py) | **[MODIFY]** | C# 런처 내 ProcessStartInfo 환경 변수 가드레일 주입 |
| `dist/agentsmith-desktop-v1.0.0/` | **[REBUILD]** | 포터블 배포 디렉터리 전면 재패키징 완료 |
| `dist/AgentSmith_Desktop_Setup_v1.0.0.exe` | **[REBUILD]** | C# 단일 인스톨러 바이너리 (**312.21 MB**) 전면 재컴파일 완료 |
