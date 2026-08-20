# ============================================================
# Agent Smith Git 브랜치 머지 플로우 (PowerShell)
# feature/* -> staging -> main 자동 머지 후 feature 복귀
# 사용법: .\scripts\git_merge_flow.ps1 feature/<작업명>
# ============================================================
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureBranch
)

# feature/* 접두사 강제 검사
if (-not $FeatureBranch.StartsWith("feature/")) {
    Write-Host "[오류] 브랜치명은 반드시 feature/ 로 시작해야 합니다." -ForegroundColor Red
    Write-Host "예시: feature/ai-model-panel"
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "[Agent Smith] 브랜치 머지 플로우 시작"
Write-Host "  $FeatureBranch --> staging --> main"
Write-Host "============================================================"
Write-Host ""

# 1단계: feature 브랜치 push
Write-Host "[1/5] $FeatureBranch push 중..." -ForegroundColor Yellow
git checkout $FeatureBranch
if ($LASTEXITCODE -ne 0) { Write-Host "[오류] checkout 실패" -ForegroundColor Red; exit 1 }
git push origin $FeatureBranch
if ($LASTEXITCODE -ne 0) { Write-Host "[오류] feature push 실패" -ForegroundColor Red; exit 1 }

# 2단계: staging 머지
Write-Host "[2/5] staging 브랜치로 merge 중..." -ForegroundColor Yellow
git checkout staging
git pull origin staging
git merge $FeatureBranch --no-ff -m "merge: $FeatureBranch -> staging"
if ($LASTEXITCODE -ne 0) { Write-Host "[오류] staging merge 실패" -ForegroundColor Red; exit 1 }
git push origin staging
if ($LASTEXITCODE -ne 0) { Write-Host "[오류] staging push 실패" -ForegroundColor Red; exit 1 }

# 3단계: main 머지
Write-Host "[3/5] main 브랜치로 merge 중..." -ForegroundColor Yellow
git checkout main
git pull origin main
git merge staging --no-ff -m "release: staging -> main (from $FeatureBranch)"
if ($LASTEXITCODE -ne 0) { Write-Host "[오류] main merge 실패" -ForegroundColor Red; exit 1 }
git push origin main
if ($LASTEXITCODE -ne 0) { Write-Host "[오류] main push 실패" -ForegroundColor Red; exit 1 }

# 4단계: feature 브랜치로 복귀 + rebase
Write-Host "[4/5] feature 브랜치로 복귀 및 rebase 중..." -ForegroundColor Yellow
git checkout $FeatureBranch
git rebase main
Write-Host "[ok] feature 브랜치 main 기반 rebase 완료" -ForegroundColor Green
git push origin $FeatureBranch --force-with-lease

# 5단계: 완료 보고
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "[SUCCESS] 머지 플로우 완료"
Write-Host "  $FeatureBranch --> staging --> main 순차 완료"
$currentBranch = git branch --show-current
Write-Host "  현재 브랜치: $currentBranch (복귀됨)"
Write-Host "============================================================"
Write-Host ""
Write-Host "최근 커밋 5개:"
git log --oneline -5
