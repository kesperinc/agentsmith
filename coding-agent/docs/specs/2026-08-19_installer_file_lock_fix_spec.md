# 📄 2026-08-19 인스톨러 파일 잠금(사용 중) 자동 해제 및 Safe Multi-Retry 엔진 구축 상세명세서

본 명세서는 2026년 8월 19일 발생한 Windows 데스크톱 인스톨러(`AgentSmith_Desktop_Setup_v1.0.0.exe`) 설치 시 "파일이 사용 중이어서 설치 불가" 오류의 근본 원인 분석 및 해결 조치 내역을 정의합니다.

---

## 📂 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 요약 |
| :--- | :--- | :--- |
| **[MODIFY]** | [`scripts/build_desktop_installer.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/build_desktop_installer.py) | C# 인스톨러 내 `targetDir` 하위 모든 실행 프로세스 자동 탐색/종료(`KillLockedProcesses`) 및 Safe Multi-Retry/Rename 오버라이트 루틴(`SafeExtractEntry`) 탑재 |
| **[NEW]** | [`dist/AgentSmith_Desktop_Setup_v1.0.0.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/AgentSmith_Desktop_Setup_v1.0.0.exe) | 파일 잠금 무결성 및 자동 해제가 적용된 최신 단일 실행 설치 바이너리 재컴파일 완료 (156.31 MB) |
| **[NEW]** | [`coding-agent/docs/specs/2026-08-19_installer_file_lock_fix_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-19_installer_file_lock_fix_spec.md) | 파일 잠금 자동 해제 인스톨러 상세명세서 (본 문서) |

---

## 🛠️ 2. 근본 원인 분석 및 해결 방안

### A. 발생 원인
- 사용자가 이전에 Agent Smith IDE(`Code - OSS.exe`, 백엔드 `python.exe`, `node.exe` 등)를 실행했거나 백그라운드 프로세스가 `%LOCALAPPDATA%\Programs\AgentSmith` 폴더 내 특정 DLL/바이너리 파일을 점유하고 있을 때, 인스톨러가 해당 파일을 덮어쓰거나 폴더를 삭제하려다 Windows OS 수준의 `IOException` (File Locking)이 발생함.

### B. 적용된 3중 안전 가드레일
1. **설치 디렉터리 기반 포괄적 프로세스 자동 종료 (`KillLockedProcesses`)**:
   - 실행 중인 모든 프로세스의 모듈 경로(`MainModule.FileName`)를 실시간 검사하여 `%LOCALAPPDATA%\Programs\AgentSmith` 하위에서 구동 중인 모든 프로세스를 설치 시작 즉시 안전하게 강제 종료 및 대기.
2. **Safe Multi-Retry & Rename 백업 추출 엔진 (`SafeExtractEntry`)**:
   - 파일 추출 시 잠금 예외 발생 시 최대 5회 자동 재시도.
   - 마지막 시도에서도 실패할 경우 잠긴 기존 파일의 이름을 `.old_[hash]`로 변경(Move)하여 새 파일이 정상적으로 쓰여질 수 있도록 조치.
3. **사용자 친화적 다이얼로그 (Abort / Retry / Ignore)**:
   - 특수한 권한 잠금 상황에서도 중단 대신 [다시 시도], [무시하고 계속] 옵션을 제공하여 설치가 실패하지 않도록 보장.
