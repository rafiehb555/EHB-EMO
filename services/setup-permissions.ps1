# EHB-5 Services Permission Setup Script
# Sets up proper read/write permissions for all services

Write-Host "🔧 Setting up EHB-5 Services Permissions..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan

# Get current directory
$servicesPath = Get-Location
Write-Host "📁 Services Path: $servicesPath" -ForegroundColor Yellow

# Function to set permissions for a service
function Set-ServicePermissions {
    param(
        [string]$ServiceName
    )

    $servicePath = Join-Path $servicesPath $ServiceName

    if (Test-Path $servicePath) {
        Write-Host "🔐 Setting permissions for: $ServiceName" -ForegroundColor Blue

        try {
            # Get current ACL
            $acl = Get-Acl $servicePath

            # Create new access rule for full control
            $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
                "Users",
                "FullControl",
                "ContainerInherit,ObjectInherit",
                "None",
                "Allow"
            )

            # Add the rule
            $acl.SetAccessRule($accessRule)

            # Apply the new ACL
            Set-Acl -Path $servicePath -AclObject $acl

            Write-Host "✅ Permissions set for: $ServiceName" -ForegroundColor Green

        } catch {
            Write-Host "❌ Error setting permissions for $ServiceName : $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "⚠️ Service directory not found: $ServiceName" -ForegroundColor Yellow
    }
}

# List of all services
$services = @(
    "EHB-API-GATEWAY",
    "EHB-AUTHENTICATION",
    "EHB-DASHBOARD",
    "EHB-WALLET",
    "EHB-TRUSTY-WALLET",
    "EHB-PAYMENT",
    "EHB-AFFILIATE",
    "EHB-FRANCHISE",
    "EHB-GOSELLER",
    "EHB-AI-MARKETPLACE",
    "EHB-ROBOT",
    "EHB-COMPLAINTS",
    "EHB-ANALYTICS",
    "EHB-REPORTING",
    "EHB-SQL-LEVEL",
    "EHB-EDR",
    "EHB-OBS",
    "EHB-JPS",
    "EHB-VALIDATOR",
    "EHB-TUBE",
    "EHB-NOTIFICATION"
)

Write-Host "📋 Setting up permissions for $($services.Count) services..." -ForegroundColor Cyan
Write-Host ""

# Set permissions for each service
foreach ($service in $services) {
    Set-ServicePermissions -ServiceName $service
}

Write-Host ""
Write-Host "🔧 Setting up main services directory permissions..." -ForegroundColor Blue

# Set permissions for main services directory
try {
    $acl = Get-Acl $servicesPath
    $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
        "Users",
        "FullControl",
        "ContainerInherit,ObjectInherit",
        "None",
        "Allow"
    )
    $acl.SetAccessRule($accessRule)
    Set-Acl -Path $servicesPath -AclObject $acl
    Write-Host "✅ Main services directory permissions set" -ForegroundColor Green
} catch {
    Write-Host "❌ Error setting main directory permissions: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔍 Verifying permissions..." -ForegroundColor Cyan

# Verify permissions
foreach ($service in $services) {
    $servicePath = Join-Path $servicesPath $service
    if (Test-Path $servicePath) {
        try {
            $acl = Get-Acl $servicePath
            $hasFullControl = $acl.Access | Where-Object {
                $_.IdentityReference -eq "Users" -and $_.FileSystemRights -match "FullControl"
            }

            if ($hasFullControl) {
                Write-Host "✅ $service - Permissions verified" -ForegroundColor Green
            } else {
                Write-Host "⚠️ $service - Permissions may need adjustment" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "❌ $service - Error verifying permissions" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "🎉 EHB-5 Services Permission Setup Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Summary:" -ForegroundColor Yellow
Write-Host "   • Services configured: $($services.Count)" -ForegroundColor White
Write-Host "   • Read/Write permissions: Enabled" -ForegroundColor White
Write-Host "   • Full control access: Granted" -ForegroundColor White
Write-Host ""
Write-Host "🚀 You can now develop and modify all services!" -ForegroundColor Green
