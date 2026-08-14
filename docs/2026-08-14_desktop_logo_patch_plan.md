# 작업 계획서: 유효 픽셀 자동 검출 기반 정중앙 대칭 마진 재정렬 및 C++ 런처 리빌드

본 계획서는 사용자가 제공해 주신 [`docs/images/ico.png`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/docs/images/ico.png) (430x430) 이미지 내의 상하 여백 편차(상단 여백 0px, 하단 여백 42px 쏠림)로 인해 발생한 위쪽 여백 비대칭 현상을 물리적으로 해결하기 위해, **실제 삼엽 심볼마크 픽셀 영역만을 자동 트리밍 검출하여 캔버스 정중앙에 상하좌우 동일 마진으로 자동 재배치**하고 C++ 런처 재컴파일을 완수하기 위한 최종 보완 계획서입니다.

---

## 🛠️ User Review Required (사용자 검토 및 의사결정 사항)

> [!IMPORTANT]
> 1. **여백 비대칭 원인 진단**:
>    - 사용자가 제작해 주신 `ico.png` 원본은 배경색 `#0b0c10` (11, 12, 16)이 가득 차 있는 불투명 구조이며, 실질적인 삼엽 심볼의 바운딩 박스는 **`[23, 0, 429, 388]`**입니다.
>    - 즉, 심볼의 꼭지점은 이미지 상단 끝(`y: 0`)에 딱 붙어 있는 반면, 하단부에는 `42px` 크기의 여백이 몰려 있어 **상하 여백 쏠림(Vertical Offset)**이 고정된 상태였습니다. 이로 인해 리사이즈 시 위쪽 또는 아래쪽이 휑하게 쏠려 보이는 착시/비대칭이 발생했습니다.
> 2. **RGB 색상차 기반 전경 자동 검출 및 정중앙 재배치 (Autocrop & Auto-Centering)**:
>    - 파이썬 코드가 배경색 대비 색상차가 20 이상 나는 유효 픽셀 경계(Bounding Box)를 스캔하여 **실제 삼엽 심볼 알맹이만 타이트하게 크롭**해 냅니다.
>    - 잘라낸 알맹이를 256x256 새 캔버스 상에 **상하좌우 오차 0.0001%의 완벽한 동일 여백 마진(1:1 정중앙 대칭)**을 주어 자동 재정렬 배치합니다.
> 3. **실행 파일 재컴파일 배포 연계**:
>    - 에셋 재생성 후, `compile_launcher.ps1`을 가동하여 상하좌우 여백이 완벽히 1:1 밸런싱된 순정 심볼 전용 `code.ico`를 헤더 리소스로 임베딩 각인한 [`agentsmith.exe`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/agentsmith.exe) 실행 파일을 다시 컴파일하여 루트 폴더에 배포합니다.

---

## 💡 Proposed Changes (제안된 변경 계획)

### 1단계: 유효 전경 자동 정렬 code.ico, code.png 생성 (정밀 크롭)
* **Pillow 변환기 수정**: [`scratch/convert_logo_to_ico.py`](file:///C:/Users/MZC01-SUNKIM317/.gemini/antigravity-ide/brain/ec807f78-ed81-4c03-9060-3fb8b0b70920/scratch/convert_logo_to_ico.py) 에서 `ico.png`를 로드한 뒤 배경색 `(11, 12, 16)` 대비 전경 픽셀의 실제 경계 박스를 디텍팅하여 크롭하고, 이를 256x256 투명 캔버스 정중앙에 상하좌우 동일 마진으로 확대 배치합니다.

### 2단계: 순정 code-icon.svg 패치 및 에디터 구동
* **SVG 패처 구동**: 리빌드된 무손실 심볼 전용 `code.png` 의 데이터를 direct base64 인코딩하여 `code-icon.svg` 에 분사 적용합니다.
* 프로세스를 클린업하고 에디터를 재기동하여 타이틀바 로고를 검증합니다.

### 3단계: C++ 런처 (`agentsmith.exe`) 재컴파일 및 4대 문서 갱신
* **실행파일 빌드**: `compile_launcher.ps1`을 구동해 상하좌우 대칭 밸런싱이 확보된 최신 `code.ico`를 각인한 런처 바이너리를 최종 배포합니다.
* **4대 문서 갱신**: 빌드가이드, 명세서, 인수인계서, 계획서의 관련 문구를 모두 이 대칭 자동 보정 마감 정보로 최신화합니다.

---

## 📂 Proposed File Changes (수정 대상 파일 목록)

### [MODIFY] [`scratch/convert_logo_to_ico.py`](file:///C:/Users/MZC01-SUNKIM317/.gemini/antigravity-ide/brain/ec807f78-ed81-4c03-9060-3fb8b0b70920/scratch/convert_logo_to_ico.py)
* **내용**: `ico.png`에 대한 RGB 전경 디텍션 및 상하좌우 자동 정중앙 대칭 마진 배치를 연산하는 스크립트로 개편.

---

## 🚀 Verification Plan (최종 검증 시나리오)

1. **빌드/컴파일 가동**: 스크립트 실행으로 자산 재생성 및 C++ 런처 재컴파일.
2. **에디터 구동 검증**: 에디터를 기동하여 작업 표시줄 및 에디터 좌상단 타이틀바에서 **여백 쏠림이 완전 리셋되고 상하좌우의 간격이 한 치의 흐트러짐도 없이 정중앙에 큼직하고 쨍하게 자리잡았는지** 시각 검증.
