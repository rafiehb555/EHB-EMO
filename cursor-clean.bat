@echo off
echo 🧹 Cleaning Cursor Environment...
echo.
echo 🗑️ Removing cache files...
if exist __pycache__ rmdir /s /q __pycache__
if exist .mypy_cache rmdir /s /q .mypy_cache
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist node_modules rmdir /s /q node_modules
if exist .venv rmdir /s /q .venv
echo.
echo ✅ Environment cleaned!
echo 💡 Ready for fresh development
pause