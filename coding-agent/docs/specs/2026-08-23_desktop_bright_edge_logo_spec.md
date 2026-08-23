# 📄 코드 변경 명세서 (Specs): 데스크톱 액티비티 바 및 UI 브랜딩 밝은 Edge 로고 적용

- **문서 번호**: `SPEC-2026-08-23-BRIGHT-EDGE-LOGO`
- **작성 일자**: 2026-08-23
- **작성자**: Agent Smith AI Architecture & Pair Engineering Team
- **대상 브랜치**: `feature/setup-git-guardrails`
- **목적**: 기존의 매트(matte)한 그레이/블랙 계열 라스터 이미지를 제거하고, 다크 테마 액티비티 바(Activity Bar) 및 에디터 타이틀바에서 최고 수준의 시인성을 발휘하는 **밝은 Edge 형태의 사이버네틱 네온 로고(Neon Cyan / Electric Purple / Crisp White)**로 전면 교체 적용함.

---

## 🛠️ 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 설명 |
| :--- | :--- | :--- |
| **[MODIFY] 로고 SVG** | [`docs/images/code-icon.svg`](file:///c:/dev/antigravity-workspace/agentsmith/docs/images/code-icon.svg) | 밝은 Edge/라인 아트 벡터 SVG 로고(외곽 헥사곤 쉴드, 아이소메트릭 뉴럴 큐브, 선글라스 렌즈, 양자 코어 노드)로 신규 제작 |
| **[MODIFY] 확장 로고** | [`extensions/agentsmith-chat/media/logo.svg`](file:///c:/dev/antigravity-workspace/agentsmith/extensions/agentsmith-chat/media/logo.svg) | 액티비티 바 아이콘 전용 고대비 밝은 Edge 벡터 SVG 적용 |
| **[MODIFY] 웹뷰 헤더** | [`extensions/agentsmith-chat/media/index.html`](file:///c:/dev/antigravity-workspace/agentsmith/extensions/agentsmith-chat/media/index.html) | 스튜디오 상단 브랜드 로고를 신규 밝은 Edge SVG 심볼로 일치화 |
| **[MODIFY] 에셋** | [`docs/images/code.png`](file:///c:/dev/antigravity-workspace/agentsmith/docs/images/code.png), [`docs/images/logo.png`](file:///c:/dev/antigravity-workspace/agentsmith/docs/images/logo.png), [`docs/images/code.ico`](file:///c:/dev/antigravity-workspace/agentsmith/docs/images/code.ico) | 고해상도 Master PNG 및 다중 해상도 Windows ICO 에셋 갱신 |
| **[MODIFY] 패키징** | [`scripts/package_desktop_dist.py`](file:///c:/dev/antigravity-workspace/agentsmith/scripts/package_desktop_dist.py) | 프로세스 파일 락 자동 해제 및 `safe_copytree` 안전 복사 가드레일 탑재 |
| **[NEW] 생성기** | [`scripts/generate_bright_edge_logo.py`](file:///c:/dev/antigravity-workspace/agentsmith/scripts/generate_bright_edge_logo.py) | 밝은 Edge 로고 에셋 자동 생성 스크립트 |
| **[NEW] 명세서** | [`coding-agent/docs/specs/2026-08-23_desktop_bright_edge_logo_spec.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-23_desktop_bright_edge_logo_spec.md) | 본 로고 교체 및 브랜딩 상세 명세서 |

---

## 🎨 2. 밝은 Edge(Line Art) 로고 디자인 사양

1. **외곽 헥사곤 쉴드 (Outer Cybernetic Hexagon)**:
   - Stroke: 12px Gradient (Cyan `#00ffff` ➔ `#00e5ff` ➔ `#00b0ff`)
   - 효과: 네온 글로우 필터(`feGaussianBlur stdDeviation=3`)를 통한 빛나는 림 라이트(Rim Light) 연출
2. **내부 아이소메트릭 뉴럴 큐브 (Isometric Neural Cube)**:
   - 상단면: Crisp Pure White (`#ffffff`) 8px Edge
   - 좌/우측면: Electric Cyan (`#00e5ff`) 및 Purple (`#b388ff`) Edge
   - 중심축: White 8px 스핀들 라인
3. **Agent Smith 시그니처 매트릭스 쉐이드 (Matrix Shades)**:
   - 좌우 렌즈 프레임: 선명한 순백 9px 윤곽선 + 25% 반투명 Cyan 내부 필
   - 브릿지: 9px White 연결선
4. **양자 코어 노드 (Quantum AI Core Nodes)**:
   - 상단 중앙 White 발광 원 노드 + 하단 좌/우 Cyan/Purple 서킷 링크

---

## 🧪 3. 빌드 및 사후 무결성 검증

- **빌드 실행**: `package_desktop_dist.py` 및 `build_desktop_installer.py`
- **산출물 검증 (`verify_desktop_bundle.py --verify-dist`)**: **100% PASS**
  - 포터블 번들: `dist/agentsmith-desktop-v1.0.0.zip` (450.39 MB)
  - C# Native 단일 실행 설치 파일: `dist/AgentSmith_Desktop_Setup_v1.0.0.exe` (448.33 MB)
