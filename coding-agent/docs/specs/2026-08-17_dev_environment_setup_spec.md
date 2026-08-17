# 2026-08-17 Agent Smith 개발환경 점검 및 셋업 명세서 (Dev Environment Setup Spec)

**작성일자**: 2026-08-17  
**작성자**: Agent Smith Engineering Team  
**상태**: 완료 (Completed)

---

## 1. 개요 및 목적
본 명세서는 Agent Smith 프로젝트의 개발환경 무결성을 점검하고, 누락되어 있던 파이썬 가상환경(`.venv`) 생성 및 백엔드 의존성 패키지 설치, Mem0 메모리 DB 셋업을 완료한 내역과 타 PC 이식을 위한 핸드오버 문서 수립 내역을 기록합니다.

---

## 2. 세부 변경 및 구축 내역 (Specs Map)

### 2.1. Python 가상환경 및 의존성 구축
- **수행 명령어**: `uv venv .venv`
- **의존성 설치**: `uv pip install -r coding-agent/requirements.txt --python .venv\Scripts\python.exe`
- **설치된 패키지**: `fastapi`, `uvicorn`, `pydantic`, `httpx`, `requests`, `pytest`, `jinja2`, `python-dotenv` 등 총 28개 백엔드 의존 라이브러리 정상 로드.

### 2.2. Mem0 및 Qdrant 로컬 벡터 DB 자동 셋업
- **수행 명령어**: `powershell -ExecutionPolicy Bypass -File 2026-08-14_setup_mem0.ps1`
- **생성 결과**: `.agentsmith/mem0_config.json` 생성 완료 및 Bun 환경에 `mem0ai` 추가 완료.

### 2.3. 핸드오버 문서 (Handover Runbook) 생성
- **생성 파일**: [`docs/2026-08-17_dev_environment_handover.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/2026-08-17_dev_environment_handover.md)
- **주요 내용**:
  - 도구 사양 (Python 3.11+, uv 0.11+, Node.js v24+, Bun 1.3+, Git 2.53+)
  - 타 PC에서 1-Click 구축을 위한 Step-by-Step 가이드
  - 데스크톱 IDE (`run_agent_smith.bat`, `2026-08-14_run_desktop.bat`) 및 웹 버전 기동 절차
  - 5000번 포트 점유 해제 및 UTF-8 BOM-less 가드레일 트러블슈팅

---

## 3. 변경 파일 맵 (Specs File Map)

| 구분 | 파일 경로 | 변경 내용 |
| :--- | :--- | :--- |
| **NEW** | [`.venv/`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/.venv) | `uv`로 파이썬 3.14/3.11 가상환경 신규 생성 |
| **NEW** | [`.agentsmith/mem0_config.json`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/.agentsmith/mem0_config.json) | Mem0 & Qdrant 설정 파일 생성 |
| **NEW** | [`docs/2026-08-17_dev_environment_handover.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/2026-08-17_dev_environment_handover.md) | 타 PC 복제용 개발환경 셋업 핸드오버 문서 |
| **NEW** | [`coding-agent/docs/specs/2026-08-17_dev_environment_setup_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-17_dev_environment_setup_spec.md) | 개발환경 구축 명세서 |

---

## 4. 검증 결과
- 파이썬 가상환경 `.venv` 정상 작동 및 패키지 28개 확인 완료.
- Mem0 셋업 스크립트 정상 완주 확인 완료.
- 핸드오버 문서 및 명세서 파일 작성 완료.
