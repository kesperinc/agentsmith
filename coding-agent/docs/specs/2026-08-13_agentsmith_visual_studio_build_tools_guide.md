# 📄 [안내 명세서] Visual Studio C++ Build Tools 설치 및 C++ Native 모듈 컴파일 가이드

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. 개요 및 목적

본 PC 환경에서 `@vscode/spdlog`, `@vscode/sqlite3` 등의 C++ Native Node module (`.node`) 바이너리를 직접 컴파일 재빌드하기 위해 요구되는 Visual Studio C++ 빌드 환경 구축 가이드입니다.

---

## 2. 3단계 설치 & 빌드 명령어

### Step 1. Visual Studio Build Tools 설치
- **다운로드 URL**: [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- **필수 워크로드**: `C++를 사용한 데스크톱 개발 (Desktop development with C++)` 선택 설치

### Step 2. npm MSVC 버전 세팅
```cmd
npm config set msvs_version 2022
```

### Step 3. Electron Native Rebuild 집행
```cmd
cd /d C:\dev\antigravity-workspace\aifullstack\agentsmith\vscode
npx electron-rebuild -f -w @vscode/spdlog,@vscode/sqlite3
```

---
*Agent Smith Visual Studio Build Tools Specification Completed*
