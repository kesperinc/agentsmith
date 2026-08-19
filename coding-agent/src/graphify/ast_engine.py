"""
Graphify AST Knowledge Graph & Hybrid RAG Engine
Parses workspace source code AST, builds symbol call graphs, and extracts hybrid RAG contexts.
"""

import os
import ast
from typing import Dict, Any, List, Optional

class GraphifyASTEngine:
    def __init__(self, workspace_root: Optional[str] = None):
        if not workspace_root:
            workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.workspace_root = workspace_root

    def scan_ast_graph(self) -> Dict[str, Any]:
        """
        워크스페이스 내 Python 소스코드를 정적 AST 파싱하여 노드와 엣지 추출
        """
        nodes = []
        edges = []
        file_count = 0
        symbol_count = 0

        target_dirs = [
            os.path.join(self.workspace_root, "coding-agent", "src"),
            os.path.join(self.workspace_root, "scripts")
        ]

        for base_dir in target_dirs:
            if not os.path.exists(base_dir):
                continue
            for root, _, files in os.walk(base_dir):
                for file in files:
                    if file.endswith(".py") and not file.startswith("__"):
                        file_count += 1
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.workspace_root).replace("\\", "/")
                        file_node_id = f"file:{rel_path}"
                        
                        nodes.append({
                            "id": file_node_id,
                            "label": file,
                            "type": "file",
                            "path": rel_path
                        })

                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                code = f.read()
                            tree = ast.parse(code)
                            
                            for item in tree.body:
                                if isinstance(item, ast.ClassDef):
                                    symbol_count += 1
                                    class_node_id = f"class:{rel_path}:{item.name}"
                                    nodes.append({
                                        "id": class_node_id,
                                        "label": item.name,
                                        "type": "class",
                                        "file": rel_path,
                                        "line": item.lineno
                                    })
                                    edges.append({
                                        "source": file_node_id,
                                        "target": class_node_id,
                                        "relation": "defines_class"
                                    })
                                    # 메서드 추출
                                    for sub in item.body:
                                        if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                            symbol_count += 1
                                            method_id = f"func:{rel_path}:{item.name}.{sub.name}"
                                            nodes.append({
                                                "id": method_id,
                                                "label": f"{item.name}.{sub.name}()",
                                                "type": "method",
                                                "file": rel_path,
                                                "line": sub.lineno
                                            })
                                            edges.append({
                                                "source": class_node_id,
                                                "target": method_id,
                                                "relation": "has_method"
                                            })
                                elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                    symbol_count += 1
                                    func_node_id = f"func:{rel_path}:{item.name}"
                                    nodes.append({
                                        "id": func_node_id,
                                        "label": f"{item.name}()",
                                        "type": "function",
                                        "file": rel_path,
                                        "line": item.lineno
                                    })
                                    edges.append({
                                        "source": file_node_id,
                                        "target": func_node_id,
                                        "relation": "defines_func"
                                    })
                        except Exception as e:
                            pass

        return {
            "status": "success",
            "stats": {
                "files_indexed": file_count,
                "symbols_indexed": symbol_count,
                "total_nodes": len(nodes),
                "total_edges": len(edges)
            },
            "nodes": nodes[:60], # UI 최적화를 위해 상위 60개 노드
            "edges": edges[:80]
        }

    def query_hybrid_rag(self, query: str) -> Dict[str, Any]:
        """
        사용자 질의와 관련된 AST 심볼 및 호출 경로 검색
        """
        graph_data = self.scan_ast_graph()
        q_lower = query.lower()
        matched_symbols = []
        
        for node in graph_data["nodes"]:
            if q_lower in node["label"].lower() or any(term in node["label"].lower() for term in q_lower.split()):
                matched_symbols.append(node)

        return {
            "query": query,
            "matched_symbols_count": len(matched_symbols),
            "symbols": matched_symbols[:10],
            "related_graph": {
                "nodes": matched_symbols[:10],
                "stats": graph_data["stats"]
            }
        }
