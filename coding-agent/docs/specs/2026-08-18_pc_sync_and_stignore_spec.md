# 2026-08-18 Agent Smith 로컬 PC 브랜치 현행화 및 Syncthing 설정 명세서 (PC Sync & Syncthing Setup Spec)

**작성일자**: 2026-08-18  
**작성자**: Antigravity AI Coding Agent  
**상태**: 완료 (Completed)  

---

## 1. 개요 및 목적
본 명세서는 다른 PC에서 진행되었던 원격 깃허브 저장소의 최신 작업 결과물(`main`, `staging`, `feature`, `hotfix` 브랜치)을 로컬 PC에 안전하게 이식(현행화)한 내역과, 개발 환경에서 생성되는 무거운 바이너리 및 빌드 임시 파일들이 Syncthing 동기화를 통해 타 PC로 불필요하게 공유되지 않도록 `.stignore` 규칙을 최적화한 내역을 기록합니다.

---

## 2. 세부 변경 및 구축 내역 (Specs Map)

### 2.1. Git 브랜치 검토 및 Fast-Forward 동기화
- **브랜치 현황 점검**: 
  - `main`, `staging`, `hotfix/agentsmith` 브랜치는 원격 저장소와 완전히 일치하여 최신 상태임을 확인.
  - `feature/setup-git-guardrails` 브랜치가 원격 최신 대비 3개 커밋 뒤처진 것을 확인.
- **비추적(Untracked) 파일 충돌 해결**:
  - 로컬 작업 디렉터리에 원격과 겹치는 비추적 파일들(`.stignore`, `package.json`, 2026-08-17 관련 문서 등)로 인해 병합 충돌 오류 발생.
  - 충돌 방지를 위해 임시 백업 디렉터리(`_backup_untracked_20260818/`)를 생성하여 비추적 파일들을 격리.
- **Git Pull 실행**:
  - 로컬 `feature/setup-git-guardrails` 브랜치를 원격 최신 커밋(`ae858ff`)으로 성공적으로 Fast-forward 동기화 완료.
- **백업 파일 검증 및 정리**:
  - 백업된 비추적 파일들과 풀(Pull)을 통해 다운로드된 파일들 간의 텍스트 무결성을 비교 분석하여 차이가 없음을 입증.
  - 검증 완료 후 임시 백업 폴더를 완전 영구 삭제.

### 2.2. Syncthing 동기화 규칙 최적화 (`.stignore`)
- **목적**: 개발 환경 전반의 무거운 컴파일 결과물, 바이너리, 가상환경, 패키지 모듈이 Syncthing으로 동기화되어 발생하는 네트워크 부하 및 바이너리 꼬임 방지.
- **추가된 제외 규칙**:
  - VSCode 클라이언트 빌드 임시 폴더 (`vscode/.build/`)
  - VSCode 아웃풋 디렉터리 (`vscode/out/`, `vscode/out-build/`)
  - VSCode 내부 의존성 모듈 (`vscode/node_modules/`)
  - VSCode CLI 빌드 바이너리 및 타겟 (`vscode/cli/target/`, `vscode/cli/openssl/`)
  - VSCode 확장 프로그램 빌드 및 컴파일 결과물 (`vscode/extensions/**/dist/`, `vscode/extensions/**/out/`)
  - VSCode 테스트 환경 임시 파일 (`vscode/.vscode-test/`)
  - 로컬 임시 백업 및 작업 폴더 (`_backup_untracked*/`)
  - **로컬 Qdrant 벡터 데이터베이스 예외 처리**:
    - `!.agentsmith/mem0_config.json` 패턴으로 환경 설정 파일은 동기화 허용.
    - `.agentsmith/` 패턴으로 하위의 로컬 Qdrant DB 디렉터리(`mem0_qdrant_db/`) 및 로컬 로그는 동기화에서 배제하여 장비별 격리 및 데이터베이스 꼬임(Lock Collision) 원천 방어.

### 2.3. Python 가상환경 의존성 점검
- **수행 명령어**: `.venv\Scripts\python.exe -m pip install -r coding-agent/requirements.txt`
- **결과**: `fastapi`, `uvicorn`, `pydantic`, `httpx` 등 28개 백엔드 의존성 패키지가 기존 `.venv` 가상환경 내에 누락 없이 무결하게 설치되어 있음을 재확인 완료.

---

## 3. 변경 파일 맵 (Specs File Map)

| 구분 | 파일 경로 | 변경 내용 |
| :--- | :--- | :--- |
| **MODIFY** | [`.stignore`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/.stignore) | VSCode 빌드 바이너리 및 임시 백업 폴더 예외 규칙 추가 최적화 |
| **NEW** | [`coding-agent/docs/specs/2026-08-18_pc_sync_and_stignore_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-18_pc_sync_and_stignore_spec.md) | 로컬 PC 동기화 및 Syncthing 설정 상세 명세서 작성 |

---

## 4. 검증 결과
- `git status` 결과 오직 `.stignore` 파일만 수정된 상태로 Clean하게 유지됨을 확인.
- 가상환경 패키지 정상 확인 완료.
- Syncthing 예외 규칙이 `vscode/` 하위의 컴파일 및 라이브러리 바이너리를 완벽하게 포함하도록 수정됨을 확인.
