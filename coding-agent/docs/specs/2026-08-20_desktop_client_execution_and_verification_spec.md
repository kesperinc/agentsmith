# 📋 [2026-08-20] [/plan-eng-review] 데스크톱 클라이언트 구동 및 무결성 정밀 진단 기술 명세서

- **문서 번호**: SPEC-AS-20260820-05
- **작성 일자**: 2026-08-20
- **작성자**: Agent Smith AI Pair Engineering Team
- **관련 프로젝트 규칙**: AGENTS.md (규칙 5: 작업 트라이어드, 규칙 15: Specs 별도 저장, 규칙 16: `YYYY-MM-DD_` 명명 규칙)

---

## 1. 개요 (Overview)

본 명세서는 [/plan-eng-review] 사전 검토를 통해 확정된 Agent Smith 데스크톱 IDE 클라이언트 및 백엔드 엔진(Port 5000) 구동 절차와, 최종 8대 산출물 무결성 진단 통과 내역을 기록합니다.

---

## 2. 구동 및 검증 세부 명세 (Implementation & Verification Specs)

### 2.1 런처 방어막 및 환경 변수 주입
- `%USERPROFILE%` 누락 방지 가드레일: `if not defined USERPROFILE set "USERPROFILE=%SystemDrive%\Users\%USERNAME%"` 적용.
- 인코딩 주입: `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8` 반영.

### 2.2 8대 무결성 진단 통과 결과 (`verify_desktop_bundle.py --verify-dist`)
1. **배포 폴더**: `dist/agentsmith-desktop-v1.0.0` (정상 통과)
2. **UI 메인 렌더러 번들**: `workbench.desktop.main.js` (**28.00 MB** 정상 통과)
3. **Unpacked Fallback 더미 asar**: `node_modules.asar` (**28 bytes** 정상 통과)
4. **C++ 네이티브 모듈**: `@vscode/sqlite3`, `node-pty`, `native-keymap` 등 **14종 100% 포함** (정상 통과)
5. **런처 가드레일**: `run_agentsmith_desktop.bat` 비동기 기동 (정상 통과)
6. **백엔드 서버 바인딩**: `coding-agent` 백엔드 엔진 Port 5000 (정상 통과)
7. **포터블 배포 ZIP Archive**: `agentsmith-desktop-v1.0.0.zip` (**291.72 MB** 정상 통과)
8. **C# Native 단일 실행 설치 파일**: `AgentSmith_Desktop_Setup_v1.0.0.exe` (**289.68 MB** 정상 통과)

---

## 3. 최종 산출물 맵 (Specs Map)

| 산출물 종류 | 파일 경로 (File Path) | 용량 및 상태 |
| :--- | :--- | :--- |
| **데스크톱 포터블 런처** | [`dist/agentsmith-desktop-v1.0.0/run_agentsmith_desktop.bat`](file:///c:/dev/antigravity-workspace/agentsmith/dist/agentsmith-desktop-v1.0.0/run_agentsmith_desktop.bat) | 100% 정상 작동 |
| **C# Native 단일 설치 파일** | `dist/AgentSmith_Desktop_Setup_v1.0.0.exe` | **289.68 MB** 완결 생성 |
| **포터블 배포 ZIP** | `dist/agentsmith-desktop-v1.0.0.zip` | **291.72 MB** 완결 생성 |
| **CortexOS 코어 스킬** | [`.agents/skills/cortexos/SKILL.md`](file:///c:/dev/antigravity-workspace/agentsmith/.agents/skills/cortexos/SKILL.md) | 정상 설치 완료 |
