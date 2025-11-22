#!/usr/bin/env pwsh
# Run vinyl record indexing and cleanup from root directory

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "RECORDS2DISCOGS - Vinyl Indexing" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Get script directory (root of repo)
$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AppPath = Join-Path $RootDir "vinyl-record-indexing\app.py"
$CleanupPath = Join-Path $RootDir "indexing-output\cleanup.py"

# Check if app.py exists
if (-Not (Test-Path $AppPath)) {
    Write-Host "❌ Error: app.py not found at $AppPath" -ForegroundColor Red
    exit 1
}

# Check if cleanup.py exists
if (-Not (Test-Path $CleanupPath)) {
    Write-Host "⚠️  Warning: cleanup.py not found at $CleanupPath" -ForegroundColor Yellow
    Write-Host "Continuing without cleanup...`n" -ForegroundColor Yellow
    $RunCleanup = $false
} else {
    $RunCleanup = $true
}

# Run the indexing app
Write-Host "✅ Starting vinyl indexing..." -ForegroundColor Green
Write-Host "📂 Location: $AppPath`n" -ForegroundColor Gray

Set-Location (Join-Path $RootDir "vinyl-record-indexing")
$IndexingExitCode = 0
try {
    python app.py
    $IndexingExitCode = $LASTEXITCODE
} catch {
    Write-Host "`n❌ Error running app.py: $_" -ForegroundColor Red
    Set-Location $RootDir
    exit 1
}

# Return to root
Set-Location $RootDir

# Run cleanup if indexing succeeded
if ($IndexingExitCode -eq 0 -and $RunCleanup) {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "Running Cleanup Script" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
    
    Set-Location (Join-Path $RootDir "indexing-output")
    python cleanup.py
    Set-Location $RootDir
} elseif ($IndexingExitCode -ne 0) {
    Write-Host "`n⚠️  Indexing did not complete successfully. Skipping cleanup." -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Session complete" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan
