@echo off
echo EHB Auto Page Opener
echo ====================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Run the Python script
python auto_open_all_pages.py

echo.
echo Press any key to exit...
pause >nul 