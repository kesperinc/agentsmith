# 📄 코드 변경 명세서 (Specs): Trinity Air 브랜드 로고 기반 밝은 Edge 리마스터 및 UI 전면 적용

- **문서 번호**: `SPEC-2026-08-23-TRINITY-AIR-BRIGHT-EDGE-LOGO`
- **작성 일자**: 2026-08-23
- **작성자**: Agent Smith AI Architecture & Pair Engineering Team
- **대상 브랜치**: `feature/setup-git-guardrails`
- **목적**: 기존의 매트(matte)한 그레이/블랙 톤이었던 **Trinity Air(트리니티 에어)** 고유 브랜드 심볼(3-Blade 에어로다이내믹 뫼비우스 루프)을 계승·발전시켜, 다크 테마 액티비티 바(Activity Bar), 에디터 타이틀바, 웹뷰 헤더 및 윈도우 인스톨러에서 최고 수준의 시인성을 발휘하는 **밝은 Edge 형태의 네온 벡터 로고(Neon Cyan `#00e5ff` + Electric Purple `#b388ff` + Sky Blue `#00b0ff` + Pure White `#ffffff`)**로 전면 리마스터하여 배포본에 반영함.

---

## 🛠️ 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 설명 |
| :--- | :--- | :--- |
| **[MODIFY] 로고 SVG** | [`docs/images/code-icon.svg`](file:///c:/dev/antigravity-workspace/agentsmith/docs/images/code-icon.svg) | Trinity Air 3-Blade 뫼비우스 루프 기반 밝은 Edge 벡터 SVG 마스터 생성 |
| **[MODIFY] 확장 로고** | [`extensions/agentsmith-chat/media/logo.svg`](file:///c:/dev/antigravity-workspace/agentsmith/extensions/agentsmith-chat/media/logo.svg) | 액티비티 바 아이콘 전용 고대비 Trinity Air 밝은 Edge 벡터 SVG 적용 |
| **[MODIFY] 웹뷰 헤더** | [`extensions/agentsmith-chat/media/index.html`](file:///c:/dev/antigravity-workspace/agentsmith/extensions/agentsmith-chat/media/index.html) | 스튜디오 상단 브랜드 로고를 Trinity Air 밝은 Edge 심볼로 일치화 |
| **[MODIFY] 에셋** | [`docs/images/code.png`](file:///c:/dev/antigravity-workspace/agentsmith/docs/images/code.png), [`docs/images/logo.png`](file:///c:/dev/antigravity-workspace/agentsmith/docs/images/logo.png), [`docs/images/code.ico`](file:///c:/dev/antigravity-workspace/agentsmith/docs/images/code.ico) | Trinity Air 형상의 고해상도 Master PNG 및 다중 해상도 Windows ICO 에셋 갱신 |
| **[MODIFY] 생성기** | [`scripts/generate_bright_edge_logo.py`](file:///c:/dev/antigravity-workspace/agentsmith/scripts/generate_bright_edge_logo.py) | Trinity Air 3-Blade 뫼비우스 루프 벡터 알고리즘 탑재 |
| **[NEW] 명세서** | [`coding-agent/docs/specs/2026-08-23_trinity_air_bright_edge_logo_spec.md`](file:///c:/dev/antigravity-workspace/agentsmith/coding-agent/docs/specs/2026-08-23_trinity_air_bright_edge_logo_spec.md) | 본 Trinity Air 로고 리마스터 상세 명세서 |

---

## 🎨 2. Trinity Air 밝은 Edge(Line Art) 디자인 사양

1. **3-Blade 에어로다이내믹 뫼비우스 루프 (Aerodynamic Möbius Wings)**:
   - **Blade 1 (좌 ➔ 상단)**: Neon Cyan `#00e5ff` / Pure White `#ffffff` 10px Edge 라인.
   - **Blade 2 (상 ➔ 우하단)**: Electric Purple `#b388ff` / Magenta `#ea80fc` 10px Edge 라인.
   - **Blade 3 (우하단 ➔ 좌하단)**: Sky Blue `#00b0ff` / Electric Cyan `#00ffff` 10px Edge 라인.
2. **내부 뫼비우스 리본 악센트 (Inner Dynamic Ribbon Curves)**:
   - 중심부로 유려하게 흘러드는 3가닥의 곡선 엣지 라인으로 입체적인 공기 역학적 흐름(Air Stream)을 표현.
3. **중심 에어 볼텍스 코어 (Air Vortex Core & Pulsar Nodes)**:
   - 중심부 양자 와류 원형 코어 + 3개 꼭짓점 발광 펄서 노드(Pulsar Energy Nodes) 탑재.

---

## 🧪 3. 빌드 및 사후 무결성 검증

- **빌드 파이프라인**: `package_desktop_dist.py` & `build_desktop_installer.py`
- **산출물 검증 (`verify_desktop_bundle.py --verify-dist`)**: **100% PASS**
  - 포터블 번들: `dist/agentsmith-desktop-v1.0.0.zip` (450.40 MB)
  - C# Native 단일 실행 설치 파일: `dist/AgentSmith_Desktop_Setup_v1.0.0.exe` (448.34 MB)
