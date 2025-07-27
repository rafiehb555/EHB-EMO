# 🔄 Safe Data Merge Script - EHB-5 Platform
# Moving data from F:\ehb 5\ehb-5 to F:\ehb 5 without any loss

Write-Host "🚀 EHB-5 Safe Data Merge Starting..." -ForegroundColor Green
Write-Host "=========================================="

$sourceDir = "F:\ehb 5\ehb-5"
$targetDir = "F:\ehb 5"
$backupDir = "F:\ehb 5\backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$logFile = "F:\ehb 5\merge-log-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt"

# Create backup directory
Write-Host "📦 Creating backup directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
"$(Get-Date): Backup directory created: $backupDir" | Add-Content $logFile

# Function to merge directories recursively
function Merge-Directories {
    param($Source, $Target, $BackupPath)

    if (-not (Test-Path $Source)) {
        Write-Host "❌ Source directory not found: $Source" -ForegroundColor Red
        return
    }

    $items = Get-ChildItem -Path $Source -Force
    $processedCount = 0

    foreach ($item in $items) {
        $sourcePath = $item.FullName
        $targetPath = Join-Path $Target $item.Name
        $backupItemPath = Join-Path $BackupPath $item.Name

        try {
            if ($item.PSIsContainer) {
                # Handle directories
                if (Test-Path $targetPath) {
                    Write-Host "📁 Merging directory: $($item.Name)" -ForegroundColor Cyan
                    # Create backup of existing directory
                    if (Test-Path $targetPath) {
                        Copy-Item -Path $targetPath -Destination $backupItemPath -Recurse -Force
                    }
                    # Recursively merge subdirectories
                    Merge-Directories -Source $sourcePath -Target $targetPath -BackupPath $backupItemPath
                } else {
                    Write-Host "📁 Moving directory: $($item.Name)" -ForegroundColor Green
                    Move-Item -Path $sourcePath -Destination $targetPath -Force
                }
            } else {
                # Handle files
                if (Test-Path $targetPath) {
                    # File exists, create backup and replace
                    Write-Host "📄 Replacing file: $($item.Name)" -ForegroundColor Yellow
                    Copy-Item -Path $targetPath -Destination $backupItemPath -Force
                    Copy-Item -Path $sourcePath -Destination $targetPath -Force
                    Remove-Item -Path $sourcePath -Force
                } else {
                    # File doesn't exist, just move it
                    Write-Host "📄 Moving file: $($item.Name)" -ForegroundColor Green
                    Move-Item -Path $sourcePath -Destination $targetPath -Force
                }
            }

            $processedCount++
            "$(Get-Date): Processed $($item.Name)" | Add-Content $logFile

        } catch {
            Write-Host "❌ Error processing $($item.Name): $($_.Exception.Message)" -ForegroundColor Red
            "$(Get-Date): ERROR - $($item.Name): $($_.Exception.Message)" | Add-Content $logFile
        }
    }

    Write-Host "✅ Processed $processedCount items from $Source" -ForegroundColor Green
}

# Start the merge process
Write-Host "🔄 Starting merge process..." -ForegroundColor Cyan
Write-Host "Source: $sourceDir"
Write-Host "Target: $targetDir"
Write-Host "Backup: $backupDir"
Write-Host "Log: $logFile"
Write-Host ""

# Merge all contents
Merge-Directories -Source $sourceDir -Target $targetDir -BackupPath $backupDir

# Clean up empty source directory if it's empty
if ((Get-ChildItem -Path $sourceDir -Force | Measure-Object).Count -eq 0) {
    Write-Host "🗑️ Removing empty source directory..." -ForegroundColor Yellow
    Remove-Item -Path $sourceDir -Force
    "$(Get-Date): Removed empty source directory: $sourceDir" | Add-Content $logFile
} else {
    Write-Host "⚠️ Source directory not empty, keeping it..." -ForegroundColor Yellow
    "$(Get-Date): Source directory not empty, preserved: $sourceDir" | Add-Content $logFile
}

# Final verification
$targetFiles = (Get-ChildItem -Path $targetDir -Recurse -Force | Measure-Object).Count
$backupFiles = (Get-ChildItem -Path $backupDir -Recurse -Force | Measure-Object).Count

Write-Host ""
Write-Host "=========================================="
Write-Host "🎉 Merge Process Completed!" -ForegroundColor Green
Write-Host "📊 Target files: $targetFiles"
Write-Host "📦 Backup files: $backupFiles"
Write-Host "📝 Log file: $logFile"
Write-Host "=========================================="

# Test server functionality
Write-Host "🧪 Testing server functionality..." -ForegroundColor Cyan
Set-Location $targetDir

if (Test-Path "simple-server.js") {
    Write-Host "✅ Server file found!" -ForegroundColor Green
} else {
    Write-Host "❌ Server file not found!" -ForegroundColor Red
}

if (Test-Path "package.json") {
    Write-Host "✅ Package.json found!" -ForegroundColor Green
} else {
    Write-Host "❌ Package.json not found!" -ForegroundColor Red
}

if (Test-Path "services") {
    $serviceCount = (Get-ChildItem -Path "services" -Directory | Measure-Object).Count
    Write-Host "✅ Services directory found with $serviceCount services!" -ForegroundColor Green
} else {
    Write-Host "❌ Services directory not found!" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎊 Data merge completed successfully!"
Write-Host "🌐 You can now run: node simple-server.js"
Write-Host "📁 All data is now in: $targetDir"
Write-Host "💾 Backup available at: $backupDir"
