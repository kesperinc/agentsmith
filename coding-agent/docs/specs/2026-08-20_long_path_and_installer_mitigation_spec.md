# 📄 코드 및 아키텍처 변경 명세서 (Specs): Windows 긴 파일 경로(Long Path) 및 깊은 폴더명 설치 대응 방안 구축

- **문서 일자**: 2026-08-20
- **작성자**: Agent Smith AI Lead / Pair Engineer
- **대상 브랜치**: `feature/setup-git-guardrails`
- **목적**: Windows OS의 기본 `MAX_PATH` (260자) 제한과 Node.js/Electron의 깊은 `node_modules` 중첩 구조로 인한 설치 실패(`PathTooLongException`) 및 디렉터리 접근 오류를 원천 차단하기 위한 5대 계층적 대응 체계를 수립하고 C# 인스톨러에 자동화 가드레일을 적용함.

---

## 🛠️ 1. 변경된 파일 목록 및 수정 맵 (Specs Map)

| 구분 | 파일 경로 | 변경 설명 |
| :--- | :--- | :--- |
| **[NEW] 가이드** | [`coding-agent/docs/2026-08-20_long_path_and_deep_folder_mitigation_guide.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/2026-08-20_long_path_and_deep_folder_mitigation_guide.md) | Windows MAX_PATH 한계 분석, 5대 계층 방어 아키텍처, 레지스트리/Git 설정 및 단축 경로 폴백 가이드라인 |
| **[MODIFY] 인스톨러** | [`scripts/build_desktop_installer.py`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/scripts/build_desktop_installer.py) | C# 인스톨러 내 `EnsureLongPathSupport` (레지스트리 활성화), 대상 경로 길이 감지 및 장문 사용자명 시 단축 경로(`C:\AgentSmith`) 추천 다이얼로그 탑재 |
| **[NEW] 명세서** | [`coding-agent/docs/specs/2026-08-20_long_path_and_installer_mitigation_spec.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/docs/specs/2026-08-20_long_path_and_installer_mitigation_spec.md) | 본 변경 명세서 |
| **[MODIFY] 로드맵** | [`coding-agent/TODO.md`](file:///c:/dev/antigravity-workspace/aifullstack/agentsmith/coding-agent/TODO.md) | Long Path 대응 방안 수립 및 인스톨러 가드레일 강화 과제 반영 |

---

## 🔍 2. 5대 계층 방어 아키텍처 요약

1. **[Layer 1] OS 레지스트리 자동 활성화 (`LongPathsEnabled`)**:
   - C# 인스톨러 실행 시 `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled = 1`을 자동 점검 및 설정.
2. **[Layer 2] `\\?\` Extended-Length Prefix 자동 연동**:
   - 240자 초과 경로에 대해 Win32 Extended Prefix(`\\?\`)를 부착하여 최대 32,767자 파일 I/O 지원.
3. **[Layer 3] 개발/빌드 도구 체인 Long Path 설정**:
   - `git config --system core.longpaths true` 및 Python Windows Long Path 활성화.
4. **[Layer 4] 지능형 단축 설치 경로(`C:\AgentSmith`) 폴백**:
   - 기본 `%LOCALAPPDATA%` 경로가 55자를 초과하는 장문 사용자 계정 감지 시 `C:\AgentSmith`로 자동 전환 추천.
5. **[Layer 5] 패키징 시 디렉터리 Flattening**:
   - 임시 빌드 캐시(`.build/`, `.pytest_cache/`) 배제로 배포 번들의 최대 경로 길이를 150자 미만으로 최적화.

---

## 🧪 3. 검증 결과 (Verification Results)
- `scripts/build_desktop_installer.py`의 C# 소스 컴파일 정상 무결성 검증 완료.
- 긴 경로 설치 다이얼로그 및 레지스트리 점검 로직 정상 삽입 확인.
