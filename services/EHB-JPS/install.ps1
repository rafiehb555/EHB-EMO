# EHB JPS Installation Script
# Complete setup for Job Portal System

param(
    [switch]$SkipDependencies,
    [switch]$SkipDatabase,
    [switch]$SkipBuild,
    [switch]$Force
)

# Set console encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Colors
$Green = "Green"
$Red = "Red"
$Yellow = "Yellow"
$Cyan = "Cyan"
$Gray = "Gray"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Header {
    param([string]$Title)
    Write-ColorOutput "`n╔══════════════════════════════════════════════════════════════╗" $Cyan
    Write-ColorOutput "║                    EHB Job Portal System                     ║" $Cyan
    Write-ColorOutput "║                        $Title" $Cyan
    Write-ColorOutput "╚══════════════════════════════════════════════════════════════╝" $Cyan
    Write-ColorOutput ""
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "✅ $Message" $Green
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "❌ $Message" $Red
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠️  $Message" $Yellow
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "📋 $Message" $Cyan
}

function Write-Step {
    param([string]$Message)
    Write-ColorOutput "📦 $Message" $Gray
}

# Clear console and show header
Clear-Host
Write-Header "Installation"
Write-ColorOutput "🚀 Starting EHB JPS Installation..." $Cyan
Write-ColorOutput ""

# Check Node.js
Write-Info "Checking Node.js installation..."
try {
    $nodeVersion = node --version
    Write-Success "Node.js found: $nodeVersion"

    # Check version
    $majorVersion = [int]($nodeVersion -replace 'v', '' -split '\.')[0]
    if ($majorVersion -lt 18) {
        Write-Error "Node.js 18 or higher is required. Current version: $nodeVersion"
        Write-ColorOutput "Download from: https://nodejs.org/" $Yellow
        exit 1
    }
} catch {
    Write-Error "Node.js is not installed. Please install Node.js 18+ first."
    Write-ColorOutput "Download from: https://nodejs.org/" $Yellow
    exit 1
}

# Check npm
Write-Info "Checking npm installation..."
try {
    $npmVersion = npm --version
    Write-Success "npm found: $npmVersion"
} catch {
    Write-Error "npm is not installed."
    exit 1
}

Write-ColorOutput ""

# Install dependencies
if (-not $SkipDependencies) {
    Write-ColorOutput "📦 Installing dependencies..." $Cyan
    Write-ColorOutput ""

    # Install main dependencies
    Write-Step "Installing main dependencies..."
    try {
        npm install
        Write-Success "Main dependencies installed"
    } catch {
        Write-Error "Failed to install main dependencies"
        exit 1
    }

    # Install frontend dependencies
    if (Test-Path "frontend") {
        Write-Step "Installing frontend dependencies..."
        try {
            Set-Location frontend
            npm install
            Set-Location ..
            Write-Success "Frontend dependencies installed"
        } catch {
            Write-Error "Failed to install frontend dependencies"
            exit 1
        }
    }

    # Install backend dependencies
    if (Test-Path "backend") {
        Write-Step "Installing backend dependencies..."
        try {
            Set-Location backend
            npm install
            Set-Location ..
            Write-Success "Backend dependencies installed"
        } catch {
            Write-Error "Failed to install backend dependencies"
            exit 1
        }
    }

    # Install admin panel dependencies
    if (Test-Path "admin-panel") {
        Write-Step "Installing admin panel dependencies..."
        try {
            Set-Location admin-panel
            npm install
            Set-Location ..
            Write-Success "Admin panel dependencies installed"
        } catch {
            Write-Error "Failed to install admin panel dependencies"
            exit 1
        }
    }

    # Install database dependencies
    if (Test-Path "database") {
        Write-Step "Installing database dependencies..."
        try {
            Set-Location database
            npm install
            Set-Location ..
            Write-Success "Database dependencies installed"
        } catch {
            Write-Error "Failed to install database dependencies"
            exit 1
        }
    }

    # Install tools dependencies
    if (Test-Path "tools") {
        Write-Step "Installing tools dependencies..."
        try {
            Set-Location tools
            npm install
            Set-Location ..
            Write-Success "Tools dependencies installed"
        } catch {
            Write-Error "Failed to install tools dependencies"
            exit 1
        }
    }

    # Install SDK dependencies
    if (Test-Path "sdk") {
        Write-Step "Installing SDK dependencies..."
        try {
            Set-Location sdk
            npm install
            Set-Location ..
            Write-Success "SDK dependencies installed"
        } catch {
            Write-Error "Failed to install SDK dependencies"
            exit 1
        }
    }

    # Install deployment dependencies
    if (Test-Path "deployment") {
        Write-Step "Installing deployment dependencies..."
        try {
            Set-Location deployment
            npm install
            Set-Location ..
            Write-Success "Deployment dependencies installed"
        } catch {
            Write-Error "Failed to install deployment dependencies"
            exit 1
        }
    }

    Write-Success "All dependencies installed successfully!"
    Write-ColorOutput ""
}

# Setup environment file
Write-Info "Setting up environment configuration..."
if (-not (Test-Path ".env")) {
    if (Test-Path "env.example") {
        Copy-Item "env.example" ".env"
        Write-Success "Environment file created from template"
    } else {
        Write-Warning "env.example not found, creating basic .env file"
        @"
NODE_ENV=development
PORT=3001
FRONTEND_PORT=3000
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ehb_jps_db
DB_USER=postgres
DB_PASSWORD=your_password
JWT_SECRET=your_super_secret_jwt_key_here
"@ | Out-File -FilePath ".env" -Encoding UTF8
        Write-Success "Basic environment file created"
    }
} else {
    Write-Info ".env file already exists"
}

# Create necessary directories
Write-Info "Creating project directories..."
$directories = @(
    "logs",
    "uploads",
    "temp",
    "backups",
    "cache",
    "public/uploads",
    "public/images",
    "public/documents"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Success "Project directories created"

# Setup database
if (-not $SkipDatabase) {
    Write-Info "Setting up database..."
    if (Test-Path "database/scripts/setup.js") {
        try {
            Set-Location database
            npm run setup
            Set-Location ..
            Write-Success "Database setup completed"
        } catch {
            Write-Warning "Database setup failed, you can run it manually later"
        }
    }
}

# Build SDK
if (-not $SkipBuild) {
    Write-Info "Building SDK..."
    if (Test-Path "sdk") {
        try {
            Set-Location sdk
            npm run build
            Set-Location ..
            Write-Success "SDK built successfully"
        } catch {
            Write-Warning "SDK build failed, you can run it manually later"
        }
    }
}

# Setup Git hooks
Write-Info "Setting up Git hooks..."
if (Test-Path ".git") {
    try {
        npx husky install
        Write-Success "Git hooks configured"
    } catch {
        Write-Warning "Git hooks setup failed, you can run it manually later"
    }
}

Write-ColorOutput ""

# Success message
Write-Header "Installation Complete!"
Write-ColorOutput "🎉 EHB JPS has been installed successfully!" $Green
Write-ColorOutput ""

Write-ColorOutput "📋 Next Steps:" $Yellow
Write-ColorOutput "    1. Configure your .env file with your settings" $Gray
Write-ColorOutput "    2. Start development: npm run start-dev" $Gray
Write-ColorOutput "    3. Access frontend: http://localhost:3000" $Gray
Write-ColorOutput "    4. Access backend: http://localhost:3001" $Gray
Write-ColorOutput "    5. Access admin: http://localhost:3002" $Gray
Write-ColorOutput ""

Write-ColorOutput "📚 Available Commands:" $Yellow
Write-ColorOutput "   npm run start-dev    - Start development servers" $Gray
Write-ColorOutput "   npm run start-prod   - Start production servers" $Gray
Write-ColorOutput "   npm run test-all     - Run all tests" $Gray
Write-ColorOutput "   npm run lint-all     - Lint all code" $Gray
Write-ColorOutput "   npm run format-all   - Format all code" $Gray
Write-ColorOutput "   npm run db:reset     - Reset database" $Gray
Write-ColorOutput "   npm run db:backup    - Backup database" $Gray
Write-ColorOutput "   npm run deploy:dev   - Deploy to development" $Gray
Write-ColorOutput "   npm run deploy:prod  - Deploy to production" $Gray
Write-ColorOutput ""

Write-ColorOutput "🚀 Happy coding!" $Cyan
Write-ColorOutput ""

if (-not $Force) {
    Read-Host "Press Enter to continue"
}
