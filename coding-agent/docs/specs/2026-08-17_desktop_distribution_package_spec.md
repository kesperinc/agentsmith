# 2026-08-17 데스크톱 배포 패키지 구축 상세 명세서 (Desktop Distribution Spec)

**작성일자**: 2026-08-17  
**작성자**: Agent Smith Engineering Team  
**상태**: 완료 (Completed)

---

## 1. 개요 및 목적
본 명세서는 Agent Smith 데스크톱 버전의 프로덕션 배포 및 타 PC 설치를 지원하기 위해 독립 배포 디렉터리(`dist/agentsmith-desktop-v1.0.0`) 및 배포용 바이너리 zip 파일(`dist/agentsmith-desktop-v1.0.0.zip`)을 생성한 기술적 내역을 기록합니다.

---

## 2. 세부 변경 및 구축 내역 (Specs Map)

### 2.1. 패키징 스크립트 작성 (`scripts/package_desktop_dist.py`)
- Python `pathlib`, `shutil`, `zipfile` 모듈을 활용하여 원터치 빌드 자동화 스크립트 작성.
- 캐시 및 불필요 파일(`__pycache__`, `.pytest_cache` 등)을 필터링하여 압축 효율성 극대화.

### 2.2. 독립 배포 폴더 구조 수립 (`dist/agentsmith-desktop-v1.0.0/`)
- `app/`: `vscode/.build/electron` 바이너리 번들 탑재 (`Code - OSS.exe`, `agentsmith_app.exe` 포함).
- `coding-agent/`: 파이썬 백엔드 API 엔진 탑재.
- `.venv/`: 백엔드 실행용 파이썬 가상환경 및 28개 의존 패키지 내장.
- `.agentsmith/`: Mem0 및 Qdrant 로컬 벡터 DB 설정 내장.
- `run_agentsmith_desktop.bat`: 5000번 백엔드 포트 자동 감지 및 에디터 팝업 실행 배치 스크립트.

### 2.3. 압축 아카이빙 (`dist/agentsmith-desktop-v1.0.0.zip`)
- 약 257 MB 규모의 단일 압축 파일 생성 완료. 타 PC 이식 시 본 zip 파일 하나로 전체 환경 복제 가능.

---

## 3. 변경 파일 맵 (Specs File Map)

| 구분 | 파일 경로 | 변경 내용 |
| :--- | :--- | :--- |
| **NEW** | [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/package_desktop_dist.py) | 데스크톱 배포 번들링 파이썬 스크립트 |
| **NEW** | [`dist/agentsmith-desktop-v1.0.0/`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/agentsmith-desktop-v1.0.0) | 데스크톱 독립 배포 전용 폴더 |
| **NEW** | [`dist/agentsmith-desktop-v1.0.0.zip`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/dist/agentsmith-desktop-v1.0.0.zip) | 데스크톱 독립 배포 압축 파일 (257MB) |
| **NEW** | [`docs/2026-08-17_desktop_distribution_package_guide.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/2026-08-17_desktop_distribution_package_guide.md) | 배포 가이드 문서 |
| **NEW** | [`coding-agent/docs/specs/2026-08-17_desktop_distribution_package_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-17_desktop_distribution_package_spec.md) | 배포 명세서 |

---

## 4. 검증 결과
- `dist/agentsmith-desktop-v1.0.0/app/Code - OSS.exe` 존재 및 `run_agentsmith_desktop.bat` 정상 생성 확인.
- `dist/agentsmith-desktop-v1.0.0.zip` 파일 (257.02 MB) 무결성 확인.
