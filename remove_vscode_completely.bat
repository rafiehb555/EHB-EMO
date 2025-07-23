@echo off
echo 🧹 COMPLETE VS CODE REMOVAL FOR CURSOR
echo ========================================
echo.

echo 🔍 Finding all VS Code related files...
echo.

REM Remove VS Code folders
if exist ".vscode" (
    echo 🗑️ Removing .vscode folder...
    rmdir /s /q ".vscode"
    echo ✅ Removed .vscode
)

if exist ".vs" (
    echo 🗑️ Removing .vs folder...
    rmdir /s /q ".vs"
    echo ✅ Removed .vs
)

REM Remove VS Code workspace files
for /r %%f in (*.code-workspace) do (
    echo 🗑️ Removing workspace file: %%f
    del "%%f"
    echo ✅ Removed %%f
)

REM Remove VS Code settings files
for /r %%f in (settings.json) do (
    if exist "%%f" (
        echo 🗑️ Removing settings: %%f
        del "%%f"
        echo ✅ Removed %%f
    )
)

for /r %%f in (tasks.json) do (
    if exist "%%f" (
        echo 🗑️ Removing tasks: %%f
        del "%%f"
        echo ✅ Removed %%f
    )
)

for /r %%f in (launch.json) do (
    if exist "%%f" (
        echo 🗑️ Removing launch: %%f
        del "%%f"
        echo ✅ Removed %%f
    )
)

REM Remove VS Code ignore files
if exist ".vscodeignore" (
    echo 🗑️ Removing .vscodeignore...
    del ".vscodeignore"
    echo ✅ Removed .vscodeignore
)

echo.
echo 🚀 Creating Cursor-only environment...
echo.

REM Create Cursor-specific .gitignore
echo # Cursor-only .gitignore > .gitignore
echo. >> .gitignore
echo # VS Code artifacts >> .gitignore
echo .vscode/ >> .gitignore
echo .vs/ >> .gitignore
echo *.code-workspace >> .gitignore
echo .vscodeignore >> .gitignore
echo. >> .gitignore
echo # Python >> .gitignore
echo __pycache__/ >> .gitignore
echo *.py[cod] >> .gitignore
echo .venv/ >> .gitignore
echo .env >> .gitignore
echo. >> .gitignore
echo # Node >> .gitignore
echo node_modules/ >> .gitignore
echo npm-debug.log* >> .gitignore
echo. >> .gitignore
echo # Logs >> .gitignore
echo *.log >> .gitignore
echo logs/ >> .gitignore
echo. >> .gitignore
echo # Database >> .gitignore
echo *.db >> .gitignore
echo *.sqlite >> .gitignore
echo. >> .gitignore
echo # Cache >> .gitignore
echo .cache/ >> .gitignore
echo .mypy_cache/ >> .gitignore
echo .pytest_cache/ >> .gitignore
echo. >> .gitignore
echo # OS >> .gitignore
echo .DS_Store >> .gitignore
echo Thumbs.db >> .gitignore

echo ✅ Created Cursor-only .gitignore

REM Create Cursor startup script
echo @echo off > start-cursor-only.bat
echo echo 🚀 Starting EHB-5 with Cursor Only... >> start-cursor-only.bat
echo echo. >> start-cursor-only.bat
echo echo 📁 Opening project in Cursor... >> start-cursor-only.bat
echo cursor . >> start-cursor-only.bat
echo echo. >> start-cursor-only.bat
echo echo ✅ Project opened in Cursor! >> start-cursor-only.bat
echo pause >> start-cursor-only.bat

echo ✅ Created start-cursor-only.bat

REM Create Cursor development script
echo @echo off > cursor-dev-only.bat
echo echo 🔧 Starting Cursor Development Environment... >> cursor-dev-only.bat
echo echo. >> cursor-dev-only.bat
echo echo 📦 Installing dependencies... >> cursor-dev-only.bat
echo npm install >> cursor-dev-only.bat
echo echo. >> cursor-dev-only.bat
echo echo 🐍 Setting up Python environment... >> cursor-dev-only.bat
echo python -m venv .venv >> cursor-dev-only.bat
echo call .venv\Scripts\activate >> cursor-dev-only.bat
echo pip install -r requirements.txt >> cursor-dev-only.bat
echo echo. >> cursor-dev-only.bat
echo echo 🚀 Starting development server... >> cursor-dev-only.bat
echo python main.py >> cursor-dev-only.bat
echo echo. >> cursor-dev-only.bat
echo echo ✅ Development environment ready! >> cursor-dev-only.bat
echo pause >> cursor-dev-only.bat

echo ✅ Created cursor-dev-only.bat

echo.
echo ========================================
echo 🎉 VS CODE COMPLETELY REMOVED!
echo ========================================
echo.
echo ✅ All VS Code artifacts removed
echo ✅ Cursor-only environment created
echo ✅ Development scripts ready
echo.
echo 🚀 Next Steps:
echo 1. Open project: start-cursor-only.bat
echo 2. Start development: cursor-dev-only.bat
echo 3. Use Cursor for all development
echo.
echo 💡 Tip: VS Code is no longer needed!
echo.
pause
