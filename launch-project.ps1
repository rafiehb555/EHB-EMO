# Project Launcher with Global Configuration
# Usage: .\launch-project.ps1 [project-name]

param(
    [Parameter(Mandatory=$false)]
    [string]$ProjectName = "new-project"
)

$workspaceRoot = "C:\CursorWorkspace"
$projectsPath = "$workspaceRoot\projects"
$projectPath = "$projectsPath\$ProjectName"

Write-Host "🚀 Launching project: $ProjectName" -ForegroundColor Green

# Create project directory if it doesn't exist
if (-not (Test-Path $projectPath)) {
    New-Item -ItemType Directory -Path $projectPath -Force | Out-Null
    Write-Host "✓ Created project directory: $projectPath" -ForegroundColor Green
    
    # Copy template files
    $templatePath = "$workspaceRoot\templates"
    if (Test-Path "$templatePath\package.json") {
        Copy-Item "$templatePath\package.json" "$projectPath\" -Force
        Write-Host "✓ Copied project template" -ForegroundColor Green
    }
    
    # Create basic project structure
    $srcPath = "$projectPath\src"
    New-Item -ItemType Directory -Path $srcPath -Force | Out-Null
    
    # Create basic files
    $indexContent = @"
// $ProjectName - Main entry point
console.log('Hello from $ProjectName!');

// Your code here
"@
    
    Set-Content "$srcPath\index.js" $indexContent
    Write-Host "✓ Created basic project structure" -ForegroundColor Green
}

# Navigate to project directory
Set-Location $projectPath
Write-Host "✓ Navigated to project directory" -ForegroundColor Green

# Show available commands
Write-Host ""
Write-Host "📋 Available commands in this project:" -ForegroundColor Cyan
Write-Host "  npm init                    - Initialize new package.json" -ForegroundColor White
Write-Host "  npm install                 - Install dependencies" -ForegroundColor White
Write-Host "  npm run dev                 - Start development server" -ForegroundColor White
Write-Host "  npm run build               - Build project" -ForegroundColor White
Write-Host "  npm run test                - Run tests" -ForegroundColor White
Write-Host "  npm run lint                - Run ESLint" -ForegroundColor White
Write-Host "  npm run format              - Format code with Prettier" -ForegroundColor White

Write-Host ""
Write-Host "🔧 Global tools available:" -ForegroundColor Cyan
Write-Host "  TypeScript, ESLint, Prettier, Nodemon, etc." -ForegroundColor White
Write-Host "  Python: virtualenv, pytest, black, flake8, mypy" -ForegroundColor White

Write-Host ""
Write-Host "📁 Project location: $projectPath" -ForegroundColor Yellow
Write-Host "🌐 Global workspace: $workspaceRoot" -ForegroundColor Yellow

Write-Host ""
Write-Host "Ready to code! 🎉" -ForegroundColor Green 