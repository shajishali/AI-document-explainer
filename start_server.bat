@echo off
echo Starting AI Legal Document Explainer FastAPI Server...
echo.
echo The server will open in a new window.
echo Close that window to stop the server.
echo.

REM Start the server in a new window
start "AI Legal Document Explainer Server" cmd /k "venv\Scripts\activate && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

echo.
echo Server is starting in a new window...
echo.
echo Once the server is running, you can access:
echo - Main app: http://127.0.0.1:8000
echo - API docs: http://127.0.0.1:8000/docs
echo - Health check: http://127.0.0.1:8000/health
echo.
echo Press any key to close this window...
pause > nul
