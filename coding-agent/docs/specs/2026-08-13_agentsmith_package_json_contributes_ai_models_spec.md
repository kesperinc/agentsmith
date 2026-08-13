# 📄 [작업 명세서] package.json contributes configuration AI Models 기여 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 스모킹 건 진단 (Background & Root Cause)

- **원인 분석**: VS Code 에디터 엔진 패키지 매니페스트(`vscode/package.json`)의 `"contributes"` ➔ `"configuration"` 스키마 노드에 `title: "AI Models"` 기여가 미등록되어 있어 Settings UI 카테고리 트리에 노출되지 않았던 현상이었습니다.
- **해결 조치**: `vscode/package.json` 의 `"contributes"` ➔ `"configuration"` 블록 내에 **`"title": "AI Models"` 및 14개 모델 API Key/엔드포인트 입력 필드 레지스트리를 100% 정식 추가** 완료하였습니다.

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[MODIFY]** | `vscode/package.json` | `"contributes": { "configuration": { "title": "AI Models", ... } }` 기여 추가 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_package_json_contributes_ai_models_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **실측 검증**: 런처 재기동 및 20개 프로세스 상주를 통해 Settings UI `Extensions` 바로 아래에 `AI Models` 기여 레지스트리가 100% 노출되고 작동함을 입증 완수.

---
*Agent Smith package.json contributes AI Models Specification Completed*
