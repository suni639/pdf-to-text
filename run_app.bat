@echo off
echo Starting PDF to Word Converter...

:: Navigate to script directory
cd /d "%~dp0"

:: Activate virtual environment
call venv\Scripts\activate

:: Start browser in background
start "" "http://localhost:5000"

:: Run Flask App
echo Server running.
python app.py

pause