# AI Legal Document Explainer - Server Starter
# This script starts the FastAPI server in a new window

Write-Host "Starting AI Legal Document Explainer FastAPI Server..." -ForegroundColor Green
Write-Host ""

Write-Host "The server will open in a new window." -ForegroundColor Yellow
Write-Host "Close that window to stop the server." -ForegroundColor Yellow
Write-Host ""

# Start the server in a new window
Start-Process -FilePath "cmd" -ArgumentList "/k", "venv\Scripts\activate && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload" -WindowStyle Normal

Write-Host ""
Write-Host "Server is starting in a new window..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Once the server is running, you can access:" -ForegroundColor White
Write-Host "- Main app: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "- API docs: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "- Health check: http://127.0.0.1:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter to close this window..." -ForegroundColor Yellow
Read-Host
