# -*- coding: utf-8 -*-
"""
Agent Smith - MCP (Model Context Protocol) Server Integration
Standard JSON-RPC 2.0 Communication Interface for Agentic CLI (Codex/Claude Code/Antigravity)
"""

import json
import sys
import logging
from typing import Dict, Any, List
from vibe_orchestrator import VibeOrchestrator

logging.basicConfig(level=logging.INFO, format="[MCP-SERVER][%(asctime)s] %(message)s")


class MCPServer:
    def __init__(self):
        self.orchestrator = VibeOrchestrator()
        self.tools = [
            {
                "name": "vibe_create_project",
                "description": "Natural language intent driven multi-file project generation",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "User intent prompt"}
                    },
                    "required": ["prompt"]
                }
            },
            {
                "name": "vibe_run_sandbox",
                "description": "Execute generated files in isolated sandbox environment",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Active Vibe session ID"}
                    },
                    "required": ["session_id"]
                }
            },
            {
                "name": "vibe_self_correct",
                "description": "Apply autonomous self-correction to broken codebase",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "error_log": {"type": "string", "description": "Error trace log"}
                    },
                    "required": ["error_log"]
                }
            }
        ]

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC 2.0 request"""
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        logging.info(f"Handling MCP method: {method}")

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "Agent Smith MCP Server", "version": "1.0.0"}
                }
            }
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": self.tools}
            }
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "vibe_create_project":
                prompt = arguments.get("prompt", "")
                result = self.orchestrator.execute_vibe_flow(prompt)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Vibe Project Created Successfully! Session ID: {result.session_id}, Files: {[f.file_path for f in result.generated_files]}"
                            }
                        ]
                    }
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": f"MCP Tool '{tool_name}' executed successfully!"}]}
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            }

    def run_simulation(self):
        """Simulate MCP JSON-RPC 2.0 handshake and tool execution"""
        logging.info("Starting Agent Smith MCP Communication Server Simulation...")
        
        # 1. Initialize Handshake
        init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        init_res = self.handle_request(init_req)
        print("\n--- [MCP HANDSHAKE] ---")
        print(json.dumps(init_res, indent=2, ensure_ascii=False))

        # 2. List Tools
        tools_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        tools_res = self.handle_request(tools_req)
        print("\n--- [MCP TOOLS LIST] ---")
        print(json.dumps(tools_res, indent=2, ensure_ascii=False))

        # 3. Call Tool (vibe_create_project)
        call_req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "vibe_create_project",
                "arguments": {"prompt": "React기반 Vibe 대시보드 모듈 만들어줘"}
            }
        }
        call_res = self.handle_request(call_req)
        print("\n--- [MCP TOOL CALL EXECUTION] ---")
        print(json.dumps(call_res, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    server = MCPServer()
    server.run_simulation()
