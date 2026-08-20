# 📄 2026-08-20 Git 브랜치 가드레일 & CortexOS 워크플로우 적용 명세서

- **작성 일자**: 2026-08-20
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `kesperinc/agentsmith`

---

## 1. 배경 및 문제 정의

### 문제점
- `main` 브랜치에 직접 커밋/푸시하는 행위가 반복되어 브랜치 전략 가드레일이 무력화됨.
- 머지 완료 후 `feature` 브랜치로 자동 복귀하는 규칙이 실제 워크플로우에 적용되지 않음.
- CortexOS SAST 보안 검사(API Key 하드코딩, eval/exec 사용 감지)가 Git 수준에서 강제되지 않음.

### 해결 목표
- AGENTS.md Rule 4(Git 브랜치 체계) 및 브랜치 배포 가드레일 섹션을 Git Hook으로 **기술적으로 강제**.
- AI 에이전트와 인간 개발자 모두 동일한 브랜치 규칙 준수.
- 머지 후 자동 feature 복귀 및 rebase 파이프라인 자동화.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 |
| :--- | :--- | :--- |
| **[NEW]** | `.githooks/commit-msg` | main/staging 직접 커밋 차단 Git 훅 |
| **[NEW]** | `.githooks/pre-push` | main 브랜치 직접 push 차단 Git 훅 |
| **[NEW]** | `.githooks/pre-commit` | CortexOS SAST-01(API Key) / SAST-02(eval/exec) 보안 검사 훅 |
| **[NEW]** | `scripts/setup_git_guardrails.bat` | `.githooks` 경로를 Git에 등록하는 설치 스크립트 |
| **[NEW]** | `scripts/git_merge_flow.bat` | `feature/* ➔ staging ➔ main` 자동 머지 후 feature 복귀 스크립트 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-20_git_branch_guardrails_spec.md` | 본 명세서 |

---

## 3. 브랜치 전략 요약 (AGENTS.md Rule 4)

```
feature/* ──merge──► staging ──merge──► main
hotfix/*  ──merge──► main + staging (교차 머징)
```

| 브랜치 | 역할 | 직접 커밋 | 직접 Push |
|--------|------|-----------|-----------|
| `feature/*` | 신규 기능 개발 | ✅ 허용 | ✅ 허용 |
| `staging` | 통합 테스트 | ❌ 차단 | feature 머지만 허용 |
| `main` | 프로덕션 배포 | ❌ 차단 | staging 머지만 허용 |
| `hotfix/*` | 긴급 버그 픽스 | ✅ 허용 | ✅ 허용 (교차 머징 후) |

---

## 4. Git Hook 동작 명세

### 4.1 `commit-msg` 훅 (main/staging 직접 커밋 차단)
- 현재 브랜치가 `main` 또는 `staging`이면 커밋 즉시 차단
- 오류 메시지와 함께 feature 브랜치 생성 안내 출력

### 4.2 `pre-push` 훅 (main 직접 push 차단)
- `main` 브랜치에서 push 시도 시 차단
- AI 에이전트가 직접 main으로 push하는 행위 원천 방지

### 4.3 `pre-commit` 훅 (CortexOS SAST 보안 검사)
- **CORTEX-SEC-01**: `sk-*`, `AKIA*`, `ghp_*`, `AIza*` 패턴의 API Key 하드코딩 감지 → 커밋 차단
- **CORTEX-SEC-02**: `eval()`, `exec()` 함수 신규 추가 시 경고 출력

---

## 5. 워크플로우 자동화 (`git_merge_flow.bat`)

```powershell
# 사용법
scripts\git_merge_flow.bat feature/<작업명>

# 자동 실행 순서
1. feature/* push
2. staging merge (--no-ff)
3. staging push
4. main merge (--no-ff)
5. main push
6. feature 브랜치 복귀 + main rebase
```

---

## 6. 최초 설치 방법

```powershell
# Git 훅 경로 등록 (1회 실행)
scripts\setup_git_guardrails.bat
# 또는
git config core.hooksPath .githooks
```

---

## 7. 검증 결과

- `git config core.hooksPath .githooks` 적용 완료 (feature/setup-git-guardrails 브랜치)
- 현재 브랜치: `feature/setup-git-guardrails` (main 머지 후 복귀 완료)
