# 📄 코드 및 환경 설정 변경 명세서 (Specs): 단독 워크스페이스 분리 이식 및 .env 환경설정 체계 구축

- **문서 일자**: 2026-08-20
- **작성자**: Agent Smith AI Lead / Pair Engineer
- **대상 브랜치**: `feature/setup-git-guardrails`
- **목적**: 기존 `c:\dev\antigravity-workspace\aifullstack\agentsmith` 경로에서 상위 `c:\dev\antigravity-workspace\agentsmith`로 프로젝트를 독립 분리(Standalone Migration)하여 운영할 수 있도록, 하드코딩된 경로를 전면 동적 상대경로 및 `.env` 환경변수 기반 아키텍처로 리팩토링함.

---

## 🛠️ 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 설명 |
| :--- | :--- | :--- |
| **[NEW] 설정** | [`.env.example`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/.env.example) | 프로젝트 루트 환경변수 템플릿 (`AGENTSMITH_WORKSPACE_ROOT`, 포트, API 키 등) |
| **[NEW] 설정** | [`.env`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/.env) | 로컬 개발 환경용 루트 환경설정 파일 |
| **[NEW] 설정** | [`coding-agent/.env.example`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/.env.example) | 백엔드 파이썬 엔진 전용 환경변수 템플릿 |
| **[NEW] 설정** | [`coding-agent/.env`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/.env) | 백엔드 파이썬 엔진 전용 환경설정 파일 |
| **[MODIFY] 메인** | [`coding-agent/src/main.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/main.py) | `load_dotenv` 자동 로딩 탑재 및 `AGENTSMITH_BACKEND_HOST`, `PORT` 환경변수 기반 uvicorn 가동 |
| **[MODIFY] 세션DB** | [`coding-agent/src/db/session_manager.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/db/session_manager.py) | `AGENTSMITH_DATA_DIR` 및 `AGENTSMITH_WORKSPACE_ROOT` 환경변수 기반 DB 경로 동적 해석 |
| **[MODIFY] 기억DB** | [`coding-agent/src/memory/mem0_manager.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/memory/mem0_manager.py) | `AGENTSMITH_DATA_DIR` 및 `AGENTSMITH_WORKSPACE_ROOT` 환경변수 기반 Mem0 경로 동적 해석 |
| **[MODIFY] 런처** | [`2026-08-14_run_desktop.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/2026-08-14_run_desktop.bat) | 하드코딩된 `aifullstack` 절대경로를 동적 상대경로(`%~dp0build\node`)로 수정 |
| **[MODIFY] 런처** | [`2026-08-14_run_web.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/2026-08-14_run_web.bat) | 하드코딩된 `aifullstack` 절대경로를 동적 상대경로(`%~dp0build\node`)로 수정 |
| **[MODIFY] 빌더** | [`build/build_agent_smith.bat`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/build/build_agent_smith.bat) | 상위 폴더 구조에 영향받지 않도록 `AGENT_SMITH_DIR=%~dp0..` 동적 지정 |
| **[MODIFY] 패키징** | [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/package_desktop_dist.py) | 루트 `.env.example` 및 `.env` 릴리즈 번들 동기화 복사 로직 반영 |
| **[NEW] 명세서** | [`coding-agent/docs/specs/2026-08-20_standalone_workspace_migration_and_env_config_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-20_standalone_workspace_migration_and_env_config_spec.md) | 본 변경 명세서 |

---

## 🔍 2. 핵심 변경 내용 및 환경변수 명세

### 2.1 환경변수 정의 (`.env`)
```bash
# 1. Project & Workspace Root Path (Standalone Configuration)
AGENTSMITH_WORKSPACE_ROOT=c:\dev\antigravity-workspace\agentsmith
AGENTSMITH_DATA_DIR=

# 2. Backend Orchestrator Server Configuration
HOST=127.0.0.1
PORT=5000
AGENTSMITH_BACKEND_HOST=127.0.0.1
AGENTSMITH_BACKEND_PORT=5000
AGENTSMITH_MCP_PORT=3000
AGENTSMITH_ENV=development

# 3. Encoding & Python Environment Guardrails
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
SpectreMitigation=false

# 4. AI Provider API Keys
GEMINI_API_KEY=
GOOGLE_API_KEY=
OPENROUTER_API_KEY=
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# 5. On-Premise Red Hat OpenShift AI (RHOAI) vLLM Configuration
RHOAI_VLLM_ENDPOINT_URL=http://qwen-coder.rhoai.svc:8000/v1
```

### 2.2 동적 경로 처리 원칙
- 모든 배치 파일(`*.bat`)은 `%~dp0`(스크립트 파일이 위치한 폴더)을 기준으로 하위 폴더(`build\node`, `vscode`, `coding-agent`)를 동적으로 탐색합니다.
- 파이썬 백엔드는 `Path(__file__).resolve()` 기준으로 상위 루트의 `.env`를 자동 로드하며, 환경변수 `AGENTSMITH_WORKSPACE_ROOT`가 주어질 경우 해당 경로를 최우선 작업 공간으로 인식합니다.

---

## 🧪 3. 검증 결과 (Verification Results)

1. **.env 환경변수 로딩 테스트**:
   ```cmd
   python -c "from src.main import app; import os; print('FastAPI App:', app.title); print('AGENTSMITH_WORKSPACE_ROOT:', os.getenv('AGENTSMITH_WORKSPACE_ROOT'))"
   ```
   - 출력:
     ```text
     FastAPI loaded: Antigravity VibeForge Enterprise Backend API
     AGENTSMITH_WORKSPACE_ROOT: c:\dev\antigravity-workspace\agentsmith
     AGENTSMITH_BACKEND_PORT: 5000
     ```
2. **사전/사후 무결성 진단**:
   - `python scripts/verify_desktop_bundle.py --all` ➔ `[✓]` 전체 통과 완료.
