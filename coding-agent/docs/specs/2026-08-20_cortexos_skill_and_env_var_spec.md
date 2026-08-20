# 📋 [2026-08-20] CortexOS 스킬 설치 및 Windows 시스템/사용자 환경 변수 가드레일 기술 명세서

- **문서 번호**: SPEC-AS-20260820-04
- **작성 일자**: 2026-08-20
- **작성자**: Agent Smith AI Pair Engineering Team
- **관련 프로젝트 규칙**: AGENTS.md (규칙 5: 작업 트라이어드, 규칙 15: Specs 별도 저장, 규칙 16: `YYYY-MM-DD_` 명명 규칙)

---

## 1. 개요 (Overview)

본 명세서는 Agent Smith IDE 플랫폼 내 CortexOS 코어 스킬(`cortexos`) 구축 및 Windows 환경 변수(`%USERPROFILE%`, `%PYTHONUTF8%`, `%PYTHONIOENCODING%`, `%AGENTSMITH_BACKEND_PORT%`) 영구 등록 및 런처 방어 가드레일 반영 내역을 기록합니다.

---

## 2. 세부 이행 내역 (Implementation Specs)

### 2.1 CortexOS 스킬 구축
- **워크스페이스 스킬**: [`.agents/skills/cortexos/SKILL.md`](file:///c:/dev/antigravity-workspace/agentsmith/.agents/skills/cortexos/SKILL.md)
- **글로벌 스킬**: [`C:\Users\kespe\.gemini\config\skills\cortexos\SKILL.md`](file:///C:/Users/kespe/.gemini/config/skills/cortexos/SKILL.md)
- **주요 가드레일**:
  1. 수칙 14: 파이썬 uv 가상환경, 2바이트 다국어 UTF-8 Bom-less 및 사전에 지정한 현지어(한국어) 출력 강제.
  2. 수칙 5: 작업 트라이어드 (Plan-Code-Doc) 1:1:1 무결성.
  3. 수칙 15 & 16: Specs 문서 독립 관리 및 `YYYY-MM-DD_` 파일명 접두사 강제.
  4. SAST 보안 검사 규격 (`CORTEX-SEC-01` API키 검출, `02` eval/exec 검출, `03` SQL Injection 검사).

### 2.2 Windows 사용자 레지스트리 환경 변수 등록
- Windows Registry / Environment API를 사용하여 영구 등록:
  - `PYTHONUTF8 = 1`
  - `PYTHONIOENCODING = utf-8`
  - `AGENTSMITH_BACKEND_PORT = 5000`
  - `USERPROFILE = C:\Users\kespe`

### 2.3 런처 파일 환경 변수 방어벽 가드레일 적용 (Specs Map)

| 변경 파일 (Target File) | 변경 구분 | 주요 수정 내역 |
| :--- | :--- | :--- |
| [`.agents/skills/cortexos/SKILL.md`](file:///c:/dev/antigravity-workspace/agentsmith/.agents/skills/cortexos/SKILL.md) | **[NEW]** | CortexOS 에이전틱 코어 스킬 신규 생성 |
| [`C:\Users\kespe\.gemini\config\skills\cortexos\SKILL.md`](file:///C:/Users/kespe/.gemini/config/skills/cortexos/SKILL.md) | **[NEW]** | 글로벌 사용자 CortexOS 스킬 신규 생성 |
| [`run_agent_smith.bat`](file:///c:/dev/antigravity-workspace/agentsmith/run_agent_smith.bat) | **[MODIFY]** | `%USERPROFILE%` 및 UTF-8 환경변수 자동 주입 가드레일 추가 |
| [`run_agent_smith_web.bat`](file:///c:/dev/antigravity-workspace/agentsmith/run_agent_smith_web.bat) | **[MODIFY]** | `%USERPROFILE%` 및 UTF-8 환경변수 자동 주입 가드레일 추가 |
| [`2026-08-14_run_desktop.bat`](file:///c:/dev/antigravity-workspace/agentsmith/2026-08-14_run_desktop.bat) | **[MODIFY]** | `%USERPROFILE%` 및 UTF-8 환경변수 자동 주입 가드레일 추가 |
| [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/agentsmith/scripts/package_desktop_dist.py) | **[MODIFY]** | `RUNNER_BAT_CONTENT` 템플릿 내 환경 변수 방어 코드 추가 |
| `dist/agentsmith-desktop-v1.0.0/run_agentsmith_desktop.bat` | **[MODIFY]** | 배포용 런처 내 `%USERPROFILE%` 환경변수 주입 반영 |

---

## 3. 검증 결과 (Verification Specs)

- `Get-ChildItem env:`: `USERPROFILE`, `APPDATA`, `LOCALAPPDATA`, `PYTHONUTF8`, `PYTHONIOENCODING` 정상 등록 확인.
- 스킬 로드 확인: `.agents/skills/cortexos/SKILL.md` 및 글로벌 스킬 정상 감지 확인.
