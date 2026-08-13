# [Spec] Agent Smith IDE 로컬 데스크톱 런너 상세명세서

본 문서는 **Agent Smith IDE 로컬 데스크톱 실행 버전**의 구현 명세서입니다.

---

## 📌 1. 실행 가이드
* **엔트리 스크립트**: `agentsmith/coding-agent/src/desktop_runner.py`
* **시작 명령**:
```bash
python agentsmith/coding-agent/src/desktop_runner.py
```

---

## 🛠️ 2. 핵심 동작 절차
1. **가상환경 감지**: 로컬 `.venv` 파이썬 패키지 세팅 검증.
2. **백엔드 서버 구동**: FastAPI (`main.py`)를 `http://localhost:5000` 포트로 론칭.
3. **터미널 Vibe CLI 인터랙티브 대화**: 콘솔에서 자연어 프롬프트를 입력하면 실시간 자율 코드 생성 및 pytest 샌드박스 검증 수행.
4. **시크릿 검사 가드레일**: `scripts/check_secrets.py`로 OpenRouter API Key 등 하드코딩 유출 차단.

---

© 2026 AI Architecture Engineering Team. All rights reserved.
