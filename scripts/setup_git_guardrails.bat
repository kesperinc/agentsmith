@echo off
chcp 65001 > nul
:: ============================================================
:: Agent Smith 브랜치 가드레일 설치 스크립트
:: 사용법: scripts\setup_git_guardrails.bat
:: ============================================================

echo [Agent Smith] Git 가드레일 훅 설치 중...

:: .githooks 디렉터리를 Git 훅 경로로 등록
git config core.hooksPath .githooks

if %ERRORLEVEL% EQU 0 (
    echo [ok] Git 훅 경로 설정 완료: .githooks/
    echo [ok] 브랜치 가드레일 활성화됨:
    echo      - commit-msg: main/staging 직접 커밋 차단
    echo      - pre-push  : main 직접 push 차단
    echo      - pre-commit: CORTEX-SEC-01/02 SAST 보안 검사
) else (
    echo [ERROR] Git 훅 설정 실패
    exit /b 1
)

echo.
echo [브랜치 전략 요약]
echo   feature/* ---merge--^> staging ---merge--^> main
echo   hotfix/*  ---merge--^> main + staging (교차 머징)
echo.
echo [현재 브랜치]
git branch --show-current
echo.
