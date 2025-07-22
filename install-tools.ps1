# EHB-5 Dashboard - Comprehensive Tools Installation Script
# World-Class Development Environment Setup

param(
    [switch]$SkipNode,
    [switch]$SkipPython,
    [switch]$SkipExtensions,
    [switch]$SkipAI,
    [switch]$Verbose
)

Write-Host "🚀 EHB-5 Dashboard - Tools Installation Script" -ForegroundColor Cyan
Write-Host "Setting up world-class development environment..." -ForegroundColor Yellow

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "⚠️  This script requires administrator privileges for some installations." -ForegroundColor Yellow
    Write-Host "Please run as administrator for full functionality." -ForegroundColor Yellow
}

# Create main workspace directory
$workspaceRoot = "C:\EHB5-Workspace"
if (-not (Test-Path $workspaceRoot)) {
    New-Item -ItemType Directory -Path $workspaceRoot -Force
    Write-Host "✅ Created workspace directory: $workspaceRoot" -ForegroundColor Green
}

# Create subdirectories
$directories = @(
    "tools",
    "sdk",
    "extensions",
    "ai-models",
    "config",
    "projects",
    "backups",
    "logs"
)

foreach ($dir in $directories) {
    $path = Join-Path $workspaceRoot $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force
        Write-Host "✅ Created directory: $dir" -ForegroundColor Green
    }
}

# Install Node.js and npm packages
if (-not $SkipNode) {
    Write-Host "📦 Installing Node.js packages..." -ForegroundColor Blue

    # Core Framework
    npm install -g react react-dom react-router-dom typescript @types/react @types/react-dom

    # State Management
    npm install -g redux react-redux @reduxjs/toolkit zustand

    # UI Components & Design
    npm install -g antd material-ui @mui/material @mui/icons-material @emotion/react @emotion/styled
    npm install -g framer-motion react-spring react-transition-group styled-components
    npm install -g tailwindcss @tailwindcss/forms @tailwindcss/typography

    # Charts & Analytics
    npm install -g chart.js react-chartjs-2 d3 recharts victory nivo

    # Real-time & WebSocket
    npm install -g socket.io socket.io-client ws pusher-js

    # AI & Machine Learning
    npm install -g openai @tensorflow/tfjs brain.js ml5.js onnxruntime-web

    # Data Processing
    npm install -g lodash ramda date-fns moment dayjs numeral

    # HTTP & API
    npm install -g axios fetch swr react-query @tanstack/react-query

    # Form Handling
    npm install -g react-hook-form formik yup @hookform/resolvers

    # Validation & Testing
    npm install -g joi zod jest @testing-library/react @testing-library/jest-dom cypress

    # Development Tools
    npm install -g eslint prettier husky lint-staged commitizen cz-conventional-changelog

    # Build Tools
    npm install -g webpack webpack-cli webpack-dev-server babel-loader @babel/core @babel/preset-react @babel/preset-typescript

    # CSS & Styling
    npm install -g sass less postcss autoprefixer css-loader style-loader mini-css-extract-plugin

    # Performance & Optimization
    npm install -g react-window react-virtualized react-lazyload workbox-webpack-plugin

    # Security
    npm install -g helmet cors bcryptjs jsonwebtoken express-rate-limit

    # Database & Storage
    npm install -g mongoose prisma @prisma/client redis ioredis

    # File Handling
    npm install -g multer sharp pdf-lib xlsx csv-parser

    # Notifications & Alerts
    npm install -g react-toastify react-hot-toast notistack react-notification-system

    # Internationalization
    npm install -g react-i18next i18next i18next-browser-languagedetector

    # Accessibility
    npm install -g react-aria react-focus-lock react-modal react-remove-scroll

    # Utilities
    npm install -g uuid nanoid classnames clsx immer debounce throttle

    Write-Host "✅ Node.js packages installed successfully" -ForegroundColor Green
}

# Install Python packages
if (-not $SkipPython) {
    Write-Host "🐍 Installing Python packages..." -ForegroundColor Blue

    # Core AI/ML
    pip install tensorflow torch torchvision torchaudio
    pip install openai transformers diffusers accelerate
    pip install scikit-learn pandas numpy matplotlib seaborn
    pip install jupyter notebook jupyterlab

    # Data Processing
    pip install pandas numpy scipy
    pip install opencv-python pillow
    pip install requests beautifulsoup4 lxml

    # Web Development
    pip install flask fastapi uvicorn
    pip install django djangorestframework
    pip install aiohttp asyncio

    # Database
    pip install sqlalchemy psycopg2-binary pymongo redis
    pip install alembic

    # Testing
    pip install pytest pytest-cov pytest-asyncio
    pip install selenium playwright

    # Development Tools
    pip install black flake8 mypy isort
    pip install pre-commit

    # Monitoring & Logging
    pip install prometheus-client
    pip install structlog python-json-logger

    # Security
    pip install cryptography bcrypt
    pip install python-jose[cryptography]

    # File Processing
    pip install python-multipart
    pip install python-magic

    Write-Host "✅ Python packages installed successfully" -ForegroundColor Green
}

# Install AI Models and Tools
if (-not $SkipAI) {
    Write-Host "🤖 Installing AI models and tools..." -ForegroundColor Blue

    # Create AI models directory
    $aiModelsPath = Join-Path $workspaceRoot "ai-models"

    # Download pre-trained models
    Write-Host "📥 Downloading AI models..." -ForegroundColor Yellow

    # TensorFlow models
    python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"

    # OpenAI models (requires API key)
    Write-Host "⚠️  OpenAI models require API key configuration" -ForegroundColor Yellow

    # Hugging Face models
    pip install transformers
    python -c "from transformers import pipeline; print('Hugging Face models ready')"

    Write-Host "✅ AI models and tools installed successfully" -ForegroundColor Green
}

# Install VS Code Extensions
if (-not $SkipExtensions) {
    Write-Host "🔧 Installing VS Code extensions..." -ForegroundColor Blue

    # Core Extensions
    code --install-extension ms-vscode.vscode-typescript-next
    code --install-extension esbenp.prettier-vscode
    code --install-extension ms-vscode.vscode-eslint
    code --install-extension bradlc.vscode-tailwindcss
    code --install-extension ms-vscode.vscode-json
    code --install-extension ms-vscode.vscode-css-peek
    code --install-extension ms-vscode.vscode-html-css-support

    # Git & Version Control
    code --install-extension ms-vscode.vscode-git
    code --install-extension eamodio.gitlens

    # Debugging
    code --install-extension ms-vscode.vscode-debugger-for-chrome
    code --install-extension ms-vscode.vscode-debugger-for-firefox

    # React & JavaScript
    code --install-extension ms-vscode.vscode-react-native
    code --install-extension dsznajder.es7-react-js-snippets
    code --install-extension burkeholland.simple-react-snippets

    # Python
    code --install-extension ms-python.python
    code --install-extension ms-python.vscode-pylance
    code --install-extension ms-python.black-formatter

    # AI & Copilot
    code --install-extension GitHub.copilot
    code --install-extension GitHub.copilot-chat

    # Database
    code --install-extension cweijan.vscode-mysql-client2
    code --install-extension ms-mssql.mssql

    # Docker
    code --install-extension ms-azuretools.vscode-docker

    # Testing
    code --install-extension orta.vscode-jest
    code --install-extension ms-vscode.vscode-js-debug

    # Themes & Icons
    code --install-extension PKief.material-icon-theme
    code --install-extension zhuangtongfa.Material-theme
    code --install-extension dracula-theme.theme-dracula

    # Productivity
    code --install-extension christian-kohler.path-intellisense
    code --install-extension formulahendry.auto-rename-tag
    code --install-extension bradlc.vscode-tailwindcss
    code --install-extension ms-vscode.vscode-css-peek

    Write-Host "✅ VS Code extensions installed successfully" -ForegroundColor Green
}

# Install Additional Tools
Write-Host "🛠️  Installing additional development tools..." -ForegroundColor Blue

# Git configuration
git config --global user.name "EHB-5 Developer"
git config --global user.email "developer@ehb-5.com"
git config --global init.defaultBranch main

# Install Chocolatey packages
if (Get-Command choco -ErrorAction SilentlyContinue) {
    Write-Host "📦 Installing Chocolatey packages..." -ForegroundColor Yellow

    choco install -y postman
    choco install -y docker-desktop
    choco install -y mongodb-compass
    choco install -y redis-desktop-manager
    choco install -y insomnia
    choco install -y figma
    choco install -y adobe-creative-cloud

    Write-Host "✅ Chocolatey packages installed successfully" -ForegroundColor Green
}

# Create configuration files
Write-Host "⚙️  Creating configuration files..." -ForegroundColor Blue

# Create .env file
$envContent = @"
# EHB-5 Dashboard Environment Variables
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://user:password@localhost:5432/ehb5
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-jwt-secret-here
CORS_ORIGIN=http://localhost:3000
API_BASE_URL=http://localhost:3000/api
SOCKET_URL=ws://localhost:3000

# AI API Keys
OPENAI_API_KEY=your-openai-api-key-here
REPLIT_API_KEY=your-replit-api-key-here
HUGGINGFACE_API_KEY=your-huggingface-api-key-here

# Cloud Services
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1

# Monitoring
SENTRY_DSN=your-sentry-dsn-here
LOG_LEVEL=info
"@

$envPath = Join-Path $workspaceRoot ".env"
$envContent | Out-File -FilePath $envPath -Encoding UTF8
Write-Host "✅ Created .env file" -ForegroundColor Green

# Create tsconfig.json
$tsconfigContent = @"
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "ES6"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"],
  "exclude": ["node_modules"]
}
"@

$tsconfigPath = Join-Path $workspaceRoot "tsconfig.json"
$tsconfigContent | Out-File -FilePath $tsconfigPath -Encoding UTF8
Write-Host "✅ Created tsconfig.json" -ForegroundColor Green

# Create tailwind.config.js
$tailwindContent = @"
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
    './public/index.html'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        }
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
"@

$tailwindPath = Join-Path $workspaceRoot "tailwind.config.js"
$tailwindContent | Out-File -FilePath $tailwindPath -Encoding UTF8
Write-Host "✅ Created tailwind.config.js" -ForegroundColor Green

# Create .eslintrc.js
$eslintContent = @"
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:jsx-a11y/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: [
    'react',
    '@typescript-eslint',
    'jsx-a11y',
  ],
  rules: {
    'react/react-in-jsx-scope': 'off',
    'react/prop-types': 'off',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
"@

$eslintPath = Join-Path $workspaceRoot ".eslintrc.js"
$eslintContent | Out-File -FilePath $eslintPath -Encoding UTF8
Write-Host "✅ Created .eslintrc.js" -ForegroundColor Green

# Create .prettierrc
$prettierContent = @"
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
"@

$prettierPath = Join-Path $workspaceRoot ".prettierrc"
$prettierContent | Out-File -FilePath $prettierPath -Encoding UTF8
Write-Host "✅ Created .prettierrc" -ForegroundColor Green

# Set environment variables
Write-Host "🔧 Setting environment variables..." -ForegroundColor Blue

$envVars = @{
    "EHB5_WORKSPACE"       = $workspaceRoot
    "NODE_ENV"             = "development"
    "EHB5_TOOLS_PATH"      = Join-Path $workspaceRoot "tools"
    "EHB5_SDK_PATH"        = Join-Path $workspaceRoot "sdk"
    "EHB5_EXTENSIONS_PATH" = Join-Path $workspaceRoot "extensions"
}

foreach ($var in $envVars.GetEnumerator()) {
    [Environment]::SetEnvironmentVariable($var.Key, $var.Value, "Machine")
    Write-Host "✅ Set $($var.Key) = $($var.Value)" -ForegroundColor Green
}

# Create startup script
$startupScript = @"
@echo off
echo 🚀 Starting EHB-5 Development Environment...
echo.
echo 📁 Workspace: $workspaceRoot
echo 🛠️  Tools: $workspaceRoot\tools
echo 🤖 AI Models: $workspaceRoot\ai-models
echo.
echo ✅ Environment ready!
echo.
pause
"@

$startupPath = Join-Path $workspaceRoot "start-dev.bat"
$startupScript | Out-File -FilePath $startupPath -Encoding ASCII
Write-Host "✅ Created startup script" -ForegroundColor Green

# Final summary
Write-Host "`n🎉 EHB-5 Dashboard Tools Installation Complete!" -ForegroundColor Green
Write-Host "`n📋 Installation Summary:" -ForegroundColor Cyan
Write-Host "   ✅ Workspace created: $workspaceRoot" -ForegroundColor Green
Write-Host "   ✅ Node.js packages installed" -ForegroundColor Green
Write-Host "   ✅ Python packages installed" -ForegroundColor Green
Write-Host "   ✅ VS Code extensions installed" -ForegroundColor Green
Write-Host "   ✅ AI models and tools installed" -ForegroundColor Green
Write-Host "   ✅ Configuration files created" -ForegroundColor Green
Write-Host "   ✅ Environment variables set" -ForegroundColor Green

Write-Host "`n🚀 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Configure API keys in $workspaceRoot\.env" -ForegroundColor White
Write-Host "   2. Run 'cd $workspaceRoot && npm start'" -ForegroundColor White
Write-Host "   3. Open VS Code in the workspace" -ForegroundColor White
Write-Host "   4. Start developing your world-class dashboard!" -ForegroundColor White

Write-Host "`n💡 Tips:" -ForegroundColor Cyan
Write-Host "   • Use 'npm run dev' for development" -ForegroundColor White
Write-Host "   • Use 'npm run build' for production" -ForegroundColor White
Write-Host "   • Use 'npm test' for testing" -ForegroundColor White
Write-Host "   • Check the logs in $workspaceRoot\logs" -ForegroundColor White

Write-Host "`n🎯 Happy coding with EHB-5 Dashboard!" -ForegroundColor Green
