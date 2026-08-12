# 2026-08-12 Agent Smith 인프라 및 하드웨어 감지 상세명세서 (Infrastructure Detector Specification)

본 문서는 **Agent Smith IDE**의 로컬 실행 환경 최적화 및 2바이트 다국어 보장, 그리고 온프레미스 AI 하드웨어 가속 검출을 담당하는 **Infrastructure Detector** 모듈의 구현 명세서입니다.

---

## 🛠️ 1. 컴포넌트 구성 정보

* **환경 검증 모듈**: `agentsmith/coding-agent/src/adapters/hardware_detector.py`
* **데스크톱 실행 제어기**: `agentsmith/coding-agent/src/desktop_runner.py`

---

## 📌 2. 상세 구현 명세 (Technical Specification)

### 2.1 1-Click Python `uv` 가상환경 및 Node.js 설치 자동화
1. **Python `uv` venv 구축**:
   - 로컬 디렉터리에 `.venv` 가상환경 유무를 탐색합니다.
   - 미설치 시 전역 `uv` 패키지 매니저의 유무를 조회하고, `uv` 감지 시 `uv venv` 및 `uv pip install -r requirements.txt` 명령을 통해 초고속(3초 내외) 가상환경 환경 구성을 진행합니다.
   - `uv`가 미설치된 환경인 경우 일반 `venv` 모듈을 폴백(Fallback)으로 기동하여 `.venv` 및 의존 패키지를 안전하게 빌드합니다.
2. **Node.js 런타임 탑재**:
   - 시스템 전역 `node` 실행 파일의 유무를 `shutil.which`로 조회합니다.
   - 미감지 시 `agentsmith/coding-agent/bin/` 디렉터리에 포터블 바이너리가 존재하는지 2차 탐색합니다.
   - 포터블 바이너리도 전무한 경우, Windows 환경 기준으로 `https://nodejs.org/dist/`에서 경량 포터블 `node.exe`를 자동 다운로드하여 IDE 전용 폴더에 이식함으로써 1-Click 구동 환경을 완결시킵니다.

### 2.2 하드웨어 및 클러스터 감지 하네스
1. **Red Hat OpenShift AI (RHOAI) 스캔**:
   - 로컬 `oc` 또는 `kubectl` 설정의 `current-context`를 조회하여 현재 활성화된 세션이 OpenShift 또는 RHOAI 클러스터 영역에 접해있는지 식별합니다.
   - 감지 성공 시 vLLM ServingRuntime API 엔드포인트(`http://qwen-coder.rhoai.svc.cluster.local:8000`)를 런너 프로세스의 환경 변수(`RHOAI_VLLM_ENDPOINT`)로 바인딩합니다.
2. **DGX Spark 식별**:
   - 시스템 BIOS/DMI 제품 정보를 쿼리하여 `DGX` 또는 `Spark` 제품명이 검출되는지 파싱합니다.
     - Windows: `wmic csproduct get name`
     - Linux: `/sys/class/dmi/id/product_name`
   - 고성능 HW 감지 성공 시 모델 실행 프로필(`AGENT_SMITH_HW_PROFILE`)을 `maximum-performance`로 설정하여 고성능 모델(32B/72B) 매핑 가속을 수행합니다.
3. **가속기 (NVIDIA CUDA / Intel / AMD) 스캔**:
   - `nvidia-smi`를 실행하여 장착된 NVIDIA GPU 명칭 및 VRAM 크기를 수집합니다.
   - PowerShell 디바이스 쿼리를 기동하여 Intel Arc(OpenVINO 대응) 및 AMD Radeon 장치의 유무를 감지해 환경 변수에 주입합니다.

### 2.3 2바이트 다국어 문자 보장 및 현지화 가드레일 (Harness)
1. **인코딩 가드레일**:
   - Windows 등 환경에서 cp949 디코딩 에러를 원천 차단하기 위해 `desktop_runner.py`가 FastAPI 서버 프로세스를 구동할 때 환경 변수에 `PYTHONIOENCODING=utf-8`을 기본 강제 주입하여 기동합니다.
2. **한글 주석/출력 생성 룰**:
   - 에디터 UI 메뉴는 영어로 기동되지만 AI 에이전트의 CLI 및 코드 주석 생성 시 가드레일 프롬프트에 의해 한국어로 강제 자동 변환되어 안전한 UTF-8 Bom-less 파일 포맷으로 디스크에 동기화 저장됩니다.

---

## 📊 3. 파일 변경점 추적 맵 (Specs Map)

1주차 작업 진행에 따라 생성 및 수정된 파일들의 매핑 구조입니다.

| 변경 일자 | 변경 유형 | 파일 경로 | 변경 세부 내용 |
|-----------|-----------|-----------|----------------|
| **2026-08-12** | **[NEW]** | [hardware_detector.py](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/adapters/hardware_detector.py) | Python uv venv 자동 구성, Node.js 포터블 다운로드, RHOAI/vLLM 감지, DGX Spark 및 GPU(CUDA/Intel/AMD) 검출 모듈 신규 구현 |
| **2026-08-12** | **[MODIFY]** | [desktop_runner.py](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/src/desktop_runner.py) | 초기 banner 실행 단계에 인프라 감지 추가, FastAPI 구동 환경변수 바인딩 추가, 깨져 있던 UI Mockup 경로 `proposal/` -> `offering/` 수정 |
| **2026-08-12** | **[NEW]** | [2026-08-12_infrastructure_detector_spec.md](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-12_infrastructure_detector_spec.md) | **[본 문서]** 1주차 완료 아티팩트 상세 구현 명세서 작성 |
| **2026-08-12** | **[MODIFY]** | [AGENTS.md](file:///c:/dev/antigravity-workspace/aifullstack/AGENTS.md) | 날짜 접두사 규칙(16번) 및 인코딩/인프라 자동화(14, 15번) 전역 룰 추가 |
| **2026-08-12** | **[MODIFY]** | [README.md](file:///c:/dev/antigravity-workspace/aifullstack/README.md) | 리네임된 `agentsmith/` 폴더 트랙 반영 |
| **2026-08-12** | **[MODIFY]** | [TODO.md](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/TODO.md) | 리네이밍 갱신 및 완료된 스펙 업데이트 반영 |
