# [Plan] Agent Smith IDE 음성·인증·모델선택 기능 구현 계획서

본 문서는 **Agent Smith IDE의 신규 3대 기능(Speech-to-Text, 사내 이메일 로그인, AI 모델 드롭다운)** 구현 계획서입니다.

---

## 🎯 1. 구현 목표
* **음성 받아쓰기 및 음성 제어 (STT)**: 마이크 오디오 인풋 캡처 및 로컬/사내 Whisper API와의 실시간 STT 연동.
* **사내 이메일 로그인**: 사내 이메일 입력 시 OTP 번호(일회용 비밀번호)를 이메일로 자동 전송하고 6자리 검증을 수행하는 인증 모듈 구축 (LDAP 연동 구조 제공).
* **AI 모델 동적 선택**: 챗 패널 UI에서 실시간 모델 전환이 가능하도록 드롭다운을 설계하고, 백엔드 MCP 라우터에 스위칭 인터페이스 탑재.

---

## 🏗️ 2. 컴포넌트 구성 및 역할

```
agentsmith/coding-agent/
├── src/
│   ├── main.py                    # OTP 이메일 전송/검증 API 스켈레톤 추가
│   └── vibe/
│       └── engine.py              # 요청으로 들어온 selected_model 동적 연동부 보완
└── docs/
    ├── plans/
    │   └── 2026-08-13_speech_auth_model_select_plan.md   # 본 문서
    └── specs/
        └── 2026-08-13_speech_auth_model_select_spec.md   # API 및 UI 상세 규격서
```

---

## 📅 3. 상세 추진 일정
1. **1단계: 백엔드 API 설계 및 스켈레톤 작성**: `main.py`에 이메일 OTP 인증용 REST Endpoint 연동. (완료 예정: 금일)
2. **2단계: IDE 웹뷰 UI 연동**: Left Chat Panel에 마이크 아이콘, 모델 선택 드롭다운, 사내 메일 OTP 로그인 모달 퍼스트 에이드 UI 렌더링.
3. **3단계: 로컬 Whisper 및 사내 SMTP 연동**: 로컬 Whisper API 연결부 및 사내망 SMTP 서버를 통한 발송 검증 기능 실구현.

---

© 2026 AI Architecture Engineering Team. All rights reserved.
