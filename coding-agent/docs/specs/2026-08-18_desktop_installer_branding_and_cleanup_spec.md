# 2026-08-18 Agent Smith 인스톨러 브랜드 로고 각인 및 재설치 감지/삭제 기능 명세서 (Desktop Installer Branding & Cleanup Spec)

**작성일자**: 2026-08-18  
**작성자**: Antigravity AI Coding Agent  
**상태**: 완료 (Completed)  

---

## 1. 개요 및 목적
본 명세서는 Agent Smith Windows Native C# 단일 설치 프로그램(`AgentSmith_Desktop_Setup_v1.0.0.exe`)에 **순정 매트그레이 브랜드 로고 아이콘(`code.ico`) 하드웨어 각인**, **배포 패키지 내 브랜드 자산 번들링**, **기존 설치 버전 감지 및 완전 삭제(Clean Install)/덮어쓰기(Update)/취소(Cancel) 선택 대화상자**를 탑재하여 재컴파일을 완료한 상세 내역을 기록합니다.

---

## 2. 세부 변경 및 구축 내역 (Specs Map)

### 2.1. 배포 번들링 스크립트 브랜드 로고 자산 동기화 (`package_desktop_dist.py`)
- `docs/images/` 디렉터리에 위치한 순정 매트그레이 브랜드 아이콘 및 이미지(`code.ico`, `code.png`, `logo.png`, `code-icon.svg`, `ico.png`)를 배포 폴더(`dist/agentsmith-desktop-v1.0.0/resources/`)에 자동 복사하도록 로직 추가.

### 2.2. C# 인스톨러 재설치 감지 대화상자 및 프로세스 정리 로직 고도화 (`build_desktop_installer.py`)
1. **기존 설치 여부 감지**: `%LocalAppData%\Programs\AgentSmith` 디렉터리 및 런처 배치 파일 존재 여부를 자동 검사.
2. **3-Button 선택 대화상자 (MessageBoxButtons.YesNoCancel)**:
   - `[예(Yes)]`: 기존 설치 디렉터리를 완전히 삭제 후 깨끗하게 새로 설치 (Clean Reinstall).
   - `[아니오(No)]`: 기존 파일 유지 및 덮어쓰기(Update) 설치.
   - `[취소(Cancel)]`: 설치 프로세스 즉시 종료.
3. **프로세스 자동 종료**: 실행 중인 Agent Smith 프로세스(`Code - OSS`, `agentsmith_app`, `agentsmith_editor`)를 자동 정리하여 파일 잠금 및 덮어쓰기 실패 방어.
4. **안전한 덮어쓰기 파일 추출**: `ZipArchive`의 개별 엔트리 순회 및 `entry.ExtractToFile(path, true)` 적용으로 덮어쓰기 시 `IOException` 원천 차단.
5. **바로가기 로고 아이콘 바인딩**: 바탕화면 및 시작메뉴 바로가기(`Agent Smith Desktop IDE.lnk`) 생성 시 `$TargetDir\resources\code.ico`를 아이콘 소스로 연동.

### 2.3. 컴파일러 브랜드 로고 아이콘 각인 (`/win32icon`)
- Windows Native C# Compiler `csc.exe` 호출 시 `/win32icon:docs\images\code.ico` 옵션을 주입하여, 생성되는 단일 실행파일 `dist/AgentSmith_Desktop_Setup_v1.0.0.exe` 파일 자체에 순정 매트그레이 로고 아이콘을 하드웨어 레벨로 내장 완료.

---

## 3. 변경 파일 맵 (Specs File Map)

| 구분 | 파일/폴더 경로 | 변경 및 빌드 내용 |
| :--- | :--- | :--- |
| **MODIFY** | [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/package_desktop_dist.py) | `resources/` 디렉터리에 브랜드 로고 자산 자동 복사 로직 추가 |
| **MODIFY** | [`scripts/build_desktop_installer.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/build_desktop_installer.py) | 재설치 감지/삭제 대화상자, 덮어쓰기 추출 로직 및 `/win32icon` 컴파일러 옵션 추가 |
| **NEW/OVERWRITE** | [`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) | **브랜드 로고 각인 및 재설치 대화상자가 탑재된 단일 설치 파일 (156.28 MB)** |
| **NEW** | [`coding-agent/docs/specs/2026-08-18_desktop_installer_branding_and_cleanup_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-18_desktop_installer_branding_and_cleanup_spec.md) | 브랜드 로고 각인 및 삭제 확인 기능 명세서 |

---

## 4. 검증 결과
- **컴파일 성공 코드**: `0`
- **바이너리 사이즈**: `156.28 MB`
- **인스톨러 아이콘**: 탐색기에서 `AgentSmith_Desktop_Setup_v1.0.0.exe` 파일에 순정 매트그레이 브랜드 로고 아이콘이 완벽히 표시됨을 확인.
- **재설치 대화상자**: 기존 설치 폴더 감지 시 3-Button(삭제 후 재설치 / 덮어쓰기 / 취소) 대화상자가 정상 팝업됨을 확인.
