@echo off
title EHB-5 Intelligent System Auto-Runner
color 0A

echo.
echo ========================================
echo    EHB-5 Intelligent System Auto-Runner
echo ========================================
echo.

echo Starting automatic system management...
echo.

:: Check if PowerShell is available
powershell -Command "Get-Host" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: PowerShell is not available
    echo Please install PowerShell or run the system manually
    pause
    exit /b 1
)

:: Run the PowerShell script with auto-start and monitoring
echo Running intelligent system with auto-start and monitoring...
echo.

powershell -ExecutionPolicy Bypass -File "auto-run-system.ps1" -AutoStart -ForceRestart

echo.
echo System has been stopped.
echo Press any key to exit...
pause >nul
