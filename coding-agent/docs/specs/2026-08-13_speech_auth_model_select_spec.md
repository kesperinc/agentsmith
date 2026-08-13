# [Spec] Agent Smith IDE 음성·인증·모델선택 상세명세서

본 문서는 **Agent Smith IDE의 Speech-to-Text, 사내 이메일 인증, AI 모델 선택 기능**의 구현 및 API 인터페이스 상세 명세서입니다.

---

## 📌 1. 사내 이메일 OTP 로그인 API 명세

### A. OTP 일회용 패스코드 발송 API
* **Endpoint**: `POST /api/auth/otp/send`
* **Request Body**:
```json
{
  "email": "user1@kesper.co.kr"
}
```
* **Response Body**:
```json
{
  "status": "success",
  "message": "인증용 6자리 OTP 코드가 사내 이메일로 전송되었습니다.",
  "expires_in_seconds": 180
}
```

### B. OTP 일회용 패스코드 검증 API
* **Endpoint**: `POST /api/auth/otp/verify`
* **Request Body**:
```json
{
  "email": "user1@kesper.co.kr",
  "otp_code": "847291"
}
```
* **Response Body**:
```json
{
  "status": "success",
  "message": "인증에 성공하였습니다.",
  "access_token": "bearer-token-xyz-12345",
  "user_hash_id": "8a7f9b8c"
}
```

---

## 🎤 2. 음성 코딩 Speech-to-Text (STT) 규격

* **음성 입력 버퍼 형식**: Left Chat Panel에서 Web Audio API를 기동하여 캡처한 PCM 리니어 단일 채널(Mono) 16kHz 데이터.
* **로컬 STT 변환 연동**: 백엔드 REST API 또는 Electron IPC를 통해 수집된 오디오 chunk를 로컬/사내 Whisper API (`/v1/audio/transcriptions`)로 전달하고 변환된 텍스트 결과를 UI 입력 창에 피딩.

---

## 🤖 3. AI 모델 동적 스위칭 명세

* **API Payload 확장**: `POST /api/vibe/generate` 호출 시 `model_id` 파라미터 전달.
```json
{
  "intent": "비동기 코드로 변경해줘",
  "model_id": "anthropic/claude-3.5-sonnet"
}
```
* 백엔드 `LLMAdapter`는 해당 `model_id`를 검출하여 OpenRouter 또는 사내 온프레미스 vLLM(`http://qwen-coder.rhoai.svc:8000/v1`)의 타깃 모델 엔드포인트로 API 요청을 동적 포워딩합니다.

---

© 2026 AI Architecture Engineering Team. All rights reserved.
