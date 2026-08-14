# Agentsmith Mem0 자동 셋업 스크립트 (Windows PowerShell용)

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Agentsmith Mem0 기능 활성화 및 셋업을 시작합니다." -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# 1. Bun 패키지 설치
Write-Host "[1/3] Bun 환경에 mem0ai 의존성을 추가합니다..." -ForegroundColor Yellow
try {
    bun add mem0ai
    Write-Host "Bun 패키지 설치 완료!" -ForegroundColor Green
} catch {
    Write-Error "Bun 패키지 설치 도중 에러가 발생했습니다."
    exit 1
}

# 2. 로컬 디렉토리 및 기본 설정 파일 생성
Write-Host "[2/3] .agentsmith 디렉토리 및 기본 설정 생성..." -ForegroundColor Yellow
$AgentsmithDir = Join-Path (Get-Location) ".agentsmith"
if (!(Test-Path $AgentsmithDir)) {
    New-Item -ItemType Directory -Path $AgentsmithDir -Force | Out-Null
}

$ConfigPath = Join-Path $AgentsmithDir "mem0_config.json"
if (!(Test-Path $ConfigPath)) {
    $DefaultConfig = @{
        vector_store = @{
            provider = "qdrant"
            config = @{
                collection_name = "agentsmith_default_memory"
                path = "./.agentsmith/mem0_qdrant_db"
                embedding_model_dims = 768
            }
        }
        llm = @{
            provider = "gemini"
            config = @{
                model = "gemini-2.5-flash"
            }
        }
        embedder = @{
            provider = "gemini"
            config = @{
                model = "models/gemini-embedding-001"
                embedding_dims = 768
            }
        }
    }
    $DefaultConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath $ConfigPath -Encoding utf8
    Write-Host "기본 설정 파일 생성 완료: $ConfigPath" -ForegroundColor Green
} else {
    Write-Host "설정 파일이 이미 존재합니다. 생성을 스킵합니다." -ForegroundColor Gray
}

# 3. 환경변수 점검
Write-Host "[3/3] API Key 바인딩 확인..." -ForegroundColor Yellow
if ([string]::IsNullOrEmpty($env:GEMINI_API_KEY) -and [string]::IsNullOrEmpty($env:GOOGLE_API_KEY)) {
    Write-Host "[WARNING] GEMINI_API_KEY 또는 GOOGLE_API_KEY 환경변수가 설정되어 있지 않습니다." -ForegroundColor Red
    Write-Host "실행 전 .env 파일에 키를 반드시 기입해 주세요." -ForegroundColor Red
} else {
    Write-Host "API Key 환경변수가 감지되었습니다." -ForegroundColor Green
}

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Agentsmith Mem0 셋업이 성공적으로 완주되었습니다!" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
