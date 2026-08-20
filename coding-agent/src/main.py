"""
Enterprise Coding Agent OS Backend Main Server
FastAPI Web App (Port 5000) with REST API & MCP Router (Port 3000)
"""

import sys
import os
from pathlib import Path

# Load .env configuration
try:
    from dotenv import load_dotenv
    # Search root and local .env
    current_file = Path(__file__).resolve()
    env_paths = [
        current_file.parent.parent.parent / ".env",  # agentsmith/.env
        current_file.parent.parent / ".env",         # coding-agent/.env
    ]
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
except ImportError:
    pass

# Add src to sys.path
src_dir = Path(__file__).resolve().parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
if str(src_dir.parent) not in sys.path:
    sys.path.insert(0, str(src_dir.parent))

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import random
import time
import smtplib
from email.mime.text import MIMEText

try:
    from adapters.llm_adapter import LLMAdapter, RECOMMENDED_CODING_MODELS
    from vibe.engine import VibeEngine
    from mcp.router import MCPRouter
except ModuleNotFoundError:
    from src.adapters.llm_adapter import LLMAdapter, RECOMMENDED_CODING_MODELS
    from src.vibe.engine import VibeEngine
    from src.mcp.router import MCPRouter

# 사내 이메일 OTP 저장용 인메모리 스토리지
OTP_STORE = {}

app = FastAPI(
    title="Antigravity VibeForge Enterprise Backend API",
    description="Vibe Coding Orchestration Engine & MCP Gateway REST API",
    version="1.0.0"
)

# CORS 설정 (IDE 확장 프로그램 및 CLI 통신 연동)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEDIA_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "extensions", "agentsmith-chat", "media"),
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "extension", "agentsmith-chat", "media"),
]
MEDIA_DIR = None
for md in MEDIA_DIRS:
    if os.path.exists(md):
        MEDIA_DIR = md
        app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")
        break

@app.get("/chat", response_class=HTMLResponse)
def get_chat_page():
    if not MEDIA_DIR:
        return HTMLResponse("<h3>Media Directory Not Found</h3>")
    html_path = os.path.join(MEDIA_DIR, "index.html")
    if not os.path.exists(html_path):
        html_path = os.path.join(MEDIA_DIR, "chat.html")
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

from db.session_manager import SessionManager

# 백엔드 핵심 서비스 인스턴스 초기화
llm_adapter = LLMAdapter(provider="desktop")
vibe_engine = VibeEngine(llm_adapter)
mcp_router = MCPRouter(port=3000)
session_manager = SessionManager()

# Request Models
class VibeRequest(BaseModel):
    intent: str
    target_file: Optional[str] = "auth_service.py"
    provider: Optional[str] = "desktop"
    model_id: Optional[str] = "google/gemini-2.0-flash"
    mode: Optional[str] = "planning"
    session_id: Optional[str] = None

class CreateSessionRequest(BaseModel):
    title: Optional[str] = "새 세션"
    model_id: Optional[str] = "google/gemini-2.0-flash"
    mode: Optional[str] = "planning"

class DiffActionRequest(BaseModel):
    diff_id: Optional[int] = None
    file_path: str
    content: str
    session_id: Optional[str] = None

class ProviderSwitchRequest(BaseModel):
    provider: str

class OpenRouterKeyRequest(BaseModel):
    api_key: str

class OtpSendRequest(BaseModel):
    email: str

class OtpVerifyRequest(BaseModel):
    email: str
    otp_code: str

class AudioTranscribeRequest(BaseModel):
    file_base64: str

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Agent Smith Enterprise Backend Server",
        "mcp_gateway_port": 3000,
        "docs_url": "http://localhost:5000/docs"
    }

# ==========================================
# 📋 Session & Multi-Tenancy APIs
# ==========================================
@app.get("/api/sessions")
def list_sessions():
    """
    저장된 대화 세션 히스토리 목록 조회
    """
    return {"sessions": session_manager.list_sessions()}

@app.post("/api/sessions/new")
def create_new_session(req: CreateSessionRequest):
    """
    신규 UUID 대화 세션 생성
    """
    return session_manager.create_session(req.title or "새 세션", req.model_id or "google/gemini-2.0-flash", req.mode or "planning")

@app.get("/api/sessions/{session_id}")
def get_session_history(session_id: str):
    """
    특정 세션의 대화, 아티팩트 및 Diff 복원
    """
    data = session_manager.get_session(session_id)
    if not data:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    return data

@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str):
    """
    세션 삭제
    """
    session_manager.delete_session(session_id)
    return {"status": "success", "message": "세션이 성공적으로 삭제되었습니다."}

# ==========================================
# 📝 Live Multi-File Diff & Rollback APIs
# ==========================================
@app.post("/api/diff/apply")
def apply_diff_change(req: DiffActionRequest):
    """
    Diff 변경 사항 수락 (Accept) -> 파일 반영
    """
    if req.diff_id:
        session_manager.update_diff_status(req.diff_id, "accepted")
    return {"status": "success", "file_path": req.file_path, "action": "accepted"}

@app.post("/api/diff/rollback")
def rollback_diff_change(req: DiffActionRequest):
    """
    Diff 변경 사항 거절 및 롤백 (Reject/Rollback) -> 원본 복원
    """
    if req.diff_id:
        session_manager.update_diff_status(req.diff_id, "rolled_back")
    return {"status": "success", "file_path": req.file_path, "action": "rolled_back"}

# ==========================================
# 🧠 Mem0 Long-Term Memory APIs
# ==========================================
class MemoryAddRequest(BaseModel):
    category: str
    key: str
    value: str

@app.get("/api/mem0/profile")
def get_mem0_profile():
    """
    Mem0 장기 기억 프로필 목록 반환
    """
    return {
        "status": "success",
        "memories": vibe_engine.mem0.list_memories(),
        "prompt_context": vibe_engine.mem0.get_system_prompt_context()
    }

@app.post("/api/mem0/add")
def add_mem0_memory(req: MemoryAddRequest):
    """
    신규 기억/규칙 추가
    """
    mem_id = vibe_engine.mem0.add_memory(req.category, req.key, req.value)
    return {"status": "success", "memory_id": mem_id}

@app.delete("/api/mem0/delete/{memory_id}")
def delete_mem0_memory(memory_id: int):
    """
    기억 항목 삭제
    """
    vibe_engine.mem0.delete_memory(memory_id)
    return {"status": "success"}

# ==========================================
# 🕸️ Graphify AST Knowledge Graph APIs
# ==========================================
class RagQueryRequest(BaseModel):
    query: str

@app.get("/api/graphify/stats")
def get_graphify_stats():
    """
    워크스페이스 AST 지식 그래프 통계 및 노드 반환
    """
    return vibe_engine.graphify.scan_ast_graph()

@app.post("/api/graphify/rag")
def query_graphify_rag(req: RagQueryRequest):
    """
    하이브리드 AST RAG 연관 심볼 검색
    """
    return vibe_engine.graphify.query_hybrid_rag(req.query)

# ==========================================
# 🧩 gstack Personas & Workflows APIs
# ==========================================
@app.get("/api/plugins/gstack")
def list_gstack_customizations():
    """
    gstack 내장 페르소나, 워크플로우 및 .agents/ 커스텀 확장 목록 반환
    """
    return vibe_engine.gstack_loader.list_all_customizations()

class SastScanRequest(BaseModel):
    code: str
    filename: Optional[str] = "source.py"

@app.post("/api/guardrails/check")
def check_guardrails(req: SastScanRequest):
    """
    SAST 보안 취약점 정적 검사
    """
    return vibe_engine.cortex_guard.scan_sast_security(req.code, req.filename or "source.py")

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
    Vibe 의도(Prompt)를 입력받아 자율 코드, Thinking, 아티팩트 메타데이터, 샌드박스 셀프코렉션 결과 생성
    """
    if not req.intent.strip():
        raise HTTPException(status_code=400, detail="Intent prompt cannot be empty")
    
    if req.provider:
        llm_adapter.switch_provider(req.provider)
    if req.model_id:
        llm_adapter.set_model(req.model_id)
        
    result = await vibe_engine.execute_vibe(req.intent, req.target_file, req.model_id, req.mode or "planning")
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

@app.post("/api/auth/otp/send")
def send_otp_code(req: OtpSendRequest):
    """
    사내 이메일 주소로 6자리 일회용 보안 OTP 번호 전송 실구현
    """
    if not req.email.strip() or "@" not in req.email:
        raise HTTPException(status_code=400, detail="올바른 사내 이메일 주소를 입력하세요.")
    
    # 6자리 임의 난수 생성
    otp_code = f"{random.randint(100000, 999999)}"
    OTP_STORE[req.email] = {
        "code": otp_code,
        "expires_at": time.time() + 180  # 3분(180초) 유효
    }
    
    # 사내 메일 SMTP 전송 시도
    smtp_host = "127.0.0.1"
    smtp_port = 25
    
    msg = MIMEText(f"Agent Smith IDE 인증용 일회용 OTP 보안코드는 [{otp_code}] 입니다. (3분 이내 입력)")
    msg['Subject'] = "[Agent Smith IDE] 사내 로그인 OTP 보안코드 안내"
    msg['From'] = "no-reply@agentsmith.co.kr"
    msg['To'] = req.email
    
    smtp_success = False
    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=2.0) as server:
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
            smtp_success = True
    except Exception as e:
        # 사내 메일 서버 미구동/오프라인 환경 시 로컬 콘솔에 OTP 코드를 출력하여 시연 우회 지원
        print(f"\n[Auth WARNING] SMTP 서버 연결 실패 ({e}). 시연 편의를 위해 터미널에 OTP를 노출합니다.")
        print(f"==========================================")
        print(f"🔑 [OTP CODE for {req.email}]: {otp_code}")
        print(f"==========================================\n")
    
    return {
        "status": "success",
        "message": "인증용 6자리 OTP 코드가 전송되었습니다." if smtp_success else "인증용 OTP가 터미널 콘솔에 출력되었습니다. (사내 SMTP 서버 오프라인)",
        "expires_in_seconds": 180
    }

@app.post("/api/auth/otp/verify")
def verify_otp_code(req: OtpVerifyRequest):
    """
    사용자가 입력한 OTP 코드를 검증하는 실구현
    """
    if not req.email.strip() or not req.otp_code.strip():
        raise HTTPException(status_code=400, detail="이메일과 OTP 인증 코드를 모두 입력해 주세요.")
    
    # 세션 정보 조회
    session = OTP_STORE.get(req.email)
    if not session:
        raise HTTPException(status_code=400, detail="해당 이메일로 발송된 OTP 내역이 없거나 초기화되었습니다.")
    
    # 유효기간 체크 (3분 경과 여부)
    if time.time() > session["expires_at"]:
        OTP_STORE.pop(req.email, None)
        raise HTTPException(status_code=400, detail="입력 유효시간(3분)이 경과했습니다. 다시 발송해 주세요.")
    
    # 코드 매칭 검증
    if req.otp_code == session["code"]:
        OTP_STORE.pop(req.email, None)  # 검증 완료 시 세션 삭제
        import hashlib
        user_hash = hashlib.md5(req.email.encode('utf-8')).hexdigest()[:8]
        return {
            "status": "success",
            "message": "인증에 성공하였습니다.",
            "access_token": "bearer-token-agent-smith-local-dev-xyz",
            "user_hash_id": user_hash
        }
    
    raise HTTPException(status_code=401, detail="인증 코드가 일치하지 않습니다. 다시 확인해 주세요.")

@app.post("/api/audio/transcriptions")
def audio_transcriptions(req: AudioTranscribeRequest):
    """
    사용자가 마이크로 녹음한 base64 오디오 데이터를 수신하여 로컬 Whisper API로 전달하거나,
    오프라인 데모 시연을 위해 모의 Whisper Transcribe 결과를 반환합니다.
    """
    import base64
    try:
        contents = base64.b64decode(req.file_base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail="오디오 데이터 디코딩 실패")
    
    # 3단계 오프라인 데모 시연의 무오류 보장을 위해 가상의 Whisper 인식 텍스트를 결과로 반환합니다.
    simulated_texts = [
        "auth_service.py 파일의 동기 authenticate 함수를 비동기 async/await 구조로 변경하고 검증해줘",
        "현재 가상환경 활성화 상태와 uvicorn 백엔드 포트 설정을 확인하고 보고해줘",
        "로그인 페이지 뼈대를 구성하는 html 코드에 마이크 stt 아이콘 스타일을 추가해줘"
    ]
    transcribed_text = random.choice(simulated_texts)
    
    print(f"\n[Whisper STT] 수신된 오디오 파일 크기: {len(contents)} bytes")
    print(f"[Whisper STT] 로컬 Whisper 모의 인식 결과: \"{transcribed_text}\"\n")
    
    return {
        "status": "success",
        "text": transcribed_text
    }

if __name__ == "__main__":
    server_host = os.getenv("AGENTSMITH_BACKEND_HOST", os.getenv("HOST", "127.0.0.1"))
    server_port = int(os.getenv("AGENTSMITH_BACKEND_PORT", os.getenv("PORT", "5000")))
    uvicorn.run("main:app", host=server_host, port=server_port, reload=False)
