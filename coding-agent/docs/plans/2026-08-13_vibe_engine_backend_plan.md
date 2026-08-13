# [Plan] Agent Smith Vibe Coding Engine & MCP 백엔드 REST API 구현 계획서

본 문서는 **엔터프라이즈 코딩 에이전트 MVP (Desktop-First)의 Vibe Coding 오케스트레이션 엔진 및 MCP 라우터 백엔드 API** 구현 계획서입니다.

---

## 🎯 구현 목적
1. **Desktop-First Vibe Engine 백엔드 구축**: 자연어 요구사항("Vibe") 입력 시 에이전트 사고 과정(Thinking), 코드 생성, 샌드박스 pytest 실행 및 셀프코렉션(Self-Correction)을 자율 수행하는 FastAPI 백엔드 구축.
2. **OpenRouter & RHOAI vLLM 1-Click 어댑터 연동**: 퍼블릭 클라우드 OpenRouter API와 사내 SNO vLLM을 자유롭게 스위칭.
3. **IDE 통합 연동 지원**: VS Code(Continue.dev) 및 CLI(Antigravity) 통합 커넥터를 위한 MCP JSON-RPC Gateway 서비스 완비.

---

## 🏗️ 백엔드 컴포넌트 구성 (Component Architecture)

```
agentsmith/coding-agent/src/
├── main.py                    # FastAPI 웹 서버 및 REST API 라우터 (Port 5000)
├── vibe/
│   ├── __init__.py
│   └── engine.py              # Vibe Coding 파서, 코드 Diff 생성 및 셀프코렉션 루프
├── mcp/
│   ├── __init__.py
│   └── router.py              # MCP (Model Context Protocol) JSON-RPC 게이트웨이
└── adapters/
    ├── __init__.py
    └── llm_adapter.py         # OpenRouter / RHOAI vLLM 1-Click 스위칭 어댑터
```

---

## 📋 API 명세서 (API Specification)

1. **`POST /api/vibe/generate`**: Vibe 프롬프트 수신 및 코드/Thinking/셀프코렉션 결과 반환.
2. **`GET /api/workspace/status`**: 샌드박스 상태, 현재 LLM 어댑터(OpenRouter vs RHOAI), Syncthing 동기화 상태 조회.
3. **`POST /api/mcp/rpc`**: MCP 표준 JSON-RPC 엔드포인트.

---

© 2026 AI Architecture Engineering Team. All rights reserved.
