# 📄 Agent Smith 데스크톱 검은 화면 결함 해결 및 작업 인수인계 보고서

- **문서 번호**: HR-AS-20260820-02
- **작성 일자**: 2026-08-20
- **작성자**: Agent Smith AI Pair Engineer
- **대상 브랜치**: `feature/setup-git-guardrails`
- **목적**: 데스크톱 바이너리 구동 시 발생한 검은 화면(Black Screen) 문제의 근본 원인을 정리하고, 다른 PC에서 즉시 작업을 재개할 수 있도록 인수인계 절차를 수립함.

---

## 🔍 1. 검은 화면(Black Screen) 장애 근본 원인 및 조치 내역

### 1.1 원인 분석 (Root Cause)
1. **프로덕션 번들 덮어쓰기 결함**:
   - `VSCode-win32-x64` 내에는 이미 29.5MB 크기의 `workbench.desktop.main.js`와 810KB 크기의 CSS가 번들링되어 있었습니다.
   - 기존 `package_desktop_dist.py`가 이를 `vscode/out`(7KB 개발용 스텁)으로 덮어쓰면서 렌더러 화면에 아무것도 로드되지 않는 현상이 발생했습니다.
2. **Asar 로더 충돌 및 네이티브 모듈 로딩 실패**:
   - Electron의 `node_modules.asar`가 네이티브 모듈 경로 탐색을 가로채면서 `@vscode/sqlite3`, `@vscode/windows-mutex`, `native-keymap` 등의 C++ 바이너리 로드가 실패했습니다.

### 1.2 영구 해결 조치 (Permanent Fixes)
1. **`scripts/package_desktop_dist.py` 로직 개편**:
   - `VSCode-win32-x64`의 대용량 번들 `out/` 디렉터리가 존재할 경우 이를 온전히 보존하도록 보호 로직을 추가했습니다.
   - 28바이트 더미 asar(`{"files":{}}`)를 자동 주입하여 asar 후킹을 우회하고 순수 `resources/app/node_modules/`로 언팩 폴백되도록 구성했습니다.
   - Antigravity IDE의 검증된 Electron 27 ABI 118 네이티브 모듈 14종 및 의존성을 안전하게 오버레이 복사하도록 표준화했습니다.
2. **`scripts/verify_desktop_bundle.py` 진단 도구 고도화**:
   - `workbench.desktop.main.js`의 번들 크기(1MB 초과)와 더미 asar 구조를 사전에 5초 내로 자동 검증하도록 강화했습니다.

---

## 🚀 2. 다른 PC에서 작업 재개 절차 (Next PC Quick-Start)

새로운 PC에서 작업을 시작할 때 아래 절차를 진행하시면 됩니다.

```powershell
# 1. 저장소 최신 커밋 풀 (Git 동기화)
git fetch --all
git pull origin feature/setup-git-guardrails

# 2. 파이썬 가상환경 점검 (없을 경우 생성)
uv venv .venv
uv pip install -r coding-agent/requirements.txt --python .venv\Scripts\python.exe

# 3. 사전 환경 무결성 진단
.venv\Scripts\python.exe scripts/verify_desktop_bundle.py --pre-check

# 4. 데스크톱 패키징 및 단일 인스톨러 빌드
.venv\Scripts\python.exe scripts/package_desktop_dist.py
.venv\Scripts\python.exe scripts/build_desktop_installer.py

# 5. 최종 사후 산출물 진단
.venv\Scripts\python.exe scripts/verify_desktop_bundle.py --verify-dist
```
