# 코드 및 산출물 변경 명세서 (Specs)

- **작성 일자**: 2026-08-18
- **문서명**: `2026-08-18_nvidia_ai_factory_vs_mzc_fullstack_spec.md`
- **관련 커밋/작업**: NVIDIA vs Dell vs MZC AI Fullstack 비교 분석 및 11단계 패키지 4-Phase 압축 로드맵 구축
- **기반 문서**: MegazoneCloud Sales Offering Guide using AI Infra & solution (2026.08)

---

## 1. 작업 목적 및 개요
엔비디아의 **순수 AI Factory**, 델의 **Dell AI Factory with NVIDIA**, 메가존클라우드의 **소버린 7-Layer AI Full Stack** 간의 3자 비교 분석을 완성하고, 첨부자료 13p의 11단계 세일즈 패키지를 고객 도입 여정에 맞게 **4대 핵심 Phase**로 압축 그루핑하여 제안서 가독성과 실행력을 극대화함.

---

## 2. 변경 일자별 파일 수정 맵 (Specs Map)

| 일자 | 구분 | 대상 파일 경로 | 작업 내용 및 주요 변경 사항 |
| :--- | :---: | :--- | :--- |
| 2026-08-18 | **[신규/갱신]** | `offering/nvidia_ai_factory_vs_mzc_fullstack_comparison.html` | • 7대 레이어 1:1 비교 분석 인터랙티브 HTML 문서<br>• Dell AI Factory with NVIDIA vs 순수 NVIDIA AI Factory vs MZC 3자 비교 전용 탭 추가<br>• **[추가] 11개 세일즈 패키지를 4대 핵심 Phase(진단/검증 ➔ 코어전환 ➔ AI현대화 ➔ 운영/확장)로 압축 그루핑** |
| 2026-08-18 | **[수정]** | `offering/index.html` | 오퍼링 포털 메인 화면 최상단에 신규 비교 분석 제안서 카드 연동 |
| 2026-08-18 | **[갱신]** | `agentsmith/coding-agent/docs/specs/2026-08-18_nvidia_ai_factory_vs_mzc_fullstack_spec.md` | 본 작업 명세서 갱신 |

---

## 3. 11단계 ➔ 4대 Phase 압축 그루핑 구조

| Phase 구분 | 명칭 및 목표 | 기간 및 도입 방식 | 포함 세부 패키지 (11-Step Mapping) |
| :---: | :--- | :---: | :--- |
| **Phase 1** | **진단 & 파일럿 검증**<br>(Assessment & Validation) | 2~4주<br>(Small Start) | • **Pkg 01. Rapid Assessment** (인벤토리/종속성/TCO 분석)<br>• **Pkg 02. Migration Pilot** (10~20 VM 기술 검증)<br>• **Pkg 09. Funding Support** (AWS/Intel/Nutanix 지원금 확보) |
| **Phase 2** | **코어 인프라 전환 & 하이브리드**<br>(Core Migration & Landing) | 1~3개월<br>(Fast Start) | • **Pkg 03. Migration Factory** (Nutanix Move 무중단 본 이관)<br>• **Pkg 04. NC2 Landing** (AWS 하이브리드 클라우드 확장)<br>• **Pkg 05. DR & Security** (RPO/RTO 최적화 DR & 망분리) |
| **Phase 3** | **AI 인프라 & 플랫폼 현대화**<br>(AI Infra & Platform Modernization) | 1~2개월<br>(소버린 AI 가동) | • **Pkg 06. AI-ready Infra** (Dell/NVIDIA GPU·NPU 클러스터 증설)<br>• **Pkg 07. AI Platform** (NVIDIA NIM, AIR Studio, RAG/Agent) |
| **Phase 4** | **운영 관리 & 전사 확장**<br>(Managed Ops & Scale-out) | 상시 지속<br>(지속 운영) | • **Pkg 08. Managed Ops** (Prism 24x7 관제 및 SLA 패치)<br>• **Pkg 10. GTM Workshop** (Top Account 맞춤 Use Case 공동 발굴)<br>• **Pkg 11. Scale-out** (전사 AI Factory 클러스터 확장) |
