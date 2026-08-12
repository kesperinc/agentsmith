# [Spec] Vibe Coding Engine & MCP 백엔드 REST API 상세명세서

본 문서는 **엔터프라이즈 코딩 에이전트 MVP의 백엔드 REST API 및 MCP 라우터** 구현 상세 규격서입니다.

---

## 📌 1. 백엔드 개요
* **서비스 엔트리포인트**: `agentsmith/coding-agent/src/main.py`
* **서버 구동 포트**: REST API (8000), MCP JSON-RPC Gateway (3000)
* **주요 의존 패키지**: FastAPI, Uvicorn, Pydantic, httpx, pytest

---

## 🛠️ 2. REST API 사양서

### A. Vibe 코드 및 사고 과정 생성 API
* **Endpoint**: `POST /api/vibe/generate`
* **Request Body**:
```json
{
  "intent": "사용자 인증 서비스 auth_service.py의 동기 DB 조회를 비동기 Async SQLAlchemy 구조로 변경하고, pytest로 자율 검증해 줘",
  "target_file": "auth_service.py",
  "provider": "desktop"
}
```
* **Response Body**:
```json
{
  "status": "success",
  "intent": "사용자 인증 서비스...",
  "elapsed_seconds": 0.35,
  "provider": "Desktop Local Engine",
  "thinking": [
    "1. Vibe 자연어 의도 분석: 대상 파일 auth_service.py 식별",
    "2. 동기 조회를 AsyncSession 비동기 구조로 변환...",
    "3. 샌드박스 pytest 실행 및 에러 셀프코렉션 보정 완료"
  ],
  "code_filename": "auth_service.py",
  "code_diff": "async def authenticate_user(db: AsyncSession, credentials: UserLogin):\n+ async with db.begin():...",
  "terminal_log": "[Sandbox] Running 'pytest tests/test_auth.py'...\n[SUCCESS] 4 passed in 0.35s."
}
```

### B. LLM Provider 1-Click 스위칭 API
* **Endpoint**: `POST /api/provider/switch`
* **Request Body**: `{"provider": "rhoai_vllm"}`

---

© 2026 AI Architecture Engineering Team. All rights reserved.
