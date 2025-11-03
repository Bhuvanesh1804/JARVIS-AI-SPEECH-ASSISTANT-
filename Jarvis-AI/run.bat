@echo off
echo ========================================
echo     JARVIS AI Assistant Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Starting JARVIS AI Assistant...
echo.

REM Run the main GUI application
python main.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start JARVIS
    echo Please check if all dependencies are installed
    echo Run: python setup.py
    pause
)
