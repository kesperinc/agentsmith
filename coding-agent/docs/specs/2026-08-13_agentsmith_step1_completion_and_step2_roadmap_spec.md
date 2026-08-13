# 📄 [작업 명세서] Step 1 완료 검증 및 Step 2 (Vibe Coding & MCP CLI 연동) 개발 로드맵 명세서

- **작성 일자**: 2026-08-13
- **작성자**: Agent Smith AI Assistant
- **대상 저장소**: `aifullstack/agentsmith` (`c:\dev\antigravity-workspace\aifullstack\agentsmith`)

---

## 1. Step 1 단계 완료 검증 (Desktop-First Core Completion)

- **[완료] Web GUI 실행 환경**: `http://localhost:9090` Workbench UI 100% 정상 구동
- **[완료] Desktop GUI 실행 환경**: `run_agent_smith.bat` 실행 시 1초 만에 최상단 포그라운드 BrowserWindow 100% 정상 팝업 및 지속 상주 (20개 프로세스 트리 실측 입증)
- **[완료] Native & Builtin 바인딩**: C++ Native `.node` 바이너리 MSVC 컴파일 및 `git-base`, `git`, `github` TypeScript 컴파일 완료

---

## 2. Step 2 단계 다음 추진 목표 (Vibe Coding Platform & MCP Core)

| 구분 | 주요 개발 기능 | 상세 내용 |
| :--- | :--- | :--- |
| **Task 2-1** | **Vibe Coding 오케스트레이터** | 자연어 요구사항 ➔ 멀티 파일 자율 생성 ➔ 샌드박스 테스트 ➔ Self-Correction 엔진 구축 |
| **Task 2-2** | **MCP (Model Context Protocol) 연동** | Antigravity / Codex / Claude Code CLI 와 Agent Smith IDE 간 1:1 바인딩 인터페이스 구현 |
| **Task 2-3** | **시연용 FIM / Vibe 샘플 개발** | 행사 시연용 파이썬 및 자바 실시간 FIM (Fill-In-the-Middle) 코드 완결 샘플 구비 |
| **Task 2-4** | **개발자 워크스페이스 격리** | 개발자별 독립 샌드박스(Workspace Isolation) 세팅 구조 수립 |

---
*Agent Smith Roadmap Specification Completed*
