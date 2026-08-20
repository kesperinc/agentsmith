@echo off
chcp 65001 > nul
:: ============================================================
:: Agent Smith Git 브랜치 워크플로우 스크립트
:: feature/* ➔ staging ➔ main 머지 자동화
:: 사용법: scripts\git_merge_flow.bat <feature-branch-name>
:: 예시:   scripts\git_merge_flow.bat feature/ai-model-panel
:: ============================================================

setlocal

if "%~1"=="" (
    echo [오류] feature 브랜치 이름을 인수로 전달하세요.
    echo 사용법: scripts\git_merge_flow.bat feature/^<작업명^>
    exit /b 1
)

set FEATURE_BRANCH=%~1

:: feature/* 접두사 강제
echo %FEATURE_BRANCH% | findstr /b "feature/" > nul
if %ERRORLEVEL% NEQ 0 (
    echo [오류] 브랜치명은 반드시 feature/ 로 시작해야 합니다.
    echo 예시: feature/ai-model-panel
    exit /b 1
)

echo.
echo ============================================================
echo [Agent Smith] 브랜치 머지 플로우 시작
echo feature: %FEATURE_BRANCH% --^> staging --^> main
echo ============================================================
echo.

:: 1단계: feature 브랜치 push
echo [1/5] %FEATURE_BRANCH% push 중...
git checkout %FEATURE_BRANCH%
git push origin %FEATURE_BRANCH%
if %ERRORLEVEL% NEQ 0 (echo [오류] feature push 실패 & exit /b 1)

:: 2단계: staging 머지
echo [2/5] staging 브랜치로 merge 중...
git checkout staging
git pull origin staging
git merge %FEATURE_BRANCH% --no-ff -m "merge: %FEATURE_BRANCH% ➔ staging"
if %ERRORLEVEL% NEQ 0 (echo [오류] staging merge 실패 & exit /b 1)
git push origin staging
if %ERRORLEVEL% NEQ 0 (echo [오류] staging push 실패 & exit /b 1)

:: 3단계: main 머지
echo [3/5] main 브랜치로 merge 중...
git checkout main
git pull origin main
git merge staging --no-ff -m "release: staging ➔ main (from %FEATURE_BRANCH%)"
if %ERRORLEVEL% NEQ 0 (echo [오류] main merge 실패 & exit /b 1)
git push origin main
if %ERRORLEVEL% NEQ 0 (echo [오류] main push 실패 & exit /b 1)

:: 4단계: feature 브랜치로 복귀
echo [4/5] feature 브랜치로 복귀 중...
git checkout %FEATURE_BRANCH%
git pull origin main --rebase
echo [ok] feature 브랜치 최신 main 기반으로 rebase 완료

:: 5단계: 완료 보고
echo.
echo ============================================================
echo [SUCCESS] 머지 플로우 완료
echo   %FEATURE_BRANCH% --^> staging --^> main 순차 완료
echo   현재 브랜치: %FEATURE_BRANCH% (복귀됨)
echo ============================================================
echo.
git branch --show-current
git log --oneline -5

endlocal
