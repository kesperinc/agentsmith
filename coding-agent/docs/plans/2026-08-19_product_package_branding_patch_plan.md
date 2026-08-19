# 📋 2026-08-19 product.json / package.json 제품명 'Agent Smith IDE' 브랜딩 패치 작업 계획서

본 문서는 Microsoft Code-OSS 기반 Agent Smith IDE의 제품 브랜딩을 위해 `product.json` 및 `package.json` 내 제품명을 `Code - OSS`에서 `Agent Smith IDE`로 변경하는 커스텀 패치 파일 생성 및 적용 계획입니다.

---

## 1. 작업 개요 및 목적
- **목적**: Upstream 소스 클론 후 빌드 시 자동으로 `Agent Smith IDE` 브랜딩이 적용될 수 있도록 표준 git diff 패치 파일을 생성하고 소스 및 런타임 배포본에 일괄 적용
- **일자**: 2026년 8월 19일
- **관련 TODO**: Phase 1 - 브랜드 로고 및 커스텀 브랜딩 적용

---

## 2. 세부 작업 항목
1. **패치 디렉터리 및 패치 파일 구축**:
   - `patches/01_branding_agent_smith_ide.patch` 작성
   - `vscode/product.json` 및 `vscode/package.json` 대상 표준 Git Unified Diff 형식 적용
2. **소스 코드 메타데이터 수정**:
   - `vscode/product.json` 수정 (제품명, 식별자, 프로토콜, 레지스트리 키 등)
   - `vscode/package.json` 수정 (`name`, `author`)
3. **배포 런타임 리소스 동기화**:
   - `VSCode-win32-x64/resources/app/product.json` 수정
   - `VSCode-win32-x64/resources/app/package.json` 수정
4. **패치 관리 도구 구현**:
   - `build/apply_patches.py` 구현하여 패치 검증 및 일괄 적용 자동화
5. **검증 및 문서화**:
   - JSON 문법 및 필드 무결성 검증
   - `update_version.py` 및 `inject_version.bat` 호환성 검증
   - `coding-agent/docs/specs/2026-08-19_product_package_branding_patch_spec.md` 상세명세서 작성
   - `coding-agent/TODO.md` 로드맵 현행화
