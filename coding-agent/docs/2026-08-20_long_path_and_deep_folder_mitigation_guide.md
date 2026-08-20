# 🛡️ Windows 긴 파일 경로(Long Path) 및 깊은 폴더명 설치 문제 대응 방안 가이드

- **문서 번호**: GUIDE-AS-20260820-02
- **작성 일자**: 2026-08-20
- **문서 목적**: Windows 운영체제의 전통적인 `MAX_PATH` (260자) 제한 및 깊은 `node_modules` 중첩 구조로 인해 발생할 수 있는 설치 실패, 압축 해제 오류(`PathTooLongException`), 파일 접근 거부 문제를 해결하기 위한 **5대 계층적 대응 방안(5-Layer Mitigation Architecture)**을 수립하고 표준 운영 지침을 제공함.

---

## 💥 1. 문제 발생 배경 및 원인 분석

```
[Windows 기존 경로 제한: MAX_PATH = 260자]
C:\Users\홍길동_매우_긴_회사_사번_사용자이름\AppData\Local\Programs\AgentSmith\app\resources\app\node_modules\@vscode\windows-process-tree\build\Release\windows_process_tree.node
▲---------------------------------------------------------------------------------------------------------------------------------------------------------▲
                                    총 경로 길이: 260자 초과 시 Win32 API 파일 I/O 실패!
```

1. **Win32 API 전통적 한계**:
   - Windows의 표준 파일 API는 드라이브 문자(`C:\`)부터 파일명 끝까지의 경로 길이가 **260자**를 초과하면 `PathTooLongException`, `DirectoryNotFoundException`, `ERROR_FILENAME_EXCED_RANGE (206)`를 발생시킵니다.
2. **VS Code / Node.js 생태계의 깊은 중첩 구조**:
   - `resources/app/node_modules/` 하위에는 scoped 패키지(`@vscode/...`)와 C++ 네이티브 빌드 경로(`.../build/Release/...`)가 포함되어 있어, 기본 설치 경로가 깊어지면 손쉽게 260자를 초과합니다.
3. **특수 사용자 환경의 취약성**:
   - Windows 사용자명이 매우 길거나(예: 사번, 한글 15자 이상), 기업 Active Directory 도메인 계정인 경우 `%LOCALAPPDATA%` 경로 자체가 70~100자를 차지하여 충돌 확률이 극대화됩니다.

---

## 🛡️ 2. 5대 계층적 대응 방안 (5-Layer Defense Architecture)

```
+-----------------------------------------------------------------------------------------+
|                  Agent Smith Long Path 5-Layer Defense Architecture                     |
+-----------------------------------------------------------------------------------------+
                                        │
    [Layer 1: OS Registry Guard]        ▼
    └── HKLM/HKCU LongPathsEnabled = 1 자동 활성화 스크립트 및 인스톨러 연동
                                        │
    [Layer 2: Win32 Extended Prefix]    ▼
    └── C# 인스톨러 및 툴에서 \\?\ 확장 접두사(Extended-Length Path, 최대 32,767자) 자동 부착
                                        │
    [Layer 3: Dev Toolchains Config]    ▼
    ├── Git: git config --system core.longpaths true
    └── Python: DisableMaxPathLimit 레지스트리 적용
                                        │
    [Layer 4: Smart Short Path Fallback]▼
    ├── 기본 경로: %LOCALAPPDATA%\Programs\AgentSmith (약 45자)
    └── 경로 초과 감지 시 -> 단축 경로(C:\AgentSmith) 자동 전환 추천
                                        │
    [Layer 5: Packaging Flattening]     ▼
    └── 불필요한 중첩 캐시(.git, .pytest_cache, .build) 배제 및 Unpacked 최적화
```

---

## 🔧 3. 세부 계층별 조치 내역 및 구현 가이드

### 3.1 [Layer 1] Windows OS 레지스트리 `LongPathsEnabled` 자동 활성화

Windows 10(버전 1607 이상), Windows 11 및 Windows Server는 레지스트리를 통해 260자 제한을 해제할 수 있습니다.

- **PowerShell 1-Click 활성화 스크립트**:
  ```powershell
  # 관리자 권한으로 실행
  New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
    -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
  ```
- **배치 파일(`enable_long_paths.bat`) 명령어**:
  ```cmd
  reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled /t REG_DWORD /d 1 /f
  ```

---

### 3.2 [Layer 2] C# 인스톨러 `\\?\` Extended-Length Prefix 자동 핸들러

C# 인스톨러(`Installer.cs`)의 파일 추출 루틴(`SafeExtractEntry`)에서 파일 경로가 **240자를 초과**하거나 `PathTooLongException`이 발생할 경우, 자동으로 `\\?\` 접두사를 부착하여 최대 **32,767자**까지 완벽하게 지원합니다.

```csharp
public static string ToExtendedPath(string path)
{
    if (string.IsNullOrEmpty(path)) return path;
    string fullPath = Path.GetFullPath(path);
    if (fullPath.StartsWith(@"\\?\")) return fullPath;
    if (fullPath.StartsWith(@"\\")) return @"\\?\UNC\" + fullPath.Substring(2);
    return @"\\?\" + fullPath;
}
```

---

### 3.3 [Layer 3] Git 및 Python 도구 체인 Long Path 설정

개발 및 빌드 머신에서 툴체인이 긴 경로를 거부하지 않도록 전역 설정을 자동화합니다:

1. **Git for Windows**:
   ```cmd
   git config --system core.longpaths true
   git config --global core.longpaths true
   ```
2. **Python Windows**:
   - 레지스트리 `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled = 1` 적용 시 Python 3.6+ 표준 라이브러리(`os`, `pathlib`, `shutil`)가 32,767자 경로를 자동 지원합니다.

---

### 3.4 [Layer 4] 지능형 설치 경로 선정 & 단축 경로(`C:\AgentSmith`) 폴백

인스톨러 시작 시 기본 대상 디렉토리 경로 길이를 실시간 검사합니다:

1. **표준 설치 경로**: `%LOCALAPPDATA%\Programs\AgentSmith`
   - 일반적인 경우 총 길이 35~45자로 안전합니다.
2. **장문 사용자명 감지 시 자동 폴백 다이얼로그**:
   - `%LOCALAPPDATA%` 경로 길이가 60자를 초과하거나 한글/특수문자 조합으로 260자 초과 위험이 감지되면, 인스톨러가 다음과 같은 단축 경로를 추천합니다:
     - **추천 단축 경로**: `C:\AgentSmith` 또는 `C:\Programs\AgentSmith`

---

### 3.5 [Layer 5] 패키징 시 디렉터리 Flattening 및 불필요한 캐시 제거

`scripts/package_desktop_dist.py`에서 불필요한 깊은 중첩 구조를 사전에 제거하여 배포 바이너리의 최대 경로 길이를 150자 미만으로 유지합니다:

- **제외 대상**:
  - `vscode/.build/` (임시 빌드 파이프라인 캐시)
  - `.pytest_cache/`, `__pycache__/`
  - 중복 깊은 submodule `.git/` 파일들

---

## 📋 4. 자가 진단 및 사전 검증 체크리스트

| 점검 항목 | 정상 기준 | 조치 방법 |
| :--- | :--- | :--- |
| **OS LongPathsEnabled** | `1` (활성화) | `enable_long_paths.bat` 또는 레지스트리 추가 |
| **Git Long Paths** | `core.longpaths=true` | `git config --global core.longpaths true` 실행 |
| **인스톨러 경로 길이** | 최장 파일 경로 < 240자 | `C:\AgentSmith` 단축 설치 경로 선택 |
| **C# Installer Prefix** | `\\?\` 확장 지원 코드 탑재 | 최신 `scripts/build_desktop_installer.py` 컴파일 바이너리 사용 |
