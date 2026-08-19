"""
gstack Specialist Personas, Lifecycle Workflows & Dynamic Plugin Loader Module
Loads built-in personas, lifecycle workflows, and user customizations from .agents/
"""

import os
import glob
from typing import Dict, Any, List, Optional

BUILTIN_PERSONAS = [
    {"id": "@pm", "name": "Product Manager", "desc": "사용자 가치, UX 로드맵 및 기획 조정", "icon": "🧭"},
    {"id": "@sa", "name": "System Architect", "desc": "시스템 인프라, 확장성 및 고수준 디자인 패턴", "icon": "🏛️"},
    {"id": "@se", "name": "Software Engineer", "desc": "핵심 로직 구현, 클린 코드 및 단위 테스트", "icon": "💻"},
    {"id": "@qa", "name": "QA Lead", "desc": "체계적인 테스트, 엣지 케이스 검증 및 리그레션 방지", "icon": "🧪"},
    {"id": "@cso", "name": "Chief Security Officer", "desc": "OWASP 보안 감사, 시크릿 탐지 및 공급망 점검", "icon": "🛡️"},
    {"id": "@dba", "name": "Database Admin", "desc": "SQL 최적화, 스키마 마이그레이션 및 무결성 관리", "icon": "💾"},
    {"id": "@growth", "name": "Growth Lead", "desc": "비즈니스 ROI, 전환율 최적화 및 지표 분석", "icon": "📈"},
    {"id": "@ceo", "name": "CEO / Founder", "desc": "제품 비전, 10-Star 제품 재정의 및 전략적 야망", "icon": "👑"}
]

BUILTIN_WORKFLOWS = [
    {"command": "/office-hours", "name": "아이디어 브레인스토밍", "category": "Plan", "desc": "코드 작성 전 요구사항과 핵심 가치를 재정의합니다."},
    {"command": "/plan-ceo-review", "name": "CEO 관점 전략 리뷰", "category": "Plan", "desc": "10-Star 제품 관점에서 기능 범위와 야망을 확장합니다."},
    {"command": "/plan-eng-review", "name": "아키텍처/엔지니어링 검토", "category": "Architecture", "desc": "데이터 흐름, 엣지 케이스, 테스트 커버리지를 확정합니다."},
    {"command": "/review", "name": "PR 코드 리뷰", "category": "Engineering", "desc": "보안, 부작용, 신뢰 경계 위반 여부를 사전 검토합니다."},
    {"command": "/investigate", "name": "체계적 근본 원인 디버깅", "category": "Debugging", "desc": "원인 규명 전 임의 수정을 금지하는 4단계 디버깅 루프입니다."},
    {"command": "/qa", "name": "실제 브라우저 QA & 자동 수정", "category": "QA", "desc": "브라우저를 열어 버그를 찾고 소스코드를 원자적으로 수정합니다."},
    {"command": "/qa-only", "name": "QA 리포트 전용", "category": "QA", "desc": "코드 수정 없이 버그 보고서와 스크린샷만 생성합니다."},
    {"command": "/design-review", "name": "디자인 시각적 감사", "category": "Design", "desc": "UI 정렬, 일관성, 슬롭 패턴을 점검하고 픽셀을 보정합니다."},
    {"command": "/ship", "name": "원클릭 릴리즈 & PR", "category": "Release", "desc": "테스트 실행, 버전 범프, 체인지로그 갱신, PR을 한 번에 실행합니다."},
    {"command": "/document-release", "name": "문서 릴리즈 동기화", "category": "Docs", "desc": "배포된 코드와 문서(README, 명세서)를 최신으로 동기화합니다."}
]

class GstackLoader:
    def __init__(self, workspace_root: Optional[str] = None):
        if not workspace_root:
            workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.workspace_root = workspace_root

    def list_all_customizations(self) -> Dict[str, Any]:
        """
        내장 페르소나, 워크플로우 및 .agents/ 하위 커스텀 스킬/룰 동적 탐색
        """
        custom_skills = []
        custom_rules = []

        # 1. .agents/skills/ 탐색
        skills_dir = os.path.join(self.workspace_root, ".agents", "skills")
        if os.path.exists(skills_dir):
            for skill_name in os.listdir(skills_dir):
                skill_path = os.path.join(skills_dir, skill_name, "SKILL.md")
                if os.path.exists(skill_path):
                    custom_skills.append({
                        "name": skill_name,
                        "path": f".agents/skills/{skill_name}/SKILL.md",
                        "type": "custom_skill"
                    })

        # 2. .agents/rules/ 탐색
        rules_dir = os.path.join(self.workspace_root, ".agents", "rules")
        if os.path.exists(rules_dir):
            for rule_file in glob.glob(os.path.join(rules_dir, "*.md")):
                rule_name = os.path.basename(rule_file)
                custom_rules.append({
                    "name": rule_name,
                    "path": f".agents/rules/{rule_name}",
                    "type": "custom_rule"
                })

        return {
            "status": "success",
            "personas": BUILTIN_PERSONAS,
            "workflows": BUILTIN_WORKFLOWS,
            "custom_skills": custom_skills,
            "custom_rules": custom_rules,
            "total_personas": len(BUILTIN_PERSONAS),
            "total_workflows": len(BUILTIN_WORKFLOWS),
            "total_custom_extensions": len(custom_skills) + len(custom_rules)
        }

    def parse_input_intent(self, intent_text: str) -> Dict[str, Any]:
        """
        사용자 입력 문자열에서 @persona 및 /command 자동 분리 및 추출
        예: "@sa /review 인증 아키텍처를 검토해줘" -> persona: "@sa", command: "/review", clean_intent: "인증 아키텍처를 검토해줘"
        """
        persona = None
        command = None
        clean_text = intent_text.strip()

        # @persona 추출
        for p in BUILTIN_PERSONAS:
            if clean_text.startswith(p["id"]) or f" {p['id']} " in f" {clean_text} ":
                persona = p["id"]
                clean_text = clean_text.replace(p["id"], "").strip()
                break

        # /command 추출
        for w in BUILTIN_WORKFLOWS:
            if clean_text.startswith(w["command"]) or f" {w['command']} " in f" {clean_text} ":
                command = w["command"]
                clean_text = clean_text.replace(w["command"], "").strip()
                break

        return {
            "original_intent": intent_text,
            "persona": persona,
            "command": command,
            "clean_intent": clean_text if clean_text else intent_text
        }
