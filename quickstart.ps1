# Quick Start Script for EduCore
# This script sets up and runs both backend and frontend

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  EduCore Quick Start" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "IMPORTANT: Please edit .env file with your MySQL credentials" -ForegroundColor Red
    Write-Host "Then run this script again." -ForegroundColor Red
    Write-Host ""
    notepad .env
    exit
}

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created!" -ForegroundColor Green
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Setup database
Write-Host ""
Write-Host "Setting up database..." -ForegroundColor Yellow
python setup_database.py

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Yellow
Write-Host "1. Open a terminal and run: .\start_backend.ps1" -ForegroundColor White
Write-Host "2. Open another terminal and run: .\start_frontend.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Or run them manually:" -ForegroundColor Yellow
Write-Host "  Backend:  cd backend && python main.py" -ForegroundColor White
Write-Host "  Frontend: cd frontend && python gui.py" -ForegroundColor White
Write-Host ""
