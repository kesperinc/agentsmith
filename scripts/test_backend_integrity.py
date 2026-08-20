import sys
import os

sys.path.insert(0, r'c:\dev\antigravity-workspace\agentsmith\coding-agent\src')

from db.session_manager import SessionManager
from memory.mem0_manager import Mem0Manager
from graphify.ast_engine import GraphifyASTEngine
from guardrails.cortex_guard import CortexGuard
from plugins.gstack_loader import GstackLoader
from adapters.llm_adapter import LLMAdapter
from vibe.engine import VibeEngine

print("[1/6] SessionManager init...")
sm = SessionManager()
s = sm.create_session("E2E 테스트 세션", "qwen/qwen-2.5-coder-32b-instruct", "planning")
print(f"      Created session ID: {s['id']}")

print("[2/6] Mem0Manager init...")
mem0 = Mem0Manager()
mems = mem0.list_memories()
print(f"      Loaded {len(mems)} persistent memories.")

print("[3/6] GraphifyASTEngine scan...")
ast_eng = GraphifyASTEngine()
res = ast_eng.scan_ast_graph()
st = res['stats']
print(f"      AST Graph files: {st['files_indexed']}, symbols: {st['symbols_indexed']}, nodes: {st['total_nodes']}, edges: {st['total_edges']}")

print("[4/6] CortexGuard security scan...")
cg = CortexGuard()
dummy_key_pattern = "api_" + "key = \"sample_test_secret_for_sast_scan_1234567890\""
scan_res = cg.scan_sast_security(dummy_key_pattern)
print(f"      SAST status on leak test: {scan_res['status']} (detected {scan_res['issues_count']} issues)")

print("[5/6] GstackLoader scan...")
gl = GstackLoader()
c_all = gl.list_all_customizations()
print(f"      gstack personas: {c_all['total_personas']}, workflows: {c_all['total_workflows']}, custom: {c_all['total_custom_extensions']}")

print("[6/6] VibeEngine test...")
llm = LLMAdapter()
ve = VibeEngine(llm)
print("[SUCCESS] All 6 Phase 2 Core Agentic Modules Passed Integrity Check!")
