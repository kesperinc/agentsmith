param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureBranch
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

if (-not $FeatureBranch.StartsWith("feature/")) {
    Write-Host "[ERROR] Branch name must start with 'feature/'." -ForegroundColor Red
    exit 1
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "[Agent Smith] Merge Flow: $FeatureBranch --> staging --> main"
Write-Host "============================================================"

# Step 1: push feature
Write-Host "[1/5] Pushing $FeatureBranch..." -ForegroundColor Yellow
git checkout $FeatureBranch
if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] checkout failed" -ForegroundColor Red; exit 1 }
git push origin $FeatureBranch
if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] feature push failed" -ForegroundColor Red; exit 1 }

# Step 2: merge to staging
Write-Host "[2/5] Merging to staging..." -ForegroundColor Yellow
git checkout staging
git pull origin staging
git merge $FeatureBranch --no-ff -m "merge: $FeatureBranch -> staging"
if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] staging merge failed" -ForegroundColor Red; exit 1 }
git push origin staging
if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] staging push failed" -ForegroundColor Red; exit 1 }

# Step 3: merge to main
Write-Host "[3/5] Merging to main..." -ForegroundColor Yellow
git checkout main
git pull origin main
git merge staging --no-ff -m "release: staging -> main (from $FeatureBranch)"
if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] main merge failed" -ForegroundColor Red; exit 1 }
git push origin main
if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] main push failed" -ForegroundColor Red; exit 1 }

# Step 4: return to feature branch
Write-Host "[4/5] Returning to feature branch..." -ForegroundColor Yellow
git checkout $FeatureBranch
git rebase main
git push origin $FeatureBranch --force-with-lease

# Step 5: done
$currentBranch = git branch --show-current
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "[SUCCESS] Merge flow complete."
Write-Host "  Current branch: $currentBranch (restored)"
Write-Host "============================================================"
git log --oneline -5
