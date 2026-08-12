# 💻 Enterprise Coding Agent MVP (Desktop-First Runner)

본 디렉터리는 **엔터프라이즈 코딩 에이전트 MVP 시연 소스코드**가 위치하는 폴더입니다.
개발자 로컬 데스크톱(Desktop/Workstation) 환경에서 1차 동작을 완수한 뒤, 구글 클라우드(GCP) 및 Red Hat OpenShift AI(SNO) 온프레미스로 확산 이식됩니다.

---

## 🌟 핵심 기능
1. **Vibe Coding Engine**: 자연어 요구사항 입력 시 요구사항 파싱, 스키마 정의 및 다중 파일 자동 생성.
2. **MCP (Model Context Protocol) Server**: VS Code(Continue.dev) & Agentic CLI(Antigravity) 통합 커넥터.
3. **Local Desktop Runner**: 로컬 Docker / Python 환경 상에서 동작하는 초경량 에이전트 오케스트레이터.
4. **Sandboxed Self-Correction**: 샌드박스 내부 테스트 실행 및 에러 스택 트레이스 자동 보정.

---

## 🚀 빠른 시작 (Local Desktop Mode)

### 1. 가상환경 및 패키지 설치
```bash
# uv를 활용한 .venv 기반 가상환경 구성
uv venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. 환경변수 설정
```bash
# .env 파일 작성 (개발 단계 OpenRouter API Key 설정)
OPENROUTER_API_KEY=your_openrouter_api_key_here
LLM_PROVIDER=openrouter  # 이식 시 'rhoai_vllm'으로 전환
```

---

© 2026 AI Architecture Engineering Team. All rights reserved.
