# EduCore Frontend Startup Script
# Run this to start the GUI application

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  EduCore GUI Application" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
}

Write-Host ""
Write-Host "Starting GUI application..." -ForegroundColor Green
Write-Host "Make sure the backend server is running!" -ForegroundColor Yellow
Write-Host ""

cd frontend
python gui.py
