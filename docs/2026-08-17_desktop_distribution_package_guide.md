# Agent Smith 데스크톱 배포 패키지 가이드 (Desktop Release Distribution Guide)

**작성 일자**: 2026-08-17  
**릴리즈 버전**: v1.0.0  
**배포 대상 경로**: [`dist/agentsmith-desktop-v1.0.0/`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/agentsmith-desktop-v1.0.0)  
**배포 아카이브**: [`dist/agentsmith-desktop-v1.0.0.zip`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/agentsmith-desktop-v1.0.0.zip)

---

## 1. 개요 (Overview)

본 문서는 Agent Smith 데스크톱 IDE 및 Vibe 코딩 엔진, Mem0 지속 기억 시스템이 일체형으로 통합되어 독립 실행이 가능한 **데스크톱 배포 전용 패키지(`dist/agentsmith-desktop-v1.0.0`)** 구성 및 사용 가이드입니다.

---

## 2. 배포 디렉터리 구성 (Directory Structure)

```text
dist/agentsmith-desktop-v1.0.0/
├── app/                              # Electron 기반 Desktop IDE 바이너리 (Code - OSS.exe, agentsmith_app.exe 등)
├── coding-agent/                     # 파이썬 Vibe 코딩 백엔드 엔진 소스 및 스크립트
├── .venv/                            # 백엔드 구동용 전용 경량 파이썬 가상환경 (의존성 28종 포함)
├── .agentsmith/                      # Mem0 & Qdrant 로컬 벡터 DB 메모리 설정
├── agentsmith.vbs                    # 백신 오진 방지용 예비 콘솔 숨김 런처
├── run_agentsmith_desktop.bat        # 원터치 종합 런처 스크립트
├── .env.example                      # 환경 변수 바인딩 샘플
└── README_RELEASE.md                 # 릴리즈 사용 설명서
```

---

## 3. 배포 패키지 바이너리 생성 자동화 (Build Pipeline)

패키징 자동화 스크립트 [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/package_desktop_dist.py)를 실행하여 1-Click으로 배포 번들 및 ZIP 아카이브를 빌드합니다.

```powershell
# 배포 패키지 번들링 및 zip 압축 스크립트 기동
.venv\Scripts\python.exe scripts/package_desktop_dist.py
```

**자동화 처리 단계**:
1. 기존 `dist/agentsmith-desktop-v1.0.0/` 폴더 초기화 및 재생성.
2. `vscode/.build/electron` 바이너리 디렉터리를 `app/`으로 번들링 복사.
3. `coding-agent/` 소스코드 및 `.venv/` 파이썬 가상환경 런타임 복사 (캐시 불필요 파일 자동 제거).
4. `.agentsmith/` 메모리 지속성 설정 복사.
5. 배포용 런처 `run_agentsmith_desktop.bat` 및 `README_RELEASE.md` 자동 생성.
6. 250MB 상당의 단일 압축 파일 `dist/agentsmith-desktop-v1.0.0.zip` 아카이빙 완료.

---

## 4. 타 PC 및 배포 환경에서의 실행 방법 (Run Instructions)

1. **배포 바이너리 배포 및 해제**:
   - `agentsmith-desktop-v1.0.0.zip` 압축을 타 PC의 원하는 위치에 해제합니다.
2. **API Key 설정**:
   - `.env.example`을 `.env`로 이름을 변경하고 `GEMINI_API_KEY` 또는 `GOOGLE_API_KEY`를 입력합니다.
3. **원터치 기동**:
   - `run_agentsmith_desktop.bat` 실행 시 Port 5000 백엔드 엔진과 Desktop IDE가 자동 연결되어 팝업 구동됩니다.

---

**관련 문서**:
- 배포 가이드: [`docs/2026-08-17_desktop_distribution_package_guide.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/2026-08-17_desktop_distribution_package_guide.md)
- 배포 명세서: [`coding-agent/docs/specs/2026-08-17_desktop_distribution_package_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-17_desktop_distribution_package_spec.md)
