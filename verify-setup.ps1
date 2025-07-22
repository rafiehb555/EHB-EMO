# Cursor Global Configuration Verification Script
# This script verifies that all components are properly set up

Write-Host "🔍 Verifying Cursor Global Configuration..." -ForegroundColor Green
Write-Host ""

$workspaceRoot = "C:\CursorWorkspace"
$configPath = "$workspaceRoot\config"
$packagesPath = "$workspaceRoot\packages"
$extensionsPath = "$workspaceRoot\extensions"
$projectsPath = "$workspaceRoot\projects"
$templatesPath = "$workspaceRoot\templates"

$allGood = $true

# Check directory structure
Write-Host "📁 Checking directory structure..." -ForegroundColor Cyan
$directories = @($workspaceRoot, $configPath, $packagesPath, $extensionsPath, $projectsPath, $templatesPath)

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Host "✓ $dir" -ForegroundColor Green
    } else {
        Write-Host "✗ $dir (missing)" -ForegroundColor Red
        $allGood = $false
    }
}

# Check environment variables
Write-Host ""
Write-Host "🔧 Checking environment variables..." -ForegroundColor Cyan
$envVars = @("CURSOR_GLOBAL_CONFIG", "GLOBAL_PACKAGES_PATH", "SHARED_EXTENSIONS_PATH", "NODE_ENV")

foreach ($var in $envVars) {
    $value = [Environment]::GetEnvironmentVariable($var, "Machine")
    if ($value) {
        Write-Host "✓ $var = $value" -ForegroundColor Green
    } else {
        Write-Host "✗ $var (not set)" -ForegroundColor Red
        $allGood = $false
    }
}

# Check configuration files
Write-Host ""
Write-Host "📋 Checking configuration files..." -ForegroundColor Cyan

if (Test-Path "$configPath\cursor-global-config.json") {
    Write-Host "✓ Global config file exists" -ForegroundColor Green
} else {
    Write-Host "✗ Global config file missing" -ForegroundColor Red
    $allGood = $false
}

# Check if Node.js packages are installed
Write-Host ""
Write-Host "📦 Checking global packages..." -ForegroundColor Cyan
$nodePackages = @("typescript", "eslint", "prettier", "nodemon")

foreach ($pkg in $nodePackages) {
    try {
        $version = npm list -g $pkg --depth=0 2>$null | Select-String $pkg
        if ($version) {
            Write-Host "✓ $pkg (installed)" -ForegroundColor Green
        } else {
            Write-Host "✗ $pkg (not installed)" -ForegroundColor Red
            $allGood = $false
        }
    } catch {
        Write-Host "✗ $pkg (check failed)" -ForegroundColor Red
        $allGood = $false
    }
}

# Check Python packages
Write-Host ""
Write-Host "🐍 Checking Python packages..." -ForegroundColor Cyan
$pythonPackages = @("virtualenv", "pytest", "black")

foreach ($pkg in $pythonPackages) {
    try {
        $version = pip show $pkg 2>$null
        if ($version) {
            Write-Host "✓ $pkg (installed)" -ForegroundColor Green
        } else {
            Write-Host "✗ $pkg (not installed)" -ForegroundColor Red
            $allGood = $false
        }
    } catch {
        Write-Host "✗ $pkg (check failed)" -ForegroundColor Red
        $allGood = $false
    }
}

# Check Cursor settings
Write-Host ""
Write-Host "⚙️ Checking Cursor settings..." -ForegroundColor Cyan
$cursorSettingsPath = "$env:APPDATA\Cursor\User\settings.json"

if (Test-Path $cursorSettingsPath) {
    Write-Host "✓ Cursor settings file exists" -ForegroundColor Green
} else {
    Write-Host "✗ Cursor settings file missing" -ForegroundColor Red
    $allGood = $false
}

# Summary
Write-Host ""
Write-Host "=" * 50
if ($allGood) {
    Write-Host "🎉 All components are properly configured!" -ForegroundColor Green
    Write-Host ""
    Write-Host "✅ You can now:" -ForegroundColor Cyan
    Write-Host "  - Open any project folder in Cursor" -ForegroundColor White
    Write-Host "  - Use all global tools and extensions" -ForegroundColor White
    Write-Host "  - Run npm, python, and other commands" -ForegroundColor White
    Write-Host "  - Create new projects with .\launch-project.ps1" -ForegroundColor White
} else {
    Write-Host "⚠️ Some components need attention!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🔧 To fix issues:" -ForegroundColor Cyan
    Write-Host "  - Run .\setup-cursor-global.ps1 as Administrator" -ForegroundColor White
    Write-Host "  - Check the error messages above" -ForegroundColor White
    Write-Host "  - Restart Cursor after setup" -ForegroundColor White
}

Write-Host ""
Write-Host "📁 Workspace location: $workspaceRoot" -ForegroundColor Yellow
Write-Host "🌐 Environment variables are set for global access" -ForegroundColor Yellow 