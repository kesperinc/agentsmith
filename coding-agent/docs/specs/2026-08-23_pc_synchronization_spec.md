# 🔬 2026-08-23 Agent Smith PC 환경 동기화 및 바이너리 무결성 상세 명세서 (Specification)

**문서 번호**: `SPEC-2026-08-23-PC-SYNC`  
**문서 작성일**: 2026-08-23  
**대상 호스트**: `HOME_SUNKIM` (Windows 11 Enterprise/Pro x64, 10.0.26200)  
**저장소 브랜치**: `feature/setup-git-guardrails` (`894d306`)  
**작성자**: Agent Smith AI Architecture & Pair Engineering Team  
**준수 규칙**: AGENTS.md (규칙 1~16 전체 준수, 작업 트라이어드, UTF-8 BOM-less)

---

## 1. 개요 및 목적

본 명세서는 타 PC(`MZC_SUNKIM317_L` 및 이전 개발 장비)에서 수립된 마스터 핸드오버 문서와 깃허브 원격 저장소(`https://github.com/kesperinc/agentsmith.git`)의 브랜치(`feature/setup-git-guardrails`, `staging`, `main`, `hotfix/agentsmith`) 형상을 정밀 분석하고, 현재 PC(`HOME_SUNKIM`) 환경으로 동기화 및 무결성 전수 검증을 완료한 기술 명세서입니다.

---

## 2. 형상 관리 및 Git 환경 최적화 명세

### 2.1 원격 브랜치 검토 및 Fast-Forward 동기화
1. **`feature/setup-git-guardrails`**:
   - 원격 커밋 `894d306` ("docs: MZC_SUNKIM317_L PC 환경 동기화 및 바이너리 빌드 완료 명세서 작성 및 TODO 현행화")을 Fast-Forward 방식으로 완벽 동기화.
   - 워킹 트리 상태: `working tree clean`.
2. **`staging` & `main`**:
   - 원격 커밋 `4742716` ("docs: 바이너리 빌드 문제점 해결 및 Agent Smith AI 구현 심층 분석서 작성 및 마스터 핸드오버 문서 반영")과 로컬 브랜치 정합성 100% 일치 확인.
3. **`hotfix/agentsmith`**:
   - 원격 커밋 `05ed0ee` 보관 상태 확인.

### 2.2 Git 환경설정 가드레일
```ini
core.autocrlf = false
core.quotepath = false
gui.encoding = utf-8
i18n.commitencoding = utf-8
core.hooksPath = .githooks
```
- Windows 환경에서 발생할 수 있는 LF/CRLF 개행 변환 충돌을 `core.autocrlf = false`로 원천 차단.
- 2바이트 한글 경로 표기를 위해 `core.quotepath = false` 적용.
- 커밋 전후 SAST 보안 검사 및 브랜치 규칙 준수를 위해 `.githooks/` 활성화.

---

## 3. 로컬 런타임 및 무결성 진단 명세

### 3.1 환경설정 (`.env`)
- 루트 경로에 `.env` 생성 완료:
  - `AGENTSMITH_WORKSPACE_ROOT=c:\dev\antigravity-workspace\agentsmith`
  - `HOST=127.0.0.1`, `PORT=5000`
  - `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`

### 3.2 Python `uv` 가상환경 및 의존성
- `.venv` 가상환경(Python 3.11.15) 내 28개 의존성 패키지 동기화 검증 완료.

### 3.3 백엔드 6대 핵심 모듈 진단 결과
- 진단 스크립트: `scripts/test_backend_integrity.py`
- 진단 결과: **100% PASS**
  1. `SessionManager`: SQLite 세션 DB 초기화 및 생성 정상
  2. `Mem0Manager`: 영속 기억 5종 로드 정상
  3. `GraphifyASTEngine`: AST 지식 그래프 및 Call Graph 파싱 정상
  4. `CortexGuard`: SAST 보안 가드레일 정적 검사 정상
  5. `GstackLoader`: 8개 페르소나 및 10개 워크플로우 로드 정상
  6. `VibeEngine`: 의도 기반 자율 코딩 오케스트레이터 정상

### 3.4 데스크톱 배포 번들 및 인스톨러 진단 결과
- 진단 스크립트: `scripts/verify_desktop_bundle.py --verify-dist`
- 진단 결과: **100% PASS**
  - 메인 번들: `workbench.desktop.main.js` (28.73 MB) 정상
  - 더미 asar: 28바이트 `node_modules.asar` 주입 정상
  - 네이티브 모듈: C++ 14종 및 ConPTY 터미널 바이너리 정상 바인딩
  - 포터블 압축 파일: `dist/agentsmith-desktop-v1.0.0.zip` (444.71 MB)
  - C# Native 단일 설치 파일: `dist/AgentSmith_Desktop_Setup_v1.0.0.exe` (442.60 MB)

---

## 4. 변경 및 생성 파일 수정 맵 (Specs File Map)

| 구분 | 파일 경로 | 변경 및 생성 설명 |
| :--- | :--- | :--- |
| **보고서** | [`docs/2026-08-23_pc_sync_and_handover_report.md`](file:///c:/dev/antigravity-workspace/agentsmith/docs/2026-08-23_pc_sync_and_handover_report.md) | 본 PC(`HOME_SUNKIM`) 현행화 및 검증 완료 보고서 |
| **명세서** | [`coding-agent/docs/specs/2026-08-23_pc_synchronization_spec.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-23_pc_synchronization_spec.md) | 본 PC 세부 동기화 및 무결성 진단 명세서 |
| **환경설정** | [`.env`](file:///c:/dev/antigravity-workspace/agentsmith/.env) | 독립 로컬 실행 및 백엔드 포트(5000) 바인딩 환경설정 |
| **로드맵** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/TODO.md) | 호스트별 검증 매트릭스(`HOME_SUNKIM`) 반영 및 로드맵 현행화 |

---

## 5. 최종 검증 요약

1. **Git 상태**: `On branch feature/setup-git-guardrails, working tree clean`.
2. **동기화 상태**: 원격 `origin/feature/setup-git-guardrails`와 완벽 일치.
3. **무결성 진단**: 백엔드 6대 모듈 및 데스크톱 배포 바이너리 산출물 100% 통과.
