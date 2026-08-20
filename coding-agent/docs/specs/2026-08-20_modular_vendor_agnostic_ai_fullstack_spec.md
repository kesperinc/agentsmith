# 벤더 중립적·모듈형 7-Layer AI 풀스택 아키텍처 개정 및 DOCX 생성 명세서

## 1. 개정 배경 및 목적 (Background & Objectives)
- **개정 일시**: 2026-08-20
- **핵심 요구사항**: 뉴타닉스(Nutanix), A8(Articul8), Cohere, 아크릴 조나단(Acryl Jonathan) 등은 메가존클라우드가 고객에게 제안할 수 있는 다양한 솔루션 생태계 중 **하나의 선택형 옵션(Pluggable Ecosystem Options)**임. 특정 단일 상품을 중심으로 전체 AI 스택을 규정하거나 종속시키지 않고, **'벤더 중립적·개방형 모듈형 7-Layer AI 아키텍처(Vendor-Agnostic Modular Architecture)'** 원칙을 전면 반영함.

---

## 2. 모듈형 7-Layer 아키텍처 재정의 (Redefined 7-Layer Architecture)

| 계층 (Layer) | 표준 기능 및 모듈 역할 | 선택 가능한 주요 솔루션 생태계 옵션 (Pluggable Options) |
|---|---|---|
| **Layer 7. Application & UI** | 현업 업무용 AI UI 및 기간계 시스템 결합 | Enterprise Chatbot UI, 사내 코딩 에이전트(MCP), ERP/CRM/AICC, SAP S/4HANA PCE CDC 실시간 연동, 사내 포털 커스텀 SI |
| **Layer 6. Orchestration & Agents** | 지능형 멀티 모델 오케스트레이션 & 보안 API Gateway | **[옵션 1]** Articul8 Model Mesh Orchestrator<br>**[옵션 2]** Dify, LangChain, LlamaIndex, Flowise<br>**[옵션 3]** 사내 프라이빗 보안 API Gateway & 커스텀 지능형 라우터 |
| **Layer 5. Foundation Models & SLM** | 사내 온프레미스 소버린 파운데이션 모델 & 파인튜닝 | **[오픈소스]** Llama 3.1, Mistral, Qwen 2.5, DeepSeek<br>**[구축형 상용]** Cohere Command R+, 아크릴 조나단(Acryl Jonathan), Upstage Solar<br>**[하이브리드]** 사내 sLLM + 외부 클라우드 LLM 하이브리드 연계 |
| **Layer 4. AI Serving & MLOps** | 고속 추론 서빙 및 MLOps 라이프사이클 관리 | **[추론 엔진]** vLLM, NVIDIA NIM, Triton Inference Server, TGI, KServe<br>**[MLOps 관제]** PyTorch, Ray, MLflow, Kubeflow, Prometheus, Grafana |
| **Layer 3. Data & Knowledge Platform** | 엔터프라이즈 데이터 레이크 & 벡터 지식 거버넌스 | **[데이터 레이크]** Databricks Lakehouse (Unity Catalog), Snowflake, MinIO, Kafka<br>**[Vector & DB]** Milvus, Qdrant, pgvector / Oracle, PostgreSQL, SAP HANA |
| **Layer 2. OS & Virtualization** | 하이브리드 가상화 및 컨테이너 오케스트레이션 | **[옵션 1]** Red Hat OpenShift AI (RHOAI)<br>**[옵션 2]** Nutanix NCI(무상 AHV) + Nutanix NKP<br>**[옵션 3]** 기존 VMware vSphere 환경 유지 연동<br>**[옵션 4]** Baremetal K8s / SUSE Rancher |
| **Layer 1. Compute, Storage & Fabric** | 가속 컴퓨팅 서버 및 고성능 I/O 스토리지 | **[서버]** Dell PowerEdge, HPE ProLiant, Supermicro<br>**[가속기]** NVIDIA GPU, Intel Gaudi 2/3, 국산 NPU(퓨리오사, 리벨리온)<br>**[스토리지]** Dell PowerScale, PureStorage, Zadara, NetApp / 400GbE, InfiniBand |
| **Cross-Cutting. Security & Governance** | 전 계층 Zero-Trust 보안 & 데이터 주권 통제 | 완전 폐쇄망(Air-Gapped) 오프라인 패키징, 부서별 세분화된 RBAC 권한 제어, PII 개인정보 자동 비식별화, 전 과정 감사 로그 및 출처 추적성(Audit) |

---

## 3. 수정 및 갱신된 산출물 (Updated Artifacts)
1. `offering/generate_ai_factory_comparison_docx.py` (모듈형 아키텍처 원칙 전면 반영)
2. `offering/docx/2026-08-20_NVIDIA_Dell_MZC_AI_Factory_Comparison_and_Implementation_Guide.docx` (갱신된 Word 문서)
3. `offering/docx/nvidia_ai_factory_vs_mzc_fullstack_comparison.docx` (동기화 파일)
4. `docs/2026-08-20_NVIDIA_Dell_MZC_AI_Factory_Comparison_and_Implementation_Guide.docx` (공용 디렉토리 복사본)
5. `offering/nvidia_ai_factory_vs_mzc_fullstack_comparison.html` (웹 제안서 내 7계층 정의 업데이트)

---

## 4. 검증 결과 (Validation)
- 특정 솔루션 종속적 표현 제거 및 계층별 선택 옵션(Pluggable Options) 구조로 완전 전환.
- 단락 55개, 테이블 9개 구조로 DOCX 빌드 완료 (48.8 KB).
