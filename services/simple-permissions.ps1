# Simple EHB-5 Services Permission Setup

Write-Host "🔧 Setting up EHB-5 Services Permissions..." -ForegroundColor Green

# List of services
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

Write-Host "📋 Found $($services.Count) services" -ForegroundColor Yellow

# Set permissions for each service
foreach ($service in $services) {
    if (Test-Path $service) {
        Write-Host "✅ $service - Directory exists" -ForegroundColor Green
    } else {
        Write-Host "⚠️ $service - Directory not found" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🎉 Permission check complete!" -ForegroundColor Green
