# 2026-08-19 Agent Smith 타 PC 핸드오버 검토, 로컬 브랜치 현행화 및 C# 브랜딩 인스톨러 재빌드 명세서 (PC Sync & Installer Rebuild Spec)

**작성일자**: 2026-08-19  
**작성자**: Antigravity AI Pair Engineering Team  
**상태**: 완료 (Completed)  

---

## 1. 개요 및 목적
본 명세서는 타 PC에서 진행 후 핸드오버 문서(`docs/2026-08-17_handover.md`, `docs/2026-08-17_dev_environment_handover.md`)에 작성된 작업 내역과 원격 깃허브 브랜치(`feature/setup-git-guardrails`) 상태를 종합 검토하여 로컬 PC 개발 환경을 100% 현행화(Sync)하고, 브랜딩 아이콘(`code.ico`) 적용 및 파일 잠금 정리 로직이 반영된 C# Native 단일 인스톨러 바이너리를 최종 재빌드한 변경 내역을 기록합니다.

---

## 2. 세부 변경 및 현행화 구축 내역 (Specs Map)

### 2.1. Git 브랜치 검토 및 저장소 상태 현행화
- **원격 브랜치 검토**: 
  - `origin/feature/setup-git-guardrails` 원격 브랜치 최신 커밋(`ae858ff`)과 로컬 HEAD 커밋이 일치함을 확인.
  - 핸드오버 문서와 8/18 추가 스크립트/명세서의 변경 사항을 로컬 워킹 트리에 현행화.
- **파이썬 가상환경 (`.venv`) 무결성 점검**:
  - `uv pip list`를 통한 `fastapi`, `uvicorn`, `pydantic`, `httpx` 등 28개 백엔드 의존성 가상환경 무결성 검증 완료.

### 2.2. 브랜딩 아이콘 적용 C# Native 인스톨러 컴파일 및 빌드
- **C# 인스톨러 스크립트 (`scripts/build_desktop_installer.py`)**:
  - `csc.exe` 컴파일러 매개변수에 `/win32icon:docs/images/code.ico` 옵션을 전달하여 실행 파일 자체에 전용 브랜딩 아이콘 정밀 주입.
  - 기존 실행 중인 `Code - OSS`, `agentsmith_app`, `agentsmith_editor` 프로세스 자동 강제 종료 로직을 통한 파일 잠금 예방.
  - `ZipArchive` extraction 유닛을 개편하여 기존 폴더 및 파일에 대한 안전한 덮어쓰기 지원.
- **배포 번들링 스크립트 (`scripts/package_desktop_dist.py`)**:
  - `docs/images/` 내 브랜드 아이콘 및 로고 자산(`code.ico`, `code.png`, `logo.png` 등)을 번들의 `resources/` 디렉터리로 복사 지원.
  - `VSCode-win32-x64` 또는 `vscode/.build/electron` 경로 자동 감지 복사 로직 적용.

### 2.3. Syncthing 동기화 최적화 (`.stignore`)
- `vscode/.build/`, `vscode/out/`, `vscode/node_modules/` 등 무거운 빌드 바이너리 및 임시 파일 배제 규칙 최적화.

---

## 3. 변경 파일 맵 (Specs File Map)

| 구분 | 파일 경로 | 변경 내용 |
| :--- | :--- | :--- |
| **MODIFY** | [`.stignore`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/.stignore) | Syncthing 빌드 임시 및 컴파일 바이너리 제외 규칙 추가 |
| **MODIFY** | [`scripts/build_desktop_installer.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/build_desktop_installer.py) | 브랜딩 아이콘 주입, 프로세스 자동 정리를 통한 파일 잠금 방지 및 덮어쓰기 인스톨러 구축 |
| **MODIFY** | [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/package_desktop_dist.py) | 브랜드 로고 자산 복사 및 배포 번들링 로직 개편 |
| **MODIFY** | [`run_agent_smith_dev.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/run_agent_smith_dev.bat) | 데스크톱 개발 환경 구동 스크립트 현행화 |
| **NEW** | [`coding-agent/docs/specs/2026-08-19_pc_sync_and_installer_rebuild_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-19_pc_sync_and_installer_rebuild_spec.md) | 현행화 및 C# 브랜딩 인스톨러 재빌드 상세 명세서 작성 |

---

## 4. 최종 검증 결과 (Verification Results)

1. **배포 번들 및 인스톨러 컴파일**:
   - `dist/agentsmith-desktop-v1.0.0.zip` (123.16 MB) 정상 패키징 확인.
   - `dist/AgentSmith_Desktop_Setup_v1.0.0.exe` (123.15 MB, 117.44 MB compressed payload) C# 브랜딩 인스톨러 단일 바이너리 생성 완료.
2. **가상환경 점검**:
   - `.venv` 내 백엔드 의존성 패키지 28종 100% 무결성 확인.
