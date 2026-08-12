# 🚀 Agent Smith IDE 단계별 TODO 로드맵

본 문서는 **Agent Smith IDE (Custom Code-OSS AI Editor)**의 개발 과제 및 릴리즈 로드맵 현행화 목록입니다. 웹 버전 개발 관련 항목을 제외하고, 로컬 데스크톱 중심의 IDE 빌드, 브랜딩, 가드레일 및 온프레미스 배포 호환성 확보를 중심으로 재작성되었습니다.

* **최종 현행화 일자**: 2026년 8월 12일
* **개발 기조**: Windows 빌드 및 기능 완성을 최우선(Phase 1)으로 진행하며, 리눅스/Red Hat 빌드 호환성(Phase 2)을 차기 진행 과제로 둡니다.

---

## 🎯 1단계: 기반 설정 및 로컬 가드레일 (완료)
- [x] 프로젝트 메인 Git 브랜치 가드레일 전략 수립 및 원격 저장소 동기화 (`main`, `staging`, `feature/setup-git-guardrails`)
- [x] .gitignore 파일 보완 (vscode/ 차단 해제 및 빌드 아티팩트 선별 차단)
- [x] AGENTS.md 프로젝트 개발/운영 수칙 단독 저장소 기준 상대경로 현행화
- [x] 1-Click 가상환경(uv) 및 Node.js 설치 감지 모듈 개발 완료
- [x] 2바이트 다국어 보장을 위한 UTF-8 Bom-less 강제화 및 cp949 환경 에러 방지 설정
- [x] 배포 타임스탬프 기반 버전 번호 규격(`Major.Minor.Patch-YYYYMMDD.HHMMSS`) 자동 생성 및 주입 스크립트 작성 ([update_version.py](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/build/update_version.py), [inject_version.bat](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/build/inject_version.bat))

---

## 🎯 Phase 1: Windows 에디터 빌드 & 브랜딩 (최우선 진행)
- [ ] **Upstream Code-OSS 동기화 및 복구**:
  - [ ] vscode/ 디렉터리 클린업 및 `.git` Upstream 재싱크 (완전한 .git 형상 관리 폴더 확보)
  - [ ] `yarn install`을 통한 100% 컴파일 의존성 모듈 설치 완료
- [ ] **브랜드 로고 및 커스텀 브랜딩 적용**:
  - [ ] 신규 확정 브랜드 로고([logo.png](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/images/logo.png))를 IDE 액티비티 바 아이콘, 웰컴 페이지, 제품 로고(`app.ico` 등)로 이식
  - [ ] product.json / package.json 내 제품명을 `Code - OSS`에서 `Agent Smith IDE`로 변경하는 커스텀 패치 파일 생성 및 적용
- [ ] **다국어 출력 제어 가드레일(Harness) 연동**:
  - [ ] IDE 메뉴 및 네이티브 레이블은 글로벌 규격인 **영문(English)**으로 고정 설계
  - [ ] AI 코드 생성 시 주석(Comments), 도큐먼트, 설명 파일 및 로그는 **한국어**로 강제 출력되도록 프롬프트 가드레일 바인딩
- [ ] **지능형 엔진 및 AST 그래프 연동**:
  - [ ] `graphify` 엔진(SQLite AST-Graph Node Indexer)을 탑재하여 로컬 코드 의존성(Class, Function)을 분석하고 질의 시 컨텍스트에 그래프 노드로 동적 인젝션
  - [ ] `mem0` 장기 기억 프로필 스토리지를 바인딩하여 오프라인 환경에서의 코딩 습관 및 LLM 설정 유지
- [ ] **1-Click 윈도우 포터블 패키징 및 최종 QA**:
  - [ ] Gulp 빌드를 수행하여 포터블 단일 실행 파일(`Agent-Smith-IDE.exe`) 패키징 완료
  - [ ] QA 서브에이전트 스킬(`/qa`) 및 Headless 브라우저를 가동하여 챗 패널 UI 및 전체 레이아웃 왜곡 유무 검증

---

## 🎯 Phase 2: Red Hat / Linux 빌드 호환성 추가 (후순위 진행)
- [ ] **리눅스용 빌드 쉘 스크립트 작성**:
  - [ ] [`build_agent_smith.sh`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/build/build_agent_smith.sh) 쉘 스크립트 신규 구현 및 LF 개행 지정
  - [ ] [`inject_version.sh`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/build/inject_version.sh) 버전 주입 쉘 스크립트 신규 구현 및 LF 개행 지정
- [ ] **WSL / Rocky Linux 크로스 플랫폼 검증**:
  - [ ] WSL 내 Rocky Linux 또는 AlmaLinux 환경에서 작성한 쉘 스크립트 가동 및 컴파일 호환성 최종 검증
- [ ] **온프레미스(RHOAI SNO) 연동**:
  - [ ] OpenShift AI 단일 노드(Baremetal)상의 vLLM ServingRuntime API 자동 스캔 및 모델 엔드포인트 연동 테스트

---

© 2026 AI Architecture Engineering Team. All rights reserved.
