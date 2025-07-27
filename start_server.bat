@echo off
echo ================================================
echo 🤖 EHB AI Dev Agent - Auto Start
echo ================================================
echo.

python start_server.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Server failed to start
    echo 💡 Please check the error messages above
    pause
) 