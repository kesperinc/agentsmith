# 📄 2026-08-19 product.json / package.json 제품명 'Agent Smith IDE' 브랜딩 패치 상세명세서

본 명세서는 2026년 8월 19일 진행된 Microsoft Code-OSS 기반 Agent Smith IDE의 제품 브랜딩을 위해 `product.json` 및 `package.json` 내 제품명을 `Code - OSS`에서 `Agent Smith IDE`로 변경하는 커스텀 패치 파일 생성 및 적용 내역을 정의합니다.

---

## 📂 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 요약 |
| :--- | :--- | :--- |
| **[NEW]** | [`patches/01_branding_agent_smith_ide.patch`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/patches/01_branding_agent_smith_ide.patch) | `product.json` 및 `package.json`의 브랜딩 변경점을 담은 표준 Git Unified Diff 패치 파일 |
| **[NEW]** | [`build/apply_patches.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/build/apply_patches.py) | 패치 유효성 사전 점검(`git apply --check`), 자동 적용 및 JSON 무결성 검증 유틸리티 |
| **[MODIFY]** | [`vscode/product.json`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/product.json) | `nameShort`, `nameLong`, `applicationName`, `win32DirName`, `urlProtocol` 등을 `Agent Smith IDE`로 갱신 |
| **[MODIFY]** | [`vscode/package.json`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/package.json) | `name`을 `agent-smith-ide`로 변경하고 `author.name`을 `MegazoneCloud Corporation`으로 갱신 |
| **[MODIFY]** | [`VSCode-win32-x64/resources/app/product.json`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/VSCode-win32-x64/resources/app/product.json) | Electron 배포 바이너리 런타임에 `Agent Smith IDE` 브랜딩 메타데이터 즉각 동기화 |
| **[MODIFY]** | [`VSCode-win32-x64/resources/app/package.json`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/VSCode-win32-x64/resources/app/package.json) | Electron 배포 바이너리 런타임에 `Agent Smith IDE` 패키지 메타데이터 즉각 동기화 |
| **[MODIFY]** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/TODO.md) | Phase 1 브랜딩 커스텀 패치 파일 생성 및 적용 과제 완료(`[x]`) 현행화 |
| **[NEW]** | [`coding-agent/docs/plans/2026-08-19_product_package_branding_patch_plan.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/plans/2026-08-19_product_package_branding_patch_plan.md) | 브랜딩 패치 생성 및 적용 작업 계획서 |
| **[NEW]** | [`coding-agent/docs/specs/2026-08-19_product_package_branding_patch_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-19_product_package_branding_patch_spec.md) | 브랜딩 패치 생성 및 적용 상세 명세서 (본 문서) |

---

## 🛠️ 2. 상세 수정 내역 및 목적

### A. 표준 Git Unified Diff 패치 파일 생성
- **대상 파일**: [`patches/01_branding_agent_smith_ide.patch`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/patches/01_branding_agent_smith_ide.patch)
- **수정 목적**: Upstream Code-OSS 저장소를 클린 체크아웃하거나 재빌드할 때 `build_agent_smith.bat`의 4단계(`git apply %PATCHES_DIR%\*.patch`)를 통해 자동으로 Agent Smith 브랜딩이 주입되도록 보장합니다.
- **수정 내용**:
  - `package.json`: `name`(`agent-smith-ide`), `author.name`(`MegazoneCloud Corporation`)
  - `product.json`:
    - `nameShort`: `Agent Smith IDE`
    - `nameLong`: `Agent Smith IDE`
    - `applicationName`: `agent-smith-ide`
    - `dataFolderName`: `.agentsmith-ide`
    - `win32MutexName`: `agentsmithide`
    - `serverApplicationName`: `agent-smith-server`
    - `serverDataFolderName`: `.agent-smith-server`
    - `tunnelApplicationName`: `agent-smith-tunnel`
    - `win32DirName`: `Agent Smith IDE`
    - `win32NameVersion`: `Agent Smith IDE`
    - `win32RegValueName`: `AgentSmithIDE`
    - `win32AppUserModelId`: `MegazoneCloud.AgentSmithIDE`
    - `win32ShellNameShort`: `Agent Smith IDE`
    - `win32TunnelServiceMutex`: `agentsmithide-tunnelservice`
    - `win32TunnelMutex`: `agentsmithide-tunnel`
    - `darwinBundleIdentifier`: `com.megazonecloud.agentsmith.ide`
    - `linuxIconName`: `agent-smith-ide`
    - `urlProtocol`: `agent-smith-ide`

### B. 소스 코드 및 배포 바이너리 런타임 동기화
- **대상 파일**: 
  - [`vscode/product.json`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/product.json)
  - [`vscode/package.json`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/vscode/package.json)
  - [`VSCode-win32-x64/resources/app/product.json`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/VSCode-win32-x64/resources/app/product.json)
  - [`VSCode-win32-x64/resources/app/package.json`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/VSCode-win32-x64/resources/app/package.json)
- **수정 목적**: 현재 개발 워크스페이스의 소스 코드와 바로 실행 가능한 배포 바이너리 양쪽에 변경된 제품명과 메타데이터를 일치시켜, 실행 시 에디터 타이틀, 정보 창(About), 바로가기 등에서 즉각 `Agent Smith IDE`로 노출되도록 보장합니다.

### C. 패치 관리 및 검증 도구 구현
- **대상 파일**: [`build/apply_patches.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/build/apply_patches.py)
- **수정 목적**: 향후 추가될 다양한 커스텀 패치 파일들의 유효성을 사전에 검증(`git apply --check`)하고, JSON 문법 및 브랜딩 속성의 무결성을 한 번에 확인할 수 있는 자동화 스크립트를 제공합니다.

---

## 🧪 3. 검증 결과

1. **패치 무결성 검증**:
   - `build/apply_patches.py` 실행 결과 `01_branding_agent_smith_ide.patch`가 작업 트리에 완벽하게 적용되어 있음을 확인 (`[OK] Patch is ALREADY applied to the working tree.`).
2. **JSON 파싱 및 브랜딩 속성 검증**:
   - `vscode/product.json`, `vscode/package.json`, `VSCode-win32-x64` 내의 각 설정 파일이 모두 유효한 JSON 포맷이며 `nameShort='Agent Smith IDE'`, `author='MegazoneCloud Corporation'`으로 올바르게 인식됨을 확인.
3. **버전 주입 스크립트 연동 검증**:
   - `update_version.py` 실행 시 변경된 `product.json` 및 `package.json`에 타임스탬프 버전(`1.86.0-YYYYMMDD.HHMMSS`)이 정상 주입됨을 확인.
