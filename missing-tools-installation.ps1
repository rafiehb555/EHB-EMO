# EHB Blockchain - Missing Tools Installation Script
# Run as Administrator

Write-Host "🚀 Installing Missing Tools for EHB Blockchain..." -ForegroundColor Green

# 1. Install Chocolatey (if not installed)
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installing Chocolatey..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# 2. Install Rust
Write-Host "🦀 Installing Rust..." -ForegroundColor Yellow
choco install rust -y

# 3. Install Docker Desktop
Write-Host "🐳 Installing Docker Desktop..." -ForegroundColor Yellow
choco install docker-desktop -y

# 4. Install PostgreSQL
Write-Host "🐘 Installing PostgreSQL..." -ForegroundColor Yellow
choco install postgresql -y

# 5. Install MongoDB
Write-Host "🍃 Installing MongoDB..." -ForegroundColor Yellow
choco install mongodb -y

# 6. Install Git LFS
Write-Host "📁 Installing Git LFS..." -ForegroundColor Yellow
choco install git-lfs -y

# 7. Install Node Version Manager
Write-Host "📦 Installing NVM for Windows..." -ForegroundColor Yellow
choco install nvm -y

# 8. Install Python
Write-Host "🐍 Installing Python..." -ForegroundColor Yellow
choco install python -y

# 9. Install Security Tools
Write-Host "🔒 Installing Security Tools..." -ForegroundColor Yellow
pip install slither-analyzer
pip install mythril

# 10. Install Development Tools
Write-Host "🛠️ Installing Development Tools..." -ForegroundColor Yellow
choco install vscode -y
choco install postman -y
choco install grafana -y

# 11. Install Blockchain Tools
Write-Host "⛓️ Installing Blockchain Tools..." -ForegroundColor Yellow
npm install -g @remix-project/remixd
npm install -g @metamask/detect-provider

# 12. Install Monitoring Tools
Write-Host "📊 Installing Monitoring Tools..." -ForegroundColor Yellow
choco install prometheus -y
choco install alertmanager -y

Write-Host "✅ All missing tools installation completed!" -ForegroundColor Green
Write-Host "🔄 Please restart your system to complete installation." -ForegroundColor Yellow
