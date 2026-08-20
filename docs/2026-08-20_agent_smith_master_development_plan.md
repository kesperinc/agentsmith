# 📄 [2026-08-20] Agent Smith 차세대 마스터 종합 개발 계획서 (Master Development Plan)

- **문서 작성일**: 2026-08-20
- **프로젝트명**: Agent Smith Enterprise AI Coding Agent & Desktop IDE Platform
- **작성자**: Agent Smith AI Pair Engineering Team
- **관련 프로젝트 필수 규칙**: AGENTS.md (규칙 3: Desktop ➔ Cloud ➔ On-Premise 3단계 배포, 규칙 5: 작업 트라이어드, 규칙 12: 기초/상세 설계서 수립, 규칙 16: `YYYY-MM-DD_` 명명 규칙)

---

## 1. 개요 (Overview)

본 개발 계획서는 Agent Smith 엔터프라이즈 코딩 에이전트 패키지의 **13가지 필수 수칙 및 가드레일**을 100% 준수하여, 데스크톱 IDE 가드레일 확보 이후 구글 클라우드(GCP) 및 온프레미스(Red Hat OpenShift AI)로 확장하는 로드맵과 세부 마일스톤을 정의합니다.

---

## 2. 3단계 배포 및 개발 아키텍처 (3-Tier Architecture)

```
+-----------------------------------------------------------------------+
| Phase 1: Desktop-First IDE (완료 및 가드레일 확보)                    |
| • Electron 27 Standalone IDE, FastAPI Backend (Port 5000)             |
| • out 렌더러 번들, %USERPROFILE% 런처 가드레일                        |
| • Mem0 Qdrant DB & CortexOS (한국어, UTF-8, 트라이어드, SAST)        |
+-----------------------------------┬-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| Phase 2: Cloud (GCP) & Multi-Tenant Sandbox (차기 마일스톤)           |
| • GCP Cloud Run / GKE 기반 멀티 테넌트 샌드박스 워크스페이스          |
| • Git branch 가드레일 (feature/* -> staging -> main)                  |
| • OpenRouter & Direct API 비용 최적화 라우팅                          |
+-----------------------------------┬-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| Phase 3: On-Premise (RHOAI) 1-Click Porting (최종 배포)               |
| • Red Hat OpenShift AI 온프레미스 GPU 환경 1-Click 포팅 스크립트      |
| • 파이썬/자바 실시간 Vibe 코딩 및 FIM (Fill-In-the-Middle) 행사 샘플  |
+-----------------------------------------------------------------------+
```

---

## 3. 핵심 마일스톤 및 개발 기능 세부 명세 (Detailed Milestones)

### Milestone 1: GCP 멀티 테넌트 샌드박스 관리자 (Rule 7)
- **목적**: 개발자별 독립된 멀티 테넌시 샌드박스 및 가상 워크스페이스 제공.
- **주요 모듈**: `coding-agent/src/cloud/sandbox_manager.py`
- **기능**: 컨테이너 세션 격리 및 로컬-클라우드 동기화 상태 유지.

### Milestone 2: Cloud-to-On-Prem 1-Click 포팅 스크립트 (Rule 8)
- **목적**: 온프레미스 HW(RHOAI) 준비 시 1-Click으로 전체 시스템 이식.
- **주요 모듈**: `scripts/port_to_rhoai.py`
- **기능**: Docker 번들 및 모델 가드레일 자동 전송.

### Milestone 3: 행사장 실시간 Vibe 코딩 및 FIM 시연 샘플 (Rule 11)
- **목적**: 관람객이 직접 시연할 수 있는 파이썬/자바 실시간 Vibe 코딩 샘플 준비.
- **주요 경로**: `samples/vibe_fim_demo/`
- **기능**: FIM 인라인 코드 완성 및 대화형 시연 흐름 제어.

---

## 4. 품질 및 보안 가드레일 (Quality & Security Guardrails)

1. **테스트 가드레일**: PR 제출 전 Pytest 및 `verify_desktop_bundle.py --verify-dist` 100% 통과.
2. **보안 가드레일**: SAST 보안 검사기(`CORTEX-SEC-01` ~ `03`) 실행.
3. **인코딩 가드레일**: 모든 생성 파일 및 로그 UTF-8 Bom-less 한글 출력 강제.
