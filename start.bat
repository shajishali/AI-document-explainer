@echo off
echo Starting AI Legal Document Explainer...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please run the setup commands first:
    echo python -m venv venv
    echo venv\Scripts\activate
    echo pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo Warning: .env file not found!
    echo Please copy env_example.txt to .env and configure your settings.
    echo.
)

REM Start the application
echo Starting FastAPI server...
echo.
echo The application will be available at:
echo - Main app: http://localhost:8000
echo - API docs: http://localhost:8000/docs
echo - Health check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause

