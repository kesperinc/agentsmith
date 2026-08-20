---
name: cortexos
description: CortexOS Mandatory Guardrails & Intent-Driven Autonomous Coding Vibe Engine Specialist Skill. Enforces Korean output, UTF-8 Bom-less encoding, Plan-Code-Doc Triad integrity, SAST security checks, and Persona workflows.
---

# 🛡️ CortexOS Specialist Skill & Guardrails

CortexOS는 의도 중심 자율 개발(Intent-Driven Autonomous Coding, Vibe Coding) 패러다임을 지지하는 차세대 에이전틱 코어 엔진 및 인프라 가드레일입니다.

---

## 📌 1. 필수 5대 가드레일 (Mandatory Guardrails)

1. **UTF-8 & 사전에 지정한 현지어(한국어) 출력 강제 (Rule 14)**:
   - 모든 AI 생성 코드 내 주석, 대화 출력, 로그 및 터미널 출력은 사전에 지정된 현지어(기본값: 한국어)로 작성합니다.
   - 모든 생성/수정 파일은 UTF-8 Bom-less 인코딩을 준수합니다.

2. **작업 트라이어드 무결성 (Rule 5)**:
   - 기능 구현 시 반드시 **[작업계획서 (Plan)] - [개발 코드 (Code)] - [상세명세서 (Doc/Spec)]**를 1:1:1 쌍으로 작성 및 유지 관리합니다.

3. **Specs 문서 별도 관리 및 날짜 명명 규칙 (Rule 15 & 16)**:
   - 코드 작성이 진행되면 변경 내역에 대한 명세서를 `coding-agent/docs/specs/` 폴더에 독립 작성합니다.
   - 모든 아티팩트 및 문서의 파일명 접두사에는 `YYYY-MM-DD_`를 반드시 추가합니다 (예: `2026-08-20_cortexos_guardrails_spec.md`).

4. **SAST 정적 보안 검사 (Cortex Guard)**:
   - `CORTEX-SEC-01`: API Key 및 Secret 토큰 하드코딩금지.
   - `CORTEX-SEC-02`: 위험 함수 `eval()`, `exec()` 사용 제한.
   - `CORTEX-SEC-03`: 원시 SQL 포매팅 금지 및 파라미터화 쿼리 강제.

5. **Windows 환경 변수 주입 및 파이썬 가상환경 가드레일**:
   - `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`, `USERPROFILE`, `AGENTSMITH_BACKEND_PORT=5000`의 전파를 보장합니다.

---

## 🛠️ 2. 사용법 (Usage & Commands)

- 코딩 에이전트 및 Vibe 엔진 기동 시 시스템 프롬프트에 `CortexGuard` 모듈이 자동으로 합성됩니다.
- SAST 보안 진단 API: `POST /api/vibe/sast-scan`
- 본 스킬은 프로젝트 내 `.agents/skills/cortexos/` 및 `~/.gemini/config/skills/cortexos/`에 동시 적용됩니다.
