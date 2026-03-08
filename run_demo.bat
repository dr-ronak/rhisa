@echo off
REM RHISA Healthcare Chatbot - Demo Mode Launcher
REM Runs without AWS resources for testing

echo ============================================================
echo RHISA Healthcare Chatbot - Demo Mode
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install requirements if needed
echo Checking dependencies...
pip install Flask flask-cors python-dotenv --quiet
echo.

REM Set environment variables
set FLASK_ENV=development
set PORT=5000

REM Start demo server
echo Starting RHISA Demo Server...
echo Server will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python app_demo.py

pause
