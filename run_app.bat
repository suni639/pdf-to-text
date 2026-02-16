@echo off
echo Starting PDF to Word Converter...

:: Navigate to script directory
cd /d "%~dp0"

:: Activate virtual environment
call venv\Scripts\activate

:: Start browser in background (waits a moment for server to start)
width=1200
height=800
start "" "http://localhost:5000"

:: Run Flask App
echo Server running. Press Ctrl+C to stop.
python app.py

pause
