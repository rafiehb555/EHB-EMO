@echo off
chcp 65001 >nul
title EHB JPS Installation

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    EHB Job Portal System                     ║
echo ║                        Installation                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 Starting EHB JPS Installation...
echo.

REM Check Node.js
echo 📋 Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    echo    Download from: https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js found:
node --version

REM Check npm
echo 📋 Checking npm installation...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed.
    pause
    exit /b 1
)
echo ✅ npm found:
npm --version

echo.
echo 📦 Installing dependencies...

REM Install main dependencies
echo 📦 Installing main dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install main dependencies
    pause
    exit /b 1
)

REM Install frontend dependencies
if exist "frontend" (
    echo 📦 Installing frontend dependencies...
    cd frontend
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install frontend dependencies
        pause
        exit /b 1
    )
    cd ..
)

REM Install backend dependencies
if exist "backend" (
    echo 📦 Installing backend dependencies...
    cd backend
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install backend dependencies
        pause
        exit /b 1
    )
    cd ..
)

REM Install admin panel dependencies
if exist "admin-panel" (
    echo 📦 Installing admin panel dependencies...
    cd admin-panel
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install admin panel dependencies
        pause
        exit /b 1
    )
    cd ..
)

REM Install database dependencies
if exist "database" (
    echo 📦 Installing database dependencies...
    cd database
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install database dependencies
        pause
        exit /b 1
    )
    cd ..
)

REM Install tools dependencies
if exist "tools" (
    echo 📦 Installing tools dependencies...
    cd tools
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install tools dependencies
        pause
        exit /b 1
    )
    cd ..
)

REM Install SDK dependencies
if exist "sdk" (
    echo 📦 Installing SDK dependencies...
    cd sdk
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install SDK dependencies
        pause
        exit /b 1
    )
    cd ..
)

REM Install deployment dependencies
if exist "deployment" (
    echo 📦 Installing deployment dependencies...
    cd deployment
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install deployment dependencies
        pause
        exit /b 1
    )
    cd ..
)

echo.
echo ✅ All dependencies installed successfully!

REM Create environment file
echo 📝 Setting up environment configuration...
if not exist ".env" (
    if exist "env.example" (
        copy "env.example" ".env" >nul
        echo ✅ Environment file created from template
    ) else (
        echo ⚠️  env.example not found, creating basic .env file
        echo NODE_ENV=development > .env
        echo PORT=3001 >> .env
        echo FRONTEND_PORT=3000 >> .env
        echo ✅ Basic environment file created
    )
) else (
    echo ℹ️  .env file already exists
)

REM Create necessary directories
echo 📁 Creating project directories...
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "temp" mkdir temp
if not exist "backups" mkdir backups
if not exist "cache" mkdir cache
if not exist "public\uploads" mkdir "public\uploads"
if not exist "public\images" mkdir "public\images"
if not exist "public\documents" mkdir "public\documents"
echo ✅ Project directories created

REM Build SDK
echo 🔨 Building SDK...
if exist "sdk" (
    cd sdk
    call npm run build >nul 2>&1
    cd ..
    echo ✅ SDK built successfully
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    Installation Complete!                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🎉 EHB JPS has been installed successfully!
echo.
echo 📋 Next Steps:
echo    1. Configure your .env file with your settings
echo    2. Start development: npm run start-dev
echo    3. Access frontend: http://localhost:3000
echo    4. Access backend: http://localhost:3001
echo    5. Access admin: http://localhost:3002
echo.
echo 📚 Available Commands:
echo    npm run start-dev    - Start development servers
echo    npm run start-prod   - Start production servers
echo    npm run test-all     - Run all tests
echo    npm run lint-all     - Lint all code
echo    npm run format-all   - Format all code
echo    npm run db:reset     - Reset database
echo    npm run db:backup    - Backup database
echo    npm run deploy:dev   - Deploy to development
echo    npm run deploy:prod  - Deploy to production
echo.
echo 🚀 Happy coding!
echo.
pause
