# [Plan] Agent Smith IDE Stage 1 로컬 데스크톱 런너(Desktop Runner) 구현 계획서

본 문서는 **Agent Smith IDE의 Stage 1 로컬 데스크톱(Desktop-First) 실행 버전 런너** 구축 계획서입니다.

---

## 🎯 1. 구현 목표
* **1-Click 로컬 데스크톱 실행 런너 (`desktop_runner.py`) 구축**:
  * 로컬 `.venv` 파이썬 가상환경 검증 및 FastAPI 백엔드 서버(Port 5000) 자율 시동.
  * CLI 터미널 환경에서도 Vibe 의도를 직접 입력하고 샌드박스 결과를 실시간 확인하는 인터랙티브 로컬 런너 제공.
  * IDE 환경(VS Code Extension/Continue)과의 로컬 MCP JSON-RPC Gateway 연동 지원.

---

## 🏗️ 2. 컴포넌트 구성
* `agentsmith/coding-agent/src/desktop_runner.py`: 로컬 데스크톱 런너 오케스트레이터
* `agentsmith/coding-agent/scripts/check_secrets.py`: OpenRouter Key 등 비밀값 누출 방지 가드레일
* `agentsmith/coding-agent/docs/specs/2026-08-13_desktop_runner_spec.md`: 상세 명세서

---

© 2026 AI Architecture Engineering Team. All rights reserved.
