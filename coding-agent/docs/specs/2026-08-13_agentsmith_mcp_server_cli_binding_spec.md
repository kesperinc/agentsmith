# 📄 [작업 명세서] Task 2-2 MCP (Model Context Protocol) 통신 서버 & CLI 바인딩 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 구현 성과 (Background & Accomplishments)

- **MCP 통신 표준 서버 구현**:
  - Agent Smith IDE와 Agentic CLI (Codex / Claude Code / Antigravity) 간 실시간 통신을 위한 MCP JSON-RPC 2.0 표준 서버 구현 완료.
  - 지원 MCP 툴 세트:
    1. `vibe_create_project`: 자연어 요구사항 기반 자율 멀티 파일 생성
    2. `vibe_run_sandbox`: 격리 샌드박스 실행 검증
    3. `vibe_self_correct`: 자율 코드 교정 파이프라인

---

## 2. 변경된 파일 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 내용 및 목적 |
| :--- | :--- | :--- |
| **[NEW]** | `coding-agent/src/mcp_server.py` | MCP JSON-RPC 2.0 서버 & CLI 바인딩 처리기 |
| **[NEW]** | `coding-agent/docs/specs/2026-08-13_agentsmith_mcp_server_cli_binding_spec.md` | 본 작업 명세서 |

---

## 3. 검증 결과 (Verification Results)

- **mcp_server.py 통신 검증**: `python coding-agent/src/mcp_server.py` 실행 시 JSON-RPC 2.0 `initialize`, `tools/list`, `tools/call` 통신 시뮬레이션 100% 정상 작동 실측 완료.

---
*Agent Smith MCP Server Specification Completed*
