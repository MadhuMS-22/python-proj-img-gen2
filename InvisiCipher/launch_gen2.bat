@echo off
echo ================================================
echo InvisiCipher Gen2 Launcher (Windows)
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Python found. Starting launcher...
echo.

REM Run the Python launcher
python launch_gen2.py

REM Pause to see any error messages
if errorlevel 1 (
    echo.
    echo Launcher failed with error code %errorlevel%
    pause
)
