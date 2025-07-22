# Cursor Global Configuration Setup Script
# Run this script as Administrator for best results

param(
    [switch]$SkipPackages,
    [switch]$SkipExtensions,
    [switch]$Verbose
)

Write-Host "🚀 Setting up Cursor Global Configuration..." -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Warning "Consider running as Administrator for full setup"
}

# Create main workspace directory
$workspaceRoot = "C:\CursorWorkspace"
$configPath = "$workspaceRoot\config"
$packagesPath = "$workspaceRoot\packages"
$extensionsPath = "$workspaceRoot\extensions"
$projectsPath = "$workspaceRoot\projects"
$templatesPath = "$workspaceRoot\templates"

# Create directory structure
$directories = @($workspaceRoot, $configPath, $packagesPath, $extensionsPath, $projectsPath, $templatesPath)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✓ Created directory: $dir" -ForegroundColor Green
    } else {
        Write-Host "✓ Directory exists: $dir" -ForegroundColor Yellow
    }
}

# Set environment variables
$envVars = @{
    "CURSOR_GLOBAL_CONFIG" = $configPath
    "GLOBAL_PACKAGES_PATH" = $packagesPath
    "SHARED_EXTENSIONS_PATH" = $extensionsPath
    "NODE_ENV" = "development"
}

foreach ($var in $envVars.GetEnumerator()) {
    [Environment]::SetEnvironmentVariable($var.Key, $var.Value, "Machine")
    Write-Host "✓ Set environment variable: $($var.Key) = $($var.Value)" -ForegroundColor Green
}

# Install global packages if not skipped
if (-not $SkipPackages) {
    Write-Host ""
    Write-Host "📦 Installing global packages..." -ForegroundColor Cyan
    
    # Node.js packages
    $nodePackages = @(
        "typescript", "eslint", "prettier", "nodemon", 
        "concurrently", "cross-env", "dotenv", "yarn", "pnpm"
    )
    
    foreach ($pkg in $nodePackages) {
        try {
            Write-Host "Installing $pkg..." -NoNewline
            npm install -g $pkg 2>$null
            Write-Host " ✓" -ForegroundColor Green
        } catch {
            Write-Host " ✗" -ForegroundColor Red
            Write-Host "  Failed to install $pkg" -ForegroundColor Red
        }
    }
    
    # Python packages
    $pythonPackages = @("virtualenv", "pytest", "black", "flake8", "mypy")
    
    foreach ($pkg in $pythonPackages) {
        try {
            Write-Host "Installing Python package $pkg..." -NoNewline
            pip install $pkg 2>$null
            Write-Host " ✓" -ForegroundColor Green
        } catch {
            Write-Host " ✗" -ForegroundColor Red
            Write-Host "  Failed to install Python package $pkg" -ForegroundColor Red
        }
    }
}

# Copy configuration files
Write-Host ""
Write-Host "📋 Copying configuration files..." -ForegroundColor Cyan

# Copy global config
if (Test-Path "cursor-global-config.json") {
    Copy-Item "cursor-global-config.json" "$configPath\" -Force
    Write-Host "✓ Copied cursor-global-config.json" -ForegroundColor Green
}

# Copy Cursor settings
if (Test-Path "cursor-settings.json") {
    $cursorSettingsPath = "$env:APPDATA\Cursor\User\settings.json"
    if (Test-Path $cursorSettingsPath) {
        $existingSettings = Get-Content $cursorSettingsPath | ConvertFrom-Json
        $newSettings = Get-Content "cursor-settings.json" | ConvertFrom-Json
        
        # Merge settings
        $mergedSettings = $existingSettings | ConvertTo-Json -Depth 10
        $mergedSettings = $mergedSettings | ConvertFrom-Json
        
        foreach ($key in $newSettings.PSObject.Properties.Name) {
            $mergedSettings.$key = $newSettings.$key
        }
        
        $mergedSettings | ConvertTo-Json -Depth 10 | Set-Content $cursorSettingsPath
        Write-Host "✓ Updated Cursor settings" -ForegroundColor Green
    } else {
        Copy-Item "cursor-settings.json" $cursorSettingsPath -Force
        Write-Host "✓ Copied Cursor settings" -ForegroundColor Green
    }
}

# Create project template
$templatePackageJson = @{
    name = "project-template"
    version = "1.0.0"
    description = "Template for new projects"
    scripts = @{
        dev = "nodemon src/index.js"
        build = "tsc"
        start = "node dist/index.js"
        test = "jest"
        lint = "eslint src/**/*.js"
        format = "prettier --write src/**/*.js"
    }
    devDependencies = @{
        typescript = "^4.9.0"
        eslint = "^8.0.0"
        prettier = "^2.8.0"
        nodemon = "^2.0.0"
        jest = "^29.0.0"
    }
}

$templatePackageJson | ConvertTo-Json -Depth 10 | Set-Content "$templatesPath\package.json"
Write-Host "✓ Created project template" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart Cursor" -ForegroundColor White
Write-Host "2. Open any project folder - all tools will be available automatically" -ForegroundColor White
Write-Host "3. Your workspace is at: $workspaceRoot" -ForegroundColor White
Write-Host ""
Write-Host "Environment variables set:" -ForegroundColor Cyan
foreach ($var in $envVars.GetEnumerator()) {
    Write-Host "  $($var.Key) = $($var.Value)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 