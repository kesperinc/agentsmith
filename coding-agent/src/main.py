"""
Enterprise Coding Agent OS Backend Main Server
FastAPI Web App (Port 5000) with REST API & MCP Router (Port 3000)
"""

import sys
from pathlib import Path

# Add src to sys.path
src_dir = Path(__file__).resolve().parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from adapters.llm_adapter import LLMAdapter, RECOMMENDED_CODING_MODELS
from vibe.engine import VibeEngine
from mcp.router import MCPRouter

app = FastAPI(
    title="Antigravity VibeForge Enterprise Backend API",
    description="Vibe Coding Orchestration Engine & MCP Gateway REST API",
    version="1.0.0"
)

# CORS 설정 (프론트엔드 HTML / 대시보드와 통신 연동)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 백엔드 핵심 서비스 인스턴스 초기화
llm_adapter = LLMAdapter(provider="desktop")
vibe_engine = VibeEngine(llm_adapter)
mcp_router = MCPRouter(port=3000)

# Request Models
class VibeRequest(BaseModel):
    intent: str
    target_file: Optional[str] = "auth_service.py"
    provider: Optional[str] = "desktop"
    model_id: Optional[str] = "qwen/qwen-2.5-coder-32b-instruct"

class ProviderSwitchRequest(BaseModel):
    provider: str

class OpenRouterKeyRequest(BaseModel):
    api_key: str

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Antigravity VibeForge Enterprise Backend Server",
        "mcp_gateway_port": 3000,
        "docs_url": "http://localhost:5000/docs"
    }

@app.get("/api/workspace/status")
def get_workspace_status():
    """
    샌드박스 상태 및 LLM/OpenRouter Key/Syncthing 동기화 정보 반환
    """
    return {
        "status": "RUNNING",
        "active_sandbox": "Local Desktop Runner (.venv)",
        "llm_provider": llm_adapter.provider,
        "selected_model": llm_adapter.selected_model,
        "has_openrouter_key": bool(llm_adapter.openrouter_key and llm_adapter.openrouter_key != "your_openrouter_api_key_here"),
        "mcp_port": 3000,
        "syncthing_protected": True,
        "quota": {
            "used": 12.40,
            "total": 35.00
        }
    }

@app.get("/api/openrouter/models")
def get_coding_models():
    """
    Coding Agent에 최적화된 SOTA 모델 리스트 반환
    """
    return {
        "models": RECOMMENDED_CODING_MODELS,
        "current_selected": llm_adapter.selected_model
    }

@app.post("/api/openrouter/key")
def set_openrouter_key(req: OpenRouterKeyRequest):
    """
    OpenRouter API Key 또는 OAuth 토큰 동적 저장
    """
    llm_adapter.set_openrouter_key(req.api_key)
    return {
        "status": "success",
        "message": "OpenRouter API Key가 성공적으로 등록 및 검증되었습니다.",
        "has_key": True
    }

@app.post("/api/vibe/generate")
async def generate_vibe_code(req: VibeRequest):
    """
    Vibe 의도(Prompt)를 입력받아 자율 코드, Thinking, 샌드박스 셀프코렉션 결과 생성
    """
    if not req.intent.strip():
        raise HTTPException(status_code=400, detail="Intent prompt cannot be empty")
    
    if req.provider:
        llm_adapter.switch_provider(req.provider)
    if req.model_id:
        llm_adapter.set_model(req.model_id)
        
    result = await vibe_engine.execute_vibe(req.intent, req.target_file, req.model_id)
    return result

@app.post("/api/provider/switch")
def switch_llm_provider(req: ProviderSwitchRequest):
    """
    OpenRouter (Desktop) vs Red Hat OpenShift AI (RHOAI) 1-Click 스위칭
    """
    llm_adapter.switch_provider(req.provider)
    return {"status": "success", "current_provider": llm_adapter.provider}

@app.post("/api/mcp/rpc")
def mcp_json_rpc(payload: Dict[str, Any]):
    """
    MCP (Model Context Protocol) JSON-RPC 게이트웨이 엔드포인트
    """
    return mcp_router.handle_rpc_request(payload)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=False)
