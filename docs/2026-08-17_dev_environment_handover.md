# Agent Smith 개발환경 세팅 및 타 PC 이식 핸드오버 가이드 (Handover Runbook)

**문서 작성일**: 2026-08-17  
**문서 버전**: v1.0  
**작성자**: Agent Smith AI Pair Engineering Team  
**관련 프로젝트 규칙**: AGENTS.md (규칙 14: uv 파이썬 가상환경 및 Node.js 자동 셋업, UTF-8 BOM-less 인코딩, 날짜 명명 규칙)

---

## 1. 개요 (Overview)

본 문서는 다른 PC(신규 데스크톱/노트북 및 타 개발자 환경)에서 **Agent Smith Enterprise Coding Agent & Desktop IDE** 개발환경을 100% 동일하게 재현하고 실행할 수 있도록 작성된 종합 핸드오버 문서입니다.

---

## 2. 필수 개발 도구 사양 (Prerequisites & Environment Matrix)

타 PC 환경 세팅 전 아래 핵심 런타임 및 CLI 도구가 미리 설치되어 있어야 합니다.

| 도구 (Tool) | 권장 버전 | 검증된 버전 | 역할 | 비고 |
| :--- | :--- | :--- | :--- | :--- |
| **Windows OS** | Windows 10/11 64-bit | Windows 11 | 기본 실행 및 샌드박스 OS | PowerShell 5.1+ 권장 |
| **Python** | 3.11.x 이상 | 3.11.15 / 3.14 | 백엔드 Vibe 코딩 엔진 (`coding-agent`) | PATH 환경변수 등록 필요 |
| **uv** | 0.10.x 이상 | 0.11.19 | 초고속 파이썬 패키지 & 가상환경 관리 | `pip install uv` 또는 scoop |
| **Node.js** | v20.0.0 LTS 이상 | v24.14.1 (npm 11.11.0) | VSCode Electron 클라이언트 & 웹 빌드 | |
| **Bun** | v1.0.0 이상 | 1.3.11 | Mem0 Vector Store & 고성능 패키지 런타임 | `powershell -c "irm bun.sh/install.ps1 \| iex"` |
| **Git** | v2.40.0 이상 | 2.53.0 | 저장소 형상관리 및 브랜치 전략 | UTF-8 인코딩 설정 필요 |

---

## 3. 타 PC 1-Click 환경 구축 절차 (Step-by-Step Setup Guide)

### Step 1: 저장소 클론 및 UTF-8 인코딩 가드레일 설정

PowerShell 또는 CMD를 열고 프로젝트를 클론합니다.

```powershell
# 1. 저장소 클론
git clone <repository-url> agentsmith
cd agentsmith

# 2. Git 한글 및 UTF-8 인코딩 깨짐 방지 설정
git config --global core.quotepath false
git config --global gui.encoding utf-8
git config --global i18n.commitencoding utf-8
```

### Step 2: Python 가상환경 (`.venv`) 구축 및 백엔드 의존성 설치

프로젝트 규칙에 따라 가상환경은 `uv`를 사용하며 루트 디렉터리의 `.venv` 경로에 구축합니다.

```powershell
# 1. uv를 통한 .venv 가상환경 생성
uv venv .venv

# 2. coding-agent 백엔드 필수 의존성 라이브러리 설치
uv pip install -r coding-agent/requirements.txt --python .venv\Scripts\python.exe
```

*설치되는 파이썬 핵심 패키지 목록*:
- `fastapi`, `uvicorn`: Vibe 코딩 에이전트 백엔드 API 서버 (Port 5000)
- `pydantic`, `httpx`, `requests`: 스키마 검증 및 비동기 HTTP 통신
- `pytest`: 테스트 자동화 가드레일
- `jinja2`, `python-dotenv`: 템플릿 렌더링 및 환경 변수 로드

### Step 3: Mem0 & Qdrant 기억 저장소 자동 셋업

에이전트의 지속적 기억(Memory Persistence)을 위한 Mem0 및 로컬 Qdrant Vector Store 설정을 자동으로 실행합니다.

```powershell
# Mem0 자동 셋업 스크립트 기동 (Bun 패키지 설치 및 .agentsmith/mem0_config.json 생성)
powershell -ExecutionPolicy Bypass -File 2026-08-14_setup_mem0.ps1
```

*생성되는 주요 설정 위치*:
- `.agentsmith/mem0_config.json`: Qdrant 로컬 벡터 DB (`./.agentsmith/mem0_qdrant_db`) 및 Gemini 임베딩 모델(768 차원) 설정

### Step 4: 환경 변수 (`.env`) 설정

프로젝트 루트 디렉터리에 `.env` 파일을 생성하고 필요한 API Key를 기입합니다.

```env
# Agent Smith API Key 바인딩
GEMINI_API_KEY=your_gemini_api_key_here
# 또는
GOOGLE_API_KEY=your_google_api_key_here

# 백엔드 서버 설정
PORT=5000
HOST=127.0.0.1
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
```

---

## 4. 애플리케이션 실행 가이드 (Launch Guide)

### [방법 A] 데스크톱 IDE 클라이언트 실행 (권장)

다음 원클릭 배치 파일 중 하나를 실행합니다:

```cmd
:: 1. 루트의 run_agent_smith.bat 실행
run_agent_smith.bat

:: 또는 상세 백엔드 점검 포함 런처 실행
2026-08-14_run_desktop.bat
```

**자동 실행 매커니즘**:
1. Port 5000번에서 파이썬 백엔드 서버(`coding-agent/src/main.py`)가 구동 중인지 점검.
2. 미구동 시 `.venv\Scripts\python coding-agent/src/main.py`를 백그라운드 프로세스로 자동 기동.
3. `vscode` 빌드 디렉터리의 Agent Smith Desktop Client (`Code - OSS.exe`) 실행.

### [방법 B] 웹(Web) 브라우저 버전 실행

```cmd
2026-08-14_run_web.bat
```

---

## 5. 환경 세팅 무결증 검증 (Verification Checklist)

새로운 PC에서 세팅 완료 후 아래 체크리스트를 실행하여 동작을 검증합니다.

```powershell
# 1. 파이썬 가상환경 및 패키지 설치 상태 검증
.venv\Scripts\python.exe -m pip list

# 2. Mem0 설정 파일 검증
Test-Path .agentsmith\mem0_config.json

# 3. Node 및 Bun 패키지 상태 검증
bun pm ls
```

- [x] `.venv` 가상환경에 `fastapi`, `uvicorn`, `pydantic` 등이 정상 설치되어 있는가?
- [x] `.agentsmith/mem0_config.json` 설정 파일이 존재하는가?
- [x] `run_agent_smith.bat` 실행 시 백엔드 서버(Port 5000) 및 Desktop IDE Window가 정상 팝업되는가?

---

## 6. 트러블슈팅 및 가드레일 (Troubleshooting & Guardrails)

### Issue 1: 5000번 포트가 이미 사용 중이라는 오류 발생 시
- **원인**: 이전 백엔드 서버 프로세스가 종료되지 않고 남아있는 경우
- **해결책**:
  ```powershell
  # 5000번 포트 점유 프로세스 확인
  netstat -ano | findstr :5000
  # 해당 PID 강제 종료
  taskkill /PID <PID> /F
  ```

### Issue 2: 한글 깨짐 또는 인코딩 에러 발생 시
- **원인**: Windows 기본 ANSI (CP949) 코드가 적용된 경우
- **해결책**:
  - 배치 파일 실행 시 `chcp 65001 > nul` 포함 확인
  - 환경변수 `set PYTHONUTF8=1` 및 `set PYTHONIOENCODING=utf-8` 적용 확인

### Issue 3: `.venv` 가상환경 중복 생성 주의
- **가드레일**: 기존에 `.venv` 폴더가 존재하면 새로 가상환경을 생성하지 않고 기존 `.venv`를 재사용합니다. 패키지 추가 시 `uv pip install <package> --python .venv\Scripts\python.exe` 명령을 이용하세요.

---

**문서 위치**: [`docs/2026-08-17_dev_environment_handover.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/2026-08-17_dev_environment_handover.md)
