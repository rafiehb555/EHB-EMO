@echo off
echo 🔧 Starting Cursor Development Environment...
echo.
echo 📦 Installing dependencies...
npm install
echo.
echo 🐍 Setting up Python environment...
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
echo.
echo 🚀 Starting development server...
python main.py
echo.
echo ✅ Development environment ready!
echo 💡 Use Cursor AI for coding assistance
pause