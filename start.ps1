# AI Legal Document Explainer - Startup Script
# Run this script to start the application

Write-Host "Starting AI Legal Document Explainer..." -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run the setup commands first:" -ForegroundColor Yellow
    Write-Host "python -m venv venv" -ForegroundColor Cyan
    Write-Host ".\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host "pip install -r requirements.txt" -ForegroundColor Cyan
    Read-Host "Press Enter to continue"
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "Warning: .env file not found!" -ForegroundColor Yellow
    Write-Host "Please copy env_example.txt to .env and configure your settings." -ForegroundColor Yellow
    Write-Host ""
}

# Start the application
Write-Host "Starting FastAPI server..." -ForegroundColor Green
Write-Host ""
Write-Host "The application will be available at:" -ForegroundColor Cyan
Write-Host "- Main app: http://localhost:8000" -ForegroundColor White
Write-Host "- API docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "- Health check: http://localhost:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

try {
    python main.py
}
catch {
    Write-Host "Error starting application: $_" -ForegroundColor Red
}

Read-Host "Press Enter to continue"
