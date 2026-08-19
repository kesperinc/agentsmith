"""
CortexOS Guardrails & Code Quality / SAST Security Inspector Module
Enforces Triad (Plan-Code-Spec), UTF-8 BOM-less, Korean System Prompts, and Static Security Scanning
"""

import os
import re
import datetime
from typing import Dict, Any, List, Optional

class CortexGuard:
    def __init__(self, workspace_root: Optional[str] = None):
        if not workspace_root:
            workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.workspace_root = workspace_root

    def build_system_prompt(self, persona: Optional[str] = None, command: Optional[str] = None) -> str:
        """
        CortexOS Mandatory Rules & gstack Persona Prompt Synthesizer
        """
        base_prompt = [
            "# CortexOS & Agent Smith Mandatory System Instructions",
            "1. [언어 규칙]: 모든 코드 주석, 설명, 커밋 메시지, 대화 응답은 반드시 한국어로만 작성합니다.",
            "2. [인코딩]: 생성/수정되는 모든 텍스트 파일은 UTF-8 (BOM-less)로 저장합니다.",
            "3. [가상환경]: 파이썬 가상환경은 .venv (uv 기반)을 유지합니다.",
            "4. [작업 트라이어드]: [작업계획서] - [개발코드] - [상세명세서] 1:1:1 쌍을 유지하며, 모든 문서 파일명은 YYYY-MM-DD_ 접두사를 사용합니다.",
            "5. [보안 가드레일]: 하드코딩된 API Key, 토큰, SQL Injection 취약 패턴 생성을 엄격히 금지합니다."
        ]

        if persona:
            personas_map = {
                "@pm": "역할: [Product Manager] - 사용자 가치, UX 최적화, 기능 요구사항 구조화 관점에서 지시를 분석합니다.",
                "@sa": "역할: [System Architect] - 대규모 확장성, 모듈 분리, 클라우드/온프레미스 이식성, 아키텍처 패턴 관점에서 설계합니다.",
                "@se": "역할: [Software Engineer] - 견고한 클린 코드, 효율적인 알고리즘, 단위 테스트(Pytest), 정밀한 예외 처리를 구현합니다.",
                "@qa": "역할: [QA Lead] - 엣지 케이스, 비정상 입력, 성능 회귀, 보안 취약점을 체계적으로 검증합니다.",
                "@cso": "역할: [Chief Security Officer] - OWASP Top 10, Secrets 유출 탐지, 의존성 공급망 보안을 엄격히 검사합니다.",
                "@dba": "역할: [Database Admin] - 인덱스 최적화, 쿼리 성능, 트랜잭션 무결성, 스키마 마이그레이션을 담당합니다.",
                "@growth": "역할: [Growth Lead] - 제품 지표, 사용자 유지율, 비즈니스 ROI를 극대화하는 방향으로 설계합니다."
            }
            role_desc = personas_map.get(persona.lower(), f"역할: [{persona}] 전문가 관점에서 작업을 수행합니다.")
            base_prompt.append(f"\n[활성화된 페르소나]\n{role_desc}")

        if command:
            base_prompt.append(f"\n[실행 워크플로우 커맨드]\n활성화된 슬래시 워크플로우: {command}")

        return "\n".join(base_prompt)

    def scan_sast_security(self, code_content: str, filename: str = "source.py") -> Dict[str, Any]:
        """
        정적 보안 SAST 검사기 (하드코딩 키, eval, SQL Injection 패턴 탐색)
        """
        issues = []
        
        # 1. Hardcoded Secret Detection
        secret_patterns = [
            (r'(?i)(api[_-]?key|secret|token|password)\s*=\s*["\'][a-zA-Z0-9_\-]{16,}["\']', "하드코딩된 시크릿/API 키가 감지되었습니다. 환경변수를 사용하세요."),
            (r'sk-[a-zA-Z0-9]{20,}', "OpenAI/OpenRouter API 키 형식의 시크릿이 소스코드에 직접 노출되었습니다.")
        ]
        for pattern, msg in secret_patterns:
            if re.search(pattern, code_content):
                issues.append({"level": "HIGH", "rule": "CORTEX-SEC-01", "message": msg})

        # 2. Insecure Eval / Exec Detection
        if re.search(r'\b(eval|exec)\s*\(', code_content):
            issues.append({"level": "CRITICAL", "rule": "CORTEX-SEC-02", "message": "임의 코드 실행을 유발할 수 있는 eval()/exec() 함수 사용이 감지되었습니다."})

        # 3. SQL Injection Regex Check
        if re.search(r'(?i)execute\s*\(\s*["\'].*?(SELECT|INSERT|UPDATE|DELETE).*?%s', code_content):
            issues.append({"level": "MEDIUM", "rule": "CORTEX-SEC-03", "message": "문자열 포매팅 기반 원시 SQL 쿼리가 감지되었습니다. 파라미터화된 쿼리를 사용하세요."})

        return {
            "status": "passed" if len(issues) == 0 else "warning" if all(i["level"] != "CRITICAL" for i in issues) else "failed",
            "issues_count": len(issues),
            "issues": issues,
            "filename": filename,
            "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

    def validate_triad(self, plan_path: Optional[str], code_path: Optional[str], spec_path: Optional[str]) -> Dict[str, Any]:
        """
        작업 트라이어드 ([계획]-[코드]-[명세서]) 1:1:1 무결성 및 날짜 명명 검사기
        """
        today_prefix = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y-%m-%d")
        
        checks = {
            "has_plan": plan_path is not None and os.path.exists(os.path.join(self.workspace_root, plan_path)),
            "has_code": code_path is not None,
            "has_spec": spec_path is not None and os.path.exists(os.path.join(self.workspace_root, spec_path)),
            "plan_has_date_prefix": plan_path.split("/")[-1].startswith(today_prefix) if plan_path else False,
            "spec_has_date_prefix": spec_path.split("/")[-1].startswith(today_prefix) if spec_path else False
        }

        all_passed = checks["has_plan"] and checks["has_code"] and checks["has_spec"] and checks["plan_has_date_prefix"] and checks["spec_has_date_prefix"]

        return {
            "triad_valid": all_passed,
            "details": checks,
            "date_rule": f"Prefix '{today_prefix}_' verified."
        }
